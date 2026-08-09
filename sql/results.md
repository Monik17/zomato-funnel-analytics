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



## 5. Delivery Delay vs Restaurant Rating — Part B: Restaurant-Level Delay Ranking
**File:** [`05_delivery_rating_analysis.sql`](./05_delivery_rating_analysis.sql)
**Question:** Which restaurants delay most often, and are they lower-rated?

| Restaurant ID | Restaurant Name    | Rating | Total Delivered | Delayed | Delay Rate % |
|---------------:|---------------------|--------:|-------------------:|---------:|----------------:|
| 208             | Classic Bistro       | 3.8     | 18                  | 13       | 72.22            |
| 483             | Burger King          | 4.4     | 10                  | 7        | 70.00            |
| 581             | Golden Restaurant    | 3.8     | 13                  | 8        | 61.54            |
| 318             | Giani's              | 3.8     | 12                  | 7        | 58.33            |
| 249             | Gupta Dhaba          | 3.5     | 13                  | 7        | 53.85            |
| 378             | Giani's              | 3.9     | 15                  | 8        | 53.33            |
| 569             | Sharma Restaurant    | 3.3     | 21                  | 11       | 52.38            |
| 332             | Faasos               | 4.7     | 14                  | 7        | 50.00            |
| 516             | Bombay Restaurant    | 3.7     | 19                  | 9        | 47.37            |
| 434             | Oven Story Pizza     | 4.1     | 19                  | 9        | 47.37            |
| 282             | Indori Bistro        | 3.5     | 11                  | 5        | 45.45            |
| 523             | Desi House           | 3.7     | 20                  | 9        | 45.00            |
| 27              | Starbucks            | 4.1     | 20                  | 9        | 45.00            |
| 549             | Delhi Restaurant     | 4.2     | 18                  | 8        | 44.44            |
| 288             | Taste of Dhaba       | 4.3     | 16                  | 7        | 43.75            |
| 235             | Sharma Dhaba         | 4.3     | 21                  | 9        | 42.86            |
| 489             | Haldiram's           | 4.1     | 21                  | 9        | 42.86            |
| 260             | Desi House           | 4.1     | 14                  | 6        | 42.86            |
| 555             | Classic Express      | 3.6     | 14                  | 6        | 42.86            |
| 74              | Oven Story Pizza     | 3.9     | 19                  | 8        | 42.11            |

**Takeaway:** The top-20 highest-delay restaurants span ratings from 3.3 to 4.7, with no
pattern toward lower-rated restaurants — well-rated chains like Burger King (4.4) and
Faasos (4.7) appear alongside lower-rated ones. This confirms Part A: delay rate and
`rating` are unrelated in this dataset, consistent with `rating` being a static field
unaffected by individual order outcomes.



## 6. Reorder / Repeat Purchase — Part A: Overall
**File:** [`06_reorder_analysis.sql`](./06_reorder_analysis.sql)
**Question:** What % of customers who order once come back and order again?

| Total Customers | Repeat Customers | Repeat Rate % |
|-------------------:|---------------------:|------------------:|
| 4,535               | 3,352                 | 73.91              |

**Takeaway:** 73.91% of customers who placed a successful order went on to order again.
This is high relative to real-world food delivery benchmarks — largely a byproduct of the
generator's volume (13K orders spread across just 5K users over 6 months, ~2.6 orders/user
on average), not necessarily evidence of strong product stickiness. Still useful as a
baseline to compare premium vs regular segments against (Part B).


## 6. Reorder / Repeat Purchase — Part B: Premium vs Regular
**File:** [`06_reorder_analysis.sql`](./06_reorder_analysis.sql)
**Question:** Do premium users reorder more than regular users?

| User Type | Total Customers | Repeat Customers | Repeat Rate % | Avg Orders/Customer |
|-----------|-------------------:|---------------------:|------------------:|------------------------:|
| Regular   | 3,618               | 2,678                 | 74.02              | 2.53                     |
| Premium   | 917                 | 674                   | 73.50              | 2.49                     |

**Takeaway:** No meaningful difference between premium and regular users (74.02% vs 73.50%
repeat rate, 2.53 vs 2.49 avg orders). Expected given the schema/generator — `is_premium`
was assigned as an independent random flag at signup, not tied to actual ordering behavior,
so there was never a real mechanism for premium status to drive more frequent ordering in
this synthetic dataset. In a real product, you'd expect premium (e.g. free delivery, faster
support) to show a genuine lift here.