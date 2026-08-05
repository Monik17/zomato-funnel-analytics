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
sessions_df = pd.read_sql(
    "SELECT s.session_id, s.user_id, s.session_start, u.city "
    "FROM sessions s JOIN users u ON s.user_id = u.user_id",
    con=engine
)
restaurants_df = pd.read_sql("SELECT restaurant_id, city FROM restaurants", con=engine)

COUPONS = [None, None, None, "FLAT50", "FIRST100", "FREEDEL", "SAVE20"]

P_HOME_TO_RESTAURANT = 0.75
P_RESTAURANT_TO_MENU = 0.82
P_MENU_TO_CART = 0.55
P_CART_TO_CHECKOUT = 0.78
P_CHECKOUT_TO_PAYMENT = 0.85
COUPON_BOOST = 0.10

events = []
session_end_updates = []  # (session_id, last_event_time)

for _, row in sessions_df.iterrows():
    session_id = int(row["session_id"])
    user_id = int(row["user_id"])
    user_city = row["city"]
    ts = row["session_start"]

    session_events = []

    def log_event(name, page, current_ts, restaurant_id=None, coupon_code=None, payment_method=None):
        session_events.append({
            "session_id": session_id, "user_id": user_id, "restaurant_id": restaurant_id,
            "event_name": name, "event_time": current_ts, "page_name": page,
            "coupon_code": coupon_code, "payment_method": payment_method
        })

    log_event("app_open", "Home", ts)

    if random.random() <= P_HOME_TO_RESTAURANT:
        city_restaurants = restaurants_df[restaurants_df["city"] == user_city]
        if len(city_restaurants) > 0 and random.random() < 0.85:
            restaurant = city_restaurants.sample(1).iloc[0]
        else:
            restaurant = restaurants_df.sample(1).iloc[0]
        restaurant_id = int(restaurant["restaurant_id"])

        ts += timedelta(seconds=random.randint(10, 60))
        log_event("restaurant_view", "Restaurant Page", ts, restaurant_id)

        if random.random() <= P_RESTAURANT_TO_MENU:
            ts += timedelta(seconds=random.randint(15, 90))
            log_event("menu_view", "Menu Page", ts, restaurant_id)

            if random.random() <= P_MENU_TO_CART:
                ts += timedelta(seconds=random.randint(30, 180))
                log_event("add_to_cart", "Cart", ts, restaurant_id)

                coupon_code = random.choice(COUPONS)
                if coupon_code:
                    ts += timedelta(seconds=random.randint(5, 30))
                    log_event("apply_coupon", "Cart", ts, restaurant_id, coupon_code=coupon_code)
                boost = COUPON_BOOST if coupon_code else 0.0

                if random.random() <= min(P_CART_TO_CHECKOUT + boost, 0.97):
                    ts += timedelta(seconds=random.randint(20, 120))
                    log_event("checkout_start", "Checkout", ts, restaurant_id)

                    if random.random() <= min(P_CHECKOUT_TO_PAYMENT + boost, 0.97):
                        payment_method = random.choices(
                            ["UPI", "Credit Card", "Debit Card", "Net Banking", "Wallet", "Cash on Delivery"],
                            weights=[45, 15, 15, 8, 12, 5], k=1
                        )[0]
                        ts += timedelta(seconds=random.randint(10, 60))
                        log_event("payment_attempt", "Payment", ts, restaurant_id,
                                   payment_method=payment_method)
                        # Note: whether payment succeeds and the resulting order
                        # is handled in generate_orders.py, not here.

    events.extend(session_events)
    session_end_updates.append((session_id, session_events[-1]["event_time"]))

events_df = pd.DataFrame(events)
events_df.to_csv("data/events.csv", index=False)
events_df.to_sql("events", con=engine, if_exists="append", index=False)

# ==========================
# Fix up session_end to match the real last event
# ==========================
with engine.begin() as conn:
    for session_id, last_event_time in session_end_updates:
        conn.execute(
            text("UPDATE sessions SET session_end = :end_time WHERE session_id = :sid"),
            {"end_time": last_event_time, "sid": session_id}
        )

print(events_df.head())
print(f"\nInserted {len(events_df)} events across {len(sessions_df)} sessions.")
print(f"Reached payment_attempt: {(events_df['event_name']=='payment_attempt').sum()}")