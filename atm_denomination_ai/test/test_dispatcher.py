# test_dispatcher.py
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# test_dispatcher.py

from algorithm.hybrid_dispatcher import hybrid_dispatcher
import random
from datetime import datetime

def generate_test_cases(n=10, seed=42):
    random.seed(seed)
    test_cases = []

    for _ in range(n):
        amount = random.choice([1000, 2000, 3000, 5000, 8000, 10000, 12000, 15000])
        notes = {
            500: random.randint(0, 20),
            200: random.randint(0, 30),
            100: random.randint(0, 30),
        }
        time = datetime(2025, 7, 17, random.randint(8, 18), random.randint(0, 59))
        test_cases.append((amount, notes, time.strftime("%Y-%m-%d %H:%M:%S")))

    return test_cases

def run_tests():
    test_cases = generate_test_cases()
    for i, (amt, notes, time) in enumerate(test_cases, 1):
        print(f"\n🔹 Test Case {i}: ₹{amt} at {time}")
        print(f"Available Notes: {notes}")

        result, algo_used = hybrid_dispatcher(amt, notes, time)
        if result:
            print(f"✅ Dispensed Notes: {result}")
            print(f"🧠 Algorithm Used: {algo_used}")
        else:
            print("❌ Could not dispense amount.")

if __name__ == "__main__":
    run_tests()