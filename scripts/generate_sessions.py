import os
import random
from datetime import datetime, timedelta

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

users_df = pd.read_sql("SELECT user_id, device_type FROM users", con=engine)
users_records = users_df.to_dict("records")

NUM_SESSIONS = 50000
DAYS_BACK = 180

APP_VERSIONS = ["3.2.1", "3.3.0", "3.4.2", "3.5.0"]

# Lunch (12-14) and dinner (19-22) traffic peaks
HOUR_WEIGHTS = {h: 1 for h in range(24)}
for h in [12, 13, 14]:
    HOUR_WEIGHTS[h] = 4
for h in [19, 20, 21, 22]:
    HOUR_WEIGHTS[h] = 5
hours = list(HOUR_WEIGHTS.keys())
hour_weights = list(HOUR_WEIGHTS.values())


def random_start_time():
    day_offset = random.randint(0, DAYS_BACK)
    base_date = datetime.now() - timedelta(days=day_offset)
    hour = random.choices(hours, weights=hour_weights, k=1)[0]
    return base_date.replace(hour=hour, minute=random.randint(0, 59),
                              second=random.randint(0, 59), microsecond=0)


sessions = []

for i in range(NUM_SESSIONS):
    user = random.choice(users_records)
    device_type = user["device_type"]

    os_versions = ["12", "13", "14"] if device_type == "Android" else ["16", "17", "18"]
    device_os = f"{device_type} {random.choice(os_versions)}"

    session_start = random_start_time()
    # Placeholder duration -- generate_events.py will correct this
    # once it simulates the actual page-by-page funnel.
    duration_seconds = random.randint(20, 900)
    session_end = session_start + timedelta(seconds=duration_seconds)

    sessions.append({
        "user_id": user["user_id"],
        "session_start": session_start,
        "session_end": session_end,
        "app_version": random.choice(APP_VERSIONS),
        "device_os": device_os
    })

df = pd.DataFrame(sessions)
df.to_csv("data/sessions.csv", index=False)
df.to_sql("sessions", con=engine, if_exists="append", index=False)

print(df.head())
print(f"\nInserted {len(df)} sessions successfully.")