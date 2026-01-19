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

    ROLE_DESCRIPTION = 'You are an expert that identifies and extracts relevant variables from the problem statement.'
    FORWARD_TASK = '''As a parameter extraction expert, your role is to identify and extract the relevant variables, constrans, objective from the problem statement. 
Your expertise in the problem domain will help in accurately identifying and describing these variables. 
Please review the problem description and provide the extracted variables along with their definitions: 
{problem_description}

And the comments from other experts are as follow:
{comments_text}

Please note that the information you extract is for the purpose of modeling, which means your variables, constraints, and objectives need to meet the requirements of a solvable LP or MIP model.

IMPORTANT OUTPUT RULES:
1) Return ONLY a valid JSON object. No extra text or explanations.
2) Do NOT use LaTeX symbols (e.g., no \leq, \geq, \text).
3) Use ONLY ASCII operators: <=, >=, =.
4) Your output MUST follow this format:
{{
    "VARIABLES": "List of variables",
    "CONSTRAINTS": "List of constraints using <=, >=, =",
    "OBJECTIVE": "Objective function"
}}
'''

    def __init__(self, model):
        super().__init__(
            name='natural_maker',
            description='',#자연어 JSON 제작
            model=model   
        )
        self.llm = get_llm(model_name=self.model,temperature=0.1)

    
    def forward(self,problem):
        comments_text=""
        message = self.forward_prompt_template.format(
            problem_description = problem['description'],
            code_example = problem['code_example'],
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





   
