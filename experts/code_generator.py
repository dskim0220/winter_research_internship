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

    ROLE_DESCRIPTION = 'You are an expert Python programmer specializing in Operations Research. You excel at implementing formal LaTeX mathematical models into executable Python code using optimization libraries like Gurobi, PuLP, or Pyomo.'
    FORWARD_TASK = '''Implement the following LaTeX mathematical model into a complete, runnable Python script.

Input Mathematical Model(LaTeX JSON) 
{LaTeX_json}

[Image of a mapping from LaTeX mathematical summation to Python Gurobi quicksum code]

IMPLEMENTATION RULES:
1) Provide ONLY the Python code block. No extra text.
2) Data Mapping: SETS to lists, PARAMETERS to dicts.
3) Modeling Logic: Use gp.quicksum() and m.addConstrs() correctly.
4) Robustness: Include sample data and print variable results.
5) Variable Types: Distinguish between CONTINUOUS, INTEGER, and BINARY based on the context.
6) Exact Mapping: Every LaTeX constraint must have a corresponding addConstr/addConstrs line.
7) Gurobi Standards: Use GRB.MAXIMIZE and check m.status == GRB.OPTIMAL.

OUTPUT FORMAT:
```python
import gurobipy as gp
from gurobipy import GRB

# 1. Data and Sets
# 2. Model Initialization
# 3. Variables
# 4. Objective
# 5. Constraints
# 6. Optimization and Output
```'''

    def __init__(self, model):
        super().__init__(
            name='code_generator',
            description='Converts LaTeX JSON to executable Python code',#LaTeX json 제작
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