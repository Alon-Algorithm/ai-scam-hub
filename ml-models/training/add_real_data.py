import pandas as pd
import json

print("Real Scam Data Collector")
print("=" * 60)

def load_from_csv(filename):
    try:
        df = pd.read_csv(filename)
        print(f"Loaded {len(df)} records from {filename}")
        return df
    except Exception as e:
        print(f"Could not load {filename}: {e}")
        return None

def load_from_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print(f"Loaded {len(df)} records from {filename}")
        return df
    except Exception as e:
        print(f"Could not load {filename}: {e}")
        return None

def add_manual_data():
    new_scams = [
        ("Your credit card has been charged R10,000. Click to dispute: https://fake-bank.xyz", 1),
        ("URGENT: Your Amazon account is locked. Verify now: https://amazon-verify.xyz", 1),
        ("You owe R5,000 in taxes. Pay immediately or face legal action.", 1),
        ("Congratulations! You've won a free vacation! Call now to claim.", 1),
        ("Your electricity will be disconnected. Pay R2,000 to keep it on.", 1),
        ("Apple Security Alert: Your phone has been compromised. Call 0800-123-456.", 1),
        ("Get rich quick with crypto! Invest R1,000 today and get R10,000 in 7 days!", 1),
        ("Your passport has been flagged. Click here to verify: https://gov-verify.xyz", 1),
        ("Dear customer, your package is stuck. Pay R200 for re-delivery.", 1),
        ("You've been pre-approved for a loan of R500,000. Reply to claim.", 1)
    ]
    
    new_legit = [
        ("Your order #789456 has been shipped. Track it here: https://amazon.com/track", 0),
        ("Bank statement for March is available. Please review it.", 0),
        ("Your application status has been updated. Login to check.", 0),
        ("Reminder: Doctor's appointment tomorrow at 9am.", 0),
        ("Your invoice #INV-789 has been generated. Please pay by Friday.", 0)
    ]
    
    return new_scams + new_legit

print("\nTo use real data for training:")
print("  1. Add your own CSV/JSON files")
print("  2. Download public datasets")
print("  3. Use manual data entries")

manual_data = add_manual_data()
if manual_data:
    print(f"\nAdded {len(manual_data)} manual entries")

print("\n" + "=" * 60)
print("Next Steps:")
print("1. Download real dataset from Kaggle or other sources")
print("2. Run: python train_scam_detector.py")
print("3. The model will use your data for training")
