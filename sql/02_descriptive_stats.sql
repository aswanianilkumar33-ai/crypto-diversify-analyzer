-- 02 Descriptive statistics of daily log returns per coin (GROUP BY + aggregates).
-- SQLite has no STDEV function, so we use Var(X) = E[X^2] - (E[X])^2 and take the square root.
-- Multiply by 100 to show percent.
SELECT coin,
       COUNT(*)                                                        AS n_days,
       ROUND(AVG(log_return) * 100, 3)                                 AS mean_daily_pct,
       ROUND(SQRT(AVG(log_return * log_return) - AVG(log_return) * AVG(log_return)) * 100, 2)
                                                                       AS sd_daily_pct,
       ROUND(MIN(log_return) * 100, 1)                                 AS worst_day_pct,
       ROUND(MAX(log_return) * 100, 1)                                 AS best_day_pct
FROM returns
GROUP BY coin
ORDER BY sd_daily_pct DESC;
