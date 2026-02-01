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

class ModelEvaluatorV2(BaseExpert):

    ROLE_DESCRIPTION = 'Mathematical Optimization Auditor (Triple-Verification)'
    FORWARD_TASK = '''
Cross-verify (1) Problem Description, (2) Extracted Queries, and (3) LaTeX Formulations.

[AUDIT PRIORITIES]
1. GROUNDING: Identify any "hallucinated" queries or constraints not in the original text.
2. DATA FIDELITY: Ensure exact numerical values (Price, Cost, Quota) are mapped 1:1. Zero-filling or placeholders = Failure.
3. LOGICAL COUPLING: Verify Big-M linking ($x \le M \cdot y$) between Decision (Binary) and Quantity (Int/Cont) variables.
4. MATH INTEGRITY: Check for MILP linearity (no $var \times var$) and dimensional/unit consistency.
5. OBJECTIVE STRUCTURE: Confirm Profit = (Revenue - Variable Cost) - Fixed Cost.

[SCORING RULE]
- Penalty: Drop Confidence Score below 0.5 if major numerical data is missing or Fixed Costs are treated as constraints instead of objective terms.

[INPUT]
1. Original Problem: {problem_description}
2. Model JSON: {model_json}

Return ONLY JSON:
{{
    "CONFIDENCE_SCORE": 0.0,
    "OVERALL_FEEDBACK": "Summary of accuracy and grounding.",
    "QUERY_GROUNDING_AUDIT": "List any fabricated or missing information.",
    "DATA_FIDELITY_CHECK": "Identify mismatches between Query numbers and LaTeX numbers.",
    "LOGICAL_COUPLING_CHECK": "Check Big-M links and Binary/Continuous separation.",
    "LINEARITY_VALIDATION": "Confirm no non-linear terms (MILP compliance).",
    "DIMENSIONAL_ANALYSIS": "Verify unit consistency across equations.",
    "CONSTRAINTS_FEEDBACK": "Detailed mapping critique for each rule_id."
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