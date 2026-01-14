import os
import torch

from langchain_core.messages import HumanMessage, SystemMessage

def ask_gemini_flash(question: str, system_instruction: str = ""):
    """
    Gemini 2.5 Flash를 사용하여 답변을 생성합니다.
    """
    # 모델 설정: max_retries가 503 에러를 내부적으로 처리합니다.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        max_retries=5,
        convert_system_message_to_human=True
    )

    # 메시지 레이아웃 구성
    messages = [
        SystemMessage(content=system_instruction),
        HumanMessage(content=question)
    ]

    # 호출 및 결과 반환
    response = llm.invoke(messages)
    return response.content


if __name__ == "__main__":
    os.environ["GOOGLE_API_KEY"] = "AIzaSyB7g1C9eS9TGR3KcKCEI6aZkGjOZfxKYmA" 

    system_instruction = "당신은 산업 데이터 사이언스 전문가입니다."
    prompt = "대한민국의 수도는 어디야? 정답만 말해"
    answer = ask_gemini_flash(prompt, system_instruction)
    
    print(answer)


    