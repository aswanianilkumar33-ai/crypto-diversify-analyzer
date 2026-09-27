"""
Core statistical analysis for CryptoDiversify.
Reads returns from data/project.db, runs the RQ1-RQ3 analysis, and exports
clean summary tables to data/processed/ for the Power BI dashboard.
"""
import sqlite3
import numpy as np
import pandas as pd
from scipy.optimize import minimize

DB_PATH = "data/project.db"
OUT_DIR = "data/processed"

CRASH_2022 = (pd.Timestamp("2022-05-01"), pd.Timestamp("2022-12-31"))
CRASH_2026 = (pd.Timestamp("2026-01-01"), pd.Timestamp("2026-06-30"))
TRAIN_TEST_SPLIT = pd.Timestamp("2025-01-01")
RF = 0.0  # risk-free rate assumed 0% (documented limitation)


def label_period(d):
    if CRASH_2022[0] <= d <= CRASH_2022[1]:
        return "crash_2022"
    elif CRASH_2026[0] <= d <= CRASH_2026[1]:
        return "crash_2026"
    return "calm"


def portfolio_stats(weights, mean_daily, cov_daily):
    ret = np.dot(weights, mean_daily) * 365
    vol = np.sqrt(weights @ cov_daily @ weights) * np.sqrt(365)
    sharpe = (ret - RF) / vol
    return ret, vol, sharpe


def optimize_max_sharpe(mean_daily, cov_daily, n):
    def neg_sharpe(w):
        return -portfolio_stats(w, mean_daily, cov_daily)[2]

    constraints = ({"type": "eq", "fun": lambda w: np.sum(w) - 1},)
    bounds = tuple((0, 1) for _ in range(n))
    result = minimize(neg_sharpe, np.array([1 / n] * n), method="SLSQP",
                       bounds=bounds, constraints=constraints)
    return result.x


def main():
    conn = sqlite3.connect(DB_PATH)
    returns = pd.read_sql("SELECT * FROM returns", conn)
    conn.close()

    returns["date"] = pd.to_datetime(returns["date"])
    wide = returns.pivot(index="date", columns="coin", values="log_return")
    coins = wide.columns.tolist()
    n = len(coins)

    # --- RQ1: correlation, overall + by period ---
    overall_corr = wide.corr()
    overall_corr.to_csv(f"{OUT_DIR}/correlation_overall.csv")

    period = wide.index.to_series().apply(label_period)
    period_rows = []
    avg_rows = []
    for pname in ["calm", "crash_2022", "crash_2026"]:
        sub = wide[period == pname]
        c = sub.corr()
        for c1 in coins:
            for c2 in coins:
                period_rows.append({"period": pname, "coin_1": c1, "coin_2": c2,
                                     "correlation": c.loc[c1, c2]})
        mask = ~np.eye(n, dtype=bool)
        avg_rows.append({"period": pname, "n_days": len(sub),
                          "avg_pairwise_correlation": c.values[mask].mean()})

    pd.DataFrame(period_rows).to_csv(f"{OUT_DIR}/correlation_by_period.csv", index=False)
    pd.DataFrame(avg_rows).to_csv(f"{OUT_DIR}/correlation_avg_by_period.csv", index=False)

    # --- RQ2: individual vs equal-weighted volatility ---
    individual_vol = wide.std() * np.sqrt(365)
    eq_weights = np.array([1 / n] * n)
    mean_full = wide.mean().values
    cov_full = wide.cov().values
    eq_ret, eq_vol, eq_sharpe = portfolio_stats(eq_weights, mean_full, cov_full)

    vol_rows = [{"asset": c, "annualized_volatility": individual_vol[c]} for c in coins]
    vol_rows.append({"asset": "Equal-weighted portfolio", "annualized_volatility": eq_vol})
    pd.DataFrame(vol_rows).to_csv(f"{OUT_DIR}/volatility_comparison.csv", index=False)

    # --- RQ3: Markowitz, in-sample vs out-of-sample ---
    opt_weights_full = optimize_max_sharpe(mean_full, cov_full, n)
    opt_ret, opt_vol, opt_sharpe = portfolio_stats(opt_weights_full, mean_full, cov_full)
    btc_weights = np.zeros(n)
    btc_weights[coins.index("BTC")] = 1
    btc_ret, btc_vol, btc_sharpe = portfolio_stats(btc_weights, mean_full, cov_full)

    train = wide[wide.index < TRAIN_TEST_SPLIT]
    test = wide[wide.index >= TRAIN_TEST_SPLIT]
    train_mean, train_cov = train.mean().values, train.cov().values
    test_mean, test_cov = test.mean().values, test.cov().values
    opt_weights_train = optimize_max_sharpe(train_mean, train_cov, n)

    oos_opt = portfolio_stats(opt_weights_train, test_mean, test_cov)
    oos_eq = portfolio_stats(eq_weights, test_mean, test_cov)
    oos_btc = portfolio_stats(btc_weights, test_mean, test_cov)

    comparison_rows = [
        {"analysis": "in_sample_full_period", "portfolio": "Optimized (max-Sharpe)",
         "return": opt_ret, "volatility": opt_vol, "sharpe": opt_sharpe},
        {"analysis": "in_sample_full_period", "portfolio": "Equal-weighted",
         "return": eq_ret, "volatility": eq_vol, "sharpe": eq_sharpe},
        {"analysis": "in_sample_full_period", "portfolio": "Bitcoin alone",
         "return": btc_ret, "volatility": btc_vol, "sharpe": btc_sharpe},
        {"analysis": "out_of_sample_2025_2026", "portfolio": "Optimized (fit on 2021-2024)",
         "return": oos_opt[0], "volatility": oos_opt[1], "sharpe": oos_opt[2]},
        {"analysis": "out_of_sample_2025_2026", "portfolio": "Equal-weighted",
         "return": oos_eq[0], "volatility": oos_eq[1], "sharpe": oos_eq[2]},
        {"analysis": "out_of_sample_2025_2026", "portfolio": "Bitcoin alone",
         "return": oos_btc[0], "volatility": oos_btc[1], "sharpe": oos_btc[2]},
    ]
    pd.DataFrame(comparison_rows).to_csv(f"{OUT_DIR}/portfolio_comparison.csv", index=False)

    weights_rows = [{"coin": c, "weight_full_period": w1, "weight_train_2021_2024": w2}
                     for c, w1, w2 in zip(coins, opt_weights_full, opt_weights_train)]
    pd.DataFrame(weights_rows).to_csv(f"{OUT_DIR}/optimal_weights.csv", index=False)

    print("Exported to data/processed/:")
    for f in ["correlation_overall.csv", "correlation_by_period.csv",
              "correlation_avg_by_period.csv", "volatility_comparison.csv",
              "portfolio_comparison.csv", "optimal_weights.csv"]:
        print(f"  {f}")


if __name__ == "__main__":
    main()
