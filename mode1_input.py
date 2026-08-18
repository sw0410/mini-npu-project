"""
mode1_input.py
--------------
모드 1: 사용자가 콘솔에서 3x3 필터 2개(A, B)와 패턴을 직접 입력하는 부분.
"""

from core import make_matrix, print_matrix, mac
from judge import decide
from perf import print_perf_table

SIZE = 3


def read_one_row(prompt, n):
    """한 줄을 입력받아서 숫자 n개로 만든다. 실패하면 에러를 낸다."""
    text = input(prompt)
    parts = text.strip().split()

    if len(parts) != n:
        raise ValueError(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")

    numbers = []
    for p in parts:
        try:
            numbers.append(float(p))
        except ValueError:
            raise ValueError(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")

    return numbers


def read_matrix(name, size=SIZE):
    """name(예: '필터 A')에 해당하는 size x size 행렬을 한 줄씩 입력받는다.

    줄 하나가 잘못 입력되면 그 줄만 다시 입력받는다.
    """
    print(f"\n[{name}] {size}x{size} 행렬을 한 줄씩 입력하세요 (숫자 {size}개, 공백 구분).")

    rows = []
    row_num = 1
    while row_num <= size:
        try:
            row = read_one_row(f"  {row_num}행: ", size)
            rows.append(row)
            row_num += 1
        except ValueError as e:
            print(f"  -> {e}")
            # row_num을 올리지 않으므로 같은 행을 다시 입력받게 됨

    return make_matrix(size, rows)


def run_mode1():
    print("=" * 60)
    print("모드 1: 사용자 입력(3x3) 처리")
    print("=" * 60)

    filter_a = read_matrix("필터 A (Cross)")
    filter_b = read_matrix("필터 B (X)")

    print("\n[저장 확인]")
    print("필터 A:")
    print_matrix(filter_a)
    print("필터 B:")
    print_matrix(filter_b)

    pattern = read_matrix("입력 패턴")
    print("\n[저장 확인] 입력 패턴:")
    print_matrix(pattern)

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    decision = decide(score_a, score_b)

    print("\n[MAC 연산 결과]")
    print(f"  필터 A(Cross) 점수: {score_a}")
    print(f"  필터 B(X) 점수    : {score_b}")
    print(f"  판정              : {decision}")

    print_perf_table([SIZE])


if __name__ == "__main__":
    run_mode1()