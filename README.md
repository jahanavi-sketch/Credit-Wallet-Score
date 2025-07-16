# Aave V2 Wallet Credit Scoring

Assign credit scores (0–1000) to wallets interacting with the Aave V2 protocol.

## 📦 What It Does

- Reads DeFi transaction JSON
- Extracts wallet-level behavior
- Computes a trust score based on repayments, liquidations, etc.
- Saves score file + chart

## 🚀 How to Use

1. Place your `user_transactions.json` file in the project
2. Run the script:
```bash
python score_wallets.py
