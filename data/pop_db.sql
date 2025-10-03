-- Insertion de données dans user
INSERT INTO fd.user (username, password, sign_up_date) VALUES
('john_doe', 'password123', '2023-01-15'),
('jane_smith', 'securepass', '2023-02-20'),
('admin_user', 'adminpass', '2023-03-10'),
('driver1', 'driverpass', '2023-04-05');

-- Insertion de données dans customer
INSERT INTO fd.customer (id_user, name, phone_number) VALUES
(1, 'John Doe', '0612345678'),
(2, 'Jane Smith', '0687654321');

-- Insertion de données dans admin
INSERT INTO fd.admin (id_user, name, phone_number) VALUES
(3, 'Admin User', '0611223344');

-- Insertion de données dans driver
INSERT INTO fd.driver (id_user, name, phone_number, vehicle_type, license_plate) VALUES
(4, 'Driver One', '0655667788', 'scooter', 'AB-123-CD');

-- Insertion de données dans item
INSERT INTO fd.item (name, item_type, price) VALUES
('Hamburger', 'plat', 8.99),
('Cheeseburger', 'plat', 9.99),
('Frites', 'accompagnement', 3.49),
('Salade', 'accompagnement', 4.99),
('Coca-Cola', 'boisson', 2.49),
('Eau', 'boisson', 1.99),
('Pizza', 'plat', 12.99),
('Nuggets', 'plat', 6.99);

-- Insertion de données dans bundle
INSERT INTO fd.bundle (name, description, bundle_type, price, discount, item_types) VALUES
('Menu Burger', 'Un hamburger, des frites et une boisson', 'predefined', 14.99, NULL, NULL),
('Menu Économique', 'Choisissez un plat, une boisson et un accompagnement et obtenez 20% de réduction', 'discount', NULL, 20, 'plat,boisson,accompagnement');

-- Insertion de données dans bundle_item (pour le predefined bundle)
INSERT INTO fd.bundle_item (id_bundle, id_item) VALUES
(1, 1), -- Hamburger
(1, 3), -- Frites
(1, 5); -- Coca-Cola

-- Insertion de données dans order
INSERT INTO fd.order (id_user, status, address) VALUES
(1, 'en cours', '123 Rue Principale, Paris'),
(2, 'terminée', '456 Avenue Secondaire, Lyon');

-- Insertion de données dans order_bundle
INSERT INTO fd.order_bundle (id_order, id_bundle) VALUES
(1, 1), -- Commande 1 contient le Menu Burger
(2, 2); -- Commande 2 contient le Menu Économique

-- Insertion de données dans delivery
INSERT INTO fd.delivery (id_driver, status, delivery_time) VALUES
(4, 'en cours', '2023-05-20 14:30:00'),
(4, 'terminée', '2023-05-19 12:15:00');

-- Insertion de données dans delivery_order
INSERT INTO fd.delivery_order (id_delivery, id_order) VALUES
(1, 1),
(2, 2);