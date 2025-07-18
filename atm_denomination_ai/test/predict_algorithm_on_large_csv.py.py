# predict_algorithm_on_large_csv.py

import pandas as pd
import joblib

MODEL_PATH = "model/atm_policy_model.pkl"
INPUT_CSV = "data/atm_transactions.csv"         # Your new unlabeled transaction file
OUTPUT_CSV = "data/predicted_with_algorithm.csv"
CHUNK_SIZE = 100_000  # Adjust based on RAM (100k is usually safe)

def extract_features(df):
    df['Transaction_DateTime'] = pd.to_datetime(df['Transaction_DateTime'])
    df['Hour'] = df['Transaction_DateTime'].dt.hour
    df['DayOfWeek'] = df['Transaction_DateTime'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeek'] >= 5
    df['IsReplenishment'] = df['Transaction_Type'].str.lower() == 'replenishment'
    return df[['Amount_INR', 'Hour', 'DayOfWeek', 'IsWeekend', 'IsReplenishment']].astype(int)

def predict_on_large_csv():
    print("📥 Loading model...")
    model = joblib.load(MODEL_PATH)

    reader = pd.read_csv(INPUT_CSV, chunksize=CHUNK_SIZE)
    all_chunks = []

    for i, chunk in enumerate(reader):
        print(f"🔄 Processing chunk {i + 1}...")
        features = extract_features(chunk.copy())
        predictions = model.predict(features)
        chunk['Predicted_Algorithm'] = predictions
        all_chunks.append(chunk)

    print("📤 Saving output...")
    full_df = pd.concat(all_chunks)
    full_df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Done! Predictions saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    predict_on_large_csv()