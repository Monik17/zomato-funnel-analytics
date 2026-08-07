-- ============================================
-- Zomato Funnel Analytics - Database Schema
-- ============================================

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    gender ENUM('Male','Female','Other'),
    age INT,
    city VARCHAR(50),
    signup_date DATE,
    is_premium BOOLEAN,
    device_type ENUM('Android','iOS')
);

CREATE TABLE restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_name VARCHAR(100),
    city VARCHAR(50),
    cuisine VARCHAR(50),
    rating DECIMAL(2,1),
    average_cost INT,
    delivery_fee DECIMAL(6,2),
    avg_delivery_time INT
);

CREATE TABLE menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT,
    item_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(8,2),
    FOREIGN KEY (restaurant_id)
    REFERENCES restaurants(restaurant_id)
);

CREATE TABLE sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    session_start DATETIME,
    session_end DATETIME,
    app_version VARCHAR(20),
    device_os VARCHAR(20),
    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
);

CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    user_id INT,
    restaurant_id INT,
    event_name VARCHAR(50),
    event_time DATETIME,
    page_name VARCHAR(50),
    coupon_code VARCHAR(30),
    payment_method VARCHAR(20),
    FOREIGN KEY (session_id)
    REFERENCES sessions(session_id),
    FOREIGN KEY (user_id)
    REFERENCES users(user_id),
    FOREIGN KEY (restaurant_id)
    REFERENCES restaurants(restaurant_id)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    restaurant_id INT,
    order_time DATETIME,
    order_value DECIMAL(10,2),
    delivery_fee DECIMAL(6,2),
    coupon_discount DECIMAL(6,2),
    payment_method VARCHAR(20),
    payment_status VARCHAR(20),
    order_status VARCHAR(20),
    delivery_time_minutes INT,
    FOREIGN KEY (user_id)
    REFERENCES users(user_id),
    FOREIGN KEY (restaurant_id)
    REFERENCES restaurants(restaurant_id)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT,
    price_at_purchase DECIMAL(8,2),
    FOREIGN KEY (order_id)
    REFERENCES orders(order_id),
    FOREIGN KEY (item_id)
    REFERENCES menu_items(item_id)
);