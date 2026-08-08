-- ============================================
-- 04. Payment Failure Analysis - Part A
-- Question: Which payment method has the highest failure rate?
-- (Note: failure_reason wasn't captured at generation time,
-- so this looks at rate by method only.)
-- ============================================

-- OUTPUT COLUMN MEANINGS:
-- payment_method   = the payment method used
-- total_attempts     = all payment attempts (success + failed) with this method
-- failed_attempts      = how many of those failed
-- failure_rate_pct      = % that failed for this method

SELECT
    payment_method,
    COUNT(*) AS total_attempts,
    SUM(CASE WHEN payment_status = 'Failed' THEN 1 ELSE 0 END) AS failed_attempts,
    ROUND(SUM(CASE WHEN payment_status = 'Failed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_rate_pct
FROM orders
GROUP BY payment_method
ORDER BY failure_rate_pct DESC;




-- ============================================
-- 04. Payment Failure Analysis - Part B
-- Question: Do bigger or smaller orders fail more often?
-- ============================================

WITH bucketed AS (
    SELECT
        order_value,
        payment_status,
        NTILE(4) OVER (ORDER BY order_value) AS value_quartile
    FROM orders
)
SELECT
    CASE value_quartile
        WHEN 1 THEN 'Q1 (Lowest value)'
        WHEN 2 THEN 'Q2'
        WHEN 3 THEN 'Q3'
        WHEN 4 THEN 'Q4 (Highest value)'
    END AS order_value_bucket,
    COUNT(*) AS total_attempts,
    SUM(CASE WHEN payment_status = 'Failed' THEN 1 ELSE 0 END) AS failed_attempts,
    ROUND(SUM(CASE WHEN payment_status = 'Failed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_rate_pct
FROM bucketed
GROUP BY value_quartile
ORDER BY value_quartile;