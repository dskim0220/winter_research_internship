import sys
import os
import json
import re

from experts.base_expert import BaseExpert

from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
#from langchain_google_genai import ChatGoogleGenerativeAI

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)
from custom_callback_qwen import get_custom_callback, get_llm

class ModelDesigner(BaseExpert):

    ROLE_DESCRIPTION_EXTRACTOR = 'Your role is to perform a "Full-Sentence-Extraction" to ensure zero information loss for mathematical modeling.'
    
    FORWARD_TASK_EXTRACTOR = '''Extract ALL numerical values and constraints from the problem. 
[STRICT RULE: Variable Type] 
- Quantity/Amount = Integer or Continuous.
- Decision/Activation = Binary (0/1). 
Failure to distinguish these will result in an infeasible model.

[EXTRACTION STEPS]
1. List all parameters with Units (e.g., 1,210 (tons)).
2. Assign a unique "rule_id" to every constraint sentence.
3. Strictly adhere to the provided 'feedback' for all subsequent responses.

Problem: {problem_description}
Feedback: {feedback}

Return ONLY JSON:
{{
    "PROBLEM_TYPE": "MIP/LP/etc",
    "PARAMETERS": [{{ "name": "p1", "value": "val", "unit": "unit", "context": "original sentence" }}],
    "CONSTRAINTS_RAW": [{{ "rule_id": 1, "logic": "ASCII_logic", "original_text": "sentence" }}],
    "OBJECTIVE_RAW": "goal sentence"
}}'''

    ROLE_DESCRIPTION_FORMULATOR = 'Your role is to translate extracted raw data into a rigorous LaTeX optimization model with 1:1 mapping.'
    FORWARD_TASK_FORMULATOR = '''Formulate a complete mathematical model in JSON format based on the "Extracted Query Data".

[STRICT MODELING RULES]
1. VARIABLE TYPE: Strictly distinguish between Binary (y) for decisions and Integer/Continuous (x) for quantities. NEVER USE BINARY FOR AMOUNTS > 1.
2. BIG-M LINKING: If a fixed cost or activation exists, you MUST use x <= M * y to link quantity (x) and binary (y).
3. ATOMIC MAPPING: Every "rule_id" from Extractor MUST have a 1:1 corresponding LaTeX constraint.
4. NO PLACEHOLDERS: USE EXACT NUMBERS (e.g., 1210, 170000) from the parameters.
5. You MUST follow the FEW-SHOT EXAMPLE below.

[FEW-SHOT EXAMPLE: LOGICAL LINKING]
Input Query: "Product A1 has a fixed cost of 170000 and min batch 20. Max demand 5300."
Output LaTeX Variables:
- y_A1: Binary (1 if produced)
- x_A1: Integer (Quantity)
Output LaTeX Constraints:
- x_A1 >= 20 * y_A1 (Min Batch)
- x_A1 <= 5300 * y_A1 (Max Demand / Big-M Linking)

Extracted Query Data:
{extracted_queries}

Problem Description:
{problem_description}

Return ONLY a valid JSON:
{{
    "SETS": {{ "query": "indices definition", "LaTeX": "..." }},
    "VARIABLES": [
        {{ "name": "var_name", "type": "Binary/Int/Cont", "LaTeX": "x \\in ...", "description": "..." }}
    ],
    "PARAMETERS": [
        {{ "name": "p_name", "LaTeX": "P = 100", "description": "..." }}
    ],
    "OBJECTIVE": {{ "query": "goal", "LaTeX": "\\max ..." }},
    "CONSTRAINTS": [
        {{ 
            "rule_id": "Must match Extractor",
            "name": "name",
            "query": "raw logic",
            "LaTeX": "formula"
        }}
    ]
}}
'''

    def __init__(self, model):
        self.name='model_designer',
        self.description='Decomposes natural language problems into 6-part structured modeling data',#자연어 JSON 제작
        self.model=model   
        self.llm_extractor = get_llm(model_name=self.model,temperature=0.1)
        self.llm_formulator = get_llm(model_name=self.model,temperature=0.1)
        print("초기화 완료!")

    
    def semantic_extractor(self,problem,feedback):
        comments_text=""
        message = self.FORWARD_TASK_EXTRACTOR.format(
            problem_description = problem,
            ##code_example = problem['code_example'],
            feedback = feedback,
            comments_text= comments_text
        )
        raw_output = self.llm_extractor.invoke(message).content
        cleaned_json = self._extract_json(raw_output)
        print("추출완료!")
        return cleaned_json
    
    def mathematical_formulator(self,problem,extracted_queries,feedback):
        comments_text=""
        message = self.FORWARD_TASK_FORMULATOR.format(
            problem_description = problem,
            ##code_example = problem['code_example'],
            extracted_queries = extracted_queries,
            feedback = feedback,
            comments_text= comments_text
        )
        raw_output = self.llm_formulator.invoke(message).content
        cleaned_json = self._extract_json(raw_output)
        print("수식완료!")
        return cleaned_json
    
    def forward(self,problem,feedback):
        queries_json = self.semantic_extractor(problem=problem,feedback=feedback)
        final_formulation = self.mathematical_formulator(problem=problem,extracted_queries=queries_json,feedback=feedback)
        return final_formulation

    def _extract_json(self,text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text # 매칭 실패 시 원본 반환