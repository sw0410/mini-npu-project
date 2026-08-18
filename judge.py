"""
judge.py
--------
라벨을 표준 형태(Cross / X)로 통일하고, 두 점수를 비교해서 판정을 내리는 부분.
"""

EPSILON = 1e-9  # 이 값보다 점수 차이가 작으면 "동점"으로 본다


def normalize_label(raw):
    """'+', 'cross', 'x' 같은 다양한 표기를 표준 라벨(Cross 또는 X)로 바꾼다."""
    text = str(raw).strip().lower()

    if text in ("+", "cross"):
        return "Cross"
    if text == "x":
        return "X"

    raise ValueError(f"알 수 없는 라벨입니다: {raw}")


def decide(score_cross, score_x):
    """Cross 점수와 X 점수를 비교해서 'Cross', 'X', 'UNDECIDED' 중 하나를 돌려준다."""
    if abs(score_cross - score_x) < EPSILON:
        return "UNDECIDED"
    if score_cross > score_x:
        return "Cross"
    return "X"


def is_pass(decision, expected_raw):
    """판정 결과(decision)와 expected 값이 같은지 확인한다."""
    if decision == "UNDECIDED":
        return False

    try:
        expected = normalize_label(expected_raw)
    except ValueError:
        return False

    return decision == expected


if __name__ == "__main__":
    assert normalize_label("+") == "Cross"
    assert normalize_label("cross") == "Cross"
    assert normalize_label("x") == "X"

    assert decide(5, 1) == "Cross"
    assert decide(1, 5) == "X"
    assert decide(3, 3) == "UNDECIDED"

    assert is_pass("Cross", "+") is True
    assert is_pass("Cross", "x") is False
    assert is_pass("UNDECIDED", "+") is False

    print("[judge.py 테스트 통과]")