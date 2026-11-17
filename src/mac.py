
from .matrix import is_square


def mac(pattern, filt):
    n = len(pattern) if isinstance(pattern, list) else 0

    if n < 1 or not is_square(pattern, n) or not is_square(filt, n):
        raise ValueError("패턴과 필터는 같은 크기의 정사각 배열이어야 합니다.")

    total = 0
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]

    return total
