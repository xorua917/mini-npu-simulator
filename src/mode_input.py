import math

from .mac import mac
from .judge import judge
from .perf import measure_mac_ms


def read_matrix(name, n=3):
    print(f"\n{name} ({n}행, 각 행 {n}개 숫자 입력)")

    rows = []

    for i in range(n):
        while True:
            line = input(f"{i + 1}행: ")
            parts = line.split()

            if len(parts) != n:
                print(f"입력 형식 오류: 숫자 {n}개를 입력하세요.")
                continue

            try:
                row = [float(value) for value in parts]

                if not all(math.isfinite(value) for value in row):
                    raise ValueError

            except ValueError:
                print("입력 오류: 유효한 숫자만 입력하세요.")
                continue

            rows.append(row)
            break

    return rows


def run_input_mode():
    print("\n=== 3x3 사용자 입력 모드 ===")

    # 1. 필터 입력
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")

    print("\n필터 A, B 저장 완료!")

    # 2. 패턴 입력
    pattern = read_matrix("입력 패턴")

    # 3. MAC 계산
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    # 4. 판정
    result = judge(score_a, score_b, "A", "B")

    # 5. 성능 측정
    time_a = measure_mac_ms(pattern, filter_a)
    time_b = measure_mac_ms(pattern, filter_b)

    print("\n=== MAC 연산 결과 ===")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")

    if result == "UNDECIDED":
        print("판정: 판정 불가 (동점)")
    else:
        print(f"판정: {result}")

    print("\n=== 3x3 성능 분석 ===")
    print(f"A 평균 연산 시간: {time_a:.6f} ms")
    print(f"B 평균 연산 시간: {time_b:.6f} ms")
    print("반복 측정: 각 10회")
    print("연산 횟수: 필터당 9회")