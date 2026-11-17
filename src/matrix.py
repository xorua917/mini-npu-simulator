
def make_matrix(n, fill=0):
    if n < 1:
        raise ValueError("배열 크기는 1 이상이어야 합니다.")
    return [[fill for _ in range(n)] for _ in range(n)]


def is_square(matrix, n):
    return (
        isinstance(matrix, list)
        and len(matrix) == n
        and all(
            isinstance(row, list) and len(row) == n
            for row in matrix
        )
    )
