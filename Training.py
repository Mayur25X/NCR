atm_denomination_ai/train_policy_model.py

import pandas as pd from sklearn.model_selection import train_test_split from sklearn.ensemble import RandomForestClassifier import joblib import datetime

def convert_timestamp(ts): try: dt = pd.to_datetime(ts) return pd.Series({ 'day_of_week': dt.dayofweek, 'hour': dt.hour, 'day': dt.day, 'month': dt.month }) except: return pd.Series({'day_of_week': 0, 'hour': 0, 'day': 0, 'month': 0})

def train_model(dataset_path="data/replenishment_logs.csv"): df = pd.read_csv(dataset_path, sep='\t')  # Assuming tab-separated format

# Convert timestamp
time_features = df["Timestamp"].apply(convert_timestamp)
df = pd.concat([df, time_features], axis=1)

# Simulate features (example): based on amount and time
df['amount_category'] = pd.cut(df['Amount'], bins=[0, 200000, 500000, 1000000], labels=[0, 1, 2])

# For training the classifier, you need labels like 'greedy' or 'knapsack'
# Let's simulate them: assume large replenishment prefers greedy, others knapsack
df['preferred_algorithm'] = df['Amount'].apply(lambda x: 'greedy' if x > 400000 else 'knapsack')

features = df[['amount_category', 'day_of_week', 'hour']]
features = features.fillna(0)
X = features.astype(int)
y = df['preferred_algorithm']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

acc = clf.score(X_test, y_test)
print(f"Model Accuracy: {acc:.2f}")

joblib.dump(clf, "model/atm_policy_model.pkl")
return clf

if name == "main": train_model()

