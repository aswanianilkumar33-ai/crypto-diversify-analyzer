-- 05 Average return and volatility per market period (CASE WHEN to label periods).
-- Periods are defined in advance from real events (see PROJECT_BRIEF.md):
--   crash_2022 = 2022-05-01 to 2022-12-31 (Terra/Luna, FTX)
--   crash_2026 = 2026-01-01 to 2026-06-30 (war + Fed-driven decline)
WITH labelled AS (
    SELECT *,
           CASE
               WHEN date BETWEEN '2022-05-01' AND '2022-12-31' THEN 'crash_2022'
               WHEN date BETWEEN '2026-01-01' AND '2026-06-30' THEN 'crash_2026'
               ELSE 'calm'
           END AS period
    FROM returns
)
SELECT period,
       COUNT(DISTINCT date)                                             AS n_days,
       ROUND(AVG(log_return) * 100, 3)                                  AS mean_daily_pct,
       ROUND(SQRT(AVG(log_return * log_return) - AVG(log_return) * AVG(log_return)) * 100, 2)
                                                                        AS sd_daily_pct
FROM labelled
GROUP BY period
ORDER BY sd_daily_pct DESC;
