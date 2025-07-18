# ---------------------------------------------
# 1. model/hybrid_dispatcher.py
# ---------------------------------------------

from model.greedy_algorithm import greedy_algorithm
from model.knapsack_solver import knapsack_solver
import joblib
import pandas as pd

# ---------------------------------------------
# 2. train/train_policy_model.py
# ---------------------------------------------

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(dataset_path="data/atm_training_data.csv"):
    df = pd.read_csv(dataset_path)

    df["Transaction_DateTime"] = pd.to_datetime(df["Transaction_DateTime"])
    df["Hour"] = df["Transaction_DateTime"].dt.hour
    df["DayOfWeek"] = df["Transaction_DateTime"].dt.dayofweek
    df["IsWeekend"] = df["DayOfWeek"] >= 5
    df["IsReplenishment"] = df["Transaction_Type"].str.lower() == "replenishment"

    df = pd.get_dummies(df, columns=["Location_Type"], prefix="Is")

    feature_cols = [
        "Amount_INR", "Hour", "DayOfWeek", "IsWeekend",
        "IsReplenishment", "Is_market", "Is_mall", "Is_bank"
    ]
    X = df[feature_cols].astype(int)
    y = df["preferred_algorithm"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Model Accuracy:", accuracy_score(y_test, y_pred))

    joblib.dump(clf, "model/atm_policy_model.pkl")

if __name__ == "__main__":
    train_model()


# ---------------------------------------------
# 3. data/generate_training_data.py
# ---------------------------------------------

import pandas as pd
import random
from datetime import datetime, timedelta
from model.hybrid_dispatcher import hybrid_dispatcher


# ---------------------------------------------
# 4. main.py
# ---------------------------------------------

from model.hybrid_dispatcher import hybrid_dispatcher

def main():
    print("\U0001f9e0 AI-Based ATM Denomination System")
    print("----------------------------------")

    try:
        withdrawal_amount = int(input("Enter withdrawal amount (₹): "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    available_notes = {
        500: int(input("Available ₹500 notes: ")),
        200: int(input("Available ₹200 notes: ")),
        100: int(input("Available ₹100 notes: ")),
        50: int(input("Available ₹50 notes: "))
    }

    txn_time = input("Enter transaction time (YYYY-MM-DD HH:MM:SS): ")
    location_type = input("Enter ATM location type (market/mall/bank): ").lower()

    print("\n🔄 Processing...")
    result, algo = hybrid_dispatcher(withdrawal_amount, available_notes, txn_time, location_type)

    if result:
        print(f"\n✅ Dispensed Notes: {result}")
        print(f"🧠 Algorithm Used: {algo}")
    else:
        print("❌ Unable to fulfill the withdrawal with available notes.")

if __name__ == "__main__":
    main()
