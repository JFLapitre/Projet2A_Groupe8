-- ========================================
-- Insertion de données volumineuses (x2-x3)
-- ========================================

-- Insert users (5 originaux + 8 nouveaux = 13 total)
INSERT INTO tests.user (id_user, username, hash_password, salt, user_type, sign_up_date) VALUES
(1, 'john_doe', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'aa453f466c612b04de2e62b5501c264e462b06bac3ce18dc4bf7ad38e2d17bdf', 'customer', '2024-01-15'),
(2, 'jane_smith', 'e34d7db48a3fb5808c8360136c07151b14b68f342a8ff87d9aef2236c405bfc8', '9faef269131b1838ab8e95af580e7c109e1de4448ba0282bdf06f19726ff55ea', 'customer', '2024-02-20'),
(3, 'bob_driver', 'cb582b020a1f3c2cd95515946c05e719da58b7424e2d256f2ca7a5e4dc07e5d0', 'db7bdbc3bc99617b49292001145c705fdde6111d24716f0c7984ea02546231c1', 'driver', '2024-01-10'),
(4, 'alice_admin', 'ae09bdc7f44c029a41114fa07ae66da4c7339b39b50329a21a316eb1ebd2ea20', '8759bb4e872578c20b9a835a4f78d8b46dcea0a80745c3dfcc71a9e5d8f6e35f', 'admin', '2024-01-01'),
(5, 'charlie_customer', 'c30d262fa113f34a7fcfe07ef3c813247170e8de9e4983c8741e30066c4c3ec0', '96feb3fd1738208a82870371dc52a5def69343165bcf2789e1a53f54eda61336', 'customer', '2024-03-05'),
-- Nouveaux utilisateurs
(6, 'emma_white', 'f2d81a260dea8b100dd6542b44f7b237e40348b11b15886618c07e036b5a10cc', 'c6a2b8e0b7b8a7b0e1b6f3c8a9f0b5d4e3f2a1c0d9e8b7a6f5d4c3b2a1e0f9d8', 'customer', '2024-04-10'),
(7, 'liam_brown', '5f4dcc3b5aa765d61d8327deb882cf99574f1b7f2f5f7f2b7f3b6a9c8b7f5b3a', 'd0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1', 'customer', '2024-05-01'),
(8, 'olivia_green', '3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1', '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b', 'customer', '2024-05-15'),
(9, 'noah_martin', '8a4f5b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a', 'f1e2d3c4b5a6f7e8d9c0b1a2e3f4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0e1f2', 'driver', '2024-02-15'),
(10, 'sophia_clark', 'b1a0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0', 'a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1', 'driver', '2024-03-20'),
(11, 'james_lewis', '1b2a3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b', 'c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4', 'admin', '2024-01-20'),
(12, 'ava_walker', 'f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8', 'e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5', 'customer', '2024-06-01'),
(13, 'william_hall', 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', 'b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3', 'customer', '2024-06-10');

-- Insert addresses (5 originaux + 8 nouveaux = 13 total)
INSERT INTO tests.address (city, postal_code, street_name, street_number) VALUES
('Paris', '75001', 'Rivoli Street', 10),
('Lyon', '69001', 'Republic Street', 25),
('Marseille', '13001', 'La Canebière Street', 50),
('Toulouse', '31000', 'Alsace Lorraine Street', 15),
('Nice', '06000', 'English Promenade', 100),
-- Nouvelles adresses
('Bordeaux', '33000', 'Sainte-Catherine Street', 200),
('Lille', '59000', 'Grand Place', 5),
('Strasbourg', '67000', 'Petite France', 12),
('Nantes', '44000', 'Bouffay Square', 30),
('Montpellier', '34000', 'Comédie Square', 45),
('Rennes', '35000', 'Liberty Street', 8),
('Reims', '51100', 'Cathedral Square', 22),
('Le Havre', '76600', 'Perret Avenue', 1);


-- Insert customers (3 originaux + 5 nouveaux = 8 total)
INSERT INTO tests.customer (id_user, name, phone_number) VALUES
(1, 'John Doe', '0601020304'),
(2, 'Jane Smith', '0612345678'),
(5, 'Charlie Customer', '0623456789'),
-- Nouveaux clients
(6, 'Emma White', '0611223344'),
(7, 'Liam Brown', '0622334455'),
(8, 'Olivia Green', '0633445566'),
(12, 'Ava Walker', '0644556677'),
(13, 'William Hall', '0655667788');

-- Insert admin (1 original + 1 nouveau = 2 total)
INSERT INTO tests.admin (id_user, name, phone_number) VALUES
(4, 'Alice Admin', '0634567890'),
-- Nouvel admin
(11, 'James Lewis', '0698765432');

-- Insert driver (1 original + 2 nouveaux = 3 total)
INSERT INTO tests.driver (id_user, name, phone_number, vehicle_type, availability) VALUES
(3, 'Bob Driver', '0645678901', 'Scooter', TRUE),
-- Nouveaux chauffeurs
(9, 'Noah Martin', '0612345600', 'Car', TRUE),
(10, 'Sophia Clark', '0612345611', 'Scooter', FALSE); -- Chauffeur non disponible

-- Insert items (8 originaux + 10 nouveaux = 18 total)
INSERT INTO tests.item (name, item_type, price, stock, availability) VALUES
('Margherita Pizza', 'main', 12.50, 20, TRUE),
('Four Cheese Pizza', 'main', 14.00, 15, TRUE),
('Caesar Salad', 'starter', 8.50, 10, TRUE),
('Tiramisu', 'dessert', 6.00, 8, TRUE),
('Coca Cola', 'drink', 3.00, 30, TRUE),
('Mineral Water', 'drink', 2.00, 25, TRUE),
('Classic Burger', 'main', 11.00, 12, TRUE),
('Fries', 'side', 4.50, 18, TRUE),
-- Nouveaux items
('Pepperoni Pizza', 'main', 13.50, 15, TRUE),
('Veggie Pizza', 'main', 13.00, 10, TRUE),
('Chicken Burger', 'main', 12.00, 10, TRUE),
('Onion Rings', 'side', 5.00, 15, TRUE),
('Greek Salad', 'starter', 9.00, 8, TRUE),
('Chocolate Cake', 'dessert', 6.50, 7, TRUE),
('Sprite', 'drink', 3.00, 30, TRUE),
('Iced Tea', 'drink', 3.50, 20, TRUE),
('Mozzarella Sticks', 'starter', 7.00, 12, TRUE),
('Pad Thai', 'main', 14.50, 8, FALSE); -- Item non disponible

-- Insert predefined bundles (2 originaux + 3 nouveaux = 5 total)
INSERT INTO tests.bundle (name, description, bundle_type, required_item_types,  price, discount) VALUES
('Pizza Menu', 'Pizza + Drink + Dessert', 'predefined', NULL, 19.00, NULL),
('Burger Menu', 'Burger + Fries + Drink', 'predefined', NULL, 16.00, NULL),
-- Nouveaux predefined
('Salad Meal', 'Salad + Drink', 'predefined', NULL, 10.00, NULL),
('Chicken Burger Menu', 'Chicken Burger + Onion Rings + Sprite', 'predefined', NULL, 18.00, NULL),
('Double Pizza Menu', '2 Pizzas + 2 Drinks', 'predefined', NULL, 32.00, NULL);

-- Insert discount bundles (3 originaux + 3 nouveaux = 6 total)
INSERT INTO tests.bundle (name, description, bundle_type, required_item_types, price, discount) VALUES
('2 Pizzas Promo', 'Buy 2 pizzas, get 10% off', 'discount', ARRAY['main', 'main'], NULL, 0.10),
('Simple bundle', '', 'discount', ARRAY['main', 'drink'], NULL, 0.20),
('Complete bundle', '', 'discount', ARRAY['starter', 'main', 'dessert'], NULL, 0.2),
-- Nouveaux discount
('Drink Duo', '2 drinks, 15% off', 'discount', ARRAY['drink', 'drink'], NULL, 0.15),
('Main & Side', 'Main course + side, 5% off', 'discount', ARRAY['main', 'side'], NULL, 0.05),
('Full Course Deal', 'Starter, Main, Side, Dessert, Drink', 'discount', ARRAY['starter', 'main', 'side', 'dessert', 'drink'], NULL, 0.25);

-- Insert single item bundles
INSERT INTO tests.bundle (name, description, bundle_type, required_item_types, price, discount)
SELECT 
    i.name, 
    '1 single item', 
    'single_item',
    NULL, 
    i.price, 
    NULL
FROM tests.item i
WHERE i.name IN ('Classic Burger', 'Fries', 'Pepperoni Pizza', 'Onion Rings', 'Chocolate Cake', 'Caesar Salad');

-- Associate items with predefined bundles
INSERT INTO tests.bundle_item (id_bundle, id_item) VALUES
-- Pizza Menu (bundle 1): Margherita Pizza (1) + Coca Cola (5) + Tiramisu (4)
(1, 1),
(1, 5),
(1, 4),
-- Burger Menu (bundle 2): Classic Burger (7) + Fries (8) + Coca Cola (5)
(2, 7),
(2, 8),
(2, 5),
-- Salad Meal (bundle 3): Caesar Salad (3) + Mineral Water (6)
(3, 3),
(3, 6),
-- Chicken Burger Menu (bundle 4): Chicken Burger (11) + Onion Rings (12) + Sprite (15)
(4, 11),
(4, 12),
(4, 15),
-- Double Pizza Menu (bundle 5): Pepperoni Pizza (9) + Veggie Pizza (10) + 2x Iced Tea (16)
(5, 9),
(5, 10),
(5, 16);

-- Insert orders (5 originaux + 9 nouveaux = 14 total)
-- Statuts : delivered, in_progress, pending
INSERT INTO tests.order (id_user, status, id_address, order_date) VALUES
(1, 'delivered', 1, '2024-10-01 12:30:00'),
(2, 'in_progress', 2, '2024-10-06 18:45:00'),
(5, 'pending', 3, '2024-10-06 19:15:00'),
(4, 'in_progress', 4, '2024-10-06 20:00:00'),
(4, 'in_progress', 5, '2024-10-06 20:05:00'),
-- Nouvelles commandes
(6, 'delivered', 6, '2024-10-02 11:00:00'),
(7, 'delivered', 7, '2024-10-03 13:15:00'),
(8, 'in_progress', 8, '2024-10-06 20:10:00'),
(1, 'pending', 1, '2024-10-06 20:15:00'),
(12, 'pending', 9, '2024-10-06 20:20:00'),
(2, 'in_progress', 10, '2024-10-06 20:25:00'),
(6, 'in_progress', 11, '2024-10-06 20:30:00'),
(7, 'delivered', 12, '2024-10-04 19:00:00'),
(13, 'pending', 13, '2024-10-06 20:35:00');

-- Associate orders with bundles
INSERT INTO tests.order_bundle (id_order, id_bundle) VALUES
(1, 1), -- Order 1: Pizza Menu
(2, 2), -- Order 2: Burger Menu
(2, 6), -- Order 2: 2 Pizzas Promo
(3, 1), -- Order 3: Pizza Menu
(4, 6), -- Order 4: 2 Pizzas Promo
(5, 2), -- Order 5: Burger Menu
-- Nouvelles associations
(6, 3), -- Order 6: Salad Meal
(7, 4), -- Order 7: Chicken Burger Menu
(8, 5), -- Order 8: Double Pizza Menu
(9, 7), -- Order 9: Simple bundle
(10, 8), -- Order 10: Complete bundle
(11, 9), -- Order 11: Drink Duo
(12, 10), -- Order 12: Main & Side
(12, 16), -- Order 12: Single item Chocolate Cake (ID bundle 16)
(13, 5); -- Order 13: Double Pizza Menu


-- Insert deliveries (3 originaux + 5 nouveaux = 8 total)
-- Statuts : completed, in_progress (conformément à la règle)
INSERT INTO tests.delivery (id_driver, status, delivery_time) VALUES
(3, 'completed', '2024-10-01 13:15:00'), -- Pour Order 1
(3, 'in_progress', NULL),                -- Pour Order 2, 4, 5
(9, 'completed', '2024-10-02 11:45:00'), -- Pour Order 6
(9, 'completed', '2024-10-03 14:00:00'), -- Pour Order 7
(3, 'in_progress', NULL),                -- Pour Order 8
(9, 'in_progress', NULL),                -- Pour Order 11
(3, 'in_progress', NULL),                -- Pour Order 12
(9, 'completed', '2024-10-04 19:40:00'); -- Pour Order 13

-- Associate orders with deliveries
-- Logique : 
--   Order 'delivered' -> Delivery 'completed'
--   Order 'in_progress' -> Delivery 'in_progress'
--   Order 'pending' -> Pas d'entrée dans delivery_order
INSERT INTO tests.delivery_order (id_delivery, id_order) VALUES
(1, 1), -- Delivery 1 (completed) -> Order 1 (delivered)
(2, 2), -- Delivery 2 (in_progress) -> Order 2 (in_progress)
(2, 4), -- Delivery 2 (in_progress) -> Order 4 (in_progress)
(2, 5), -- Delivery 2 (in_progress) -> Order 5 (in_progress)
-- Nouvelles associations
(3, 6), -- Delivery 3 (completed) -> Order 6 (delivered)
(4, 7), -- Delivery 4 (completed) -> Order 7 (delivered)
(5, 8), -- Delivery 5 (in_progress) -> Order 8 (in_progress)
(6, 11), -- Delivery 6 (in_progress) -> Order 11 (in_progress)
(7, 12), -- Delivery 7 (in_progress) -> Order 12 (in_progress)
(8, 13); -- Delivery 8 (completed) -> Order 13 (delivered)
-- Les commandes 3, 9, 10, 14 (status 'pending') n'ont pas de livraison associée.

-- ========================================
-- Reset all sequences to continue after existing data
-- ========================================

-- Reset user sequence
SELECT setval('tests.user_id_user_seq', (SELECT MAX(id_user) FROM tests.user));

-- Reset address sequence
SELECT setval('tests.address_id_address_seq', (SELECT MAX(id_address) FROM tests.address));

-- Reset item sequence
SELECT setval('tests.item_id_item_seq', (SELECT MAX(id_item) FROM tests.item));

-- Reset bundle sequence
SELECT setval('tests.bundle_id_bundle_seq', (SELECT MAX(id_bundle) FROM tests.bundle));

-- Reset order sequence
SELECT setval('tests.order_id_order_seq', (SELECT MAX(id_order) FROM tests.order));

-- Reset delivery sequence
SELECT setval('tests.delivery_id_delivery_seq', (SELECT MAX(id_delivery) FROM tests.delivery));