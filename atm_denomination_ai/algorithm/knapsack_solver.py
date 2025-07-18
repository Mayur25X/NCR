# model/knapsack_solver.py

from itertools import product

def knapsack_solver(withdrawal_amount, available_notes):
    denominations = sorted(available_notes.keys(), reverse=True)
    best_combo = None
    best_score = float('-inf')

    def generate_note_combinations():
        ranges = [range(available_notes[d] + 1) for d in denominations]
        for combo in product(*ranges):
            total = sum(c * d for c, d in zip(combo, denominations))
            if total == withdrawal_amount:
                yield combo

    for combo in generate_note_combinations():
        total_notes = sum(combo)
        high_denom_bonus = sum(combo[i] * denominations[i] for i in range(len(denominations)))
        score = -total_notes + 0.0001 * high_denom_bonus  # Bias toward fewer notes and higher values

        if score > best_score:
            best_score = score
            best_combo = combo

    if best_combo is None:
        return None

    return {denominations[i]: best_combo[i] for i in range(len(denominations))}