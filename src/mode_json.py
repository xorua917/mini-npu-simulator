
import json
import math
import re
from pathlib import Path

from .judge import judge, normalize_label
from .mac import mac
from .perf import measure_mac_ms

DATA_PATH = Path(__file__).resolve().parent.parent / "data.json"


def check_matrix(matrix, n, name):
    if not isinstance(matrix, list) or len(matrix) != n or any(
        not isinstance(row, list) or len(row) != n
        for row in matrix
    ):
        raise ValueError(f"{name}: {n}x{n} 크기 불일치")

    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for row in matrix for value in row
    ):
        raise ValueError(f"{name}: 유효하지 않은 숫자")


def run_case(case_id, case, filters):
    match = re.fullmatch(r"size_(\d+)_(\d+)", case_id)

    if match is None:
        raise ValueError("패턴 키 형식 오류")

    n = int(match.group(1))

    if n < 1 or not isinstance(case, dict):
        raise ValueError("케이스 형식 오류")

    pattern = case.get("input")
    check_matrix(pattern, n, "패턴")

    expected = normalize_label(case.get("expected"))

    if expected is None:
        raise ValueError("expected 라벨 오류")

    pair = filters.get(f"size_{n}")

    if not isinstance(pair, dict):
        raise ValueError(f"size_{n} 필터 없음/형식 오류")

    named_filters = {}

    for raw_label, filt in pair.items():
        label = normalize_label(raw_label)

        if label is None or label in named_filters:
            raise ValueError("필터 라벨 오류 또는 중복")

        check_matrix(filt, n, f"{label} 필터")
        named_filters[label] = filt

    if set(named_filters) != {"Cross", "X"}:
        raise ValueError("Cross/X 필터 누락")

    score_cross = mac(pattern, named_filters["Cross"])
    score_x = mac(pattern, named_filters["X"])

    verdict = judge(score_cross, score_x)
    status = "PASS" if verdict == expected else "FAIL"

    reason = ""
    if status == "FAIL":
        reason = (
            "epsilon 동점"
            if verdict == "UNDECIDED"
            else "판정과 expected 불일치"
        )

    return score_cross, score_x, verdict, expected, status, reason


def print_performance(filters):
    cross3 = [
        [1 if i == 1 or j == 1 else 0 for j in range(3)]
        for i in range(3)
    ]

    print("\n[성능 분석] 각 크기별 10회 평균")
    print("크기     평균 시간(ms)  연산 횟수(N²)")
    print("-" * 40)

    for n in (3, 5, 13, 25):
        if n == 3:
            pattern = filt = cross3
        else:
            pair = filters.get(f"size_{n}", {})

            filt = next(
                (
                    value for key, value in pair.items()
                    if normalize_label(key) == "Cross"
                ),
                None
            ) if isinstance(pair, dict) else None

            try:
                check_matrix(filt, n, f"{n}x{n} 성능용 필터")
            except ValueError as exc:
                print(f"{n}x{n}: 측정 불가 ({exc})")
                continue

            pattern = filt

        avg = measure_mac_ms(pattern, filt, repeat=10)
        print(f"{n}x{n:<4} {avg:>12.6f}   {n*n:>9}")


def run_json_mode():
    print("\n=== data.json 분석 모드 ===")

    try:
        with DATA_PATH.open(encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"데이터 파일 읽기 오류: {exc}")
        return

    if not isinstance(data, dict):
        print("오류: JSON 최상위 구조가 객체가 아닙니다.")
        return

    filters = data.get("filters")
    patterns = data.get("patterns")

    if not isinstance(filters, dict) or not isinstance(patterns, dict):
        print("오류: filters 또는 patterns 구조가 없습니다.")
        return

    total = 0
    passed = 0
    failures = []

    for case_id, case in patterns.items():
        total += 1

        try:
            a, b, verdict, expected, status, reason = run_case(
                case_id, case, filters
            )
            print(
                f"{case_id}: Cross={a!r}, X={b!r} | "
                f"판정={verdict} | expected={expected} | {status}"
            )
        except (ValueError, TypeError, OverflowError) as exc:
            status = "FAIL"
            reason = f"데이터/스키마: {exc}"
            print(f"{case_id}: FAIL ({reason})")

        if status == "PASS":
            passed += 1
        else:
            failures.append((case_id, reason))

    print_performance(filters)

    print(
        f"\n[결과 요약] 전체 {total} / "
        f"통과 {passed} / 실패 {len(failures)}"
    )

    for case_id, reason in failures:
        print(f"- {case_id}: {reason}")
