import sys
import os
#from langchain_core.prompts import PromptTemplate
#from langchain_classic.chains.llm import LLMChain
#from langchain_google_genai import ChatGoogleGenerativeAI

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

#from custom_callback_qwen import get_custom_callback, get_llm

class BaseExpert(object):

    def __init__(self, name, description, model):
        self.name = name
        self.description = description
        self.model = model

        self.llm = get_llm(model_name=self.model,temperature=0.1)
        self.forward_prompt_template = self.ROLE_DESCRIPTION + '\n' + self.FORWARD_TASK
        self.forward_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.forward_prompt_template)
        )
        if hasattr(self, 'BACKWARD_TASK'):
            self.backward_prompt_template = self.ROLE_DESCRIPTION + '\n' + self.BACKWARD_TASK
            self.backward_chain = LLMChain(
                llm=self.llm,
                prompt=PromptTemplate.from_template(self.backward_prompt_template)
            )

    def forward(self):
        pass

    def backward(self):
        pass

    def __str__(self):
        return f'{self.name}: {self.description}'
