# test_dispatcher.py
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import random
from datetime import datetime, timedelta
from algorithm.hybrid_dispatcher import hybrid_dispatcher

def generate_synthetic_data(num_records=10_000_000, seed=52):
    random.seed(seed)
    data = []

    atm_locations = [
        ("ATM001", "Nagpur"),
        ("ATM002", "Mumbai"),
        ("ATM003", "Pune"),
        ("ATM004", "Nashik"),
        ("ATM005", "Delhi")
    ]

    base_time = datetime(2025, 7, 1, 8, 0, 0)

    for i in range(num_records):
        atm_id, location = random.choice(atm_locations)
        txn_type = random.choices(["Withdrawal", "Replenishment"], weights=[0.8, 0.2])[0]
        
        if txn_type == "Withdrawal":
            amount = random.choice([500, 1000, 2000, 3000, 4000, 5000, 8000, 10000, 12000, 15000])
        else:
            amount = random.choice([100000, 200000, 300000, 400000, 500000])

        txn_datetime = base_time + timedelta(minutes=random.randint(0, 60 * 24 * 30))
        txn_id = f"txn_{i:06d}"

        # Simulate realistic note availability (no ₹2000 note)
        available_notes = {
            500: random.randint(0, 20),
            200: random.randint(0, 20),
            100: random.randint(0, 20),
            50: random.randint(0, 10)
        }

        # Use real dispatcher to choose algorithm
        result = hybrid_dispatcher(amount, available_notes, txn_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        if result is None:
            continue  # skip failed transactions

        total_notes_used = sum(result.values())
        if total_notes_used <= 10:
            label = "greedy"
        else:
            label = "knapsack"

        data.append({
            "ATM_ID": atm_id,
            "Location": location,
            "Transaction_ID": txn_id,
            "Transaction_Type": txn_type,
            "Amount_INR": amount,
            "Transaction_DateTime": txn_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "preferred_algorithm": label
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    print("⏳ Generating data using real dispatcher logic...")
    df = generate_synthetic_data(10_000_000)  # Adjust count here
    df.to_csv("data/atm_training_data.csv", index=False)
    print("✅ Updated training data saved: data/atm_training_data.csv")