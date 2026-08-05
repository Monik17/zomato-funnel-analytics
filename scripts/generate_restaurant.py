import random
import pandas as pd
from sqlalchemy import create_engine

# ==========================
# MySQL Connection
# ==========================

USERNAME = "root"
PASSWORD = "170106"
HOST = "localhost"
PORT = 3306
DATABASE = "zomato_analytics"

engine = create_engine(
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# ==========================
# Cities
# ==========================

cities = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Pune",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Indore"
]

# ==========================
# Restaurant Brands
# ==========================

brands = [
    "Domino's Pizza",
    "Pizza Hut",
    "Burger King",
    "KFC",
    "McDonald's",
    "Subway",
    "Starbucks",
    "Biryani By Kilo",
    "Haldiram's",
    "Barbeque Nation",
    "The Belgian Waffle Co.",
    "Faasos",
    "Behrouz Biryani",
    "Oven Story Pizza",
    "Natural Ice Cream",
    "La Pino'z Pizza",
    "WOW! Momo",
    "Giani's",
    "Sagar Ratna",
    "Cafe Coffee Day"
]

local_prefix = [
    "Sharma",
    "Gupta",
    "Singh",
    "Royal",
    "Urban",
    "Spicy",
    "Bombay",
    "Indori",
    "Delhi",
    "Tandoori",
    "Foodie's",
    "Classic",
    "Golden",
    "Desi",
    "Taste of"
]

local_suffix = [
    "Kitchen",
    "Cafe",
    "Bistro",
    "House",
    "Corner",
    "Restaurant",
    "Dhaba",
    "Grill",
    "Express",
    "Tadka"
]

# ==========================
# Cuisine Mapping
# ==========================

brand_cuisine = {
    "Domino's Pizza":"Pizza",
    "Pizza Hut":"Pizza",
    "Burger King":"Fast Food",
    "KFC":"Fast Food",
    "McDonald's":"Fast Food",
    "Subway":"Healthy",
    "Starbucks":"Cafe",
    "Biryani By Kilo":"Biryani",
    "Haldiram's":"North Indian",
    "Barbeque Nation":"BBQ",
    "The Belgian Waffle Co.":"Desserts",
    "Faasos":"Rolls",
    "Behrouz Biryani":"Biryani",
    "Oven Story Pizza":"Pizza",
    "Natural Ice Cream":"Desserts",
    "La Pino'z Pizza":"Pizza",
    "WOW! Momo":"Chinese",
    "Giani's":"Desserts",
    "Sagar Ratna":"South Indian",
    "Cafe Coffee Day":"Cafe"
}

other_cuisines = [
    "North Indian",
    "South Indian",
    "Chinese",
    "Italian",
    "Cafe",
    "Street Food",
    "Desserts",
    "Fast Food",
    "Biryani"
]

restaurants = []

# --------------------------
# Add Brand Restaurants
# --------------------------

for city in cities:
    for brand in brands:

        restaurants.append({

            "restaurant_name": brand,

            "city": city,

            "cuisine": brand_cuisine[brand],

            "rating": round(random.uniform(3.8,4.9),1),

            "average_cost": random.randint(250,900),

            "delivery_fee": random.choice([20,30,40,50]),

            "avg_delivery_time": random.randint(20,45)

        })

# --------------------------
# Add Local Restaurants
# --------------------------

while len(restaurants) < 300:

    restaurants.append({

        "restaurant_name":
        random.choice(local_prefix)+" "+
        random.choice(local_suffix),

        "city": random.choice(cities),

        "cuisine": random.choice(other_cuisines),

        "rating": round(random.uniform(3.2,4.8),1),

        "average_cost": random.randint(150,700),

        "delivery_fee": random.choice([20,30,40,50,60]),

        "avg_delivery_time": random.randint(20,60)

    })

df = pd.DataFrame(restaurants)

# ==========================
# Save CSV
# ==========================

df.to_csv("data/restaurants.csv", index=False)

# ==========================
# Insert into MySQL
# ==========================

df.to_sql(
    "restaurants",
    con=engine,
    if_exists="append",
    index=False
)

print(df.head())

print(f"\nInserted {len(df)} restaurants successfully.")