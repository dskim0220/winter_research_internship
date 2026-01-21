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

class NaturalMaker(BaseExpert):

    ROLE_DESCRIPTION = 'You are an expert in mathematical problem formulation. Your role is to translate natural language problems into structured optimization data.'
    FORWARD_TASK = '''Analyze the problem and extract the type, Sets, Variables, Parameters, Objective, and Constraints from the problem statement for mathematical modeling.
Problem Description:
{problem_description}

IMPORTANT OUTPUT RULES:
1) Return ONLY a valid JSON object. No extra text or explanations.
2) Do NOT use LaTeX. Use ASCII operators (<=, >=, =).
3) Be specific about indices and sets (e.g.,"Set I: Factories, Set J: Customers").

JSON Format:
{{
    "PROBLEM_TYPE":"LP/MIP/NLP/etc"
    "SETS": "Index sets for the problem",
    "PARAMETERS": "Given fixed values and data with their units",
    "VARIABLES": "Decision variables to be determined",
    "OBJECTIVE": "The optimization goal function",
    "CONSTRAINTS": "List of functional constraints"
}}
'''

    def __init__(self, model):
        super().__init__(
            name='natural_maker',
            description='Decomposes natural language problems into 6-part structured modeling data',#자연어 JSON 제작
            model=model   
        )
        self.llm = get_llm(model_name=self.model,temperature=0.1)

    
    def forward(self,problem):
        comments_text=""
        message = self.forward_prompt_template.format(
            problem_description = problem,
            ##code_example = problem['code_example'],
            comments_text= comments_text
        )
        raw_output = self.llm.invoke(message).content

        cleaned_json = self._extract_json(raw_output)

        return cleaned_json
    

    def _extract_json(self,text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text # 매칭 실패 시 원본 반환





   
