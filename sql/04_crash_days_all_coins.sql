-- 04 Days when ALL six coins fell more than 5% together (GROUP BY + HAVING).
-- Why: "everything falls at once" is exactly the failure of diversification (RQ1).
SELECT date,
       COUNT(*)                          AS coins_down_5pct,
       ROUND(AVG(log_return) * 100, 1)   AS avg_return_pct
FROM returns
WHERE log_return < -0.05
GROUP BY date
HAVING COUNT(*) = 6
ORDER BY avg_return_pct;
