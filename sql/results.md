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