# model/greedy_algorithm.py

def greedy_algorithm(withdrawal_amount, available_notes):
    denominations = sorted(available_notes.keys(), reverse=True)
    result = {denom: 0 for denom in available_notes}

    for denom in denominations:
        if withdrawal_amount == 0:
            break

        max_notes = min(available_notes[denom], withdrawal_amount // denom)
        result[denom] = max_notes
        withdrawal_amount -= max_notes * denom

    if withdrawal_amount != 0:
        return None  # Cannot fulfill the request

    return result

