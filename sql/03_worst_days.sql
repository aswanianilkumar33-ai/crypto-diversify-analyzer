-- 03 The 10 worst single days across all coins (ORDER BY + LIMIT).
-- Why: the biggest crashes show which events drive the tails of the distribution.
SELECT date,
       coin,
       ROUND(log_return * 100, 1) AS log_return_pct
FROM returns
ORDER BY log_return ASC
LIMIT 10;
