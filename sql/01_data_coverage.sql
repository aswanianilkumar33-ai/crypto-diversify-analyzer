-- 01 Data coverage: does every coin have the same date range and number of days?
-- Why: before any analysis, check for gaps. Unequal counts would mean missing days.
SELECT coin,
       MIN(date)  AS first_day,
       MAX(date)  AS last_day,
       COUNT(*)   AS n_days
FROM prices
GROUP BY coin
ORDER BY coin;
