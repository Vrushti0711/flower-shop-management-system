DROP DATABASE IF EXISTS flower_shop;
CREATE DATABASE flower_shop;
USE flower_shop;
show tables;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);
desc users;

INSERT INTO users (username, password) VALUES
('admin', 'admin123'),
('manager', 'flower@123'),
('staff', 'shop2026');
select*from users;

CREATE TABLE flowers (
    flower_id INT PRIMARY KEY AUTO_INCREMENT,
    flower_name VARCHAR(50) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    supplier_name VARCHAR(100)
);
desc flowers;

INSERT INTO flowers (flower_name, category, price, quantity, supplier_name) VALUES
('Rose', 'Bouquet', 50.00, 120, 'Pastel Flowers'),
('Lily', 'Decorative', 70.00, 90, 'Plant Nursery'),
('Tulip', 'Gift', 60.00, 80, 'Bloom Supply'),
('Sunflower', 'Decorative', 40.00, 100, 'Sun Flora'),
('Orchid', 'Premium', 120.00, 30, 'Royal Garden'),
('Jasmine', 'Fragrance', 30.00, 150, 'Fresh Garden'),
('Marigold', 'Decoration', 25.00, 200, 'Festival Blooms'),
('Lavender', 'Premium', 90.00, 60, 'Herbal Farms'),
('Daisy', 'Gift', 35.00, 110, 'Petal World'),
('Carnation', 'Bouquet', 55.00, 75, 'Pastel Flowers');
select*from flowers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255)
);
desc customers;

INSERT INTO customers (customer_name, phone, address) VALUES
('Rahul Patel', '9876543210', 'Mumbai'),
('Priya Shah', '9123456780', 'Ahmedabad'),
('Ananya Mehta', '9988776655', 'Pune'),
('Sneha Kapoor', '9988771100', 'Delhi');
select*from customers;

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
desc orders;

CREATE TABLE order_details (
    detail_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    flower_id INT,
    quantity INT,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (flower_id) REFERENCES flowers(flower_id)
);
desc order_details;



CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    payment_date DATE,
    amount DECIMAL(10,2),
    payment_method VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
desc payments;