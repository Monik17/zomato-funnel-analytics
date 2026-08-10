-- ============================================
-- 09. Revenue by City
-- Question: Which cities generate the most GMV and net revenue?
-- (Complements Query 2, which looked at conversion % by city --
-- this looks at actual revenue, since a lower-converting city
-- could still generate more revenue if it has more/bigger orders.)
-- ============================================

-- COLUMN MEANINGS:
-- user_city            = city of the customer who placed the order
-- total_orders            = number of successful orders from this city
-- gmv                       = total order_value (before fees/discounts)
-- net_revenue                = order_value + delivery_fee - coupon_discount
-- avg_order_value              = average order size for this city
-- pct_of_total_gmv               = this city's share of overall GMV

SELECT
    u.city AS user_city,
    COUNT(*) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS gmv,
    ROUND(SUM(o.order_value + o.delivery_fee - o.coupon_discount), 2) AS net_revenue,
    ROUND(AVG(o.order_value), 2) AS avg_order_value,
    ROUND(SUM(o.order_value) * 100.0 / SUM(SUM(o.order_value)) OVER (), 2) AS pct_of_total_gmv
FROM orders o
JOIN users u ON o.user_id = u.user_id
WHERE o.payment_status = 'Success'
GROUP BY u.city
ORDER BY gmv DESC;