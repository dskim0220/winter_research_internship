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

class CodeGeneratorV2(BaseExpert):

    ROLE_DESCRIPTION = 'You are a Gurobi Script Expert. Your mission is to generate a Python script that is 100 percents executable without any external data dependencies.'
    FORWARD_TASK = '''Convert the provided JSON model into a standalone Gurobi Python script.

[STRICT RULES: NO SYMBOLIC PLACEHOLDERS]
1. ZERO SYMBOLIC ABSTRACTION: Do NOT use variables like 'sets["PARAMETERS"]' or 'P[i]' in the code.
2. DIRECT VALUE MAPPING: 
   - Look at the "query" field to find the ACTUAL NUMBERS (e.g., 124, 109, 170000).
   - Look at the "LaTeX" field to understand the MATHEMATICAL LOGIC.
   - Combine them to write explicit code (e.g., `m.setObjective(124 * x1 + 109 * x2, GRB.MAXIMIZE)`).
3. HARD-CODED DATA SECTION: Explicitly define all parameters as numeric constants at the beginning of the script based on the "query" values.
4. UNIT CONVERSION: If the 'query' mentions 'tons' but the model uses '100kg units', calculate the numeric value (e.g., 1210 tons = 12100 units) and use that number directly.

[MODELING GUIDELINE]
- Variables: Check "VARIABLES" for (Binary, Integer, Continuous).
- Constraints: Implement the "LaTeX" logic using the specific numbers from its paired "query".
- Logic: Use Big-M (e.g., 1000000) for linking constraints if the LaTeX suggests conditional logic.    

JSON Input:
{model_json}

[OUTPUT FORMAT]
- Return ONLY the Python code.
- Every constant (Price, Cost, Limit) must be defined as a Python variable (e.g., price_A1 = 124) based on the "query".
- Do NOT include any code that attempts to read or parse JSON.

Format Example:
```python
import gurobipy as gp
from gurobipy import GRB

# 1. Data Section (Directly extracted from JSON 'query' fields)
# Define numeric constants here (e.g., demand_A1 = 5300)
# DO NOT USE symbolic placeholders.

# 2. Model Initialization
m = gp.Model("production_optimization")

# 3. Variables (Check 'type' in VARIABLES section: Binary, Continuous, etc.)

# 4. Objective (Use 'LaTeX' logic + 'query' numbers)

# 5. Constraints (Combine 'LaTeX' structure with 'query' numeric values)
# Ensure unit consistency (e.g., 1,210 tons -> 12100 in 100kg units)

# 6. Optimization and Output
m.optimize()
# ... (Print results for each variable)

'''

    def __init__(self, model):
        super().__init__(
            name='code_generator',
            description='Converts LaTeX JSON to executable Python code',#LaTeX json 제작
            model=model   
        )
        self.llm = get_llm(model_name=self.model,temperature=0.1)

    
    def forward(self,model_json):
        full_prompt = f"{self.ROLE_DESCRIPTION}\n\n{self.FORWARD_TASK.format(model_json=model_json)}"
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