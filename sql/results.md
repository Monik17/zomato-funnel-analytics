# SQL Analysis — Zomato Funnel Analytics

Each section links a business question to its query file and results.

---

## 1. Funnel Conversion Analysis
**File:** [`01_funnel_conversion.sql`](./01_funnel_conversion.sql)
**Question:** Where in the ordering journey do users drop off the most?

| Stage           | Sessions | % of Start | Drop-off % |
|-----------------|---------:|-----------:|-----------:|
| Home            | 50,000   | 100.00     | —          |
| Restaurant View | 37,571   | 75.14      | 24.86      |
| Menu View       | 30,920   | 61.84      | 17.70      |
| Add to Cart     | 17,064   | 34.13      | 44.81      |
| Checkout Start  | 14,294   | 28.59      | 16.23      |
| Payment Attempt | 13,041   | 26.08      | 8.77       |
| Order Placed    | 11,435   | 22.87      | 12.32      |

**Takeaway:** The biggest leak is **Menu View → Add to Cart (44.81% drop)** — nearly
half of users who open a menu never add an item to their cart. This is the
highest-leverage stage to investigate first — e.g. menu UX, item photos, load time,
or price/portion visibility.




## 2. Segment Conversion — City & Device
**File:** [`02_segment_conversion.sql`](./02_segment_conversion.sql)
**Question:** Which cities/devices convert worse than average? (Tests the "Android SDK bug" hypothesis.)

| Segment Type | Value      | Sessions | Orders | Conversion % | Overall % | vs Overall (pts) | Rank |
|--------------|------------|---------:|-------:|--------------:|----------:|------------------:|-----:|
| City         | Ahmedabad  | 4,937    | 1,163  | 23.56          | 22.87     | +0.69              | 1    |
| City         | Bangalore  | 4,902    | 1,148  | 23.42          | 22.87     | +0.55              | 2    |
| City         | Indore     | 4,620    | 1,072  | 23.20          | 22.87     | +0.33              | 3    |
| City         | Jaipur     | 5,281    | 1,208  | 22.87          | 22.87     | 0.00               | 4    |
| City         | Pune       | 5,260    | 1,203  | 22.87          | 22.87     | 0.00               | 5    |
| City         | Mumbai     | 5,827    | 1,325  | 22.74          | 22.87     | -0.13              | 6    |
| City         | Hyderabad  | 4,550    | 1,030  | 22.64          | 22.87     | -0.23              | 7    |
| City         | Kolkata    | 4,900    | 1,109  | 22.63          | 22.87     | -0.24              | 8    |
| City         | Delhi      | 4,974    | 1,118  | 22.48          | 22.87     | -0.39              | 9    |
| City         | Chennai    | 4,749    | 1,059  | 22.30          | 22.87     | -0.57              | 10   |
| Device       | Android    | 25,447   | 5,854  | 23.00          | 22.87     | +0.13              | 1    |
| Device       | iOS        | 24,553   | 5,581  | 22.73          | 22.87     | -0.14              | 2    |

**Takeaway:** Conversion is essentially flat across both city (22.3%–23.6%) and device
(22.7%–23.0%) — a spread of ~1 percentage point, well within normal variation. This
**rules out** the hypothesis of an Android-specific conversion issue in this dataset.
No city or device shows a meaningfully underperforming funnel.