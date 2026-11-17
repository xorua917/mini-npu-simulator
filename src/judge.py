
EPSILON = 1e-9


def normalize_label(raw):
    if not isinstance(raw, str):
        return None

    label = raw.strip().lower()

    if label in ("+", "cross"):
        return "Cross"
    if label == "x":
        return "X"

    return None


def judge(score_a, score_b, label_a="Cross", label_b="X"):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"

    if score_a > score_b:
        return label_a

    return label_b
