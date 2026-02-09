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

class CodeGeneratorV2(BaseExpert):

    ROLE_DESCRIPTION = 'Your mission is to generate a Python script that is 100 percents executable without any external data dependencies.'
    FORWARD_TASK = '''Translate the provided JSON model into a standalone, executable Python script.

[STRICT RULES]
1. LITERAL CODING: Do NOT use abstract loops or symbolic placeholders (e.g., `params["A1"]`). Hard-code every value.
2. SOURCE MAPPING: 
   - Logic: Use the 'LaTeX' field as the mathematical blueprint.
   - Numbers: Use the 'query' field to extract exact numerical values (e.g., 170000, 124).
3. DATA SECTION: Define all parameters as Python constants at the top of the script.
4. UNIT SYNC: Perform necessary unit conversions (e.g., tons to kg) based on the 'query' context before defining constants.
5. NO PARSING: The script must not contain any JSON loading or parsing logic. It must be 100 percents self-contained.


Input: {model_json}

[OUTPUT FORMAT]
- Return ONLY the Python code.
- Every constant (Price, Cost, Limit) must be defined as a Python variable (e.g., price_A1 = 124) based on the "query".
- Do NOT include any code that attempts to read or parse JSON.

[OUTPUT FORMAT]
```python
import gurobipy as gp
from gurobipy import GRB

# 1. Constants (Derived from 'query' values)
# Example: price_A1 = 124

# 2. Model Initialization
m = gp.Model("optimization_model")

# 3. Variables (Check 'type' in VARIABLES: Binary/Int/Cont)

# 4. Objective (LaTeX structure + query numbers)

# 5. Constraints (LaTeX structure + query numbers)
# Ensure Big-M values are large enough (e.g., 1e6) if logic requires.

# 6. Optimization & Output
m.optimize()
if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f"{{v.varName}}: {{v.x}}")
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