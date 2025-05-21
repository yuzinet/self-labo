# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 仮の株主優待データ
yutai_data = {
    "7203.T": "保有6ヶ月以上でオリジナルギフト",
    "6758.T": "保有期間に応じたポイント付与",
    "9984.T": "株主限定セミナー参加券",
}

st.title("好きな銘柄の株価一覧")

# 複数銘柄のティッカーを入力
tickers = st.text_input("銘柄コード（カンマ区切り）", "7203.T,6758.T,9984.T")
ticker_list = [t.strip() for t in tickers.split(",") if t.strip()]

if ticker_list:
    for ticker in ticker_list:
        stock = yf.Ticker(ticker)

        st.subheader(f"{ticker} の情報")

        # 現在の株価
        current_price = stock.info.get("regularMarketPrice", "不明")
        st.write(f"**現在の株価：** {current_price} 円")

        # 配当利回り
        dividend_yield = stock.info.get("dividendYield")
        if dividend_yield:
            st.write(f"**配当利回り：** {round(dividend_yield * 100, 2)} %")
        else:
            st.write("**配当利回り：** 情報なし")

        # 株主優待（仮データ）
        yutai = yutai_data.get(ticker, "情報なし")
        st.write(f"**株主優待：** {yutai}")

        # 株価の変動グラフ（過去1ヶ月）
        st.write("**株価の変動（過去1ヶ月）**")
        hist = stock.history(period="1mo")
        if not hist.empty:
            fig, ax = plt.subplots()
            hist["Close"].plot(ax=ax)
            ax.set_title(f"{ticker} の株価推移")
            ax.set_ylabel("株価")
            st.pyplot(fig)
        else:
            st.write("株価データが取得できませんでした。")