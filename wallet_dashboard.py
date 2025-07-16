import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Aave Wallet Credit Score Dashboard")

# Load CSV
uploaded = st.file_uploader("Upload wallet_scores.csv", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)

    # Score Range Filter
    score_min, score_max = st.slider("Select Score Range", 0, 1000, (0, 1000), step=50)
    filtered_df = df[(df['score'] >= score_min) & (df['score'] <= score_max)]

    # Show filtered data
    st.subheader(f"Wallets with Score Between {score_min}–{score_max}")
    st.write(filtered_df[['wallet', 'score']].reset_index(drop=True))

    # Top risky wallets
    st.subheader("⚠️ Risky Wallets (Score < 200)")
    st.write(df[df['score'] < 200].sort_values(by='score').head(10))

    # Plot score distribution
    st.subheader("📊 Score Distribution")
    fig, ax = plt.subplots()
    df['score'].hist(bins=10, edgecolor='black', ax=ax)
    ax.set_xlabel("Score")
    ax.set_ylabel("Number of Wallets")
    st.pyplot(fig)

    # Optional CSV export
    st.download_button("Download Filtered CSV", data=filtered_df.to_csv(index=False), file_name="filtered_scores.csv")
else:
    st.warning("Please upload the `wallet_scores.csv` file.")
