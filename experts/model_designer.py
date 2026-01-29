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

    ROLE_DESCRIPTION_EXTRACTOR = 'You are an expert in mathematical problem formulation. Your role is to translate natural language problems into structured optimization data.'
    FORWARD_TASK_EXTRACTOR = '''Analyze the problem and extract the type, Sets, Variables, Parameters, Objective, and Constraints from the problem statement for mathematical modeling.

CRITICAL INSTRUCTION:
If "feedback from evaluator" is provided, you MUST prioritize addressing all issues, corrections, or suggestions mentioned in the feedback to refine the previous model. Integrate the feedback into the new formulation to ensure higher accuracy.

Problem Description:
{problem_description}

feedback from evaluator:
{feedback}

To ensure the generated code is immediately executable and produces valid results, you MUST adhere to the following rules:
1. Eliminate Symbolic Placeholders: Never use undefined symbolic constants (e.g., P, C, Q, T) or placeholders. Using undefined variables causes a `NameError` and renders the code non-executable.
2. Mandatory Data Dictionary: Every Python script MUST begin with a comprehensive data section. Define a `data` or `parameters` dictionary that contains ALL numerical values extracted from the problem description.
3. Explicit Parameter Mapping: You must explicitly map every specific number provided (e.g., Prices: 124, 109, 115; Costs: 73.3, 52.9, 65.4) into the model. Do not leave parameters for the user to fill in.
4. Zero-Abstraction for Instances: If a specific problem instance is provided, your task is to solve that specific instance, not to create a generalized template. Use the exact coefficients provided in the text for objective functions and constraints.
5. Dimensional Consistency: Verify that the units used in the data section (e.g., 100kg units vs. tons) are consistently applied throughout the constraints to avoid dimensional hallucinations.

IMPORTANT OUTPUT RULES:
1) Return ONLY a valid JSON object. No extra text or explanations.
2) Do NOT use LaTeX. Use ASCII operators (<=, >=, =).
3) Decision Unit Accuracy: Determine if variables are Binary (Yes/No), Integer (Counts), or Continuous (Amounts). If the problem says "number of orders must be an integer", use Integer.
4) Conditional Logic: Explicitly capture "If-Then" or "Only if" relationships in the CONSTRAINTS. (e.g., "If A is ordered, B must be at least 30").
5) Indexing: Be specific about indices and sets (e.g., "Set I: Suppliers").

JSON Format:
{{
    "PROBLEM_TYPE": "LP/MIP/NLP/etc",
    "SETS": "Index sets for the problem",
    "PARAMETERS": "Given fixed values and data with their units",
    "VARIABLES": "List variables to be determined with (Type, Unit). Example: orders_A (Integer, count)",
    "OBJECTIVE": "The optimization goal function",
    "CONSTRAINTS": "List of functional constraints reflecting the provided feedback"
}}
'''

    ROLE_DESCRIPTION_FORMULATOR = ''
    FORWARD_TASK_FORMULATOR = '''Using the extracted queries and original problem, formulate a complete mathematical model in LaTeX.

[CRITICAL INSTRUCTION]
1. Grounding: Each LaTeX formula MUST correspond to its provided "query".
2. Symbolic Check: Use specific coefficients from the query. No undefined symbols like P, C, T.
3. Logical Reformulation: Use Big-M notation for conditional constraints (If-Then) found in the queries.
4. Decision Type: Strictly define variables as Binary, Integer, or Continuous.

Extracted Query Data (from Agent 1):
{extracted_queries}

Problem Description (for context):
{problem_description}
####
####
####
JSON Format:
{{
    "SETS": {{ "query": "...", "LaTeX": "LaTeX formulation" }},
    "PARAMETERS": [
        {{ "name": "...", "query": "...", "LaTeX": "LaTeX with exact values" }},
        {{ "name": "...", "query": "...", "LaTeX": "LaTeX with exact values" }},
    ],
    "VARIABLES": [
        {{ "name": "...", "type": "Binary/Int/Cont", "query": "...", "LaTeX": "LaTeX definition" }}
    ],
    "OBJECTIVE": {{ "query": "...", "LaTeX": "LaTeX objective function" }},
    "CONSTRAINTS": [
        {{ "name": "...", "query": "...", "LaTeX": "LaTeX equation" }}
    ]
}}

Following example given below
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