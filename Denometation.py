atm_denomination_ai/greedy_algorithm.py

def greedy_algorithm(withdrawal_amount, available_notes): denominations = sorted(available_notes.keys(), reverse=True) result = {denom: 0 for denom in available_notes}

for denom in denominations:
    if withdrawal_amount == 0:
        break

    max_notes = min(available_notes[denom], withdrawal_amount // denom)
    result[denom] = max_notes
    withdrawal_amount -= max_notes * denom

if withdrawal_amount != 0:
    return None  # Cannot fulfill the request

return result

atm_denomination_ai/knapsack_solver.py

def knapsack_solver(withdrawal_amount, available_notes): from itertools import product

denominations = sorted(available_notes.keys(), reverse=True)
best_combo = None
min_notes = float('inf')

def generate_note_combinations():
    ranges = [range(available_notes[d] + 1) for d in denominations]
    for combo in product(*ranges):
        total = sum(c * d for c, d in zip(combo, denominations))
        if total == withdrawal_amount:
            yield combo

for combo in generate_note_combinations():
    total_notes = sum(combo)
    if total_notes < min_notes:
        best_combo = combo
        min_notes = total_notes

if best_combo is None:
    return None

return {denominations[i]: best_combo[i] for i in range(len(denominations))}

atm_denomination_ai/hybrid_dispatcher.py

from greedy_algorithm import greedy_algorithm from knapsack_solver import knapsack_solver

def hybrid_dispatcher(withdrawal_amount, available_notes): total_notes_available = sum(available_notes.values()) highest_stock_denom = max(available_notes, key=available_notes.get)

if total_notes_available < 10 or available_notes[highest_stock_denom] < 3:
    return knapsack_solver(withdrawal_amount, available_notes)
else:
    return greedy_algorithm(withdrawal_amount, available_notes)

atm_denomination_ai/train_policy_model.py

import pandas as pd from sklearn.model_selection import train_test_split from sklearn.ensemble import RandomForestClassifier import joblib

def train_model(dataset_path="data/atm_training_data.csv"): df = pd.read_csv(dataset_path) X = df.drop(columns=["preferred_algorithm"]) y = df["preferred_algorithm"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

acc = clf.score(X_test, y_test)
print(f"Model Accuracy: {acc:.2f}")

joblib.dump(clf, "model/atm_policy_model.pkl")
return clf

atm_denomination_ai/main.py

from hybrid_dispatcher import hybrid_dispatcher

def main(): withdrawal_amount = 3900 available_notes = { 2000: 1, 500: 5, 200: 10, 100: 8, 50: 10 }

result = hybrid_dispatcher(withdrawal_amount, available_notes)
if result:
    print("Dispensed Notes:", result)
else:
    print("Cannot fulfill withdrawal with available denominations.")

if name == "main": main()

