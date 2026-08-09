-- ============================================
-- 06. Reorder / Repeat Purchase Analysis
-- Question: What % of users who order once come back and order
-- again? Does this differ for premium vs regular users?
-- ============================================

-- OUTPUT COLUMN MEANINGS (Part A - Overall):
-- total_customers       = users who placed at least one successful order
-- repeat_customers        = users who placed 2 or more successful orders
-- repeat_rate_pct           = % of customers who came back for a second order

WITH customer_order_counts AS (
    SELECT
        user_id,
        COUNT(*) AS order_count
    FROM orders
    WHERE payment_status = 'Success'
    GROUP BY user_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS repeat_rate_pct
FROM customer_order_counts;



-- OUTPUT COLUMN MEANINGS (Part B - Premium vs Regular):
-- is_premium         = whether the user is a premium member
-- total_customers      = users of this type who placed at least one successful order
-- repeat_customers       = of those, how many placed 2+ orders
-- repeat_rate_pct          = % who reordered
-- avg_orders_per_customer   = average number of orders placed by users of this type

WITH customer_order_counts AS (
    SELECT
        o.user_id,
        u.is_premium,
        COUNT(*) AS order_count
    FROM orders o
    JOIN users u ON o.user_id = u.user_id
    WHERE o.payment_status = 'Success'
    GROUP BY o.user_id, u.is_premium
)
SELECT
    CASE WHEN is_premium = 1 THEN 'Premium' ELSE 'Regular' END AS is_premium,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS repeat_rate_pct,
    ROUND(AVG(order_count), 2) AS avg_orders_per_customer
FROM customer_order_counts
GROUP BY is_premium;