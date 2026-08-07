-- ============================================
-- 03. Coupon Effectiveness
-- Advanced: two-part analysis using conditional aggregation.
-- Question A: Does applying a coupon increase completion rate
--             (cart -> order), not just order value?
-- Question B: What does the discount actually cost the business
--             per order, and is it worth it?
-- ============================================

-- OUTPUT COLUMN MEANINGS (Part A):
-- coupon_applied         = whether the session applied a coupon after adding to cart
-- sessions_with_cart      = sessions that reached 'add_to_cart' in this group
-- sessions_completed       = of those, how many went all the way to 'order_placed'
-- completion_pct           = % of cart sessions that converted to an order (the real "lift" metric)

WITH cart_sessions AS (
    SELECT DISTINCT session_id
    FROM events
    WHERE event_name = 'add_to_cart'
),
coupon_sessions AS (
    SELECT DISTINCT session_id
    FROM events
    WHERE event_name = 'apply_coupon'
),
completed_sessions AS (
    SELECT DISTINCT session_id
    FROM events
    WHERE event_name = 'order_placed'
)
SELECT
    CASE WHEN cs.session_id IN (SELECT session_id FROM coupon_sessions)
         THEN 'Coupon Applied' ELSE 'No Coupon' END AS coupon_applied,
    COUNT(DISTINCT cs.session_id) AS sessions_with_cart,
    COUNT(DISTINCT CASE WHEN cs.session_id IN (SELECT session_id FROM completed_sessions)
                         THEN cs.session_id END) AS sessions_completed,
    ROUND(
        COUNT(DISTINCT CASE WHEN cs.session_id IN (SELECT session_id FROM completed_sessions)
                             THEN cs.session_id END) * 100.0 / COUNT(DISTINCT cs.session_id), 2
    ) AS completion_pct
FROM cart_sessions cs
GROUP BY coupon_applied;




-- OUTPUT COLUMN MEANINGS (Part B):
-- used_coupon          = whether this successful order had a discount applied
-- total_orders          = number of successful orders in this group
-- avg_order_value        = average cart value before fees/discount
-- avg_discount_given      = average ₹ discount given per order (business cost)
-- avg_net_revenue         = what the business actually nets per order (order_value + delivery_fee - discount)
-- delivered_pct            = % of these orders that were actually delivered (not cancelled)

SELECT
    CASE WHEN coupon_discount > 0 THEN 'Used Coupon' ELSE 'No Coupon' END AS used_coupon,
    COUNT(*) AS total_orders,
    ROUND(AVG(order_value), 2) AS avg_order_value,
    ROUND(AVG(coupon_discount), 2) AS avg_discount_given,
    ROUND(AVG(order_value + delivery_fee - coupon_discount), 2) AS avg_net_revenue,
    ROUND(
        SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS delivered_pct
FROM orders
WHERE payment_status = 'Success'
GROUP BY used_coupon;