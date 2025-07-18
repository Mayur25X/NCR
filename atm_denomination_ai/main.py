# main.py

from algorithm.hybrid_dispatcher import hybrid_dispatcher

def main():
    print("🧠 AI-Based ATM Denomination System")
    print("----------------------------------")

    # Example manual input
    try:
        withdrawal_amount = int(input("Enter withdrawal amount (₹): "))
    except ValueError:
        print("❌ Invalid amount.")
        return

    available_notes = {
        500: 10,
        200: 20,
        100: 30,
       }

    txn_time = "2025-12-30 10:10:59"

    print("\n🔄 Processing...")
    result, algo = hybrid_dispatcher(withdrawal_amount, available_notes, txn_time)

    if result:
        print(f"\n✅ Dispensed Notes: {result}")
        print(f"🧠 Algorithm Used: {algo}")
    else:
        print("❌ Unable to fulfill the withdrawal with available notes.")

if __name__ == "__main__":
    main()