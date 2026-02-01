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

    ROLE_DESCRIPTION_EXTRACTOR = 'Your role is to perform a "Full-Sentence-Extraction" to ensure no information loss for mathematical modeling.'
    
    FORWARD_TASK_EXTRACTOR = '''Extract ALL numerical values and constraints into a structured JSON format. 
[STRICT RULES]
1. VARIABLE TYPE: Clearly distinguish between QUANTITY(Integer/Continuous) and SELECTION(Binary 0/1).
2. PARAMETERS: List all values with their specific units.
3. CONSTRAINTS: Assign a unique 'rule_id' to every sentence containing a limit or requirement.
4. FORMAT: Return ONLY the JSON object.
5. You MUST strictly adhere to the provided feedback reference for all extraction logic.

[INPUT DATA]
1. Problem: {problem_description}
2. Feedback Reference: {feedback}

JSON Format:
{{
    "PROBLEM_TYPE": "MIP/LP/etc",
    "PARAMETERS": [{{ "name": "p1", "value": "val", "unit": "unit", "context": "original sentence" }}],
    "CONSTRAINTS_RAW": [{{ "rule_id": 1, "logic": "ASCII_logic", "original_text": "sentence" }}],
    "OBJECTIVE_RAW": "goal sentence"
}}
'''

    ROLE_DESCRIPTION_FORMULATOR = 'Your role is to translate extracted raw data into a rigorous LaTeX optimization model with 1:1 mapping.'
    FORWARD_TASK_FORMULATOR = '''Convert extracted data into a rigorous optimization model. Ensure 1:1 mapping with rule_ids.".

[STRICT MODELING RULES]
1. VARIABLE TYPE: x (Integer/Continuous) for quantities, y (Binary) for decisions.
2. LOGICAL LINKING: Use Big-M ($x \le M \cdot y$) for fixed costs or activation logic.
3. ATOMICITY: Every rule_id from the Extractor must have exactly one corresponding LaTeX constraint.
4. LITERAL VALUES: Do not use symbolic placeholders; use exact numerical values from the parameters.

[LOGICAL EXAMPLE]
Input: "Fixed cost 170,000, Min batch 20, Max demand 5,300"
LaTeX Variables: $y_{A1} \in {{0, 1}}$, $x_{A1} \in \mathbb{{Z}}^+$
LaTeX Constraints: $x_{A1} \ge 20 \cdot y_{A1}$ (Min Batch), $x_{A1} \le 5300 \cdot y_{A1}$ (Big-M Link)

[INPUT DATA]
1. Extracted Query: {extracted_queries}
2. Original Problem: {problem_description}

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