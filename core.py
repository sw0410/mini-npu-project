"""
core.py
--------
가장 핵심이 되는 부분.

1) 행렬(패턴/필터)을 리스트의 리스트(List of List)로 저장하고,
   특정 위치의 값을 읽고 쓰는 함수들.
2) MAC(Multiply-Accumulate) 연산: 두 행렬을 같은 위치끼리 곱해서 다 더하는 함수.
   -> NumPy 같은 외부 라이브러리 없이 for문으로만 구현.
"""


def make_matrix(size, data=None):
    """size x size 크기의 행렬을 만든다.

    data를 주면 그 값을 그대로 쓰고, 안 주면 전부 0으로 채운다.
    행렬은 그냥 파이썬 리스트의 리스트(2차원 리스트)다.
    """
    if data is None:
        # 0으로 채워진 size x size 행렬
        return [[0 for _ in range(size)] for _ in range(size)]

    # data가 제대로 된 size x size 모양인지 확인
    if len(data) != size:
        raise ValueError(f"행 개수가 {size}개가 아닙니다. (실제: {len(data)}개)")
    for row in data:
        if len(row) != size:
            raise ValueError(f"열 개수가 {size}개가 아닌 행이 있습니다. (실제: {len(row)}개)")

    return data


def get_value(matrix, row, col):
    """행렬의 (row, col) 위치 값을 읽는다."""
    return matrix[row][col]


def set_value(matrix, row, col, value):
    """행렬의 (row, col) 위치에 값을 저장한다."""
    matrix[row][col] = value


def print_matrix(matrix):
    """행렬을 보기 좋게 한 줄씩 출력한다. (1.0 대신 1처럼 깔끔하게 표시)"""
    for row in matrix:
        print(" ".join(format_number(v) for v in row))


def format_number(v):
    """정수와 같은 값이면 소수점 없이, 아니면 그대로 문자열로 바꾼다."""
    if float(v) == int(v):
        return str(int(v))
    return str(v)


def mac(pattern, filt):
    """MAC(Multiply-Accumulate) 연산.

    pattern과 filt(필터)를 같은 위치끼리 곱한 다음, 그 값들을 전부 더해서 반환한다.
    외부 라이브러리 없이 순수 반복문으로만 계산한다.
    """
    size = len(pattern)

    if len(filt) != size:
        raise ValueError(f"pattern과 filter의 크기가 다릅니다. (pattern: {size}, filter: {len(filt)})")

    score = 0
    for i in range(size):
        for j in range(size):
            score += pattern[i][j] * filt[i][j]

    return score


if __name__ == "__main__":
    # 간단한 자체 테스트
    cross = make_matrix(3, [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ])
    x = make_matrix(3, [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ])
    pattern = make_matrix(3, [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ])

    print("Cross 필터:")
    print_matrix(cross)
    print("X 필터:")
    print_matrix(x)
    print("입력 패턴:")
    print_matrix(pattern)

    score_cross = mac(pattern, cross)
    score_x = mac(pattern, x)
    print(f"\nMAC(pattern, Cross) = {score_cross}")
    print(f"MAC(pattern, X)     = {score_x}")

    assert score_cross == 5
    assert score_x == 1
    print("\n[core.py 테스트 통과]")