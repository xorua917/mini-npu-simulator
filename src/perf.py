import time
from .mac import mac


def measure_mac_ms(pattern, filt, repeat=10):
    elapsed = 0.0

    for _ in range(repeat):
        start = time.perf_counter()
        mac(pattern, filt)
        elapsed += time.perf_counter() - start

    return elapsed / repeat * 1000