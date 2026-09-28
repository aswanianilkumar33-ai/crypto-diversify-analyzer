"""
Load the raw price CSVs into the SQLite database data/project.db.

Creates two tables (long format: one row per coin per day):
  prices  (date, coin, close_price)  - daily close in USDT, dates in UTC
  returns (date, coin, log_return)   - daily log return = ln(P_t / P_{t-1})
"""
import sqlite3
import numpy as np
import pandas as pd

COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE"]
RAW_DIR = "data/raw"
DB_PATH = "data/project.db"


def main():
    frames = []
    for coin in COINS:
        df = pd.read_csv(f"{RAW_DIR}/{coin}_prices.csv")
        df = df.rename(columns={coin: "close_price"})
        df["coin"] = coin
        frames.append(df[["date", "coin", "close_price"]])
    prices = pd.concat(frames, ignore_index=True)

    # Basic quality checks: no duplicate days, no missing prices
    assert not prices.duplicated(["date", "coin"]).any(), "duplicate coin-days found"
    assert prices["close_price"].notna().all(), "missing prices found"

    # Log returns are computed within each coin, in date order
    prices = prices.sort_values(["coin", "date"])
    prices["log_return"] = prices.groupby("coin")["close_price"].transform(lambda p: np.log(p).diff())
    returns = prices.dropna(subset=["log_return"])[["date", "coin", "log_return"]]

    conn = sqlite3.connect(DB_PATH)
    prices[["date", "coin", "close_price"]].to_sql("prices", conn, if_exists="replace", index=False)
    returns.to_sql("returns", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Loaded {len(prices)} price rows and {len(returns)} return rows into {DB_PATH}")


if __name__ == "__main__":
    main()
