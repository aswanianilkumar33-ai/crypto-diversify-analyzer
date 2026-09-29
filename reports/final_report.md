# CryptoDiversify: Final Report

**Does diversifying across cryptocurrencies actually protect investors?**
Aswani A · September 2026 · Data: Binance daily prices, 2021-01-01 to 2026-09-27 (UTC)

---

## 1. Motivation

"Don't put all your eggs in one basket" is the first rule of investing. Many crypto
investors apply it by holding several coins. But diversification only works if the assets
do **not** all fall at the same time. This study asks whether that holds for crypto,
especially during crashes, which is when protection matters most.

## 2. Research questions and hypotheses

These were written in `PROJECT_BRIEF.md` **before** any results were computed, so the
analysis could not be bent to fit whatever looked best afterwards.

| | Question | H0 | H1 |
|---|---|---|---|
| RQ1 | Are coins more correlated in crashes? | Average pairwise correlation is the same in crash and calm periods | It is higher in crashes |
| RQ2 | Does diversifying reduce volatility? | Equal-weighted portfolio volatility equals that of a single coin | It is lower |
| RQ3 | Does Markowitz beat equal-weighting? | Optimized Sharpe ratio equals the equal-weighted Sharpe | Optimized Sharpe is higher |

## 3. Data

- Six coins: BTC, ETH, SOL, BNB, XRP, DOGE, each priced in USDT, 2,096 daily closes each.
  There were no missing days or duplicates (verified in SQL and in `load_to_db.py`).
- Daily **log returns** `r_t = ln(P_t / P_{t−1})` were used for all statistics. Correlating
  price *levels* would mostly measure the shared long-term trend. For example, BNB–BTC is
  0.89 on prices but 0.67 on returns.
- **Crash windows** were fixed from known events: 2022-05-01 to 2022-12-31 (Terra/Luna, FTX)
  and 2026-01-01 to 2026-06-30 (war and Fed-driven decline). The remaining 1,669 days are "calm".

**What the data looks like** (from `sql/02` and `sql/04`):
- Daily volatility ranges from 3.0% (BTC) to 7.0% (DOGE).
- The worst single day was **SOL −54.9% on 2022-11-09** (FTX collapse).
- On **47 days**, all six coins fell by more than 5% on the same day.

## 4. Methods

**Correlation (RQ1).** Pearson correlation matrix per period. The summary measure is the
mean of the 15 off-diagonal pairs.

**Volatility (RQ2).** Annualized standard deviation `σ_daily × √365`. We use 365 because
crypto trades every day. The equal-weighted portfolio is rebalanced daily
(`r_p = mean of the six returns`).

**Markowitz optimization (RQ3).** We choose long-only weights (0 ≤ wᵢ ≤ 1, Σwᵢ = 1) to
maximize the Sharpe ratio `μ_p / σ_p` (risk-free rate 0%), using SciPy's SLSQP solver.
- **In-sample:** fit and evaluate on 2021–2026.
- **Out-of-sample:** fit on 2021–2024, then evaluate on 2025-01-01 to 2026-09-27
  (635 days) with the weights fixed.

**Uncertainty.** Daily returns show volatility clustering, so they are not independent.
A plain bootstrap would therefore understate uncertainty. We use a **circular
moving-block bootstrap**: blocks of 20 consecutive days, 2,000 resamples, fixed seed 42.
We report 95% percentile confidence intervals and one-sided p-values. The p-value is the
share of resamples where the effect falls on the H0 side of zero.

## 5. Results

### RQ1: Correlation rises sharply in crashes

| Period | Days | Avg pairwise correlation |
|---|---|---|
| Calm | 1,669 | **0.54** |
| Crash 2022 | 245 | **0.76** |
| Crash 2026 | 181 | **0.84** |

| Comparison | Difference | 95% CI | p (one-sided) |
|---|---|---|---|
| Crash 2022 − calm | +0.22 | [0.09, 0.33] | < 0.001 |
| Crash 2026 − calm | +0.30 | [0.17, 0.40] | < 0.001 |

**H0 is rejected** for both crashes. The most diversifying pair shows the effect clearly.
BNB–DOGE has a correlation of 0.35 in calm times but 0.76 in the 2026 crash, which is
almost as high as the *strongest* calm pair (BTC–ETH, 0.80).

*Robustness check.* Correlation can rise simply because volatility rises (Forbes and
Rigobon, 2002). That does not explain this result. Daily volatility was 5.1% in calm
periods, 5.1% in the 2022 crash, and only **3.2% in the 2026 crash** (`sql/05`). So
correlation rose even though volatility did not.

### RQ2: Diversification helps, but less than hoped

| | Annualized volatility |
|---|---|
| Average single coin | 91.7% |
| Equal-weighted portfolio | **72.6%** |
| Bitcoin alone | 57.1% |

- Equal-weighted minus average coin: **−19.2 points**, 95% CI [−25.7, −12.6], p < 0.001.
- Equal-weighted minus BTC: **+15.5 points**, 95% CI [10.8, 20.8].

**H0 is rejected against the typical coin.** Mixing coins reduces volatility by about a
fifth. But the diversified basket is still clearly *riskier than holding Bitcoin alone*,
because the other five coins are much more volatile than BTC and highly correlated with it.

### RQ3: The "optimal" portfolio did not survive new data

| | In-sample Sharpe (2021–26) | Out-of-sample Sharpe (2025–26) |
|---|---|---|
| Markowitz max-Sharpe | **0.76** | −0.35 |
| Equal-weighted | 0.57 | −0.34 |
| Bitcoin alone | 0.32 | **−0.13** |

- The 2021–2024 fit put **48% in SOL, 34% in BNB, 18% in DOGE and 0% in BTC, ETH and XRP**.
  In other words, it bet on the past winners.
- Out-of-sample, optimized minus equal-weighted Sharpe = **−0.01**, 95% CI [−0.30, 0.27], p = 0.52.
- Optimized minus BTC = −0.22, 95% CI [−0.91, 0.46].

**H0 is not rejected.** There is no evidence that optimization beats equal-weighting. Its
large in-sample advantage disappeared on new data. The point estimates even rank it last,
but the test period is short, so we cannot claim it is *significantly* worse.

## 6. Conclusions

1. **Crypto diversification fails when it is needed most.** Correlations rise from about 0.5
   to about 0.8 in crashes, and this is statistically clear.
2. **Diversification still has value in normal times.** It is roughly 20% less volatile than
   a typical single coin, but not less volatile than Bitcoin alone.
3. **Mean-variance optimization overfits.** Weights estimated from past returns concentrate
   in past winners and lose their edge out-of-sample. A simple equal-weight rule did at least
   as well. This matches a well-known finding in finance: estimation error in expected
   returns dominates the optimizer.

## 7. Limitations

- **Survivorship bias.** All six coins are still large today. Coins that collapsed since
  2021 are not in the sample, so real-world diversification may look even worse.
- Crash windows are defined by judgment about event dates, not by a statistical changepoint test.
- The out-of-sample period is short (635 days, largely a falling market), so Sharpe
  confidence intervals are wide.
- Six tests were run. The RQ1 and RQ2 results stay significant even after a Bonferroni
  correction (0.05 / 6 ≈ 0.008).
- There are no transaction costs, and the risk-free rate is 0%. Daily rebalancing is assumed.
- This is backward-looking research. **Not financial advice.**

## 8. Possible extensions

- Add more coins, including delisted ones, to measure survivorship bias.
- Detect crash regimes statistically, for example with a Markov-switching model.
- Use DCC-GARCH for time-varying correlations.
- Use shrinkage estimators (Ledoit–Wolf) or minimum-variance portfolios, which are less
  sensitive to noisy mean estimates.
- Use a longer out-of-sample test with rolling re-optimization.

---

*Reproduce everything with `python main.py`. See README.md for setup.*
