-- 07 30-day rolling volatility of BTC (window function).
-- AVG(...) OVER (... ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) = moving average over 30 days.
-- Shows the most recent 10 days; annualized with sqrt(365), in percent.
WITH w AS (
    SELECT date,
           AVG(log_return)              OVER win AS m,
           AVG(log_return * log_return) OVER win AS m2
    FROM returns
    WHERE coin = 'BTC'
    WINDOW win AS (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
)
SELECT date,
       ROUND(SQRT(m2 - m * m) * SQRT(365) * 100, 1) AS rolling_30d_vol_annual_pct
FROM w
ORDER BY date DESC
LIMIT 10;
