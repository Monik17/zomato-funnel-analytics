-- ============================================
-- 07. Dashboard Master View
-- A single flattened table combining orders + users + restaurants,
-- so Power BI can filter/slice by any dimension (city, cuisine,
-- device, premium status, etc.) without needing a separate query
-- for every possible breakdown.
-- ============================================

-- COLUMN MEANINGS:
-- net_revenue        = order_value + delivery_fee - coupon_discount (actual revenue earned)
-- user_city            = city of the customer who placed the order
-- restaurant_city        = city where the restaurant is located
-- delivery_status         = 'Delayed' if actual time exceeded the restaurant's avg_delivery_time
-- coupon_used              = whether this order used a coupon

CREATE OR REPLACE VIEW vw_orders_master AS
SELECT
    o.order_id,
    o.order_time,
    DATE(o.order_time) AS order_date,
    o.order_value,
    o.delivery_fee,
    o.coupon_discount,
    (o.order_value + o.delivery_fee - o.coupon_discount) AS net_revenue,
    o.payment_method,
    o.payment_status,
    o.order_status,
    o.delivery_time_minutes,
    u.user_id,
    u.gender,
    u.age,
    u.city AS user_city,
    u.is_premium,
    u.device_type,
    u.signup_date,
    r.restaurant_id,
    r.restaurant_name,
    r.city AS restaurant_city,
    r.cuisine,
    r.rating AS restaurant_rating,
    r.avg_delivery_time,
    CASE
        WHEN o.delivery_time_minutes > r.avg_delivery_time THEN 'Delayed'
        WHEN o.delivery_time_minutes IS NULL THEN NULL
        ELSE 'On Time'
    END AS delivery_status,
    CASE WHEN o.coupon_discount > 0 THEN 'Coupon Used' ELSE 'No Coupon' END AS coupon_used
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id;


SELECT * FROM vw_orders_master LIMIT 10;