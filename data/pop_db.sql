-- Insert users
INSERT INTO fd.user (id_user, username, password, user_type, sign_up_date) VALUES
(1, 'john_doe', 'password123', 'customer', '2024-01-15'),
(2, 'jane_smith', 'securepass456', 'customer', '2024-02-20'),
(3, 'bob_driver', 'driverpass789', 'driver', '2024-01-10'),
(4, 'alice_admin', 'adminpass321', 'admin', '2024-01-01'),
(5, 'charlie_customer', 'custpass654', 'customer', '2024-03-05');

-- Insert addresses
INSERT INTO fd.address (city, postal_code, street_name, street_number) VALUES
('Paris', '75001', 'Rivoli Street', 10),
('Lyon', '69001', 'Republic Street', 25),
('Marseille', '13001', 'La Canebière Street', 50),
('Toulouse', '31000', 'Alsace Lorraine Street', 15),
('Nice', '06000', 'English Promenade', 100);

-- Insert customers
INSERT INTO fd.customer (id_user, name, phone_number) VALUES
(1, 'John Doe', '0601020304'),
(2, 'Jane Smith', '0612345678'),
(5, 'Charlie Customer', '0623456789');

-- Insert admin
INSERT INTO fd.admin (id_user, name, phone_number) VALUES
(4, 'Alice Admin', '0634567890');

-- Insert driver
INSERT INTO fd.driver (id_user, name, phone_number, vehicle_type, availability) VALUES
(3, 'Bob Driver', '0645678901', 'Scooter', TRUE);

-- Insert items
INSERT INTO fd.item (name, item_type, price) VALUES
('Margherita Pizza', 'main', 12.50),
('Four Cheese Pizza', 'main', 14.00),
('Caesar Salad', 'starter', 8.50),
('Tiramisu', 'dessert', 6.00),
('Coca Cola', 'drink', 3.00),
('Mineral Water', 'drink', 2.00),
('Classic Burger', 'main', 11.00),
('Fries', 'side', 4.50);

-- Insert predefined bundles
INSERT INTO fd.bundle (name, description, bundle_type, price, discount) VALUES
('Pizza Menu', 'Pizza + Drink + Dessert', 'predefined', 19.00, NULL),
('Burger Menu', 'Burger + Fries + Drink', 'predefined', 16.00, NULL);

-- Insert discount bundles
INSERT INTO fd.bundle (name, description, bundle_type, price, discount) VALUES
('2 Pizzas Promo', 'Buy 2 pizzas, get 10% off', 'discount', NULL, 0.10),
('Happy Hour', '20% off on any order before 7 PM', 'discount', NULL, 0.20);

-- Insert single item
-- Insert single items as bundles with the corresponding item price
INSERT INTO fd.bundle (name, description, bundle_type, price, discount)
SELECT 
    i.name, 
    '1 single item', 
    'single_item', 
    i.price, 
    NULL
FROM fd.item i
WHERE i.name IN ('Classic Burger', 'Fries');

-- Associate items with predefined bundles
INSERT INTO fd.bundle_item (id_bundle, id_item) VALUES
-- Pizza Menu (bundle 1): Margherita Pizza + Coca Cola + Tiramisu
(1, 1),
(1, 5),
(1, 4),
-- Burger Menu (bundle 2): Classic Burger + Fries + Coca Cola
(2, 7),
(2, 8),
(2, 5);

-- Insert orders
INSERT INTO fd.order (id_user, status, address, order_date) VALUES
(1, 'delivered', '10 Rivoli Street, 75001 Paris', '2024-10-01 12:30:00'),
(2, 'in_progress', '25 Republic Street, 69001 Lyon', '2024-10-06 18:45:00'),
(5, 'pending', '50 La Canebière Street, 13001 Marseille', '2024-10-06 19:15:00');

-- Associate orders with bundles
INSERT INTO fd.order_bundle (id_order, id_bundle) VALUES
(1, 1), -- Order 1: Pizza Menu
(2, 2), -- Order 2: Burger Menu
(2, 3), -- Order 2: 2 Pizzas Promo
(3, 1); -- Order 3: Pizza Menu

-- Insert deliveries
INSERT INTO fd.delivery (id_driver, status, delivery_time) VALUES
(3, 'completed', '2024-10-01 13:15:00'),
(3, 'in_progress', NULL),
(NULL, 'pending', NULL);

-- Associate deliveries with orders
INSERT INTO fd.delivery_order (id_delivery, id_order) VALUES
(1, 1), -- Delivery 1 for order 1
(2, 2), -- Delivery 2 for order 2
(3, 3); -- Delivery 3 for order 3

-- ========================================
-- Reset all sequences to continue after existing data
-- ========================================

-- Reset user sequence
SELECT setval('fd.user_id_user_seq', (SELECT MAX(id_user) FROM fd.user));

-- Reset address sequence
SELECT setval('fd.address_id_address_seq', (SELECT MAX(id_address) FROM fd.address));

-- Reset item sequence
SELECT setval('fd.item_id_item_seq', (SELECT MAX(id_item) FROM fd.item));

-- Reset bundle sequence
SELECT setval('fd.bundle_id_bundle_seq', (SELECT MAX(id_bundle) FROM fd.bundle));

-- Reset order sequence
SELECT setval('fd.order_id_order_seq', (SELECT MAX(id_order) FROM fd.order));

-- Reset delivery sequence
SELECT setval('fd.delivery_id_delivery_seq', (SELECT MAX(id_delivery) FROM fd.delivery));