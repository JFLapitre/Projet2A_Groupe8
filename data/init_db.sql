-- Suppression du schéma existant
DROP SCHEMA IF EXISTS fd CASCADE;
CREATE SCHEMA fd;

-- Table user
DROP TABLE IF EXISTS fd.user CASCADE;
CREATE TABLE fd.user (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    user_type VARCHAR(10) NOT NULL,
    sign_up_date DATE NOT NULL
);

-- Table address
DROP TABLE IF EXISTS fd.address CASCADE;
CREATE TABLE fd.address (
    id_address SERIAL PRIMARY KEY,
    city VARCHAR(20) NOT NULL,
    postal_code VARCHAR(5) NOT NULL,
    street_name VARCHAR(50) NOT NULL,
    street_number INT NOT NULL
);


-- Table customer
DROP TABLE IF EXISTS fd.customer CASCADE;
CREATE TABLE fd.customer (
    id_user INT PRIMARY KEY REFERENCES fd.user(id_user) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Table admin
DROP TABLE IF EXISTS fd.admin CASCADE;
CREATE TABLE fd.admin (
    id_user INT PRIMARY KEY REFERENCES fd.user(id_user) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Table driver
DROP TABLE IF EXISTS fd.driver CASCADE;
CREATE TABLE fd.driver (
    id_user INT PRIMARY KEY REFERENCES fd.user(id_user) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    vehicle_type VARCHAR(50),
    availability BOOLEAN DEFAULT TRUE
);

-- Table item
DROP TABLE IF EXISTS fd.item CASCADE;
CREATE TABLE fd.item (
    id_item SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(300),
    item_type VARCHAR(20) NOT NULL,
    price FLOAT NOT NULL
);

-- Table bundle
DROP TABLE IF EXISTS fd.bundle CASCADE;
CREATE TABLE fd.bundle (
    id_bundle SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(300),
    bundle_type VARCHAR(20) NOT NULL, -- "predefined" ou "discount"
    price FLOAT, -- Peut être NULL pour les discounted bundles
    discount FLOAT -- Peut être NULL pour les predefined bundles
);

-- Table bundle_item (pour les predefined bundles)
DROP TABLE IF EXISTS fd.bundle_item CASCADE;
CREATE TABLE fd.bundle_item (
    id_bundle INT REFERENCES fd.bundle(id_bundle) ON DELETE CASCADE,
    id_item INT REFERENCES fd.item(id_item) ON DELETE CASCADE,
    PRIMARY KEY (id_bundle, id_item)
);

-- Table order
DROP TABLE IF EXISTS fd.order CASCADE;
CREATE TABLE fd.order (
    id_order SERIAL PRIMARY KEY,
    id_user INT REFERENCES fd.user(id_user) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table order_bundle (table de jointure entre order et bundle)
DROP TABLE IF EXISTS fd.order_bundle CASCADE;
CREATE TABLE fd.order_bundle (
    id_order INT REFERENCES fd.order(id_order) ON DELETE CASCADE,
    id_bundle INT REFERENCES fd.bundle(id_bundle) ON DELETE CASCADE,
    PRIMARY KEY (id_order, id_bundle)
);

-- Table delivery
DROP TABLE IF EXISTS fd.delivery CASCADE;
CREATE TABLE fd.delivery (
    id_delivery SERIAL PRIMARY KEY,
    id_driver INT REFERENCES fd.driver(id_user) ON DELETE SET NULL,
    status VARCHAR(20) NOT NULL,
    delivery_time TIMESTAMP
);

-- Table delivery_order (table de jointure entre delivery et order)
DROP TABLE IF EXISTS fd.delivery_order CASCADE;
CREATE TABLE fd.delivery_order (
    id_delivery INT REFERENCES fd.delivery(id_delivery) ON DELETE CASCADE,
    id_order INT REFERENCES fd.order(id_order) ON DELETE CASCADE,
    PRIMARY KEY (id_delivery, id_order)
);


