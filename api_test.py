import requests
import json
import os
from dotenv import load_dotenv
import re

load_dotenv()

url = "https://genai.postech.ac.kr/agent/api/a1/gpt"
api_key = os.getenv("api_key") 
file_path = "dataset/newset/routing_problem/description.txt"
problem_text = ""

try:
    with open(file_path, "r", encoding="utf-8") as f:
        problem_text = f.read()
    print("파일 읽기 성공!")
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
    exit(-1)


headers = {
    "Content-Type": "application/json",
    "X-Api-Key": api_key
}


payload = {
    "message": f"{problem_text}\n\n---\n Abobe is the problem description. Generate the Gurobi Python code to solve this problem.",
    "stream": False,
    "files": []
}

try:
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("호출 (상태 코드: 200)")
        
        # [수정된 부분] 전체 응답 구조를 그대로 출력해서 확인합니다.
        print("-" * 30)
        print("서버 응답 원본 데이터:")
        res_data = response.json()
         
        print(res_data)
        print("-" * 30)
        
    else:
        print(f"실패 (상태 코드: {response.status_code})")
        print("에러 내용:", response.text)

except Exception as e:
    print(f"에러 발생: {e}")