-- ============================================
-- 02. Funnel Conversion by Segment (City & Device)
-- Advanced: combines multiple segment types, benchmarks each
-- segment against the overall conversion rate, and ranks them.
-- Question: Which cities/devices convert worse than average?
-- (Tests the "Android SDK bug" hypothesis from the project brief.)
-- ============================================

-- OUTPUT COLUMN MEANINGS:
-- segment_type            = which dimension this row belongs to ('City' or 'Device')
-- segment_value            = the actual city name or device type (Android/iOS)
-- total_sessions            = how many sessions came from users in this segment
-- orders_placed             = how many of those sessions ended in a placed order
-- conversion_pct            = % of this segment's sessions that converted (orders_placed / total_sessions)
-- overall_conversion_pct    = the platform-wide conversion rate, for comparison
-- pct_points_vs_overall     = how many percentage points this segment is above/below the overall rate
--                              (negative = underperforming, positive = outperforming)
-- rank_in_segment_type      = this segment's rank vs others of the SAME type (1 = best converting city,
--                              or 1 = best converting device) -- window function, not a global rank

WITH overall AS (
    SELECT
        COUNT(DISTINCT session_id) AS total_sessions,
        COUNT(DISTINCT CASE WHEN event_name = 'order_placed' THEN session_id END) AS total_orders
    FROM events
),
overall_rate AS (
    SELECT ROUND(total_orders * 100.0 / total_sessions, 2) AS overall_conversion_pct
    FROM overall
),
segments AS (
    SELECT
        'City' AS segment_type,
        u.city AS segment_value,
        COUNT(DISTINCT e.session_id) AS total_sessions,
        COUNT(DISTINCT CASE WHEN e.event_name = 'order_placed' THEN e.session_id END) AS orders_placed
    FROM events e
    JOIN users u ON e.user_id = u.user_id
    GROUP BY u.city

    UNION ALL

    SELECT
        'Device' AS segment_type,
        u.device_type AS segment_value,
        COUNT(DISTINCT e.session_id) AS total_sessions,
        COUNT(DISTINCT CASE WHEN e.event_name = 'order_placed' THEN e.session_id END) AS orders_placed
    FROM events e
    JOIN users u ON e.user_id = u.user_id
    GROUP BY u.device_type
)

SELECT
    segment_type,
    segment_value,
    total_sessions,
    orders_placed,
    ROUND(orders_placed * 100.0 / total_sessions, 2) AS conversion_pct,
    (SELECT overall_conversion_pct FROM overall_rate) AS overall_conversion_pct,
    ROUND(
        (orders_placed * 100.0 / total_sessions) - (SELECT overall_conversion_pct FROM overall_rate), 2
    ) AS pct_points_vs_overall,
    RANK() OVER (
        PARTITION BY segment_type
        ORDER BY orders_placed * 1.0 / total_sessions DESC
    ) AS rank_in_segment_type
FROM segments
ORDER BY segment_type, conversion_pct DESC;