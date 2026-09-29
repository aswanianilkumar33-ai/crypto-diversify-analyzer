# Project Brief: CryptoDiversify

**Does diversifying across cryptocurrencies actually protect investors?**

A statistical study of whether holding several cryptocurrencies really reduces risk, or
whether they all fall together exactly when protection is needed most. It covers six major
coins over 2021–2026, including two real market crashes.

---

## 1. What is this project?

Investors are told to diversify: "don't put all your eggs in one basket". In crypto, many
people do this by holding several coins. Diversification only works, however, if the assets
do **not** fall at the same time. This project tests that assumption with real market data,
using three research questions. The hypotheses were written **before** the analysis was run.

| | Research question | H0 | H1 |
|---|---|---|---|
| **RQ1** | Do coins become more correlated during crashes? | Average pairwise correlation is the same in crash and calm periods | It is higher in crash periods |
| **RQ2** | Does an equal-weighted portfolio reduce volatility? | Portfolio volatility equals that of a single coin | Portfolio volatility is lower |
| **RQ3** | Does Markowitz optimization beat simple equal-weighting? | Optimized and equal-weighted Sharpe ratios are the same | The optimized Sharpe ratio is higher |

## 2. How was it done?

**Data**
- Daily closing prices from the Binance public API for **BTC, ETH, SOL, BNB, XRP and DOGE**
  (in USDT), from 2021-01-01 to 2026-09-27 (UTC).
- That is 2,096 days per coin, with no missing days.
- Daily **log returns** are used for all statistics. Correlating price levels would mostly
  pick up the shared long-term trend.

**Crash periods** were fixed in advance from real events. They were not chosen after
seeing the results.
- 2022-05-01 to 2022-12-31: Terra/Luna and FTX collapses
- 2026-01-01 to 2026-06-30: war and Fed-driven market decline
- All other days are treated as "calm".

**Methods**
| Question | Method |
|---|---|
| RQ1 | Pearson correlation matrix per period. Average of the 15 coin pairs. |
| RQ2 | Annualized volatility (×√365) of each coin vs an equal-weighted, daily-rebalanced portfolio. |
| RQ3 | Long-only max-Sharpe Markowitz optimization. Weights are fitted on 2021–2024 and tested on unseen 2025–2026 data. |
| All | Moving-block bootstrap (20-day blocks, 2,000 resamples) for 95% confidence intervals and one-sided p-values. Blocks keep the volatility clustering in daily returns. |

**Pipeline:**
Binance API → Python (pandas) → SQLite database → SQL queries → statistical analysis
(NumPy, SciPy) → Power BI dashboard. The entire pipeline reruns with `python main.py`.

## 3. Scope

**Included**
- Six large, still-active coins, at daily frequency, 2021–2026
- Correlation in calm vs crash periods, portfolio volatility, Markowitz optimization with an out-of-sample test
- Bootstrap confidence intervals for every main result
- SQL database and queries, Jupyter notebooks, Power BI dashboard, written report

**Not included**
- Price prediction or trading strategies
- Transaction costs, slippage and taxes. The risk-free rate is set to 0%.
- Coins that have been delisted or collapsed (see Limitations)

## 4. What was done: results

| | Result | Conclusion |
|---|---|---|
| **RQ1** | Average correlation **0.54 (calm) → 0.76 (2022 crash) → 0.84 (2026 crash)**. Increase 95% CI: [0.09, 0.33] and [0.17, 0.40], p < 0.001. | **H0 rejected.** Diversification weakens exactly during crashes. |
| **RQ2** | Equal-weighted portfolio **72.6%** volatility vs **91.7%** for the average coin (95% CI of difference: −25.7 to −12.6 points). Still above Bitcoin alone (57.1%). | **Partly supported.** Less risky than a typical coin, not less risky than BTC. |
| **RQ3** | In-sample Sharpe 0.76 vs 0.57 (equal-weighted). **Out-of-sample: −0.35 vs −0.34**; the difference −0.01 has 95% CI [−0.30, 0.27]. | **H0 not rejected.** The optimizer's in-sample advantage did not carry over to new data. |

**Deliverables**
| File / folder | Contents |
|---|---|
| `README.md` | Project overview, findings, how to run |
| `reports/final_report.md` | Full written report |
| `src/` | Data download, database build, analysis, bootstrap tests |
| `sql/` | 8 commented SQL queries (aggregates, JOIN, CASE, window function) |
| `notebooks/` | Exploratory analysis and main analysis with charts |
| `dashboard/` | Power BI dashboard (3 pages) and screenshots |
| `data/processed/` | Result tables used by the dashboard |

## 5. Limitations

- **Survivorship bias:** all six coins are still large today. Coins that failed are not included.
- The crash window boundaries involve judgment. They are not detected statistically.
- The out-of-sample test covers only ~21 months, so the Sharpe ratio intervals are wide.
- Correlation does not imply causation, and future crashes may behave differently.
- This is research for analysis purposes only. **Not financial advice.**
