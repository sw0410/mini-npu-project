"""
gen_data.py
-----------
과제 제출용 샘플 data.json 생성 스크립트.
(실행 시 한 번만 사용하는 유틸리티 - 최종 제출물에는 결과물인 data.json만 포함되면 된다)

구조:
{
  "filters": {
    "size_5":  {"cross": [[...]], "x": [[...]]},
    "size_13": {"cross": [[...]], "x": [[...]]},
    "size_25": {"cross": [[...]], "x": [[...]]}
  },
  "patterns": {
    "size_5_1":  {"input": [[...]], "expected": "+"},
    "size_5_2":  {"input": [[...]], "expected": "x"},
    ...
  }
}
"""
import json
import random

random.seed(42)


def make_cross(n):
    mid = n // 2
    return [[1 if (i == mid or j == mid) else 0 for j in range(n)] for i in range(n)]


def make_x(n):
    return [[1 if (i == j or i + j == n - 1) else 0 for j in range(n)] for i in range(n)]


def make_pattern(n, kind, noise=0):
    """kind: 'cross' or 'x'. noise만큼 임의 위치를 뒤집어 약간의 변형을 준다."""
    base = make_cross(n) if kind == "cross" else make_x(n)
    pat = [row[:] for row in base]
    for _ in range(noise):
        i = random.randrange(n)
        j = random.randrange(n)
        pat[i][j] = 1 - pat[i][j]
    return pat


data = {"filters": {}, "patterns": {}}

sizes = [5, 13, 25]
for n in sizes:
    data["filters"][f"size_{n}"] = {
        "cross": make_cross(n),
        "x": make_x(n),
    }

# 각 크기별로 정상 케이스 2개 + 약간의 노이즈가 섞인 케이스 1개씩 생성
idx_counter = {n: 0 for n in sizes}
for n in sizes:
    # 깨끗한 cross 패턴 -> expected '+'
    idx_counter[n] += 1
    data["patterns"][f"size_{n}_{idx_counter[n]}"] = {
        "input": make_pattern(n, "cross", noise=0),
        "expected": "+",
    }
    # 깨끗한 x 패턴 -> expected 'x'
    idx_counter[n] += 1
    data["patterns"][f"size_{n}_{idx_counter[n]}"] = {
        "input": make_pattern(n, "x", noise=0),
        "expected": "x",
    }
    # 약간의 노이즈가 섞인 cross 패턴 -> expected '+' (그래도 cross 쪽 점수가 더 높을 것)
    idx_counter[n] += 1
    data["patterns"][f"size_{n}_{idx_counter[n]}"] = {
        "input": make_pattern(n, "cross", noise=max(1, n // 8)),
        "expected": "+",
    }

# 크기 불일치(스키마 검증 실패) 케이스를 하나 일부러 추가한다: size_5_99 키인데 실제 input은 3x3
data["patterns"]["size_5_99"] = {
    "input": [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    "expected": "+",
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("data.json 생성 완료")
print("filters keys:", list(data["filters"].keys()))
print("patterns keys:", list(data["patterns"].keys()))