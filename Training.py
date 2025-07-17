# atm_denomination_ai/train_policy_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def extract_features(df):
    df['Transaction_DateTime'] = pd.to_datetime(df['Transaction_DateTime'])
    df['Hour'] = df['Transaction_DateTime'].dt.hour
    df['DayOfWeek'] = df['Transaction_DateTime'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    df['IsReplenishment'] = df['Transaction_Type'].apply(lambda x: 1 if x.lower() == 'replenishment' else 0)
    return df[[
        'Amount_INR', 'Hour', 'DayOfWeek', 'IsWeekend', 'IsReplenishment'
    ]]

def train_model(dataset_path="data/atm_training_data.csv"):
    df = pd.read_csv(dataset_path)

    # Simulate label for now (replace with real labels if available)
    df['preferred_algorithm'] = df['Amount_INR'].apply(
        lambda x: 'greedy' if x <= 10000 else 'knapsack'
    )

    X = extract_features(df)
    y = df['preferred_algorithm']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    acc = clf.score(X_test, y_test)
    print(f"Model Accuracy: {acc:.2f}")

    joblib.dump(clf, "model/atm_policy_model.pkl")
    return clf

if __name__ == "__main__":
    train_model()




# atm_denomination_ai/hybrid_dispatcher.py

from greedy_algorithm import greedy_algorithm
from knapsack_solver import knapsack_solver
import joblib
import pandas as pd
from datetime import datetime

# Load the trained classifier model
try:
    model = joblib.load("model/atm_policy_model.pkl")
except FileNotFoundError:
    model = None
    print("Warning: AI model not found. Defaulting to rule-based logic.")

def extract_features(input_data):
    dt = datetime.strptime(input_data['Transaction_DateTime'], "%Y-%m-%d %H:%M:%S")
    return pd.DataFrame([{
        'Amount_INR': input_data['withdrawal_amount'],
        'Hour': dt.hour,
        'DayOfWeek': dt.weekday(),
        'IsWeekend': 1 if dt.weekday() >= 5 else 0,
        'IsReplenishment': 0
    }])

def hybrid_dispatcher(withdrawal_amount, available_notes, transaction_datetime="2025-07-17 12:00:00"):
    if model:
        input_features = extract_features({
            'withdrawal_amount': withdrawal_amount,
            'Transaction_DateTime': transaction_datetime
        })
        prediction = model.predict(input_features)[0]

        if prediction == 'greedy':
            return greedy_algorithm(withdrawal_amount, available_notes)
        else:
            return knapsack_solver(withdrawal_amount, available_notes)
    else:
        total_notes_available = sum(available_notes.values())
        highest_stock_denom = max(available_notes, key=available_notes.get)

        if total_notes_available < 10 or available_notes[highest_stock_denom] < 3:
            return knapsack_solver(withdrawal_amount, available_notes)
        else:
            return greedy_algorithm(withdrawal_amount, available_notes)
  
  
