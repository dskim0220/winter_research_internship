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

class CodeGenerator(BaseExpert):

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
            description='',#LaTeX json 제작
            model=model   
        )
        self.llm = get_llm(model_name=self.model,temperature=0.1)

    
    def forward(self,LaTeX_json):
        full_prompt = f"{self.ROLE_DESCRIPTION}\n\n{self.FORWARD_TASK.format(LaTeX_json=LaTeX_json)}"
        raw_output = self.llm.invoke(full_prompt).content
        code = self._extract_code(raw_output)
        return code

    def _extract_code(self, text):
        """텍스트에서 파이썬 코드 블록만 추출"""
        # ```python ... ``` 또는 ``` ... ``` 블록을 찾음
        match = re.search(r'```(?:python)?\s*(.*?)```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip() # 코드 블록이 없으면 전체 텍스트 반환