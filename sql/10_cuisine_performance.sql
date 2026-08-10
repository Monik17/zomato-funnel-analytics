-- ============================================
-- 10. Cuisine Performance
-- Question: Which cuisines drive the most orders/revenue, and
-- which have the worst delivery reliability?
-- ============================================

-- COLUMN MEANINGS:
-- cuisine               = restaurant cuisine type
-- total_restaurants        = number of restaurants of this cuisine
-- total_orders                = number of successful orders across all restaurants of this cuisine
-- gmv                            = total order_value for this cuisine
-- avg_order_value                  = average order size for this cuisine
-- delayed_pct                        = % of delivered orders that were delayed
-- avg_restaurant_rating                = average rating across restaurants of this cuisine

SELECT
    r.cuisine,
    COUNT(DISTINCT r.restaurant_id) AS total_restaurants,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS gmv,
    ROUND(AVG(o.order_value), 2) AS avg_order_value,
    ROUND(
        SUM(CASE WHEN o.order_status = 'Delivered' AND o.delivery_time_minutes > r.avg_delivery_time
                  THEN 1 ELSE 0 END) * 100.0
        / NULLIF(SUM(CASE WHEN o.order_status = 'Delivered' THEN 1 ELSE 0 END), 0), 2
    ) AS delayed_pct,
    ROUND(AVG(r.rating), 2) AS avg_restaurant_rating
FROM restaurants r
LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id AND o.payment_status = 'Success'
GROUP BY r.cuisine
ORDER BY gmv DESC;