"""
perf.py
-------
크기별로 MAC 연산이 얼마나 걸리는지 시간을 재는 부분.
"""

import time
from core import make_matrix, mac


def make_dummy_matrix(size, offset):
    """성능 측정용으로 아무 값이나 채운 행렬을 만든다. (값 자체는 중요하지 않음)"""
    data = [[(i * size + j + offset) % 7 for j in range(size)] for i in range(size)]
    return make_matrix(size, data)


def measure_mac_time(size, repeat=10):
    """size x size MAC 연산을 repeat번 반복해서 평균 시간(ms)을 구한다."""
    pattern = make_dummy_matrix(size, 0)
    filt = make_dummy_matrix(size, 3)

    total_time = 0
    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filt)  # 여기(연산 구간)만 시간을 잰다. 입출력은 포함하지 않는다.
        end = time.perf_counter()
        total_time += (end - start) * 1000  # ms 단위로 변환

    avg_time = total_time / repeat
    op_count = size * size
    return avg_time, op_count


def print_perf_table(sizes, repeat=10):
    """여러 크기에 대해 성능을 측정하고 표로 출력한다."""
    print("\n[성능 분석] MAC 연산 평균 시간 (10회 반복 평균)")
    print(f"{'크기(N x N)':<15}{'평균 시간(ms)':<18}{'연산 횟수(N^2)':<15}")
    print("-" * 48)

    for size in sizes:
        avg_time, op_count = measure_mac_time(size, repeat)
        label = f"{size}x{size}"
        print(f"{label:<15}{avg_time:<18.6f}{op_count:<15}")


if __name__ == "__main__":
    print_perf_table([3, 5, 13, 25])
    print("\n[perf.py 테스트 통과]")