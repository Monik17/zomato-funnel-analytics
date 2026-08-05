import random
import os
import pandas as pd
from faker import Faker
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "localhost")
PORT = int(os.getenv("DB_PORT", 3306))
DATABASE = os.getenv("DB_NAME")

engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
fake = Faker("en_IN")

cities = [
    "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune",
    "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Indore"
]

NUM_USERS = 5000
users = []

for i in range(NUM_USERS):
    gender = random.choice(["Male", "Female", "Other"])
    if gender == "Male":
        name = fake.name_male()
    elif gender == "Female":
        name = fake.name_female()
    else:
        name = fake.name()

    users.append({
        "name": name,
        "email": fake.unique.email(),
        "gender": gender,
        "age": random.randint(18, 55),
        "city": random.choice(cities),
        "signup_date": fake.date_between(start_date="-2y", end_date="today"),
        "is_premium": random.choices([0, 1], weights=[80, 20])[0],
        "device_type": random.choice(["Android", "iOS"])
    })

df = pd.DataFrame(users)
df.to_csv("data/users.csv", index=False)
df.to_sql("users", con=engine, if_exists="append", index=False)

print(df.head())
print(f"\nInserted {len(df)} users successfully.")