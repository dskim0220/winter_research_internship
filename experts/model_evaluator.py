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

class ModelEvaluator(BaseExpert):

    ROLE_DESCRIPTION = 'You are an expert in mathematical optimization and modeling. Your role is to translate complex natural language descriptions into rigorous mathematical formulations and evaluate the modeling accuracy.'
    FORWARD_TASK = '''
Analyze the provided problem description and perform a rigorous auditing task: 
1) Audit the LaTeX model against the natural language problem.
2) Detect and flag "Modeling Hallucinations" (e.g., using constants not in the text, or ignoring given constraints).
3) Verify Dimensional Consistency: Ensure units (e.g., USD, Kg, Minutes) align across equations.
4) Linearity Audit: Explicitly check for non-linearities (variable multiplications) that violate MILP standards.

Problem Description:
{problem_description}

LaTeX model:
{LaTeX_json}

IMPORTANT OUTPUT RULES:
1) Output Integrity: Return ONLY a valid JSON object. No preamble, postscript, or markdown code blocks.
2) LaTeX Standard: Use standard LaTeX for all mathematical components (e.g., \sum, \forall, \in, \ge, \le, \min, \max).
3) Decision Unit Precision: Categorize variables strictly: Binary, Integer, or Continuous.
4) Logical Constraint Modeling: For conditional logic (If-Then), use Big-M notation or linear reformulations in LaTeX.
5) Descriptive Feedback: Each "FEEDBACK" field must justify the specific modeling choice.
6) Data Consistency: Every set defined in "SETS" must be utilized in other components.
7) Confidence Quantification: Assign a CONFIDENCE_SCORE [0.0, 1.0]:
   - [0.85 - 1.0]: Complete model, no ambiguity.
   - [0.70 - 0.84]: Solid, but 1-2 minor assumptions made.
   - [0.50 - 0.69]: Major assumptions or complex logic (Big-M) needs human verification.
   - [Below 0.5]: Critical information missing.

JSON Format:
{{
    "CONFIDENCE_SCORE": 0.0,
    "OVERALL_FEEDBACK": "...",
    "DATA_FIDELITY_CHECK": "Did the model use the exact numbers from the problem? Flag any arbitrary constants.",
    "LOGICAL_COUPLING_CHECK": "Are Binary and Continuous variables correctly linked (e.g., Big-M)?",
    "LINEARITY_VALIDATION": "Confirm no variable-to-variable multiplication exists.",
    "DIMENSIONAL_ANALYSIS": "Do the units on LHS and RHS of all constraints match?",
    "CONSTRAINTS_FEEDBACK": "..."
}}
'''

    def __init__(self, model):
        super().__init__(
            name='model_evaluator',
            description='Decomposes natural language problems into 6-part structured modeling data',#자연어 JSON 제작
            model=model   
        )
        self.llm = get_llm(model_name=self.model,temperature=0.1)

    
    def forward(self,problem,LaTeX_json):
        comments_text=""
        message = self.forward_prompt_template.format(
            problem_description = problem,
            ##code_example = problem['code_example'],
            LaTeX_json = LaTeX_json,
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