import os
import torch
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

# 1. Blackwell(sm_121) 하드웨어 호환성 강제 설정
os.environ["TORCH_CUDA_ARCH_LIST"] = "12.1"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

# 모델 경로
path = "/home/logistics/.cache/huggingface/hub/models--Qwen--Qwen2.5-32B-Instruct-AWQ/snapshots/5c7cb76a268fc6cfbb9c4777eb24ba6e27f9ee6c"

print("--- 🚀 Blackwell(GB10) 가속 커널로 Qwen-32B 로딩 중... ---")

try:
    # 2. 모델 로드
    model = AutoAWQForCausalLM.from_quantized(
        path, 
        fuse_layers=True, 
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)

    # 3. NL2Opt 연구용 질문
    prompt = "Linear Programming 모델링 시, Gurobi에서 변수를 'Integer'와 'Continuous'로 설정할 때의 차이점을 설명해줘."
    msg = [{"role": "user", "content": prompt}]
    
    text = tokenizer.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to("cuda")

    # 4. 답변 생성 (Inference Mode 사용)
    print("--- ✍️ 답변 생성 중... ---\n")
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=512)
    
    print(f"AI 답변:\n{tokenizer.decode(out[0], skip_special_tokens=True).split('assistant')[-1].strip()}")

except Exception as e:
    print(f"❌ 에러 발생: {e}")
    print("팁: 여전히 커널 에러가 난다면 서버의 NVIDIA 드라이버가 570.xx 이상인지 확인해 주세요.")