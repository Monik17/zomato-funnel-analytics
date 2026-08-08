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


## 3. Coupon Effectiveness — Part A: Completion Rate
**File:** [`03_coupon_effectiveness.sql`](./03_coupon_effectiveness.sql)
**Question:** Does applying a coupon increase the chance a cart converts to an order?

| Coupon Applied  | Sessions with Cart | Sessions Completed | Completion % |
|-----------------|--------------------:|---------------------:|---------------:|
| Coupon Applied  | 9,740               | 7,200                | 73.92           |
| No Coupon       | 7,324               | 4,235                | 57.82           |

**Takeaway:** Applying a coupon lifts cart-to-order completion from 57.82% to 73.92% —
a ~16 percentage point (≈28% relative) increase. Unlike order value (which barely moves —
see Part B), coupons have a real, measurable effect on whether a cart converts at all.


## 3. Coupon Effectiveness — Part B: Cost & Net Revenue
**File:** [`03_coupon_effectiveness.sql`](./03_coupon_effectiveness.sql)
**Question:** What does the discount cost per order, and does it still pay off?

| Used Coupon  | Total Orders | Avg Order Value | Avg Discount Given | Avg Net Revenue | Delivered % |
|--------------|-------------:|------------------:|----------------------:|-------------------:|--------------:|
| Used Coupon  | 7,200        | 867.90             | 89.33                  | 805.72              | 96.88          |
| No Coupon    | 4,235        | 874.92             | 0.00                   | 910.97              | 96.79          |

**Combined verdict (Part A + Part B):** Coupons cost ₹89.33 per order on average, cutting
net revenue per order by ~11.6% (₹910.97 → ₹805.72). But because coupons lift cart-to-order
completion from 57.82% to 73.92% (Part A), they generate significantly more *orders* from
the same pool of carts. Modeling the counterfactual — the same 9,740 cart sessions converting
at the no-coupon rate instead — coupons produced an estimated **~₹670,600 more total revenue**
than not offering them, even after the discount cost. **Net verdict: coupons are worth it in
this dataset**, driven by volume, not order value. Delivered % is essentially unaffected either
way (96.88% vs 96.79%), so the extra volume isn't coming at the cost of order quality.



## 4. Payment Failure Analysis — Part A: By Method
**File:** [`04_payment_failure_analysis.sql`](./04_payment_failure_analysis.sql)
**Question:** Which payment method has the highest failure rate?

| Payment Method   | Total Attempts | Failed | Failure Rate % |
|------------------|----------------:|-------:|------------------:|
| Cash on Delivery | 601              | 83     | 13.81              |
| Wallet           | 1,541            | 203    | 13.17              |
| UPI              | 5,944            | 742    | 12.48              |
| Net Banking      | 1,072            | 131    | 12.22              |
| Credit Card      | 1,949            | 229    | 11.75              |
| Debit Card       | 1,934            | 218    | 11.27              |

**Takeaway:** Failure rates are fairly close across methods (11.27%–13.81%), with Cash on
Delivery and Wallet slightly higher than card-based methods. Not a dramatic outlier — the
gap (~2.5 pts) is modest, but if this were a real product, COD/Wallet would still be the
first place to investigate (e.g. wallet balance checks, COD order confirmation flow).



## 4. Payment Failure Analysis — Part B: By Order Value
**File:** [`04_payment_failure_analysis.sql`](./04_payment_failure_analysis.sql)
**Question:** Do bigger or smaller orders fail more often?

| Order Value Bucket | Total Attempts | Failed | Failure Rate % |
|---------------------|-----------------:|-------:|------------------:|
| Q1 (Lowest value)   | 3,261             | 407    | 12.48              |
| Q2                  | 3,260             | 392    | 12.02              |
| Q3                  | 3,260             | 398    | 12.21              |
| Q4 (Highest value)  | 3,260             | 409    | 12.55              |

**Takeaway:** Failure rate is flat (~12.0%–12.6%) across all order value quartiles — order
size has no meaningful effect on payment failure in this dataset. Combined with Part A,
this suggests payment failures here are close to random noise rather than driven by any
identifiable pattern (method or value) — consistent with how failures were generated
(a flat probability applied uniformly).



## 5. Delivery Delay vs Restaurant Rating — Part A: On-Time vs Delayed
**File:** [`05_delivery_rating_analysis.sql`](./05_delivery_rating_analysis.sql)
**Question:** Do delayed orders come from lower-rated restaurants?

| Delivery Status | Total Orders | Avg Restaurant Rating | Avg Delivery Time (min) |
|------------------|---------------:|-------------------------:|----------------------------:|
| On Time          | 8,373          | 4.23                      | 35.3                         |
| Delayed          | 2,701          | 4.21                      | 63.0                         |

**Takeaway:** No meaningful difference in rating between on-time and delayed orders
(4.23 vs 4.21). This is expected given the schema: `rating` is a static, restaurant-level
attribute rather than a per-order rating, so it can't reflect how a customer felt about
*this specific* delivery. A production dataset would need a per-order rating field to
properly test whether delays hurt customer satisfaction — worth noting as a schema
limitation rather than treating this as evidence delays don't matter.