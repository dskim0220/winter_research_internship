import sys
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.callbacks import BaseCallbackHandler

from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain


from utils import extract_code_from_string

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

from custom_callback_qwen import get_custom_callback, get_llm

def solve(problem, model_name="Qwen/Qwen2.5-3B-Instruct"):
    prompt_template = """You are a Python programmer in the field of operations research and optimization. Your proficiency in utilizing third-party libraries such as Gurobi is essential. In addition to your expertise in Gurobi, it would be great if you could also provide some background in related libraries or tools, like NumPy, SciPy, or PuLP.
You are given a specific problem. You aim to develop an efficient Python program that addresses the given problem.
Now the origin problem is as follow:\n{problem}\nGive your Python code directly."""
    llm = get_llm(model_name, temperature=0.1)
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt_template)
    )
    answer = llm_chain.predict(problem=problem)
    code = extract_code_from_string(answer)
    return code
