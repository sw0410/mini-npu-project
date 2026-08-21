import time

EPSILON = 1e-9


def make_matrix(size, data=None):
    """전달받은 데이터의 행/열 크기를 검사합니다."""
    if len(data) != size:
        raise ValueError(f"행 개수가 {size}개가 아닙니다. (실제: {len(data)}개)")
    for row in data:
        if len(row) != size:
            raise ValueError(f"열 개수가 {size}개가 아닌 행이 있습니다. (실제: {len(row)}개)")

    return data


def mac(pattern, filt):
    """두 행렬의 같은 위치 값을 곱해서 전부 더합니다."""
    size = len(pattern)
    if len(filt) != size:
        raise ValueError("패턴과 필터의 크기가 일치하지 않습니다.")

    score = 0
    for i in range(size):
        for j in range(size):
            score += pattern[i][j] * filt[i][j]
    return score


def normalize_label(raw):
    """다양한 표기(+, cross, x)를 'Cross' 또는 'X'로 통일합니다."""
    text = str(raw).strip().lower()
    if text == "+" or text == "cross":
        return "Cross"
    if text == "x":
        return "X"
    raise ValueError(f"알 수 없는 라벨입니다: {raw}")


def decide(score_cross, score_x):
    """두 점수를 비교하여 판정합니다. (차이가 1e-9 미만이면 UNDECIDED)"""
    if abs(score_cross - score_x) < EPSILON:
        return "UNDECIDED"
    if score_cross > score_x:
        return "Cross"
    return "X"


def is_pass(decision, expected_raw):
    """판정 결과와 expected 정답이 일치하는지 확인합니다."""
    if decision == "UNDECIDED":
        return False
    try:
        expected = normalize_label(expected_raw)
    except ValueError:
        return False
    return decision == expected


def print_perf_table(sizes, repeat=10):
    """지정된 크기들에 대해 MAC 연산 평균 시간(ms)을 측정하여 출력합니다."""
    print("\n[성능 분석] MAC 연산 평균 시간 (10회 반복)")
    print(f"{'크기(N x N)':<15}{'평균 시간(ms)':<18}{'연산 횟수(N^2)':<15}")
    print("-" * 48)

    ## 3 / [3]
    for size in sizes:
        # 측정용 더미 행렬 생성
        dummy_pattern = [[1 for _ in range(size)] for _ in range(size)]
        dummy_filter = [[1 for _ in range(size)] for _ in range(size)]

        total_time = 0
        
        for _ in range(repeat):
            start = time.perf_counter()
            mac(dummy_pattern, dummy_filter)
            end = time.perf_counter()
            total_time += (end - start) * 1000

        avg_time = total_time / repeat
        op_count = size * size
        print(f"{size}x{size:<13}{avg_time:<18.6f}{op_count:<15}")