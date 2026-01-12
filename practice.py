import pandas as pd

# 간단한 데이터프레임 만들기
data = {'이름': ['A', 'B', 'C'], '램 용량': ['16GB', '32GB', '256GB']}
df = pd.DataFrame(data)

print("--- 아나콘다 연동 성공! ---")
print(df)

