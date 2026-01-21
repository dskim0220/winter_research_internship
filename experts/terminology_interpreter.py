import sys
import os

import json
from experts.base_expert import BaseExpert
from utils import extract_code_from_string
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
#from langchain_google_genai import ChatGoogleGenerativeAI

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)
    
from custom_callback_qwen import get_custom_callback, get_llm

class TerminologyInterpreter(BaseExpert):

    ROLE_DESCRIPTION = 'You are a Domain Knowledge Expert. Your only goal is to provide concise, technical interpretations of complex terms to help solve optimization problems.'
    FORWARD_TASK = '''[System] Output ONLY a valid JSON list. Do not include markdown code blocks (```json), explanations, or any extra text. 
    
    [Background Knowledge]: {knowledge}. 

    [Problem Description]: {problem_description}

    [Task]
    Identify and interpret at most 3 hardest terminologies from the problem. Keep interpretations under 20 words.

    [Required Output Format]
    [
      {{
        "terminology": "...",
        "interpretation": "..."
      }}
    ]
'''

    BACKWARD_TASK = '''[System] You are an Error Analyist. Analyze the feedback and output ONLY a JSON structure.

    [Feedback]
    {feedback}

    [Previous Answer]
    {previous_answer}

    [Required Output Format]
    {{
        "is_caused_by_you": false,
        "reason": "short reason or empty if false",
        "refined_result": "updated interpretation or same if no change"
    }}
'''

    def __init__(self, model):
        super().__init__(
            name='Terminology Interpreter',
            description='Provides additional domain-specific knowledge to enhance problem understanding and formulation.',
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
            problem_description=problem, 
            knowledge='None',
            comments_text=comments_text
        ))
        print()

        output = self.forward_chain.predict(
            problem_description=problem, 
            knowledge='None',
            comments_text=comments_text
        )

        answer = ""
        parsed_output = []

        try:
            clean_json = extract_code_from_string(output)
            clean_json = clean_json.replace("```json", "").replace("```", "").strip()
            parsed_output = json.loads(clean_json)
            #output = json.loads(output)

        except Exception as e:
            print(f'Failed to parse JSON output from Terminology Interpreter. Error: {e}')
            print(f'Raw Output: {output}')
            parsed_output = []

        for item in parsed_output:
            #answer += item['terminology'] + ':' + item['interpretation'] + '\n'
            term = item.get('terminology','')
            interp = item.get('interpretation','')
            answer += term + ':'+interp + '\n'

        self.previous_answer = answer
        return answer

    def backward(self, feedback_pool):
        if not hasattr(self, 'problem'):
            raise NotImplementedError('Please call forward first!')
        output = self.backward_chain.predict(
            problem_description=self.problem, 
            previous_answer=self.previous_answer,
            feedback=feedback_pool.get_current_comment_text())
        return output


if __name__ == '__main__':
    from comment_pool import CommentPool
    import numpy as np
    num_experts = 0
    all_experts = []
    problem = {
        'description': 'A telecom company needs to build a set of cell towers to provide signal coverage for the inhabitants of a given city. A number of potential locations where the towers could be built have been identified. The towers have a fixed range, and due to budget constraints only a limited number of them can be built. Given these restrictions, the company wishes to provide coverage to the largest percentage of the population possible. To simplify the problem, the company has split the area it wishes to cover into a set of regions, each of which has a known population. The goal is then to choose which of the potential locations the company should build cell towers on in order to provide coverage to as many people as possible. Please formulate a mathematical programming model for this problem based on the description above.',
    }
    comment_pool = CommentPool(all_experts, visible_matrix=np.ones((num_experts, num_experts)))
    expert = TerminologyInterpreter('Qwen/Qwen2.5-3B-Instruct')
    answer = expert.forward(problem, comment_pool)
    print(answer)
    ##temperate
