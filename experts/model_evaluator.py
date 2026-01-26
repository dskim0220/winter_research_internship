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
Analyze the provided problem description and perform a dual task: 
1) Formulate the mathematical model using LaTeX within a structured JSON.
2) Critically evaluate the formulation's alignment with the problem constraints and provide feedback.

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
    "CONFIDENCE_SCORE": 0.00,
    "OVERALL_FEEDBACK": "General assessment of the model's completeness and assumptions.",
    "SETS_FEEDBACK": "Rationale for the defined index sets and their ranges.",
    "PARAMETERS_FEEDBACK": "Explanation of given constants, data values, and their units.",
    "VARIABLES_FEEDBACK": "Justification for variable types (Binary/Integer/Cont) and decision units.",
    "OBJECTIVE_FEEDBACK": "Reasoning behind the objective function's structure and optimization goal.",
    "CONSTRAINTS_FEEDBACK": "Detailed logic for all functional constraints, including Big-M or conditional handling."
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