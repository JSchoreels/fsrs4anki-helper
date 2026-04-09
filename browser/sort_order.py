BUILTIN_RETRIEVABILITY_KEY = "retrievability"


def target_retrievability_order(columns: dict, fallback_order):
    return columns.get(BUILTIN_RETRIEVABILITY_KEY, fallback_order)
