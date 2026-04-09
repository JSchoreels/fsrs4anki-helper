from typing import Sequence

DEFAULT_DECAY = -0.2


def power_forgetting_curve(t: float, s: float, decay: float = DEFAULT_DECAY) -> float:
    factor = 0.9 ** (1 / decay) - 1
    return (1 + factor * t / s) ** decay


def next_interval(s: float, r: float, decay: float = DEFAULT_DECAY) -> int:
    factor = 0.9 ** (1 / decay) - 1
    ivl = s / factor * (r ** (1 / decay) - 1)
    return max(1, int(round(ivl)))


def fsrs7_forgetting_curve(t: float, s: float, params: Sequence[float]) -> float:
    s = max(float(s), 0.001)
    t_over_s = max(float(t), 0.0) / s

    decay1 = -float(params[27])
    decay2 = -float(params[28])
    base1 = float(params[29])
    base2 = float(params[30])

    factor1 = base1 ** (1.0 / decay1) - 1.0
    factor2 = base2 ** (1.0 / decay2) - 1.0
    r1 = (1.0 + factor1 * t_over_s) ** decay1
    r2 = (1.0 + factor2 * t_over_s) ** decay2

    weight1 = float(params[31]) * (s ** (-float(params[33])))
    weight2 = float(params[32]) * (s ** float(params[34]))

    return (weight1 * r1 + weight2 * r2) / (weight1 + weight2)


def fsrs7_next_interval(
    stability: float, desired_retention: float, params: Sequence[float]
) -> int:
    desired_retention = min(max(float(desired_retention), 0.0001), 0.9999)
    stability = max(float(stability), 0.001)
    if desired_retention >= 0.9999:
        return 1

    low = 0.0
    high = max(stability, 1.0)
    s_max = 36500.0

    while (
        fsrs7_forgetting_curve(high, stability, params) > desired_retention
        and high < s_max
    ):
        high = min(high * 2.0, s_max)
        if high == s_max:
            break

    for _ in range(50):
        mid = (low + high) / 2.0
        retention = fsrs7_forgetting_curve(mid, stability, params)
        if retention > desired_retention:
            low = mid
        else:
            high = mid

    return max(1, int(round((low + high) / 2.0)))


def interval_for_target_retrievability(
    stability: float,
    desired_retention: float,
    params: Sequence[float] | None = None,
    decay: float = DEFAULT_DECAY,
) -> int:
    if params is not None and len(params) >= 35:
        return fsrs7_next_interval(stability, desired_retention, params)
    return next_interval(stability, desired_retention, decay)
