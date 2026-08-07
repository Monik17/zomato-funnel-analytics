import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "localhost")
PORT = int(os.getenv("DB_PORT", 3306))
DATABASE = os.getenv("DB_NAME")

engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# payment_attempt events and orders were created 1:1, in the same order
# (generate_orders.py looped through payment_attempts row-by-row and made
# exactly one order per attempt) -- so we can match them by position.
payment_attempts = pd.read_sql(
    "SELECT session_id, user_id, restaurant_id, event_time "
    "FROM events WHERE event_name = 'payment_attempt' ORDER BY event_id",
    con=engine
)

orders = pd.read_sql(
    "SELECT order_id, user_id, restaurant_id, order_time, payment_status "
    "FROM orders ORDER BY order_id",
    con=engine
)

print(f"Payment attempts: {len(payment_attempts)} | Orders: {len(orders)}")
assert len(payment_attempts) == len(orders), "Counts don't match -- stop, don't proceed"

# Sanity check: user_id/restaurant_id should line up row-for-row
mismatches = (
    (payment_attempts["user_id"].values != orders["user_id"].values).sum()
    + (payment_attempts["restaurant_id"].values != orders["restaurant_id"].values).sum()
)
print(f"Mismatches between matched rows: {mismatches} (should be 0)")

merged = payment_attempts.copy()
merged["payment_status"] = orders["payment_status"].values
merged["order_time"] = orders["order_time"].values

successful = merged[merged["payment_status"] == "Success"]

order_placed_events = pd.DataFrame({
    "session_id": successful["session_id"],
    "user_id": successful["user_id"],
    "restaurant_id": successful["restaurant_id"],
    "event_name": "order_placed",
    "event_time": successful["order_time"],
    "page_name": "Order Confirmation",
    "coupon_code": None,
    "payment_method": None
})

order_placed_events.to_csv("data/order_placed_backfill.csv", index=False)
order_placed_events.to_sql("events", con=engine, if_exists="append", index=False)

print(f"Inserted {len(order_placed_events)} order_placed events.")