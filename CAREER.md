# CAREER.md: Using CryptoDiversify in job applications

> Draft written with Claude. **Edit every line into your own words** before using it.
> Interviewers can tell when an answer is memorized rather than understood.

---

## Resume bullets (pick 3–4)

- Built an end-to-end analytics pipeline (**Python, SQLite, Power BI**) on 12,500+ daily
  price records for 6 cryptocurrencies (2021–2026), collected from the Binance public API.
- Showed that crypto correlations rise sharply in market crashes (**0.54 → 0.84**). Quantified
  uncertainty with a **moving-block bootstrap** (95% CI for the increase: 0.17–0.40, p < 0.001).
- Tested **Markowitz portfolio optimization out-of-sample**. The in-sample Sharpe advantage
  (0.76 vs 0.57) vanished on unseen 2025–26 data, demonstrating overfitting and look-ahead
  bias risks.
- Wrote 8 analytical **SQL** queries (aggregations, joins, CASE, window functions) and
  designed a 3-page **Power BI** dashboard with KPI cards and an interactive correlation heatmap.

## 60-second pitch

> "In my project, CryptoDiversify, I asked a simple investor question: does holding several
> cryptocurrencies actually protect you? I collected six years of daily prices for six major
> coins through the Binance API, stored them in a SQLite database, and analyzed them in Python.
>
> I found three things. First, correlations jump from about 0.54 in normal times to 0.84 in
> crashes, so diversification weakens exactly when you need it. I used a block bootstrap to
> make sure this wasn't noise. Second, an equal-weighted basket is about 20% less volatile
> than a typical coin, but still riskier than just holding Bitcoin. Third, a Markowitz
> 'optimal' portfolio looked great on historical data but lost its advantage on 2025–26 data
> it hadn't seen. That's a classic overfitting lesson.
>
> I summarized everything in a Power BI dashboard where a manager can see the main message
> in 30 seconds."

## Likely interview questions (write your own answers in the blank lines)

**About the project**
1. Why did you choose this question?
   *Hint: practical investor question, uses your stats strength, not "predict the price".*
2. Walk me through your pipeline from data to dashboard.
3. Why log returns instead of prices?
   *Hint: prices share a trend, which causes spurious correlation. BNB–BTC was 0.89 on prices vs 0.67 on returns.*
4. How did you define the crash periods? Isn't that cherry-picking?
   *Hint: fixed from real events BEFORE looking at results. Limitation: the boundaries involve judgment.*
5. Why a block bootstrap and not a normal t-test or a plain bootstrap?
   *Hint: returns aren't independent (volatility clustering), and correlations aren't normally distributed.*
6. Could the higher correlation just be caused by higher volatility?
   *Hint: Forbes–Rigobon. In the 2026 crash volatility was actually LOWER (3.2% vs 5.1%), yet correlation was higher.*
7. What does a Sharpe ratio of −0.35 mean?
8. Why did the Markowitz portfolio fail out-of-sample?
   *Hint: expected returns are estimated with huge error. The optimizer piles into past winners (SOL, BNB).*
9. The optimized portfolio did worse, but the difference isn't significant. How do you report that honestly?
10. What would you do with more time?
    *Hint: more coins including dead ones, regime detection, DCC-GARCH, shrinkage.*

**About statistics and tools**
11. What is survivorship bias, and where does it appear in your project?
12. What's the difference between statistical significance and practical importance?
13. Explain a SQL window function you used.
14. How did you make the project reproducible?
    *Hint: `main.py` reruns everything, requirements pinned, fixed random seed.*
15. Did you use AI tools?
    *Honest answer: "Yes, as a tutor and pair-programmer. I made the design decisions, and I can explain and reproduce every step."*

## LinkedIn post (draft)

> 📊 **Does diversifying across crypto actually protect you?** I tested it.
>
> Using 6 years of daily data for BTC, ETH, SOL, BNB, XRP and DOGE, I found:
> 🔹 Correlation between coins jumps from 0.54 in calm markets to 0.84 in crashes, so
> diversification fails right when you need it (block-bootstrap 95% CI, p < 0.001).
> 🔹 An equal-weighted basket cuts volatility by ~20% vs a typical coin, but is still riskier than Bitcoin alone.
> 🔹 A Markowitz "optimal" portfolio looked great on past data and lost its edge on new data. A textbook overfitting lesson.
>
> Built with Python, SQL (SQLite) and Power BI. Code and dashboard on GitHub: [link]
>
> Research only, not financial advice.
> #DataAnalytics #Statistics #PowerBI #SQL #Python #Crypto
