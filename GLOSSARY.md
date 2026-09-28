# GLOSSARY

| Term | Simple meaning | Tiny example |
|---|---|---|
| API | A "waiter" program that takes your request to a server and brings data back | Binance API returns daily prices |
| JSON | Text format for data, like a nested dictionary | `{"coin": "BTC", "close": 29331.69}` |
| DataFrame | A table in pandas, like the data matrix X in regression | rows = days, columns = coins |
| CSV | Plain-text table, values separated by commas | `date,coin,close_price` |
| SQLite database | One file holding several related tables you query with SQL | `data/project.db` |
| Primary key | Column(s) that uniquely identify a row | (date, coin) |
| GROUP BY | Split rows into groups, then summarise each | average return per coin |
| JOIN | Combine rows from two tables that match on a key | each coin's return next to BTC's on the same date |
| Window function | Calculation over a moving set of rows without collapsing them | 30-day rolling volatility |
| Log return | `ln(P_t / P_{t-1})`; adds up over time | +10% then −10% ≠ 0 in simple returns |
| Annualized volatility | Daily std dev × √365 | 3% daily ≈ 57% per year |
| Correlation (Pearson) | How closely two returns move together, −1 to 1 | BTC–ETH 0.82 |
| Sharpe ratio | Return per unit of risk (return ÷ volatility); no units | 0.76 |
| Markowitz optimization | Choosing weights that give the best return-for-risk on past data | 48% SOL, 34% BNB… |
| In-sample / out-of-sample | Data the model was fitted on / new data it never saw | 2021–24 / 2025–26 |
| Overfitting | A model fits the past very well but fails on new data | optimal weights lose their edge |
| Look-ahead bias | Accidentally using future information in a past decision | fitting weights on 2026 data to "invest" in 2025 |
| Survivorship bias | Studying only the winners that survived | our 6 coins all still exist |
| Bootstrap | Resampling your data many times to see how much an estimate varies | 2,000 resamples → 95% CI |
| Block bootstrap | Bootstrap that resamples runs of consecutive days | 20-day blocks keep volatility clustering |
| Virtual environment (.venv) | A separate "lab" with this project's own Python packages | `.venv\Scripts\activate` |
| Git commit | A saved snapshot of the project with a message | "EDA and analysis notebooks" |
| Power BI data model | All tables loaded into a report, possibly linked | 7 CSV tables |
| Long vs wide format | One row per observation vs one column per variable | `coin_1, coin_2, correlation` vs a matrix |
| Slicer | On-page filter buttons in Power BI | pick "crash_2026" |
| KPI card | One big headline number on a dashboard | 0.84 |
| Theme (Power BI) | A JSON file of colours and fonts applied to every visual | `cryptodiversify_theme.json` |
| Log scale | Axis where equal distances mean equal % changes | 100 → 1,000 → 10,000 evenly spaced |
