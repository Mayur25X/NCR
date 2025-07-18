# model/hybrid_dispatcher.py (MODIFY THIS)

from algorithm.greedy_algorithm import greedy_algorithm
from algorithm.knapsack_solver import knapsack_solver
import joblib
import pandas as pd

model = joblib.load("model/atm_policy_model.pkl")

def hybrid_dispatcher(withdrawal_amount, available_notes, txn_time):
    # Feature extraction
    txn_time = pd.to_datetime(txn_time)
    hour = txn_time.hour
    day_of_week = txn_time.dayofweek
    is_weekend = 1 if day_of_week >= 5 else 0
    is_replenishment = 0  # since test is withdrawal

    features = pd.DataFrame([{
        "Amount_INR": withdrawal_amount,
        "Hour": hour,
        "DayOfWeek": day_of_week,
        "IsWeekend": is_weekend,
        "IsReplenishment": is_replenishment
    }])

    algo = model.predict(features)[0]

    if algo == "greedy":
        result = greedy_algorithm(withdrawal_amount, available_notes)
    else:
        result = knapsack_solver(withdrawal_amount, available_notes)

    if result is None:
        return None, algo

    return result, algo