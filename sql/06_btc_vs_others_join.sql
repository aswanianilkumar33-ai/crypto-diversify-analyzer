-- 06 How often does each coin move in the same direction as Bitcoin on the same day? (self-JOIN)
-- Why: a simple, non-parametric view of co-movement that complements correlation.
SELECT o.coin,
       COUNT(*)                                                                       AS n_days,
       ROUND(100.0 * SUM(CASE WHEN (o.log_return > 0) = (b.log_return > 0) THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                                      AS same_direction_pct
FROM returns AS o
JOIN returns AS b
  ON o.date = b.date
 AND b.coin = 'BTC'
WHERE o.coin <> 'BTC'
GROUP BY o.coin
ORDER BY same_direction_pct DESC;
