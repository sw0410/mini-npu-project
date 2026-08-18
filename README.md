## 프로그램 흐름

`main.py`가 프로그램의 시작점입니다. 실행하면 사용자에게 모드를 선택하게 하고,
선택에 따라 `mode1_input.py` 또는 `mode2_json.py`의 함수를 호출합니다.

```
                main.py
               /        \
      mode1_input.py   mode2_json.py
               \        /
          core.py  judge.py  perf.py   ← 공통으로 쓰는 부품들
```

- **`main.py`** : 사용자에게 "1번? 2번?"을 물어보고, 선택에 따라 알맞은 모드 함수를 실행하는 진입점(안내데스크 역할)
- **`mode1_input.py`** : 콘솔에서 3×3 필터 A/B와 패턴을 직접 입력받는 모드
- **`mode2_json.py`** : `data.json` 파일을 읽어서 5×5/13×13/25×25 패턴을 한꺼번에 채점하는 모드
- **`core.py`** : 행렬을 저장하고, MAC 연산(같은 위치끼리 곱해서 다 더하기)을 수행하는 가장 기초적인 도구
- **`judge.py`** : Cross 점수와 X 점수를 비교해서 "Cross냐 X냐 동점이냐"를 판정하는 도구
- **`perf.py`** : MAC 연산이 얼마나 걸리는지 시간을 측정하는 도구

두 모드(`mode1_input.py`, `mode2_json.py`)는 각자 필요한 곳에서
`core.py`, `judge.py`, `perf.py`를 공통으로 가져다 씁니다. 비유하자면
`core.py`/`judge.py`/`perf.py`는 공구함 속 개별 도구(망치, 드라이버, 자)이고,
`mode1_input.py`/`mode2_json.py`는 그 도구들을 조합해 하나의 작업
(입력받기 → 계산 → 판정 → 출력)을 완성하는 매뉴얼이며,
`main.py`는 어떤 매뉴얼을 쓸지 고르는 안내데스크에 해당합니다.