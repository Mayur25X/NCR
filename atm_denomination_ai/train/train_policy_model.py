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

def train_model(dataset_path="D:/Denomenation/atm_denomination_ai/data/atm_training_data.csv"):
    df = pd.read_csv(dataset_path)

    # Simulate label for now (replace with real labels if available)
    df['preferred_algorithm'] = df['Amount_INR'].apply(
        lambda x: 'greedy' if x <= 1000 else 'knapsack'
    )

    X = extract_features(df)
    y = df['preferred_algorithm']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    acc = clf.score(X_test, y_test)
    print(f"Model Accuracy: {acc:.2f}")

    joblib.dump(clf, "./model/atm_policy_model.pkl")
    return clf

if __name__ == "__main__":
    train_model()