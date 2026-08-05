import os
import random
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

restaurants_df = pd.read_sql("SELECT restaurant_id, cuisine FROM restaurants", con=engine)

# cuisine -> [(item_name, category, min_price, max_price), ...]
CUISINE_MENU = {
    "Pizza": [
        ("Margherita Pizza", "Main Course", 199, 349),
        ("Farmhouse Pizza", "Main Course", 249, 399),
        ("Pepperoni Pizza", "Main Course", 299, 449),
        ("Cheese Burst Pizza", "Main Course", 279, 429),
        ("Garlic Bread", "Sides", 99, 149),
        ("Pasta Alfredo", "Main Course", 199, 299),
        ("Choco Lava Cake", "Desserts", 89, 129),
    ],
    "Fast Food": [
        ("Chicken Burger", "Main Course", 129, 199),
        ("Veg Burger", "Main Course", 99, 159),
        ("French Fries", "Sides", 79, 129),
        ("Chicken Nuggets", "Sides", 129, 179),
        ("Cold Drink", "Beverages", 40, 60),
    ],
    "Healthy": [
        ("Veggie Delite Sub", "Main Course", 149, 219),
        ("Grilled Chicken Sub", "Main Course", 199, 269),
        ("Fresh Fruit Salad Bowl", "Sides", 129, 179),
        ("Fresh Juice", "Beverages", 89, 129),
    ],
    "Cafe": [
        ("Cappuccino", "Beverages", 129, 179),
        ("Cold Coffee", "Beverages", 139, 189),
        ("Grilled Sandwich", "Main Course", 149, 219),
        ("Blueberry Muffin", "Desserts", 99, 149),
        ("Chocolate Brownie", "Desserts", 109, 159),
    ],
    "Biryani": [
        ("Chicken Biryani", "Main Course", 219, 329),
        ("Mutton Biryani", "Main Course", 299, 429),
        ("Veg Biryani", "Main Course", 169, 249),
        ("Raita", "Sides", 39, 59),
        ("Chicken 65", "Starters", 179, 249),
    ],
    "North Indian": [
        ("Butter Chicken", "Main Course", 249, 349),
        ("Paneer Butter Masala", "Main Course", 219, 299),
        ("Dal Makhani", "Main Course", 179, 249),
        ("Butter Naan", "Sides", 39, 59),
        ("Jeera Rice", "Sides", 129, 169),
    ],
    "BBQ": [
        ("Grilled Chicken Platter", "Starters", 299, 429),
        ("Seekh Kebab", "Starters", 249, 349),
        ("Tandoori Chicken (Half)", "Starters", 259, 349),
        ("Paneer Tikka", "Starters", 219, 299),
    ],
    "Desserts": [
        ("Belgian Waffle", "Desserts", 149, 229),
        ("Ice Cream Sundae", "Desserts", 99, 169),
        ("Chocolate Brownie", "Desserts", 109, 159),
        ("Gulab Jamun (2 pcs)", "Desserts", 69, 99),
    ],
    "Rolls": [
        ("Chicken Roll", "Main Course", 99, 159),
        ("Paneer Roll", "Main Course", 89, 139),
        ("Egg Roll", "Main Course", 79, 129),
        ("Double Egg Chicken Roll", "Main Course", 129, 189),
    ],
    "Chinese": [
        ("Veg Manchurian", "Starters", 149, 219),
        ("Chicken Fried Rice", "Main Course", 179, 249),
        ("Chicken Momos", "Starters", 129, 189),
        ("Hakka Noodles", "Main Course", 159, 229),
        ("Spring Rolls", "Starters", 99, 149),
    ],
    "South Indian": [
        ("Masala Dosa", "Main Course", 99, 159),
        ("Idli Sambar (4 pcs)", "Main Course", 79, 129),
        ("Medu Vada (2 pcs)", "Starters", 69, 109),
        ("Rava Uttapam", "Main Course", 99, 149),
    ],
    "Italian": [
        ("Penne Arrabbiata", "Main Course", 219, 299),
        ("Margherita Pizza", "Main Course", 199, 349),
        ("Vegetable Lasagna", "Main Course", 249, 349),
        ("Garlic Bread", "Sides", 99, 149),
    ],
    "Street Food": [
        ("Pani Puri (Plate)", "Starters", 49, 89),
        ("Vada Pav", "Starters", 29, 49),
        ("Bhel Puri", "Starters", 59, 99),
        ("Samosa (2 pcs)", "Starters", 39, 59),
    ],
}

DEFAULT_ITEMS = [
    ("Chef's Special Thali", "Main Course", 199, 299),
    ("Mineral Water Bottle", "Beverages", 20, 30),
]

menu_items = []

for _, row in restaurants_df.iterrows():
    restaurant_id = int(row["restaurant_id"])
    items = CUISINE_MENU.get(row["cuisine"], DEFAULT_ITEMS)
    for item_name, category, low, high in items:
        menu_items.append({
            "restaurant_id": restaurant_id,
            "item_name": item_name,
            "category": category,
            "price": round(random.uniform(low, high), 2)
        })

df = pd.DataFrame(menu_items)
df.to_csv("data/menu_items.csv", index=False)
df.to_sql("menu_items", con=engine, if_exists="append", index=False)

print(df.head())
print(f"\nInserted {len(df)} menu items across {restaurants_df['restaurant_id'].nunique()} restaurants.")