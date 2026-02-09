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

class Formulator(BaseExpert):
    ROLE_DESCRIPTION_FORMULATOR = 'Your role is to translate extracted raw data into a rigorous LaTeX optimization model with 1:1 mapping.'
    FORWARD_TASK_FORMULATOR = '''Convert extracted data into a rigorous optimization model. Ensure 1:1 mapping with rule_ids.".

[STRICT MODELING RULES]
1. INDICATOR ALGEBRA: 
   - If a rule says "If A then B", use: $y_B \ge y_A$ (Binary logic).
   - If a rule says "If A, then $x \ge \text{{Value}}$", use: $x \ge \text{{Value}} \cdot y_A$ (Linking logic).
2. INDEX CONSISTENCY: Use clear indices (e.g., $i \in {{A, B, C}}$). Ensure all summations $\sum$ have explicit ranges.
3. DOMAIN DEFINITION: 
   - Binary: $y \in {{0, 1}}$
   - Integer: $x \in \mathbb{{Z}}^+$
   - Continuous: $x \ge 0$
4. BIG-M VALUE: If a maximum capacity is not given for Big-M, use $M = 10000$ and state it clearly.
5. NO LOOSE ENDS: Every parameter from the input must appear in either the Objective or Constraints.

[LOGICAL TEMPLATE]
- Goal: "Minimize cost" -> $\min \sum (\text{{Cost}}_i \cdot x_i)$
- Logic: "Selection forces minimum" -> $x_i \ge \text{{Min}}_i \cdot y_i$
- Logic: "Mutual exclusivity" -> $\sum y_i \le 1$

[INPUT DATA]
1. Extracted Query: {extracted_queries}
2. Original Problem: {problem_description}

[OUTPUT FORMAT]
Return ONLY a JSON with the following structure:
{{
    "VARIABLES": [
        {{ 
          "name": "var_name", 
          "type": "Binary/Int/Cont", 
          "LaTeX": "x_{{i}} \\in ...", 
          "description": "..." 
        }}
    ],
    "OBJECTIVE": {{ 
      "query": "The specific part of extracted_queries used for objective",
      "goal": "MIN/MAX", 
      "LaTeX": "\\min Z = ..."
    }},
    "CONSTRAINTS": [
        {{ 
          "rule_id": "Must match Extractor",
          "query": "The exact 'logic' or 'original_text' from extracted_queries used here",
          "LaTeX": "f(x) \\le b",
          "description": "Plain English explanation of how the query was transformed"
        }}
    ]
}}
'''

    def __init__(self, model):
        self.name='model_designer',
        self.description='Decomposes natural language problems into 6-part structured modeling data',#자연어 JSON 제작
        self.model=model   
        self.llm_formulator = get_llm(model_name=self.model,temperature=0.1)
        print("수식화 준비완료!")

    def formulate(self,problem,extraction):
        comments_text=""
        message = self.FORWARD_TASK_FORMULATOR.format(
            problem_description = problem,
            ##code_example = problem['code_example'],
            extracted_queries = extraction,
            comments_text= comments_text
        )
        raw_output = self.llm_formulator.invoke(message).content
        cleaned_json = self._extract_json(raw_output)
        print("수식화 완료!")
        return cleaned_json
    

    def _extract_json(self,text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text # 매칭 실패 시 원본 반환