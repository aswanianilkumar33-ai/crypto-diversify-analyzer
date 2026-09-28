"""
Uncertainty for the three research questions, using a moving-block bootstrap.

Why a *block* bootstrap: daily crypto returns show volatility clustering (calm and
wild days come in runs), so resampling single days would break that dependence and
make intervals too narrow. We resample blocks of consecutive days instead.

Output: data/processed/significance_tests.csv
  estimate, 95% percentile CI, and a one-sided bootstrap p-value
  (share of resamples where the effect is on the "H0 side" of zero).
"""
import sqlite3
import numpy as np
import pandas as pd

from analysis import DB_PATH, OUT_DIR, TRAIN_TEST_SPLIT, label_period

BLOCK_LEN = 20      # ~1 month of trading days per block
N_BOOT = 2000       # bootstrap resamples
SEED = 42           # fixed seed so results are reproducible


def block_indices(n, rng):
    """Indices for one circular moving-block bootstrap resample of length n."""
    n_blocks = int(np.ceil(n / BLOCK_LEN))
    starts = rng.integers(0, n, n_blocks)
    idx = (starts[:, None] + np.arange(BLOCK_LEN)) % n
    return idx.ravel()[:n]


def avg_pairwise_corr(x):
    c = np.corrcoef(x, rowvar=False)
    return c[~np.eye(c.shape[0], dtype=bool)].mean()


def ann_vol(r):
    return r.std(ddof=1) * np.sqrt(365)


def ann_sharpe(r):
    return r.mean() * 365 / (r.std(ddof=1) * np.sqrt(365))


def summarize(question, comparison, estimate, boot, h1_greater):
    lo, hi = np.percentile(boot, [2.5, 97.5])
    p = np.mean(boot <= 0) if h1_greater else np.mean(boot >= 0)
    return {"question": question, "comparison": comparison, "estimate": estimate,
            "ci_low": lo, "ci_high": hi, "p_value_one_sided": p,
            "method": f"moving-block bootstrap (block={BLOCK_LEN} days, B={N_BOOT})"}


def main():
    rng = np.random.default_rng(SEED)
    conn = sqlite3.connect(DB_PATH)
    returns = pd.read_sql("SELECT * FROM returns", conn)
    conn.close()
    returns["date"] = pd.to_datetime(returns["date"])
    wide = returns.pivot(index="date", columns="coin", values="log_return")
    coins = wide.columns.tolist()
    rows = []

    # --- RQ1: is average pairwise correlation higher in crashes than in calm periods? ---
    period = wide.index.to_series().apply(label_period)
    calm = wide[period == "calm"].values
    for crash in ["crash_2022", "crash_2026"]:
        cr = wide[period == crash].values
        est = avg_pairwise_corr(cr) - avg_pairwise_corr(calm)
        boot = np.array([avg_pairwise_corr(cr[block_indices(len(cr), rng)])
                         - avg_pairwise_corr(calm[block_indices(len(calm), rng)])
                         for _ in range(N_BOOT)])
        rows.append(summarize("RQ1", f"avg correlation: {crash} minus calm", est, boot, True))

    # --- RQ2: does the equal-weighted portfolio have lower volatility? (full period) ---
    x = wide.values
    ew = lambda m: m.mean(axis=1)                 # equal-weighted daily return
    btc = coins.index("BTC")

    def vol_gaps(m):
        port = ann_vol(ew(m))
        singles = np.array([ann_vol(m[:, j]) for j in range(m.shape[1])])
        return port - singles.mean(), port - singles[btc]

    est_avg, est_btc = vol_gaps(x)
    boot = np.array([vol_gaps(x[block_indices(len(x), rng)]) for _ in range(N_BOOT)])
    rows.append(summarize("RQ2", "volatility: equal-weighted minus average single coin", est_avg, boot[:, 0], False))
    rows.append(summarize("RQ2", "volatility: equal-weighted minus BTC alone", est_btc, boot[:, 1], False))

    # --- RQ3: out-of-sample Sharpe (2025-2026), weights fixed from the 2021-2024 fit ---
    w = pd.read_csv(f"{OUT_DIR}/optimal_weights.csv").set_index("coin")["weight_train_2021_2024"]
    w = w.reindex(coins).values
    test = wide[wide.index >= TRAIN_TEST_SPLIT].values

    def sharpe_gaps(m):
        opt, eq, b = ann_sharpe(m @ w), ann_sharpe(ew(m)), ann_sharpe(m[:, btc])
        return opt - eq, opt - b

    est_eq, est_b = sharpe_gaps(test)
    boot = np.array([sharpe_gaps(test[block_indices(len(test), rng)]) for _ in range(N_BOOT)])
    rows.append(summarize("RQ3", "OOS Sharpe: optimized minus equal-weighted", est_eq, boot[:, 0], True))
    rows.append(summarize("RQ3", "OOS Sharpe: optimized minus BTC alone", est_b, boot[:, 1], True))

    out = pd.DataFrame(rows)
    out.to_csv(f"{OUT_DIR}/significance_tests.csv", index=False)
    pd.set_option("display.width", 200)
    print(out.drop(columns="method").round(3).to_string(index=False))


if __name__ == "__main__":
    main()
