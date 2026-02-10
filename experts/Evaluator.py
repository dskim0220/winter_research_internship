import os
import torch
import requests
import re
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

# 1. Blackwell(sm_121) 하드웨어 호환성 강제 설정
os.environ["TORCH_CUDA_ARCH_LIST"] = "12.1"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
    
class Evaluator():
    def __init__(self,model_name,url,threshold):
        self.url = url
        self.model_name = model_name
        self.threshold = threshold
        self.role_description = 'Mathematical Optimization Auditor (Triple-Verification)'
        self.task = 'Cross-verify (1) Problem Description, (2) Extracted Queries, and (3) LaTeX Formulations.'
        
        self.rules = """[AUDIT PRIORITIES & CRITICAL CHECKS]
1. NUMERICAL HARVESTING: Are the numbers in LaTeX (e.g., 120, 150, 7) EXACTLY the same as the problem text? 
2. UNIT MISMATCH (FATAL): Did the model add 'Orders' to 'Tables'? (e.g., n_A + n_B >= 150 is WRONG if 150 is tables and n is orders).
3. THE BINARY BRIDGE: Every "If" condition must have a Binary variable ($y$). Does every $x$ (quantity) have a corresponding $y$ (selection) linked via Big-M ($x \le M \cdot y$)?
4. OBJECTIVE PURITY: Ensure Fixed Costs are multiplied by Binary variables in the Objective function, not hidden in Constraints.
5. DIMENSIONAL SANITY: Check if $/unit \times units = Total$.

[AUDIT PROCESS - STEP-BY-STEP]
- Step 1: List all numbers in the Problem. Compare them to the PARAMETERS in JSON.
- Step 2: Check every 'if-then' sentence. Verify if $y_{{A}} \to y_{{B}}$ or $x_{{A}} \to y_{{A}}$ logic exists in LaTeX.
- Step 3: Identify any $var \times var$ terms (Non-linear) which will break MILP solvers."""
        
        self.output_format = """[OUTPUT FORMAT]
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
}}"""
        
    def evaluate(self, problem_description, whole_interpretation):
        problem = problem_description
        full_prompt = f"""[Role] {self.role_description}
[Problem] {problem}
[Whole Interpretation] {whole_interpretation}
[Task] {self.task}
[Threshold] {self.threshold}
[Rules] {self.rules}
[Format] {self.output_format}"""
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 2048   
            }
        }
        print("model evaluation 요청중...") 
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            print("model evaluation 완료!")
            return response.json().get('response', '').strip()       
        
        except Exception as e:
            return f"model evaluation 실패: {e}"
        
    def _extract_json(self,text):
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text # 매칭 실패 시 원본 반환