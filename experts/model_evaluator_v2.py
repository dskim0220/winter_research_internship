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

class ModelEvaluatorV2(BaseExpert):

    ROLE_DESCRIPTION = 'Mathematical Optimization Auditor (Triple-Verification)'
    FORWARD_TASK = '''
Cross-verify (1) Problem Description, (2) Extracted Queries, and (3) LaTeX Formulations.

[AUDIT PRIORITIES & CRITICAL CHECKS]
1. NUMERICAL HARVESTING: Are the numbers in LaTeX (e.g., 120, 150, 7) EXACTLY the same as the problem text? 
2. UNIT MISMATCH (FATAL): Did the model add 'Orders' to 'Tables'? (e.g., n_A + n_B >= 150 is WRONG if 150 is tables and n is orders).
3. THE BINARY BRIDGE: Every "If" condition must have a Binary variable ($y$). Does every $x$ (quantity) have a corresponding $y$ (selection) linked via Big-M ($x \le M \cdot y$)?
4. OBJECTIVE PURITY: Ensure Fixed Costs are multiplied by Binary variables in the Objective function, not hidden in Constraints.
5. DIMENSIONAL SANITY: Check if $/unit \times units = Total$.

[AUDIT PROCESS - STEP-BY-STEP]
- Step 1: List all numbers in the Problem. Compare them to the PARAMETERS in JSON.
- Step 2: Check every 'if-then' sentence. Verify if $y_{{A}} \to y_{{B}}$ or $x_{{A}} \to y_{{A}}$ logic exists in LaTeX.
- Step 3: Identify any $var \times var$ terms (Non-linear) which will break MILP solvers.

[INPUT]
1. Original Problem: {problem_description}
2. Model JSON: {model_json}

[OUTPUT FORMAT]
Return ONLY a JSON:
{{
    "CONFIDENCE_SCORE": 0.0,
    "CRITICAL_FAILURE_FOUND": "YES/NO",
    "DATA_FIDELITY": {{
        "problem_numbers": [120, 110, 150],
        "latex_numbers": [120, 110, 150],
        "mismatch": "List any differences"
    }},
    "LOGICAL_LINKING_AUDIT": "Verify Big-M ($x \\le M \\cdot y$) and Binary logic ($y_B \\ge y_A$).",
    "DIMENSIONAL_CONSISTENCY": "Check if (Price * Quantity) logic is applied correctly in Objective.",
    "CONSTRAINTS_FEEDBACK": [
        {{ "rule_id": "R1", "status": "PASS/FAIL", "reason": "Detailed critique" }}
    ],
    "FINAL_VERDICT": "Final summary for the Generator to fix the code."
}}
'''

    def __init__(self, model):
        super().__init__(
            name='model_evaluator',
            description='Decomposes natural language problems into 6-part structured modeling data',#자연어 JSON 제작
            model=model   
        )
        self.llm = get_llm(model_name=self.model,temperature=0.1)

    
    def forward(self,problem,model_json):
        comments_text=""
        message = self.forward_prompt_template.format(
            problem_description = problem,
            ##code_example = problem['code_example'],
            model_json = model_json,
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