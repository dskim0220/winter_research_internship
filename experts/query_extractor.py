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

class Extractor(BaseExpert):

    ROLE_DESCRIPTION_EXTRACTOR = 'Your role is to perform a "Full-Sentence-Extraction" to ensure no information loss for mathematical modeling.'
    
    FORWARD_TASK_EXTRACTOR = '''Extract ALL numerical values and constraints into a structured JSON format. 
[THINKING PROCESS - DO THIS FIRST]
1. Identify all entities (Suppliers, Nodes, Products).
2. Determine if a decision is a 'How much' (Integer/Continuous) OR 'Whether to' (Binary).
3. Identify "Conditional Logic": Does selecting A force a limit on B? (If-Then).
4. Identify "Unit Consistency": Ensure you don't add 'Orders' to 'Tables'.

[STRICT EXTRACTION RULES]
1. VARIABLE_MAPPING: 
   - If a cost is per "order", and an order has "20 tables", define TWO parameters: 'cost_per_order' and 'units_per_order'.
2. LOGIC_MAPPING (Big-M):
   - For "If A then B" constraints, explicitly flag them as "CONDITIONAL_LOGIC".
3. NUMERIC_PRECISION:
   - Extract 'at least', 'no more than', 'exactly' as >=, <=, ==.
4. TYPE_ASSIGNMENT:
   - Countable units (people, orders, tables) = INTEGER.
   - Flow/Money/Time = CONTINUOUS.
   - Selection/On-Off = BINARY.

[LOGIC EXAMPLE]
1. Conditional Selection (If A, then B): 
   - Rule: "If Supplier A is chosen, Supplier B must also be chosen."
   - Logic: y_B >= y_A  (Binary variables)

2. Minimum Requirement on Selection:
   - Rule: "If Supplier A is chosen, order at least 30 units."
   - Logic: x_A >= 30 * y_A (where x is quantity, y is binary)

3. Linking Selection to Quantity (Big-M):
   - Rule: "If we order from A, total units cannot exceed 100."
   - Logic: x_A <= 100 * y_A

[INPUT DATA]
Problem: {problem_description}
Feedback: {feedback}

[OUTPUT FORMAT]
Return ONLY a JSON with this enhanced structure:
{{
    "DECISION_VARIABLES": [
        {{ "name": "x_i", "type": "BINARY/INTEGER/CONTINUOUS", "description": "definition" }}
    ],
    "PARAMETERS": [
        {{ "name": "p_i", "value": 0.0, "unit": "unit", "relates_to": "variable_name" }}
    ],
    "CONSTRAINTS": [
        {{ 
          "rule_id": "R1", 
          "type": "LINEAR/CONDITIONAL/BIG_M", 
          "logic": "ASCII_formula", 
          "original_text": "sentence" 
        }}
    ],
    "OBJECTIVE": {{ "goal": "MIN/MAX", "formula": "ASCII_formula" }}
}}
'''

    def __init__(self, model):
        self.name='extractor',
        self.description='Decomposes natural language problems into 6-part structured modeling data',#자연어 JSON 제작
        self.model=model   
        self.llm_extractor = get_llm(model_name=self.model,temperature=0.1)
        print("추출준비 완료!")

    
    def extract(self,problem,feedback):
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
    
    def _extract_json(self,text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text # 매칭 실패 시 원본 반환