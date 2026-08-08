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



-- ============================================
-- 05B. Restaurant-Level Delay Rate vs Rating
-- Question: Do restaurants that delay more often have lower ratings?
-- ============================================

-- OUTPUT COLUMN MEANINGS:
-- restaurant_id / restaurant_name = the restaurant
-- rating                            = its listed rating
-- total_delivered                    = how many delivered orders it has
-- delayed_orders                      = how many of those were delayed
-- delay_rate_pct                       = % of its orders that were delayed

SELECT
    r.restaurant_id,
    r.restaurant_name,
    r.rating,
    COUNT(*) AS total_delivered,
    SUM(CASE WHEN o.delivery_time_minutes > r.avg_delivery_time THEN 1 ELSE 0 END) AS delayed_orders,
    ROUND(
        SUM(CASE WHEN o.delivery_time_minutes > r.avg_delivery_time THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS delay_rate_pct
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.restaurant_id, r.restaurant_name, r.rating
HAVING COUNT(*) >= 10   -- ignore restaurants with too few orders to be meaningful
ORDER BY delay_rate_pct DESC
LIMIT 20;