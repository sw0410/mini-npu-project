"""
mode2_json.py
-------------
모드 2: data.json을 읽어서 5x5 / 13x13 / 25x25 패턴들을 한꺼번에 판정하는 부분.

data.json 구조:
{
  "filters": {
    "size_5":  {"cross": [[...]], "x": [[...]]},
    "size_13": {...},
    "size_25": {...}
  },
  "patterns": {
    "size_5_1": {"input": [[...]], "expected": "+"},
    ...
  }
}
"""

import json
import re

from core import make_matrix, mac
from judge import decide, normalize_label, is_pass
from perf import print_perf_table

# "size_5_1" 같은 키에서 크기(5)를 뽑아내기 위한 패턴
KEY_PATTERN = re.compile(r"^size_(\d+)_\w+$")


def load_data_json(path):
    """data.json 파일을 읽어서 딕셔너리로 반환한다. 문제가 있으면 None을 반환한다."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"[오류] 파일을 찾을 수 없습니다: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"[오류] JSON 파싱 오류: {e}")
        return None

    if "filters" not in raw or "patterns" not in raw:
        print("[오류] 'filters'와 'patterns' 키가 모두 있어야 합니다.")
        return None

    return raw


def build_filters(raw_filters):
    """raw_filters를 {5: {"Cross": 행렬, "X": 행렬}, 13: {...}, ...} 형태로 정리한다."""
    filters = {}

    for size_key, sub in raw_filters.items():
        m = re.match(r"^size_(\d+)$", size_key)
        if not m:
            continue  # 형식에 안 맞는 키는 그냥 건너뜀
        size = int(m.group(1))

        label_map = {}
        for label_key, matrix_data in sub.items():
            try:
                std_label = normalize_label(label_key)
                label_map[std_label] = make_matrix(size, matrix_data)
            except ValueError:
                continue  # 이 필터 하나는 등록하지 않고 넘어감

        # Cross, X 둘 다 있어야 유효한 필터 세트로 인정
        if "Cross" in label_map and "X" in label_map:
            filters[size] = label_map

    return filters


def get_size_from_key(key):
    """'size_5_1' 같은 키에서 크기(5)만 뽑아낸다. 형식이 다르면 None."""
    m = KEY_PATTERN.match(key)
    if not m:
        return None
    return int(m.group(1))


def evaluate_case(case_id, entry, filters):
    """패턴 하나를 검증하고 MAC 연산 -> 판정 -> PASS/FAIL 결과를 딕셔너리로 돌려준다.

    문제가 생기면 프로그램을 멈추지 않고 FAIL(사유 포함)로 처리한다.
    """
    size = get_size_from_key(case_id)
    if size is None:
        return {"id": case_id, "status": "FAIL", "reason": f"키 형식 오류: '{case_id}'"}

    if "input" not in entry or "expected" not in entry:
        return {"id": case_id, "status": "FAIL", "reason": "'input' 또는 'expected' 필드가 없습니다."}

    if size not in filters:
        return {"id": case_id, "status": "FAIL", "reason": f"size_{size} 필터가 없습니다."}

    try:
        pattern = make_matrix(size, entry["input"])
    except ValueError as e:
        return {"id": case_id, "status": "FAIL", "reason": f"크기 불일치: {e}"}

    try:
        normalize_label(entry["expected"])
    except ValueError as e:
        return {"id": case_id, "status": "FAIL", "reason": f"expected 값 오류: {e}"}

    score_cross = mac(pattern, filters[size]["Cross"])
    score_x = mac(pattern, filters[size]["X"])
    decision = decide(score_cross, score_x)

    passed = is_pass(decision, entry["expected"])
    if passed:
        return {"id": case_id, "status": "PASS", "score_cross": score_cross,
                "score_x": score_x, "decision": decision}

    if decision == "UNDECIDED":
        reason = f"동점(UNDECIDED)으로 판정 불가 (Cross={score_cross}, X={score_x})"
    else:
        reason = f"판정({decision}) != expected({entry['expected']})"

    return {"id": case_id, "status": "FAIL", "reason": reason,
            "score_cross": score_cross, "score_x": score_x, "decision": decision}


def run_mode2(path="data.json"):
    print("=" * 60)
    print("모드 2: data.json 분석")
    print("=" * 60)

    raw = load_data_json(path)
    if raw is None:
        return

    filters = build_filters(raw.get("filters", {}))
    if not filters:
        print("[경고] 유효한 필터가 없습니다.")

    patterns = raw.get("patterns", {})
    if not patterns:
        print("[경고] patterns가 비어 있습니다.")

    results = []
    print(f"\n[패턴 판정 결과] 총 {len(patterns)}건")
    print("-" * 60)
    for case_id, entry in patterns.items():
        result = evaluate_case(case_id, entry, filters)
        results.append(result)

        if "score_cross" in result:
            print(f"- {case_id}: Cross={result['score_cross']:.4f}, "
                  f"X={result['score_x']:.4f}, 판정={result['decision']} -> {result['status']}")
        else:
            print(f"- {case_id}: {result['status']} (사유: {result['reason']})")

    print_perf_table([3, 5, 13, 25])

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    print("\n[결과 요약]")
    print(f"  전체: {total} / 통과: {passed} / 실패: {failed}")

    if failed > 0:
        print("\n  실패 케이스 목록:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"    - {r['id']}: {r['reason']}")


if __name__ == "__main__":
    run_mode2("data.json")