"""
main.py
-------
Mini NPU 시뮬레이터 실행 시작점.

1) 입력 방식 선택: 사용자 입력(3x3) 또는 data.json 분석
2) 선택한 모드 실행
"""

from mode1_input import run_mode1
from mode2_json import run_mode2


def main():
    print("=" * 60)
    print(" Mini NPU 시뮬레이터")
    print("=" * 60)
    print("입력 방식을 선택하세요.")
    print("  1) 사용자 입력 (3x3 필터 A/B + 패턴 직접 입력)")
    print("  2) data.json 분석 (5x5 / 13x13 / 25x25 포함)")

    while True:
        choice = input("선택 (1 또는 2): ").strip()
        if choice == "1":
            run_mode1()
            break
        elif choice == "2":
            run_mode2("data.json")
            break
        else:
            print("잘못된 입력입니다. 1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()