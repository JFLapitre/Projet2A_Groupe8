INSERT INTO fd.user (id_user, username, hash_password, salt, user_type, sign_up_date) VALUES
(1,'groupe8', '05530bfc09764dcbce797ad8c1313819ea19bd932684c9b056b95d523ba3bdcf', '8759bb4e872578c20b9a835a4f78d8b46dcea0a80745c3dfcc71a9e5d8f6e35f', 'admin', '2000-01-01'),
(2, 'jane_smith', '9faef269131b1838ab8e95af580e7c109e1de4448ba0282bdf06f19726ff55ea', '776e37cc088064e6aef5cd504181f07e83ab5e495e724a5a492f0b495cec3e1c', 'customer', '2024-02-20'),
(3, 'bob_driver', 'db7bdbc3bc99617b49292001145c705fdde6111d24716f0c7984ea02546231c1', '5002971dd49c959b140e1ad3576cdd34be96c3ccab3fbc355009934f89137111', 'driver', '2024-01-10'),
(4,'john_doe', 'aa453f466c612b04de2e62b5501c264e462b06bac3ce18dc4bf7ad38e2d17bdf', '9a7fc02853c99c560238517027351d7deb7efeb2097686bd565c59bdaf059af6', 'customer', '2024-01-15'),
(5, 'charlie_customer', '96feb3fd1738208a82870371dc52a5def69343165bcf2789e1a53f54eda61336', '76b132d093f2081b52c12bf8bd9add1c857fd1a4d924093b170c8c7acad1df25', 'customer', '2024-03-05'),
(6, 'emma_white', 'f2d81a260dea8b100dd6542b44f7b237e40348b11b15886618c07e036b5a10cc', 'c6a2b8e0b7b8a7b0e1b6f3c8a9f0b5d4e3f2a1c0d9e8b7a6f5d4c3b2a1e0f9d8', 'customer', '2024-04-10'),
(7, 'liam_brown', '5f4dcc3b5aa765d61d8327deb882cf99574f1b7f2f5f7f2b7f3b6a9c8b7f5b3a', 'd0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1', 'customer', '2024-05-01'),
(8, 'sophia_clark', '3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1', '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b', 'customer', '2024-05-15'),
(9, 'Bryanisinthekitchen', '8a4f5b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a', 'f1e2d3c4b5a6f7e8d9c0b1a2e3f4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0e1f2', 'driver', '2024-02-15'),
(10, 'Maxivitesse', 'b1a0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0', 'a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1', 'driver', '2024-03-20'),
(11, 'james_lewis', '1b2a3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b', 'c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4', 'admin', '2024-01-20'),
(12, 'ava_walker', 'f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8', 'e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5', 'customer', '2024-06-01'),
(13, 'william_hall', 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', 'b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3', 'customer', '2024-06-10');

INSERT INTO fd.address (city, postal_code, street_name, street_number) VALUES
('Rennes', '35000', 'Rue de la Soif', 10),
('Rennes', '35000', 'Place de la Mairie', 25),
('Rennes', '35200', 'Avenue Jean Jaurès', 50),
('Rennes', '35700', 'Rue de Fougères', 15),
('Rennes', '35000', 'Place Sainte-Anne', 100);

INSERT INTO fd.customer (id_user, name, phone_number) VALUES
(4, 'John Doe', '+33 6 01 02 03 04'),
(2, 'Jane Smith', '+33 6 12 34 56 78'),
(5, 'Charlie Customer', '+33 6 23 45 67 89'),
(6, 'Emma White', '+33 6 06 06 06 06'),
(7, 'Liam Brown', '+33 6 07 07 07 07'),
(8, 'Sophia Clark', '+33 6 08 08 08 08'),
(12, 'Ava Walker', '+33 6 12 12 12 12'),
(13, 'William Hall', '+33 6 13 13 13 13');

INSERT INTO fd.admin (id_user, name, phone_number) VALUES
(1, 'Groupe 8', '+33 7 69 52 27 94');

INSERT INTO fd.driver (id_user, name, phone_number, vehicle_type, availability) VALUES
(3, 'Bob Driver', '+33 6 45 67 89 01', 'Bike', TRUE),
(9, 'Bryan Donato Da Costa', '+33 6 56 87 46 89', 'Car', TRUE),
(10, 'Maxine Voinson', '+33 6 67 54 78 91', 'Car', TRUE);

INSERT INTO fd.item (name, item_type, price, stock, availability) VALUES
('Banh mi', 'main', 10.50, 20, TRUE),
('Fajitas', 'main', 14.00, 15, TRUE),
('Galettes bretonnes', 'main', 9.00, 30, TRUE),
('Caesar Salad', 'starter', 8.50, 10, TRUE),
('Greek Salad', 'starter', 7, 10, TRUE),
('Tarte aux pommes', 'dessert', 6.00, 8, TRUE),
('Coca Cola', 'drink', 3.00, 30, TRUE),
('Mineral Water', 'drink', 2.00, 25, TRUE),
('Lemonade', 'drink', 3, 20, TRUE),
('Classic Burger', 'main', 11.00, 12, TRUE),
('Fries', 'side', 3, 18, TRUE),
('Mozzarella sticks', 'side', 4, 15, TRUE);

INSERT INTO fd.bundle (name, description, bundle_type, required_item_types,  price, discount) VALUES
('Banh mi Menu', 'Banh mi + Drink + Dessert', 'predefined', NULL, 17.00, NULL),
('Burger Menu', 'Burger + Fries + Drink', 'predefined', NULL, 16.00, NULL);

INSERT INTO fd.bundle (name, description, bundle_type, required_item_types, price, discount) VALUES
('Promo for couple', 'Buy 2 main, get 10% off', 'discount', ARRAY['main', 'main'], NULL, 0.10),
('Main and drink', '', 'discount', ARRAY['main', 'drink'], NULL, 0.20),
('Complete bundle', '', 'discount', ARRAY['starter', 'main', 'dessert'], NULL, 0.2);

INSERT INTO fd.bundle_item (id_bundle, id_item) VALUES
(1, 1),
(1, 9),
(1, 6),
(2, 9),
(2, 10),
(2, 11);

INSERT INTO fd.order (id_user, status, price, id_address, order_date) VALUES
(1, 'delivered', 13.5, 1, '2024-10-01 12:30:00'),
(2, 'in_progress', 31, 2, '2024-10-06 18:45:00'),
(5, 'pending', 19, 3, '2024-10-06 19:15:00'),
(4, 'in_progress', 11, 4, '2024-10-06 20:00:00'),
(4, 'in_progress', 15.5, 5, '2024-10-06 20:05:00'); 

INSERT INTO fd.delivery (id_driver, status, delivery_time) VALUES
(3, 'completed', '2024-10-01 13:15:00'),
(3, 'in_progress', NULL),
(3, 'in_progress', NULL);

INSERT INTO fd.delivery_order (id_delivery, id_order) VALUES
(1, 1),
(2, 2),
(2, 4),
(2, 5);

INSERT INTO fd.order_item (id_order, id_item) VALUES
(1, 1),
(1, 6),
(2, 2),
(2, 2),
(2, 8),
(3, 9),
(3, 10),
(3, 5),
(4, 3),
(4, 7),
(5, 4),
(5, 11),
(5, 6);


SELECT setval('fd.user_id_user_seq', (SELECT MAX(id_user) FROM fd.user));
SELECT setval('fd.address_id_address_seq', (SELECT MAX(id_address) FROM fd.address));
SELECT setval('fd.item_id_item_seq', (SELECT MAX(id_item) FROM fd.item));
SELECT setval('fd.bundle_id_bundle_seq', (SELECT MAX(id_bundle) FROM fd.bundle));
SELECT setval('fd.order_id_order_seq', (SELECT MAX(id_order) FROM fd.order));
SELECT setval('fd.delivery_id_delivery_seq', (SELECT MAX(id_delivery) FROM fd.delivery));