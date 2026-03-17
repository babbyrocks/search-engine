
def rank_results(results: dict) -> list:
    ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return ranked