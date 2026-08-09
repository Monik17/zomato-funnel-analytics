-- ============================================
-- 08. GMV & Orders Trend Over Time (Daily)
-- Powers a time-series line chart in the dashboard.
-- ============================================

-- COLUMN MEANINGS:
-- order_date       = the calendar date
-- total_orders       = number of successful orders placed that day
-- gmv                  = Gross Merchandise Value = total order_value that day (before fees/discounts)
-- net_revenue           = actual revenue after delivery fee and coupon discount
-- avg_order_value        = average order size that day

SELECT
    DATE(order_time) AS order_date,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_value), 2) AS gmv,
    ROUND(SUM(order_value + delivery_fee - coupon_discount), 2) AS net_revenue,
    ROUND(AVG(order_value), 2) AS avg_order_value
FROM orders
WHERE payment_status = 'Success'
GROUP BY DATE(order_time)
ORDER BY order_date;