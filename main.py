import json
from engine import make_matrix, mac, normalize_label, decide, is_pass, print_perf_table


# --- [문자열 처리 유틸리티: 정규식 대신 split 사용] ---

def get_size_from_key(key):
    """'size_5_1' 같은 문자열을 '_'로 잘라서 크기(5)를 가져옵니다."""
    parts = str(key).split("_")
    # 'size', '5', '1' 처럼 3개로 나뉘고 두 번째가 숫자인지 확인
    if len(parts) == 3 and parts[0] == "size" and parts[1].isdigit():
        return int(parts[1])
    return None


def get_size_from_filter_key(key):
    """'size_5' 같은 문자열에서 크기(5)를 가져옵니다."""
    parts = str(key).split("_")
    if len(parts) == 2 and parts[0] == "size" and parts[1].isdigit():
        return int(parts[1])
    return None


# --- [모드 1: 사용자 입력 (3x3)] ---

def read_matrix_from_input(name, size=3):
    """사용자로부터 한 줄씩 숫자를 입력받아 행렬을 만듭니다."""
    print(f"\n[{name}] {size}x{size} 행렬을 한 줄씩 입력하세요 (숫자 {size}개, 공백 구분).")
    rows = []
    row_num = 1

    while row_num <= size:
        text = input(f"  {row_num}행: ").strip()
        parts = text.split()

        if len(parts) != size:
            print(f"  -> 오류: 숫자를 정확히 {size}개 입력해야 합니다.")
            continue

        try:
            row = [float(p) for p in parts]
            rows.append(row)
            row_num += 1
        except ValueError:
            print("  -> 오류: 숫자만 입력 가능합니다.")

    return make_matrix(size, rows)


def run_mode1():
    print("=" * 60)
    print("모드 1: 사용자 입력(3x3) 처리")
    print("=" * 60)

    filter_a = read_matrix_from_input("필터 A (Cross)")
    filter_b = read_matrix_from_input("필터 B (X)")
    pattern = read_matrix_from_input("입력 패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    decision = decide(score_a, score_b)

    print("\n[MAC 연산 결과]")
    print(f"  필터 A(Cross) 점수: {score_a}")
    print(f"  필터 B(X) 점수    : {score_b}")
    print(f"  판정              : {decision}")

    print_perf_table([3])


# --- [모드 2: data.json 일괄 채점] ---

def build_filters(raw_filters):
    """JSON의 filters 데이터를 {5: {'Cross': [...], 'X': [...]}} 형태로 정리합니다."""
    filters = {}
    for key, val in raw_filters.items():
        size = get_size_from_filter_key(key)
        if size is None or not isinstance(val, dict):
            continue

        label_map = {}
        for raw_label, matrix_data in val.items():
            try:
                label = normalize_label(raw_label)
                label_map[label] = make_matrix(size, matrix_data)
            except ValueError:
                continue

        if "Cross" in label_map and "X" in label_map:
            filters[size] = label_map
    return filters


def evaluate_case(case_id, entry, filters):
    """개별 패턴 데이터를 검증하고 판정합니다."""
    size = get_size_from_key(case_id)
    if size is None:
        return {"id": case_id, "status": "FAIL", "reason": f"키 형식 오류: '{case_id}'"}

    if "input" not in entry or "expected" not in entry:
        return {"id": case_id, "status": "FAIL", "reason": "'input' 또는 'expected'가 없습니다."}

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

# 1. 정답과 일치하는 경우 (성공)
    if is_pass(decision, entry["expected"]):
        return {"id": case_id, "status": "PASS", "score_cross": score_cross,
                "score_x": score_x, "decision": decision}
    
# 2. 실패한 경우 원인을 2가지로 세분화
    if decision == "UNDECIDED":
        reason = f"동점(UNDECIDED)으로 판정 불가 (Cross={score_cross}, X={score_x})"
    else:
        reason = f"판정({decision}) != expected({entry['expected']})"

# 3. 상세 이유를 담은 실패 결과표 반환
    return {"id": case_id, "status": "FAIL", "reason": reason,
            "score_cross": score_cross, "score_x": score_x, "decision": decision}


def run_mode2(path="data.json"):
    print("=" * 60)
    print("모드 2: data.json 분석")
    print("=" * 60)

# 1. 파일 안전하게 읽기 (예외 처리)
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"[오류] 파일을 찾을 수 없습니다: {path}")
        return
    except json.JSONDecodeError:
        print("[오류] JSON 형식이 올바르지 않습니다.")
        return

# 2. 필터 데이터 정제 및 패턴 데이터 분리

# JSON의 filters 데이터를 {5: {'Cross': [...], 'X': [...]}} 형태로 가공
    filters = build_filters(raw.get("filters", {}))
# 분석할 테스트 패턴 데이터들만 딕셔너리로 추출
    patterns = raw.get("patterns", {})

    results = []
    print(f"\n[패턴 판정 결과] 총 {len(patterns)}건")
    print("-" * 60)

# 3. 모든 패턴 데이터를 하나씩 순회하며 채점 및 실시간 출력
    for case_id, entry in patterns.items():
    # 개별 케이스를 채점 공장에 넣어 결과 딕셔너리를 받아옴
        res = evaluate_case(case_id, entry, filters)
        results.append(res)
    # 점수가 정상적으로 계산된 케이스는 점수/판정/결과를 포맷팅하여 출력
        if "score_cross" in res:
            print(f"- {case_id}: Cross={res['score_cross']:.4f}, "
                  f"X={res['score_x']:.4f}, 판정={res['decision']} -> {res['status']}")
    # 규격 오류 등으로 연산 전 탈출한 케이스는 실패 사유만 출력
        else:
            print(f"- {case_id}: {res['status']} (사유: {res['reason']})")

    print_perf_table([3, 5, 13, 25])

    total = len(results)        # 전체 테스트 케이스 수
    passed = sum(1 for r in results if r["status"] == "PASS")   # 통과(PASS)한 케이스 수
    failed = total - passed     # 통과(PASS)한 케이스 수

    print("\n[결과 요약]")
    print(f"  전체: {total} / 통과: {passed} / 실패: {failed}")

    if failed > 0:
        print("\n  실패 케이스 목록:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"    - {r['id']}: {r['reason']}")


# --- [프로그램 시작점] ---

def main():
    print("=" * 60)
    print(" Mini NPU 시뮬레이터")
    print("=" * 60)
    print("1) 사용자 입력 (3x3 직접 입력)")
    print("2) data.json 분석 (5x5 / 13x13 / 25x25)")

    while True:
        choice = input("선택 (1 또는 2): ").strip()
        if choice == "1":
            run_mode1()
            break
        elif choice == "2":
            run_mode2("data.json")
            break
        else:
            print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()