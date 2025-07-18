import pandas as pd
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_records=100000000, seed=52):
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
            amount = random.choice([500, 1000, 2000, 3000, 4000, 5000, 10000, 15000])
        else:
            amount = random.choice([100000, 200000, 300000, 400000, 500000])

        txn_datetime = base_time + timedelta(minutes=random.randint(0, 60 * 24 * 30))  # Random date in July
        txn_id = f"txn_{i:05d}"
        
        # Simulated label based on logic
        label = "greedy" if amount <= 1000 else "knapsack"

        data.append({
            "ATM_ID": atm_id,
            "Location": location,
            "Transaction_ID": txn_id,
            "Transaction_Type": txn_type,
            "Amount_INR": amount,
            "Transaction_DateTime": txn_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "preferred_algorithm": label
        })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_synthetic_data(10000000)
    df.to_csv("./data/atm_training_data.csv", index=False)
    print("✅ Synthetic training data generated at: data/atm_training_data.csv")