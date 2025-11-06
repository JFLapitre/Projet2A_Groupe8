-- Insert users
INSERT INTO fd.user (id_user, username, hash_password, salt, user_type, sign_up_date) VALUES
(1, 'john_doe', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'aa453f466c612b04de2e62b5501c264e462b06bac3ce18dc4bf7ad38e2d17bdf', 'customer', '2024-01-15'),
(2, 'jane_smith', 'e34d7db48a3fb5808c8360136c07151b14b68f342a8ff87d9aef2236c405bfc8', '9faef269131b1838ab8e95af580e7c109e1de4448ba0282bdf06f19726ff55ea', 'customer', '2024-02-20'),
(3, 'bob_driver', 'cb582b020a1f3c2cd95515946c05e719da58b7424e2d256f2ca7a5e4dc07e5d0', 'db7bdbc3bc99617b49292001145c705fdde6111d24716f0c7984ea02546231c1', 'driver', '2024-01-10'),
(4, 'groupe8', '05530bfc09764dcbce797ad8c1313819ea19bd932684c9b056b95d523ba3bdcf', '8759bb4e872578c20b9a835a4f78d8b46dcea0a80745c3dfcc71a9e5d8f6e35f', 'admin', '2000-01-01'),
(5, 'charlie_customer', 'c30d262fa113f34a7fcfe07ef3c813247170e8de9e4983c8741e30066c4c3ec0', '96feb3fd1738208a82870371dc52a5def69343165bcf2789e1a53f54eda61336', 'customer', '2024-03-05');

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
(4, 'Groupe 8', '0769522794');

-- Insert driver
INSERT INTO fd.driver (id_user, name, phone_number, vehicle_type, availability) VALUES
(3, 'Bob Driver', '0645678901', 'Scooter', TRUE);

-- Insert items
INSERT INTO fd.item (name, item_type, price, stock, availability) VALUES
('Margherita Pizza', 'main', 12.50, 20, TRUE),
('Four Cheese Pizza', 'main', 14.00, 15, TRUE),
('Caesar Salad', 'starter', 8.50, 10, TRUE),
('Tiramisu', 'dessert', 6.00, 8, TRUE),
('Coca Cola', 'drink', 3.00, 30, TRUE),
('Mineral Water', 'drink', 2.00, 25, TRUE),
('Classic Burger', 'main', 11.00, 12, TRUE),
('Fries', 'side', 4.50, 18, TRUE);

-- Insert predefined bundles
INSERT INTO fd.bundle (name, description, bundle_type, required_item_types,  price, discount) VALUES
('Pizza Menu', 'Pizza + Drink + Dessert', 'predefined', NULL, 19.00, NULL),
('Burger Menu', 'Burger + Fries + Drink', 'predefined', NULL, 16.00, NULL);

-- Insert discount bundles
INSERT INTO fd.bundle (name, description, bundle_type, required_item_types, price, discount) VALUES
('2 Pizzas Promo', 'Buy 2 pizzas, get 10% off', 'discount', ARRAY['main', 'main'], NULL, 0.10),
('Simple bundle', '', 'discount', ARRAY['main', 'drink'], NULL, 0.20),
('Complete bundle', '', 'discount', ARRAY['starter', 'main', 'dessert'], NULL, 0.2);

-- Insert single item bundles
-- Insert single items as bundles with the corresponding item price
INSERT INTO fd.bundle (name, description, bundle_type, required_item_types, price, discount)
SELECT 
    i.name, 
    '1 single item', 
    'single_item',
    NULL, 
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
INSERT INTO fd.order (id_user, status, id_address, order_date) VALUES
(1, 'delivered', 1, '2024-10-01 12:30:00'),
(2, 'in_progress', 2, '2024-10-06 18:45:00'),
(5, 'pending', 3, '2024-10-06 19:15:00'),
(4, 'in_progress', 4, '2024-10-06 20:00:00'), -- New order 4
(4, 'in_progress', 5, '2024-10-06 20:05:00'); -- New order 5

-- Associate orders with bundles
INSERT INTO fd.order_bundle (id_order, id_bundle) VALUES
(1, 1), -- Order 1: Pizza Menu
(2, 2), -- Order 2: Burger Menu
(2, 3), -- Order 2: 2 Pizzas Promo
(3, 1), -- Order 3: Pizza Menu
(4, 3), -- Order 4: 2 Pizzas Promo
(5, 2); -- Order 5: Burger Menu

-- Insert deliveries
INSERT INTO fd.delivery (id_driver, status, delivery_time) VALUES
(3, 'completed', '2024-10-01 13:15:00'),
(3, 'in_progress', NULL),
(3, 'in_progress', NULL);

-- Associate orders with deliveries
INSERT INTO fd.delivery_order (id_delivery, id_order) VALUES
(1, 1), -- Delivery 1 -> Order 1
(2, 2), -- Delivery 2 -> Order 2
(3, 3), -- Delivery 3 -> Order 3
(2, 4), -- Delivery 2 -> Order 4 (new)
(2, 5); -- Delivery 2 -> Order 5 (new)


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