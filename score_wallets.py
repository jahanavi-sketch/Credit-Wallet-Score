import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# === 1. Load the JSON data ===
with open('user-wallet-transactions.json') as f:
    raw_data = json.load(f)

df = pd.DataFrame(raw_data)

# === 2. Filter out missing or broken rows ===
df = df[df['actionData'].notnull() & df['userWallet'].notnull()]

# === 3. Convert timestamp ===
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')


# === 4. Extract amount (from actionData.amount) ===
def extract_amount(row):
    try:
        amt = float(row['actionData'].get('amount', '0'))
        return amt / 1e6  # scale (assuming USDC-like 6 decimals)
    except:
        return 0


df['amount'] = df.apply(extract_amount, axis=1)

# === 5. Group by wallet ===
wallets = df.groupby('userWallet')

wallet_features = []

for wallet, group in tqdm(wallets, desc="Processing wallets"):
    total_txns = len(group)
    num_deposits = len(group[group['action'] == 'deposit'])
    num_borrows = len(group[group['action'] == 'borrow'])
    num_repays = len(group[group['action'] == 'repay'])
    num_redeems = len(group[group['action'] == 'redeemunderlying'])
    num_liquidations = len(group[group['action'] == 'liquidationcall'])

    total_deposit_amt = group[group['action'] == 'deposit']['amount'].sum()
    total_borrow_amt = group[group['action'] == 'borrow']['amount'].sum()
    total_repay_amt = group[group['action'] == 'repay']['amount'].sum()

    repay_ratio = (
        total_repay_amt / total_borrow_amt if total_borrow_amt > 0 else 0
    )

    group_sorted = group.sort_values('timestamp')
    activity_days = (group_sorted['timestamp'].iloc[-1] - group_sorted['timestamp'].iloc[0]).days + 1

    wallet_features.append({
        'wallet': wallet,
        'num_txns': total_txns,
        'num_deposits': num_deposits,
        'num_borrows': num_borrows,
        'num_repays': num_repays,
        'num_redeems': num_redeems,
        'num_liquidations': num_liquidations,
        'total_deposit_amt': total_deposit_amt,
        'total_borrow_amt': total_borrow_amt,
        'total_repay_amt': total_repay_amt,
        'repay_ratio': repay_ratio,
        'activity_days': activity_days,
    })

features_df = pd.DataFrame(wallet_features)


# === 6. Scoring Logic ===
def score_wallet(row):
    score = 0
    score += np.log1p(row['total_deposit_amt']) * 10
    score += row['repay_ratio'] * 300
    score -= row['num_liquidations'] * 100
    score += np.log1p(row['activity_days']) * 10
    score += row['num_txns'] * 2
    return int(np.clip(score, 0, 1000))


features_df['score'] = features_df.apply(score_wallet, axis=1)

# === 7. Save results ===
features_df.to_csv("wallet_scores.csv", index=False)

# === 8. Plot distribution ===
bins = list(range(0, 1100, 100))
features_df['score_bin'] = pd.cut(features_df['score'], bins)

plt.figure(figsize=(10, 6))
features_df['score_bin'].value_counts().sort_index().plot(kind='bar', color='skyblue')
plt.title("Wallet Score Distribution")
plt.xlabel("Score Range")
plt.ylabel("Number of Wallets")
plt.grid(True)
plt.tight_layout()
plt.savefig("score_distribution.png")

print("✅ Scoring complete. Output saved to 'wallet_scores.csv' and 'score_distribution.png'")
