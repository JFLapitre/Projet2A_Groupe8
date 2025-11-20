-- ============================================================
-- TEST DATA POPULATION (Schema: tests)
-- ============================================================

-- 1. USERS (Hash/Salt pairs provided by user)
INSERT INTO tests.user (username, hash_password, salt, user_type, sign_up_date) VALUES
-- Customers (ID 1-5)
('alice_dupont',  '48509134ada98578077b37eed8faade004bb036b314ed8fafe80abb4feb17d29', '071bd72d2e52b72b94b3e47afe5e172a2f8826e355e54285fa466e26e24e5282', 'customer', '2024-01-01'), -- Pwd: P@ssW0rd1
('bob_martin',    '7dde5351f5852fdcc6bc4f1a2b12b2ba35ea93823776cbbba8f306bc6f2bb634', 'a1dd5ab3dda693d41837c73ad3fd347ba046588db991cc3f1cc5cb260eddf5af', 'customer', '2024-01-05'), -- Pwd: S3cure!TxT
('charlie_brown', '68e4498e77e7c3940c1a8da24d31c53308c2e26e6c8bf83808bfa7e77fd9f55e', 'fb480e326fcc737c273064cd0153234c18d6c0777c9a6d91ba4c2c7fe93d7a13', 'customer', '2024-02-10'), -- Pwd: Azerty_789!
('david_lee',     '167ec9a6e356723a4b1de1c92806876b86a18b5a2eefef860c18b1e78f0ecb75', 'b9d8e3cd2c777cffc84c050632b337ce8b719fa16a39369073a6a55e1c2a3ff7', 'customer', '2024-03-15'), -- Pwd: L0gin$2024
('eve_adam',      'c0ee2a3c9cbbc9a01fa92aa4e706dec11dd507f50b896c2cd6ff70523d1d9fe7', '23e8b3acd44f1b44329c92c983bc068fa724d78c75ff201ec297f2f66bccee48', 'customer', '2024-03-20'), -- Pwd: H@shM3Pls

-- Drivers (ID 6-8)
('driver_max',    '13cc81bcd5d058ef87a9c859b17edcd80efea1d0f284763cec7770cbdb9555b0', '9f8e44c0294740eaf225486a75b6275b80f3d8cd68376a1226d16620a78e6c6d', 'driver',   '2024-01-10'), -- Pwd: Pyth0n#Code
('driver_sam',    'd959c789ceae5753cdf3b839a0163f4a9caf810632269bdc2c1009d021bb2ae7', '15ce15d8ad64fb40e017918e2750598fd77a657b6f2dac8d5789cab7c3d4095b', 'driver',   '2024-02-01'), -- Pwd: D3vOpp$99
('driver_leo',    '1c7d807324a0fbdd6b9ff6b69893a32328335ceec2af4fd806bd2bdee8386709', '497a026f233f10ee2dd1d2d93e8bca35ab3fb91eb346d1b22fe32a7783edacc9', 'driver',   '2024-02-15'), -- Pwd: Adm1n?SYS

-- Admin (ID 9)
('admin_chief',   '948cc6ee100cb405c55b01e2ca7e8bd6313b941b66593fd4b79242f8ab49eb9d', '78da12e0656b329bcb8a017ac0c1589c377722e7bb471d8c0ae538295e4bc993', 'admin',    '2023-01-01'); -- Pwd: B1tCoin*Up


-- Customer details
INSERT INTO tests.customer (id_user, name, phone_number) VALUES
(1, 'Alice Dupont', '0601010101'),
(2, 'Bob Martin', '0602020202'),
(3, 'Charlie Brown', '0603030303'),
(4, 'David Lee', '0604040404'),
(5, 'Eve Adam', '0605050505');

-- Driver details
INSERT INTO tests.driver (id_user, name, phone_number, vehicle_type, availability) VALUES
(6, 'Max Verstappen', '0701010101', 'car', TRUE),
(7, 'Sam Porter', '0702020202', 'bike', TRUE),
(8, 'Leo Messi', '0703030303', 'scooter', FALSE);

-- Admin details
INSERT INTO tests.admin (id_user, name, phone_number) VALUES
(9, 'Big Boss', '0101010101');


-- 2. ADDRESSES
INSERT INTO tests.address (city, postal_code, street_name, street_number) VALUES
('Paris', '75001', 'Rue de Rivoli', '10'),
('Paris', '75011', 'Rue Oberkampf', '42'),
('Lyon', '69002', 'Place Bellecour', '5'),
('Marseille', '13001', 'Vieux Port', '1'),
('Bordeaux', '33000', 'Rue Sainte-Catherine', '120');


-- 3. ITEMS
INSERT INTO tests.item (name, description, item_type, price, stock, availability) VALUES
('Cheeseburger', 'Classic cheese burger', 'main', 12.50, 50, TRUE),
('Vegan Burger', 'No meat burger', 'main', 13.50, 20, TRUE),
('Fries', 'Crispy french fries', 'side', 4.00, 100, TRUE),
('Coke', '33cl Can', 'drink', 2.50, 100, TRUE),
('Water', '50cl Bottle', 'drink', 1.50, 100, TRUE),
('Tiramisu', 'Homemade coffee cake', 'dessert', 6.00, 15, TRUE),
('Caesar Salad', 'Chicken and salad', 'starter', 9.00, 20, TRUE),
('Sushi Set', '12 pieces', 'main', 18.00, 10, TRUE),
('Miso Soup', 'Hot soup', 'starter', 4.50, 30, TRUE),
('Chocolate Cake', 'Delicious cake', 'dessert', 5.50, 0, TRUE); 


-- 4. BUNDLES
-- Predefined Bundles
INSERT INTO tests.bundle (name, description, bundle_type, price, discount) VALUES
('Burger Menu', 'Burger + Fries + Coke', 'predefined', 16.00, NULL),
('Healthy Choice', 'Vegan Burger + Water', 'predefined', 14.00, NULL);

-- Predefined Bundle Items
INSERT INTO tests.bundle_item (id_bundle, id_item) VALUES 
(1, 1), (1, 3), (1, 4), -- Burger Menu
(2, 2), (2, 5);         -- Healthy Choice

-- Discount Bundles
INSERT INTO tests.bundle (name, description, bundle_type, required_item_types, discount) VALUES
('Couple Promo', '2 Mains - 10% off', 'discount', ARRAY['main', 'main'], 0.10);


-- 5. ORDERS
INSERT INTO tests.order (id_user, status, price, id_address, order_date) VALUES
(1, 'validated', 16.00, 1, NOW() - INTERVAL '1 HOUR'), 
(2, 'in_progress', 25.00, 2, NOW() - INTERVAL '30 MINUTE'),
(3, 'delivered', 18.00, 3, NOW() - INTERVAL '1 DAY'),
(1, 'pending', 12.50, 1, NOW());

-- 6. ORDER ITEMS
INSERT INTO tests.order_item (id_order, id_item) VALUES 
(1, 1), (1, 3), (1, 4), -- Order 1
(2, 1), (2, 1),         -- Order 2
(3, 8),                 -- Order 3
(4, 1);                 -- Order 4


-- 7. DELIVERIES
-- Active delivery (Order 2 -> Driver 6)
INSERT INTO tests.delivery (id_driver, status, delivery_time) VALUES
(6, 'in_progress', NULL);

INSERT INTO tests.delivery_order (id_delivery, id_order) VALUES (1, 2);

-- Completed delivery (Order 3 -> Driver 7)
INSERT INTO tests.delivery (id_driver, status, delivery_time) VALUES
(7, 'delivered', NOW() - INTERVAL '23 HOUR');

INSERT INTO tests.delivery_order (id_delivery, id_order) VALUES (2, 3);


-- 8. RESET SEQUENCES
SELECT setval('tests.user_id_user_seq', (SELECT MAX(id_user) FROM tests.user));
SELECT setval('tests.address_id_address_seq', (SELECT MAX(id_address) FROM tests.address));
SELECT setval('tests.item_id_item_seq', (SELECT MAX(id_item) FROM tests.item));
SELECT setval('tests.bundle_id_bundle_seq', (SELECT MAX(id_bundle) FROM tests.bundle));
SELECT setval('tests.order_id_order_seq', (SELECT MAX(id_order) FROM tests.order));
SELECT setval('tests.delivery_id_delivery_seq', (SELECT MAX(id_delivery) FROM tests.delivery));