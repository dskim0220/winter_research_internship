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

    ROLE_DESCRIPTION_EXTRACTOR = 'You are an expert in mathematical problem extraction. Your role is to perform a "Full-Sentence-Extraction" to ensure zero information loss.'
    
    FORWARD_TASK_EXTRACTOR = '''Analyze the problem and extract EVERY single numerical value, logical rule, and set definition. 
Do not summarize; perform a literal extraction of all constraints.

[STRICT EXTRACTION RULES]
1. Zero-Loss Extraction: Create a dedicated entry for every sentence containing a number or a constraint. 
2. Reference Tagging: Assign a unique "rule_id" to each extracted constraint to ensure the Formulator can track them later.
3. Unit Mapping: Explicitly extract units (e.g., tons, 100kg, KRW, hours) and ensure they are paired with their values.
4. Data Dictionary Focus: Identify every coefficient (Price, Cost, Demand, etc.) and list them explicitly.
5. Feedback Priority: If "feedback from evaluator" is provided, you MUST specifically address and correct the failed components mentioned in the feedback.

Problem Description:
{problem_description}

feedback from evaluator:
{feedback}

IMPORTANT OUTPUT RULES:
1) Return ONLY a valid JSON object. No extra text.
2) Do NOT use LaTeX here. Use plain text or ASCII for logical expressions.
3) Accuracy: If a value is "1,210 tons", do not just write "1210". Write "1210 (tons)".

JSON Format:
{{
    "PROBLEM_TYPE": "MIP/LP/Routing/etc",
    "SETS": [
        {{ "id": "index_symbol", "description": "set_name", "size": "N" }}
    ],
    "PARAMETERS": [
        {{ 
            "name": "param_name", 
            "value": "numeric_value", 
            "unit": "unit_name", 
            "context": "The original sentence this data came from" 
        }}
    ],
    "CONSTRAINTS_RAW": [
        {{ 
            "rule_id": 1, 
            "logic": "mathematical_logic_in_ASCII", 
            "original_text": "Complete sentence from problem description" 
        }}
    ],
    "OBJECTIVE_RAW": "The exact goal sentence from the text"
}}
'''

    ROLE_DESCRIPTION_FORMULATOR = 'You are a Mathematical Formulator. Your role is to translate extracted raw data into a rigorous LaTeX optimization model with 1:1 mapping.'
    FORWARD_TASK_FORMULATOR = '''Using the "Extracted Query Data", formulate a complete mathematical model in LaTeX.

[CRITICAL MAPPING RULES]
1. Atomic Correspondence: For every "rule_id" in CONSTRAINTS_RAW, you MUST generate exactly one corresponding LaTeX formula. 
2. Symbolic Consistency: Use the exact numerical values (e.g., 124, 1000) in LaTeX. No undefined symbols like P, C, or T.
3. Explicit Indices: For routing/grid problems, use specific indices (i for path, u,v for nodes, d for direction).
4. Logic Reformulation: Use Big-M notation or binary indicators for conditional constraints (If-Then).

Extracted Query Data (from Extractor):
{extracted_queries}

Problem Description (for context):
{problem_description}

JSON Format:
{{
    "SETS": {{ "query": "Definition of all indices", "LaTeX": "LaTeX formulation" }},
    "VARIABLES": [
        {{ "name": "var_name", "type": "Binary/Int/Cont", "LaTeX": "x_{{i}} \\in \\{{0, 1\\}}", "description": "..." }}
    ],
    "PARAMETERS": [
        {{ "name": "param_name", "LaTeX": "Value = 100", "description": "..." }}
    ],
    "OBJECTIVE": {{ "query": "Objective from Extractor", "LaTeX": "\\min \\sum ..." }},
    "CONSTRAINTS": [
        {{ 
            "rule_id": "Must match rule_id from Extractor",
            "name": "constraint_name",
            "query": "The raw logic from Extractor",
            "LaTeX": "The formal equation"
        }}
    ]
}}

[EXAMPLE OUTPUT]
{{
    "SETS": {{
        "query": "Set of 3 products (A1, A2, A3) and 2 production lines (L1, L2)",
        "LaTeX": "I = \\{{A1, A2, A3\\}}, J = \\{{L1, L2\\}}"
    }},
    "VARIABLES": [
        {{
            "name": "x_ij",
            "type": "Continuous",
            "LaTeX": "x_{{i,j}} \\geq 0, \\forall i \\in I, j \\in J",
            "description": "Quantity of product i produced on line j"
        }},
        {{
            "name": "y_ij",
            "type": "Binary",
            "LaTeX": "y_{{i,j}} \\in \\{{0, 1\\}}, \\forall i \\in I, j \\in J",
            "description": "Binary indicator: 1 if product i is assigned to line j"
        }}
    ],
    "PARAMETERS": [
        {{
            "name": "Price_A1",
            "LaTeX": "P_{{A1}} = 124",
            "description": "Selling price of product A1"
        }},
        {{
            "name": "Capacity_L1",
            "LaTeX": "Cap_{{L1}} = 5000",
            "description": "Total production capacity of line L1"
        }}
    ],
    "OBJECTIVE": {{
        "query": "Maximize total profit (Revenue - Fixed Cost)",
        "LaTeX": "\\max \\sum_{{i \\in I}} \\sum_{{j \\in J}} (P_i \\cdot x_{{i,j}}) - \\sum_{{i \\in I}} \\sum_{{j \\in J}} (FixedCost_{{i,j}} \\cdot y_{{i,j}})"
    }},
    "CONSTRAINTS": [
        {{
            "rule_id": 1,
            "name": "Demand_Constraint",
            "query": "Total production of A1 must be at least 300 units",
            "LaTeX": "\\sum_{{j \\in J}} x_{{A1,j}} \\geq 300"
        }},
        {{
            "rule_id": 2,
            "name": "BigM_Activation",
            "query": "Product i can only be produced on line j if line j is activated",
            "LaTeX": "x_{{i,j}} \\leq 1000000 \\cdot y_{{i,j}}, \\forall i \\in I, j \\in J"
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