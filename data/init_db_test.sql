-- Schema setup
DROP SCHEMA IF EXISTS tests CASCADE;
CREATE SCHEMA tests;

-- Users table
CREATE TABLE tests.user (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    hash_password VARCHAR(100) NOT NULL,
    salt VARCHAR(128) NOT NULL,
    user_type VARCHAR(10) NOT NULL, -- 'customer', 'driver', 'admin'
    sign_up_date DATE 
);

-- Addresses table
CREATE TABLE tests.address (
    id_address SERIAL PRIMARY KEY,
    city VARCHAR(20) NOT NULL,
    postal_code VARCHAR(5) NOT NULL,
    street_name VARCHAR(50) NOT NULL,
    street_number VARCHAR(10) NOT NULL
);

-- Customer details
CREATE TABLE tests.customer (
    id_user INT PRIMARY KEY REFERENCES tests.user(id_user) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(40) NOT NULL
);

-- Admin details
CREATE TABLE tests.admin (
    id_user INT PRIMARY KEY REFERENCES tests.user(id_user) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(40) NOT NULL
);

-- Driver details
CREATE TABLE tests.driver (
    id_user INT PRIMARY KEY REFERENCES tests.user(id_user) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(40) NOT NULL,
    vehicle_type VARCHAR(50),
    availability BOOLEAN DEFAULT TRUE
);

-- Items table
CREATE TABLE tests.item (
    id_item SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(300),
    item_type VARCHAR(20) NOT NULL, -- 'starter', 'main', 'dessert', 'drink', 'side'
    price FLOAT NOT NULL,
    stock INT NOT NULL,
    availability BOOLEAN NOT NULL
);

-- Bundles table
CREATE TABLE tests.bundle (
    id_bundle SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(300),
    bundle_type VARCHAR(20) NOT NULL, -- 'predefined', 'discount'
    required_item_types VARCHAR(30)[],
    price FLOAT, -- NULL for 'discount' bundles
    discount FLOAT -- NULL for 'predefined' bundles
);

-- Predefined Bundle items (Link bundle <-> item)
CREATE TABLE tests.bundle_item (
    id_bundle INT REFERENCES tests.bundle(id_bundle) ON DELETE CASCADE,
    id_item INT REFERENCES tests.item(id_item) ON DELETE CASCADE,
    PRIMARY KEY (id_bundle, id_item)
);

-- Orders table
CREATE TABLE tests.order (
    id_order SERIAL PRIMARY KEY,
    id_user INT REFERENCES tests.user(id_user) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL, -- 'pending', 'validated', 'in_progress', 'delivered'
    price FLOAT,
    id_address INT REFERENCES tests.address(id_address),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items (Link order <-> item)
CREATE TABLE tests.order_item (
    id_order_item SERIAL PRIMARY KEY,
    id_order INT REFERENCES tests.order(id_order) ON DELETE CASCADE,
    id_item INT REFERENCES tests.item(id_item) ON DELETE CASCADE
);

-- Deliveries table
CREATE TABLE tests.delivery (
    id_delivery SERIAL PRIMARY KEY,
    id_driver INT REFERENCES tests.driver(id_user) ON DELETE SET NULL,
    status VARCHAR(20) NOT NULL, -- 'pending', 'in_progress', 'completed'
    delivery_time TIMESTAMP
);

-- Delivery orders (Link delivery <-> order)
CREATE TABLE tests.delivery_order (
    id_delivery INT REFERENCES tests.delivery(id_delivery) ON DELETE CASCADE,
    id_order INT REFERENCES tests.order(id_order) ON DELETE CASCADE,
    PRIMARY KEY (id_delivery, id_order)
);