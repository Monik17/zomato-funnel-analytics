-- ============================================
-- 01. Funnel Conversion Analysis
-- Stage-by-stage counts and drop-off %
-- ============================================

WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event_name = 'app_open'        THEN session_id END) AS home,
        COUNT(DISTINCT CASE WHEN event_name = 'restaurant_view' THEN session_id END) AS restaurant_view,
        COUNT(DISTINCT CASE WHEN event_name = 'menu_view'       THEN session_id END) AS menu_view,
        COUNT(DISTINCT CASE WHEN event_name = 'add_to_cart'     THEN session_id END) AS add_to_cart,
        COUNT(DISTINCT CASE WHEN event_name = 'checkout_start'  THEN session_id END) AS checkout_start,
        COUNT(DISTINCT CASE WHEN event_name = 'payment_attempt' THEN session_id END) AS payment_attempt,
        COUNT(DISTINCT CASE WHEN event_name = 'order_placed'    THEN session_id END) AS order_placed
    FROM events
)


-- stage         = name of the funnel step
-- sessions      = number of sessions that reached this stage
-- pct_of_start  = % of the original 50,000 sessions (Home) that made it this far
-- drop_off_pct  = % that dropped off since the PREVIOUS stage (shows where the leak is)


SELECT 'Home' AS stage, home AS sessions,
       100.0 AS pct_of_start,
       NULL AS drop_off_pct
FROM funnel

UNION ALL
SELECT 'Restaurant View', restaurant_view,
       ROUND(restaurant_view * 100.0 / home, 2),
       ROUND(100 - (restaurant_view * 100.0 / home), 2)
FROM funnel

UNION ALL
SELECT 'Menu View', menu_view,
       ROUND(menu_view * 100.0 / home, 2),
       ROUND(100 - (menu_view * 100.0 / restaurant_view), 2)
FROM funnel

UNION ALL
SELECT 'Add to Cart', add_to_cart,
       ROUND(add_to_cart * 100.0 / home, 2),
       ROUND(100 - (add_to_cart * 100.0 / menu_view), 2)
FROM funnel

UNION ALL
SELECT 'Checkout Start', checkout_start,
       ROUND(checkout_start * 100.0 / home, 2),
       ROUND(100 - (checkout_start * 100.0 / add_to_cart), 2)
FROM funnel

UNION ALL
SELECT 'Payment Attempt', payment_attempt,
       ROUND(payment_attempt * 100.0 / home, 2),
       ROUND(100 - (payment_attempt * 100.0 / checkout_start), 2)
FROM funnel

UNION ALL
SELECT 'Order Placed', order_placed,
       ROUND(order_placed * 100.0 / home, 2),
       ROUND(100 - (order_placed * 100.0 / payment_attempt), 2)
FROM funnel;