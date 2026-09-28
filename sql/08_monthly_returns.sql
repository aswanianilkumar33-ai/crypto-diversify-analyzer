-- 08 Monthly return per coin (sum of daily log returns = log return for the month).
-- Why: log returns add up over time; this turns daily data into a monthly table for reports.
-- Shows the 12 most recent months for BTC and SOL; exp(x) - 1 converts back to a simple return.
SELECT substr(date, 1, 7)                          AS month,
       coin,
       ROUND((EXP(SUM(log_return)) - 1) * 100, 1)  AS monthly_return_pct
FROM returns
WHERE coin IN ('BTC', 'SOL')
GROUP BY month, coin
ORDER BY month DESC, coin
LIMIT 24;
