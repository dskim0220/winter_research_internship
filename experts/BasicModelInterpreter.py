import os
import torch
import requests
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

# 1. Blackwell(sm_121) 하드웨어 호환성 강제 설정
os.environ["TORCH_CUDA_ARCH_LIST"] = "12.1"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
    
class BasicModelInterpreter():
    def __init__(self,model_name,url):
        self.url = url
        self.model_name = model_name
        self.role_description = 'Your role is to perform a "Full-Sentence-Extraction" to ensure no information loss for mathematical modeling.'
        self.task = """1. Identify all entities (Suppliers, Nodes, Products).
2. Determine if a decision is a 'How much' (Integer/Continuous) OR 'Whether to' (Binary).
3. Identify "Conditional Logic": Does selecting A force a limit on B? (If-Then).
4. Identify "Unit Consistency": Ensure you don't add 'Orders' to 'Tables'."""
        self.rules = """[STRICT EXTRACTION RULES]
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
[Output Rules]
1. Response must be a single valid JSON object.
2. No conversational text or markdown code blocks.
3. Use double backslashes (\\\\) for all LaTeX commands to ensure JSON compatibility.
   """
        self.output_format = """
{
  "Set": [
    { "id": "I", "User Query": "Factories ...", "Latex Model": "I" }
  ],
  "Parameter": [
    { "id": "c", "User Query": "Transportation ...", "Latex Model": "c_{ij}", "index": ["i", "j"] }
  ],
  "Decision Variables": [
    { 
      "id": "x", 
      "User Query": "Amount ...", 
      "Latex Model": "x_{ij}", 
      "index": ["i", "j"], 
      "domain": "continuous", 
      "lower_bound": 0 
    }
  ],
  "Objective function": [
    { "id": "OBJ", "sense": "min", "User Query": "Minimize ...", "Latex Model": "\\\\min ..." }
  ],
  "Constraints": [
    { "id": "C1", "User Query": "Description ...", "Latex Model": "..." }
  ]
}
"""
        
    def interpret(self, problem_description,feedback):
        problem = problem_description
        full_prompt = f"""[Role] {self.role_description}
[Problem] {problem}
[Feedback] {feedback}
[Task] {self.task}
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
        print("basic interpretation 요청중...")
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            print("basic interpretation 완료!")
            return response.json().get('response', '').strip()       
        
        except Exception as e:
            return f"basic interpretation 실패: {e}"
        
                