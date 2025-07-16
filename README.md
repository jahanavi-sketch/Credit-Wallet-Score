# 🏦 Aave V2 Credit Wallet Scoring

This project computes a **credit score (0–1000)** for each wallet that interacted with the Aave V2 protocol, based solely on transaction behavior. It helps to evaluate wallet reliability in a decentralized finance (DeFi) context.

---

## 🎯 Problem Statement

You are provided with user-level transaction data (actions: deposit, borrow, repay, redeem, liquidationcall) and must generate wallet scores reflecting how "trustworthy" or risky each wallet is.

---

## 🧠 Method Chosen

We used a **rule-based scoring system** that assigns weight to key behaviors:
- **Deposits** → positive impact
- **Repayments** → positive impact
- **Liquidations** → strong negative impact
- **Number of transactions** and **active days** → reliability proxy

Final score is scaled and clipped between `0–1000`.

---

## ⚙️ Score Formula

```python
score = log1p(total_deposit_amt) * 10 \
      + repay_ratio * 300 \
      - num_liquidations * 100 \
      + log1p(activity_days) * 10 \
      + num_txns * 2
