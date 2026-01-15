import sys
import os

from experts.base_expert import BaseExpert

from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
#from langchain_google_genai import ChatGoogleGenerativeAI

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)
from custom_callback_qwen import get_custom_callback, get_llm

class ParameterExtractor(BaseExpert):

    ROLE_DESCRIPTION = 'You are an expert that identifies and extracts relevant variables from the problem statement.'
    FORWARD_TASK = '''As a parameter extraction expert, your role is to identify and extract the relevant variables, constrans, objective from the problem statement. 
Your expertise in the problem domain will help in accurately identifying and describing these variables. 
Please review the problem description and provide the extracted variables along with their definitions: 
{problem_description}

And the comments from other experts are as follow:
{comments_text}

Please note that the information you extract is for the purpose of modeling, which means your variables, constraints, and objectives need to meet the requirements of a solvable LP or MIP model.

IMPORTANT OUTPUT RULES:
1) Return ONLY a valid JSON object. No extra text or explanations.
2) Do NOT use LaTeX symbols (e.g., no \leq, \geq, \text).
3) Use ONLY ASCII operators: <=, >=, =.
4) Your output MUST follow this format:
{{
    "VARIABLES": "List of variables",
    "CONSTRAINTS": "List of constraints using <=, >=, =",
    "OBJECTIVE": "Objective function"
}}
'''
    BACKWARD_TASK = '''When you are solving a problem, you get a feedback from the external environment. You need to judge whether this is a problem caused by you or by other experts (other experts have given some results before you). If it is your problem, you need to give Come up with solutions and refined code.

The original problem is as follow:
{problem_description}

The code you give previously is as follow:
{previous_answer}
    
The feedback is as follow:
{feedback}

The output format is a JSON structure followed by refined code:
{{
    'is_caused_by_you': false,
    'reason': 'leave empty string if the problem is not caused by you',
    'refined_result': 'Your refined code...'
}}
'''

    def __init__(self, model):
        super().__init__(
            name='Parameter Extractor',
            description='Skilled in programming and coding, capable of implementing the optimization solution in a programming language.',
            model=model   
        )
        self.llm = get_llm(model_name=self.model,temperature=0.1)

        self.forward_prompt_template = self.ROLE_DESCRIPTION + '\n' + self.FORWARD_TASK
        self.forward_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.forward_prompt_template)
        )
        self.backward_prompt_template = self.ROLE_DESCRIPTION + '\n' + self.BACKWARD_TASK
        self.backward_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.backward_prompt_template)
        )

    def forward(self, problem, comment_pool):
        self.problem = problem
        comments_text = comment_pool.get_current_comment_text()
        print('Input')
        print(self.FORWARD_TASK.format(
            problem_description=problem['description'], 
            comments_text=comments_text
        ))
        print()
        output = self.forward_chain.predict(
            problem_description=problem['description'], 
            comments_text=comments_text
        )
        self.previous_answer = output
        return output

    def backward(self, feedback_pool):
        if not hasattr(self, 'problem'):
            raise NotImplementedError('Please call forward first!')
        output = self.backward_chain.predict(
            problem_description=self.problem['description'], 
            previous_answer=self.previous_answer,
            feedback=feedback_pool.get_current_comment_text())
        return output
