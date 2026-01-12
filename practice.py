import langchain
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyB7g1C9eS9TGR3KcKCEI6aZkGjOZfxKYmA"

llm = ChatGoogleGenerativeAI(
    model="gemini-1.0-pro",
    temperature=0.0
)

response = llm.invoke("Say hello in Korean.")
print(response.content)
