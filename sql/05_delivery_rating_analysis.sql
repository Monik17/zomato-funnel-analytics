-- ============================================
-- 05. Delivery Delay vs Restaurant Rating
-- Note: orders has no per-order rating column, so this uses each
-- restaurant's overall `rating` as a proxy instead.
-- Question: Do restaurants with more delayed deliveries have
-- lower overall ratings?
-- ============================================

-- OUTPUT COLUMN MEANINGS:
-- delivery_status         = 'On Time' if actual time <= restaurant's avg_delivery_time, else 'Delayed'
-- total_orders              = number of delivered orders in this group
-- avg_restaurant_rating       = average listed rating of the restaurant these orders came from
-- avg_delivery_time_min        = average actual delivery time in minutes for this group

SELECT
    CASE
        WHEN o.delivery_time_minutes <= r.avg_delivery_time THEN 'On Time'
        ELSE 'Delayed'
    END AS delivery_status,
    COUNT(*) AS total_orders,
    ROUND(AVG(r.rating), 2) AS avg_restaurant_rating,
    ROUND(AVG(o.delivery_time_minutes), 1) AS avg_delivery_time_min
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY delivery_status;