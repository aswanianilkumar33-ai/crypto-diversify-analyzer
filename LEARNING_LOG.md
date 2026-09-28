# LEARNING LOG

## Earlier sessions (reconstructed from Git history, 2026-09-26/27)
- **Built:** project brief; Python practice; Binance data download; SQLite database;
  EDA and analysis notebooks (correlation by period, volatility, Markowitz).
- **Decisions:** switched to "build first, explain after" mode; errors explained all at once.

## 2026-09-28: Power BI dashboard + project completion
**What we built**
- 3-page Power BI dashboard: Overview (KPI cards, growth of $100 on a log scale), Crash
  Correlation (bar chart + heatmap with a period slicer), Portfolio Results.
- Custom theme and a professional layout: navy header, key-finding cards, footer.
- `src/load_to_db.py`, `main.py` (whole pipeline in one command), `src/significance.py`
  (block-bootstrap CIs), 8 SQL queries, README, final report, CAREER.md.

**Concepts learned**
- Data model = several tables loaded side by side. Long vs wide format (Power BI prefers long).
- Formatting changes only how a number is *displayed*, not the value (Sharpe must not be a %).
- Aggregation matters: Sum vs Average vs Count. A text column gets *counted*, so every bar showed 1.
- `table[column]` notation. Slicer = on-page filter using a category column.
- KPI card = one big headline number. Footer = source and disclaimer line.
- Date hierarchy vs plain date. Log scale = equal distances mean equal % changes.
- Block bootstrap: resample blocks of days to keep volatility clustering.

**Questions she asked**
- "Did you mean correlation_by_period[correlation]?" (slicer needs the category `period`)
- "What is KPI cards?" / "What is the footer part?"
- Why data labels showed 1 for every bar (rounding / count).

**Results to remember**
- Correlation 0.54 calm → 0.76 (2022) → 0.84 (2026); CIs exclude 0.
- Equal-weighted volatility is 19 points below the average coin but 15 points above BTC.
- Optimized portfolio's out-of-sample Sharpe −0.35 vs −0.34 EW; the difference is not significant.

**Still to practise**
- Explaining `significance.py` and the SQL window function (query 07) in her own words.
- Writing CAREER.md interview answers herself.

**Next step:** 5-minute mock interview: present the project and defend each method.
