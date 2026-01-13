import os
import threading
from contextvars import ContextVar
from typing import Optional, Generator
from contextlib import contextmanager

# 최신 랭체인 코어에서 가져옵니다.
from langchain_core.callbacks import BaseCallbackHandler
from langchain_google_genai import ChatGoogleGenerativeAI

if"GOOGLE_API_KEY"not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "Your Google API Key Here"

# 1. 전역 컨텍스트 변수 (바구니)
gemini_callback_var: ContextVar[Optional[BaseCallbackHandler]] = ContextVar(
    "gemini_callback", default=None
)

# 2. 대리인(Proxy) 핸들러 클래스 정의 (이게 Pydantic 에러를 잡는 핵심입니다!)
class ProxyCallbackHandler(BaseCallbackHandler):
    """
    이 핸들러는 항상 모델에 등록되어 있지만, 
    실제 작업은 ContextVar에 등록된 핸들러가 있을 때만 수행합니다.
    """
    def on_llm_start(self, serialized, prompts, **kwargs):
        handler = gemini_callback_var.get()
        if handler:
            try:
                handler.on_llm_start(serialized, prompts, **kwargs)
            except Exception:
                pass

    def on_llm_end(self, response, **kwargs):
        handler = gemini_callback_var.get()
        if handler:
            try:
                handler.on_llm_end(response, **kwargs)
            except Exception:
                pass
                
    def on_llm_new_token(self, token, **kwargs):
        handler = gemini_callback_var.get()
        if handler:
            try:
                handler.on_llm_new_token(token, **kwargs)
            except Exception:
                pass

    def on_llm_error(self, error, **kwargs):
        handler = gemini_callback_var.get()
        if handler:
            try:
                handler.on_llm_error(error, **kwargs)
            except Exception:
                pass

# 3. 실제 토큰 계산 로직이 담긴 핸들러
class CustomCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.successful_requests = 0
        self._lock = threading.Lock()

    def on_llm_end(self, response, **kwargs):
        try:
            # Gemini 응답 객체에서 메타데이터 추출
            # generations -> list -> ChatGeneration -> message -> usage_metadata
            if response.generations:
                generation = response.generations[0][0]
                if hasattr(generation, 'message') and hasattr(generation.message, 'usage_metadata'):
                    usage = generation.message.usage_metadata
                    # usage가 None이 아닐 때만 집계
                    if usage:
                        with self._lock:
                            self.prompt_tokens += usage.get("input_tokens", 0)
                            self.completion_tokens += usage.get("output_tokens", 0)
                            self.total_tokens += usage.get("total_tokens", 0)
                            self.successful_requests += 1
        except Exception:
            pass

# 4. with 문에서 사용할 컨텍스트 매니저
@contextmanager
def get_custom_callback() -> Generator[CustomCallbackHandler, None, None]:
    cb = CustomCallbackHandler()
    token = gemini_callback_var.set(cb) # 바구니에 핸들러 등록
    try:
        yield cb
    finally:
        gemini_callback_var.reset(token) # 바구니 비우기

# 5. LLM 생성 함수 (수정 완료)
def get_llm(model_name, temperature):
    return ChatGoogleGenerativeAI(
        model=model_name,  # model_name 인자를 'model'로 매핑
        temperature=temperature,
        # [중요] 함수(lambda)가 아니라 '객체'를 생성해서 넣어야 에러가 안 납니다.
        callbacks=[ProxyCallbackHandler()] 
    )