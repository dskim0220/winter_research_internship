import sys
import os
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

from utils import extract_code_from_string

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

from custom_callback import get_custom_callback, get_llm

def solve(problem_data, model_name='gemini-1.5-flash'):
    problem_description = problem_data['description']
    code_example = problem_data['code_example']

    MAX_TRIALS = 5
    history_answer = []
    for i in range(MAX_TRIALS):
        prompt_template = """You are a Python programmer in the field of operations research and optimization. Your proficiency in utilizing third-party libraries such as Gurobi is essential. In addition to your expertise in Gurobi, it would be great if you could also provide some background in related libraries or tools, like NumPy, SciPy, or PuLP.
You are given a specific problem. You aim to develop an efficient Python program that addresses the given problem.
Now the origin problem is as follow:
{problem_description}
Let's analyse the problem step by step, and then give your Python code.
Here is a starter code:
{code_example}"""
        if len(history_answer) != 0:
            prompt_template = prompt_template + '\nThe code looks like as following:\n' + "\n".join(history_answer)
        llm = get_llm(model_name, temperature=0)
        llm_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(prompt_template)
        )
        answer = llm_chain.predict(problem_description=problem_description, code_example=code_example)
        code = extract_code_from_string(answer)
        history_answer.append(code)
    return code
