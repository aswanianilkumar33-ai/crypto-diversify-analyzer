# CryptoDiversify — Does Diversifying Across Cryptocurrencies Actually Protect Investors?

**One-sentence pitch:** A statistical study testing whether holding multiple cryptocurrencies
genuinely reduces an investor's risk — or whether they all crash together exactly when
protection is needed most — using correlation analysis and Markowitz portfolio optimization
on six coins across two real market crashes (2022, 2026).

---

## Research questions, hypotheses, and planned tests

### RQ1 — Do crypto returns become more correlated during market crashes than during calm periods?
- **H0:** Average pairwise correlation among the six coins is the same during crash periods
  and calm periods.
- **H1:** Average pairwise correlation is significantly *higher* during crash periods than
  calm periods.
- **Planned test:** Rolling-window correlation matrices over time; compare correlation levels
  in identified crash windows vs. calm windows.

### RQ2 — Does diversifying across multiple coins actually reduce portfolio risk vs. holding one coin?
- **H0:** A diversified portfolio (equal-weighted or optimized) has the same volatility as the
  average single-coin holding.
- **H1:** A diversified portfolio has significantly *lower* volatility than a single coin.
- **Planned test:** Compare portfolio standard deviation (equal-weighted, optimized) against
  individual coins' volatility.

### RQ3 — Can Markowitz optimization find a better risk-adjusted allocation than naive equal-weighting?
- **H0:** The optimized portfolio's Sharpe ratio is not meaningfully different from the
  equal-weighted portfolio's Sharpe ratio.
- **H1:** The optimized portfolio achieves a higher Sharpe ratio than equal-weighting.
- **Planned test:** Compute and compare Sharpe ratios for equal-weighted vs.
  Markowitz-optimized portfolios; efficient frontier plot.

*(Hypotheses are stated now, before we look at results, so we don't unconsciously fit our
analysis to whatever answer looks best afterward.)*

---

## Data

- **Source:** Binance public market data (daily candles/"klines"), free, no API key required.
- **Assets:** BTC, ETH, SOL, BNB, XRP, DOGE (all priced in USDT) — a mix of market benchmark,
  large-cap alt, exchange-linked, payments-focused, and meme/high-volatility coins.
- **Time period:** 2021-01-01 to present (2026). Covers two distinct crash episodes:
  - **2022** — Terra/Luna and FTX collapses (crypto-specific shock)
  - **2026** — US–Israel–Iran war + Fed policy response (macro/geopolitical shock)
- **Frequency:** Daily.

---

## Scope

### Core (must-have)
- Clean daily price/return data for all six coins, 2021–present, stored in SQLite.
- Overall correlation matrix + rolling correlation over time.
- Identification of crash windows (2022, 2026) vs. calm periods.
- Markowitz optimization (efficient frontier) + Sharpe ratio.
- Comparison: single-asset vs. equal-weighted vs. optimized portfolio.
- Power BI dashboard with key findings.
- README + short written report.

### Stretch (only if time allows, after core is solid)
- Formal significance test on the crash-period correlation shift (e.g., Fisher z-test).
- Additional risk metrics per portfolio (max drawdown, VaR).
- Extending back to include the March 2020 COVID crash, data permitting.

---

## Deliverables
- `data/project.db` — SQLite database
- `sql/` — commented SQL queries
- `notebooks/01_eda.ipynb`, `notebooks/02_analysis.ipynb`
- `dashboard/cryptodiversify.pbix` + screenshots
- `reports/final_report.md`
- `README.md`

---

## Target roles & resume story
- **Target roles:** open — Data Analyst, Risk Analyst, or Quant/Research Analyst roles that
  value applied statistics for real investment decisions.
- **Resume story (finalized with actual results):** "Analyzed 6 cryptocurrencies' historical
  returns (2021–2026) to test portfolio diversification using correlation regimes and
  Markowitz optimization; found that pairwise correlation rises sharply during crashes
  (0.54 calm vs. 0.76–0.84 during the 2022 and 2026 crashes; block-bootstrap 95% CIs
  exclude zero), and that an in-sample 'optimal' Markowitz portfolio lost its edge
  out-of-sample (Sharpe −0.35 vs −0.34 equal-weighted and −0.13 Bitcoin; difference not
  statistically significant) — demonstrating that backward-looking optimization can be
  overconfident and fragile in a fast-evolving asset class."
- **Stretch goal completed:** formal significance testing was done with a moving-block
  bootstrap (instead of the Fisher z-test first planned, because daily returns are not
  independent). See `src/significance.py`.

---

## Known limitations (stated upfront, honestly)
- Six coins are not representative of the entire crypto market (thousands of tokens exist).
- Correlation does not imply causation.
- Historical relationships may not hold in future crashes — this is backward-looking research,
  not a prediction guarantee.
- Some coins may have slightly shorter price history than others within the window; any gaps
  will be documented when we pull the data.
- No transaction costs, slippage, or exchange risk are modeled in the portfolio comparisons.
- This is research for learning and portfolio purposes — **not financial advice**.
- Crash windows (2022-05-01 to 2022-12-31; 2026-01-01 to 2026-06-30) were manually defined
  from known real-world events (Terra/Luna collapse, FTX collapse, 2026 war/Fed-driven
  decline), not statistically detected from the data. This is a defensible, theory-driven
  choice (it avoids cherry-picking windows after seeing results) but the exact boundary
  dates involve judgment, not a data-driven changepoint test.
- Correlation was deliberately computed on log returns, not raw price levels, to avoid
  spurious correlation from shared long-term trend (raw-level correlation was noticeably
  higher for several pairs, e.g. BNB-BTC 0.89 vs 0.67 on returns — confirmed empirically
  during this analysis, not just assumed from theory).
