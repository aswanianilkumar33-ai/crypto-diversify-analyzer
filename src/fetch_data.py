import time
import requests
import pandas as pd

COINS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "BNB": "BNBUSDT",
    "XRP": "XRPUSDT",
    "DOGE": "DOGEUSDT",
}

START_DATE = "2021-01-01"
BINANCE_URL = "https://api.binance.com/api/v3/klines"


def fetch_klines(symbol, start_date):
    start_ts = int(pd.Timestamp(start_date, tz="UTC").timestamp() * 1000)
    end_ts = int(pd.Timestamp.now(tz="UTC").timestamp() * 1000)

    all_rows = []
    current_start = start_ts

    while current_start < end_ts:
        params = {
            "symbol": symbol,
            "interval": "1d",
            "startTime": current_start,
            "endTime": end_ts,
            "limit": 1000,
        }
        response = requests.get(BINANCE_URL, params=params)
        response.raise_for_status()
        rows = response.json()

        if not rows:
            break

        all_rows.extend(rows)
        current_start = rows[-1][0] + 1

        if len(rows) < 1000:
            break

        time.sleep(0.3)

    df = pd.DataFrame(all_rows, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore",
    ])
    df["date"] = pd.to_datetime(df["open_time"], unit="ms").dt.date
    df["close"] = df["close"].astype(float)

    return df[["date", "close"]]


def main():
    for coin, symbol in COINS.items():
        print(f"Fetching {coin} ({symbol})...")
        df = fetch_klines(symbol, START_DATE)
        df = df.rename(columns={"close": coin})
        out_path = f"data/raw/{coin}_prices.csv"
        df.to_csv(out_path, index=False)
        print(f"  Saved {len(df)} rows to {out_path} "
              f"(from {df['date'].min()} to {df['date'].max()})")


if __name__ == "__main__":
    main()
