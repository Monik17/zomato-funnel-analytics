import os
import random
from datetime import timedelta

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "localhost")
PORT = int(os.getenv("DB_PORT", 3306))
DATABASE = os.getenv("DB_NAME")

engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# ==========================
# Load reference data
# ==========================
payment_attempts = pd.read_sql(
    "SELECT session_id, user_id, restaurant_id, event_time, payment_method "
    "FROM events WHERE event_name = 'payment_attempt'",
    con=engine
)

coupons_used = pd.read_sql(
    "SELECT session_id, coupon_code FROM events WHERE event_name = 'apply_coupon'",
    con=engine
)

restaurants_df = pd.read_sql(
    "SELECT restaurant_id, delivery_fee, avg_delivery_time FROM restaurants",
    con=engine
).set_index("restaurant_id")

menu_items_df = pd.read_sql("SELECT item_id, restaurant_id, price FROM menu_items", con=engine)
menu_by_restaurant = {
    rid: grp[["item_id", "price"]].to_dict("records")
    for rid, grp in menu_items_df.groupby("restaurant_id")
}

# Attach coupon_code to each payment attempt (None if no coupon was applied)
payment_attempts = payment_attempts.merge(coupons_used, on="session_id", how="left")

with engine.connect() as conn:
    next_order_id = conn.execute(text("SELECT COALESCE(MAX(order_id),0)+1 FROM orders")).scalar()

# ==========================
# Config
# ==========================
P_PAYMENT_SUCCESS = 0.88
P_POST_PAYMENT_CANCEL = 0.03
P_DELAYED = 0.25

PAYMENT_FAILURE_REASONS = [
    "Insufficient Balance", "Bank Server Down", "OTP Timeout",
    "Card Declined", "Network Issue"
]

orders_rows = []
order_items_rows = []
order_id_counter = next_order_id

for _, attempt in payment_attempts.iterrows():
    restaurant_id = int(attempt["restaurant_id"])
    if restaurant_id not in menu_by_restaurant:
        continue

    available_items = menu_by_restaurant[restaurant_id]
    k = min(random.randint(1, 4), len(available_items))
    cart_items = random.sample(available_items, k=k)
    cart_quantities = [random.randint(1, 3) for _ in cart_items]

    order_value = round(sum(
        item["price"] * qty for item, qty in zip(cart_items, cart_quantities)
    ), 2)

    restaurant = restaurants_df.loc[restaurant_id]
    delivery_fee = float(restaurant["delivery_fee"])
    coupon_code = attempt["coupon_code"]

    discount = 0.0
    if coupon_code == "FLAT50":
        discount = 50.0
    elif coupon_code == "FIRST100":
        discount = 100.0
    elif coupon_code == "FREEDEL":
        discount = delivery_fee
        delivery_fee = 0.0
    elif coupon_code == "SAVE20":
        discount = round(order_value * 0.20, 2)

    order_id = order_id_counter
    order_id_counter += 1

    order_time = attempt["event_time"] + timedelta(seconds=random.randint(2, 10))
    payment_success = random.random() <= P_PAYMENT_SUCCESS

    if payment_success:
        cancelled = random.random() <= P_POST_PAYMENT_CANCEL
        is_delayed = random.random() < P_DELAYED
        delay_minutes = random.randint(10, 45) if is_delayed else 0
        delivery_time_minutes = (
            None if cancelled else int(restaurant["avg_delivery_time"]) + delay_minutes
        )
        order_status = "Cancelled" if cancelled else "Delivered"

        orders_rows.append({
            "order_id": order_id, "user_id": int(attempt["user_id"]), "restaurant_id": restaurant_id,
            "order_time": order_time, "order_value": order_value, "delivery_fee": delivery_fee,
            "coupon_discount": discount, "payment_method": attempt["payment_method"],
            "payment_status": "Success", "order_status": order_status,
            "delivery_time_minutes": delivery_time_minutes
        })
    else:
        orders_rows.append({
            "order_id": order_id, "user_id": int(attempt["user_id"]), "restaurant_id": restaurant_id,
            "order_time": order_time, "order_value": order_value, "delivery_fee": delivery_fee,
            "coupon_discount": discount, "payment_method": attempt["payment_method"],
            "payment_status": "Failed", "order_status": "Failed",
            "delivery_time_minutes": None
        })

    for item, qty in zip(cart_items, cart_quantities):
        order_items_rows.append({
            "order_id": order_id, "item_id": item["item_id"],
            "quantity": qty, "price_at_purchase": item["price"]
        })

orders_df = pd.DataFrame(orders_rows)
order_items_df = pd.DataFrame(order_items_rows)

orders_df.to_csv("data/orders.csv", index=False)
order_items_df.to_csv("data/order_items.csv", index=False)

orders_df.to_sql("orders", con=engine, if_exists="append", index=False)
order_items_df.to_sql("order_items", con=engine, if_exists="append", index=False)

print(orders_df.head())
print(f"\nOrders: {len(orders_df)}")
print(f"Payment success rate: {(orders_df['payment_status']=='Success').mean():.2%}")
print(f"Order items: {len(order_items_df)}")