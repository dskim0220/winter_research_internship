import sys
import os
import json
import re

from experts.base_expert import BaseExpert

from langchain_core.prompts import PromptTemplate
#from langchain_classic.chains.llm import LLMChain
#from langchain_google_genai import ChatGoogleGenerativeAI

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)
from custom_callback_qwen import get_custom_callback, get_llm

class LaTeXMaker(BaseExpert):

    ROLE_DESCRIPTION = 'You are a mathematical modeling expert. Your role is to convert structured natural language modeling elements into formal LaTeX expressions.'
    
    FORWARD_TASK = '''Convert the following structured data into a formal LaTeX.

Input Data (Natural JSON): 
{natural_json}

OUTPUT RULES:
1) Return ONLY a valid JSON object.
2) Do NOT use \( or \) or $ delimiters. Just the LaTeX commands.
3) Use double backslashes (\\\\) for all commands (e.g., \\\\sum, \\\\forall).
4) For multiple constraints, combine them into a single string separated by newline (\\\\n).
5) Use proper indices like x_{{i}} instead of x[I].

JSON Format (Strictly follow this structure):
{{
    "PROBLEM_TYPE": "State the type (e.g., LP, MIP, QP)",
    "SETS_LATEX": "Example: I = \\{{\\\\text{{{{color}}}}, \\\\text{{{{bw}}}} \\}}, J = \\{{1, 2, 3\\}}",
    "PARAMETERS_LATEX": "Example: P_{{{{i}}}}: \\\\text{{{{profit}}}}, R_{{{{i}}}}: \\\\text{{{{limit}}}}",
    "VARIABLES_LATEX": "Example: x_{{{{i}}}} \\\\geq 0, \\\\forall i \\\\in I",
    "OBJECTIVE_LATEX": "Example: \\\\max \\\\sum_{{{{i \\\\in I}}}} P_{{{{i}}}} x_{{{{i}}}}",
    "CONSTRAINTS_LATEX": "Example: x_{{{{i}}}} \\\\leq R_{{{{i}}}}, \\\\forall i \\\\in I; \\\\sum_{{{{i \\\\in I}}}} x_{{{{i}}}} \\\\leq 35"
}}'''

    def __init__(self, model):
        super().__init__(
            name='LaTeX_maker',
            description='Converts structured modeling elements into formal LaTeX mathematical formulations',#LaTeX json 제작
            model=model   
        )
        self.llm = get_llm(model_name=self.model,temperature=0.1)

    
    def forward(self,natural_json):
        full_prompt = f"{self.ROLE_DESCRIPTION}\n\n{self.FORWARD_TASK.format(natural_json=natural_json)}"
        response = self.llm.invoke(full_prompt).content
        cleaned_latex_json = self._extract_json(response)
        return cleaned_latex_json

    def _extract_json(self,text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text # 매칭 실패 시 원본 반환