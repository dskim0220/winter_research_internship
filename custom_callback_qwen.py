import os
import threading
from contextvars import ContextVar
from typing import Optional, Generator
from contextlib import contextmanager

# [변경] HuggingFace 관련 임포트
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace

# [공통] 랭체인 코어 임포트
from langchain_core.callbacks import BaseCallbackHandler

_shared_chat_model = None

# 1. 전역 컨텍스트 변수 (이름만 qwen으로 변경, 기능은 동일)
qwen_callback_var: ContextVar[Optional[BaseCallbackHandler]] = ContextVar(
    "qwen_callback", default=None
)

# 2. 대리인(Proxy) 핸들러 (구조 100% 동일)
class ProxyCallbackHandler(BaseCallbackHandler):
    """
    ContextVar에 등록된 핸들러가 있을 때만 동작을 위임하는 프록시 핸들러
    """
    def on_llm_start(self, serialized, prompts, **kwargs):
        handler = qwen_callback_var.get()
        if handler:
            try: handler.on_llm_start(serialized, prompts, **kwargs)
            except Exception: pass

    def on_llm_end(self, response, **kwargs):
        handler = qwen_callback_var.get()
        if handler:
            try: handler.on_llm_end(response, **kwargs)
            except Exception: pass
                
    def on_llm_new_token(self, token, **kwargs):
        handler = qwen_callback_var.get()
        if handler:
            try: handler.on_llm_new_token(token, **kwargs)
            except Exception: pass

    def on_llm_error(self, error, **kwargs):
        handler = qwen_callback_var.get()
        if handler:
            try: handler.on_llm_error(error, **kwargs)
            except Exception: pass

# 3. 실제 토큰 계산 핸들러
class CustomCallbackHandler(BaseCallbackHandler):
    def __init__(self,tokenizer=None):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.successful_requests = 0
        self._lock = threading.Lock()
        self.tokenizer=tokenizer
    def on_llm_start(self,serialized,prompts,**kwargs):
        if self.tokenizer:
            count = 0
            for p in prompts:
                count+=len(self.tokenizer.encode(p))
            with self._lock:
                self.prompt_tokens += count

    def on_llm_end(self, response, **kwargs):

        meta_found = False
        try:
            if response.generations:
                generation = response.generations[0][0]
                if hasattr(generation, 'message') and hasattr(generation.message, 'usage_metadata'):
                    usage = generation.message.usage_metadata
                    if usage:
                        with self._lock:
                            # 메타데이터가 있으면 그걸 신뢰하여 덮어쓰거나 더함
                            # (주의: on_llm_start에서 이미 더했으므로 중복 방지 로직이 필요할 수 있으나,
                            #  보통 로컬 모델은 여기가 없으므로 바로 아래 else로 넘어갑니다.)
                            self.prompt_tokens += usage.get("input_tokens", 0)
                            self.completion_tokens += usage.get("output_tokens", 0)
                            self.total_tokens += usage.get("total_tokens", 0)
                            self.successful_requests += 1
                            meta_found = True
        except Exception:
            pass

        # 2. 메타데이터가 없고 토크나이저가 있다면 직접 계산 (로컬 모델용)
        if not meta_found and self.tokenizer and response.generations:
            completion_count = 0
            # response.generations는 [[Generation, ...], ...] 형태
            for generations_list in response.generations:
                for gen in generations_list:
                    # 생성된 텍스트(gen.text)를 토큰화하여 계산
                    completion_count += len(self.tokenizer.encode(gen.text))
            
            with self._lock:
                self.completion_tokens += completion_count
                self.total_tokens = self.prompt_tokens + self.completion_tokens
                self.successful_requests += 1

# 4. 컨텍스트 매니저
@contextmanager
def get_custom_callback(tokenizer) -> Generator[CustomCallbackHandler, None, None]:
    cb = CustomCallbackHandler(tokenizer=tokenizer)
    token = qwen_callback_var.set(cb) # 바구니 등록
    try:
        yield cb
    finally:
        qwen_callback_var.reset(token) # 바구니 비우기

# [핵심 변경] 5. LLM 생성 함수 (Qwen 로드 및 파이프라인 구성)
# 모델을 매번 로드하면 느리므로, 전역 혹은 캐시로 한 번만 로드하는 것이 좋습니다.
# 여기서는 예시를 위해 함수 내부에 둡니다.

def get_llm(model_name, temperature):
    global _shared_chat_model

    if _shared_chat_model is not None:
        return _shared_chat_model
    
    # 1) 토크나이저 및 모델 로드 (Transformers)
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto", # GPU 자동 할당
        low_cpu_mem_usage=True,
        local_files_only=True
    )

    # 2) 파이프라인 생성 
    pipe = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=2048, # 출력 최대 길이
        temperature=temperature,
        return_full_text = False,
        #device_map="auto",
        trust_remote_code=True
        #top_p=0.9,
        # model_kwargs는 파이프라인 생성 시 전달
    )

    # 3) LangChain LLM 래퍼 (Pipeline -> LLM)
    llm = HuggingFacePipeline(pipeline=pipe)

    # 4) Chat Model 래퍼 (LLM -> Chat Model)
    # Qwen은 채팅 모델이므로 ChatHuggingFace로 감싸주어야 시스템/사용자 프롬프트가 정상 동작합니다.
    _shared_chat_model = ChatHuggingFace(
        llm=llm,
        tokenizer=tokenizer,
        callbacks=[ProxyCallbackHandler()] # 여기에 프록시 핸들러 등록
    )

    return _shared_chat_model