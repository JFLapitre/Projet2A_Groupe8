-- Insertion des utilisateurs
INSERT INTO fd.user (username, password, sign_up_date) VALUES
('john_doe', 'password123', '2024-01-15'),
('jane_smith', 'securepass456', '2024-02-20'),
('bob_driver', 'driverpass789', '2024-01-10'),
('alice_admin', 'adminpass321', '2024-01-01'),
('charlie_customer', 'custpass654', '2024-03-05');

-- Insertion des adresses
INSERT INTO fd.address (city, postal_code, street_name, street_number) VALUES
('Paris', '75001', 'Rue de Rivoli', 10),
('Lyon', '69001', 'Rue de la République', 25),
('Marseille', '13001', 'La Canebière', 50),
('Toulouse', '31000', 'Rue Alsace Lorraine', 15),
('Nice', '06000', 'Promenade des Anglais', 100);

-- Insertion des clients
INSERT INTO fd.customer (id_user, name, phone_number) VALUES
(1, 'John Doe', '0601020304'),
(2, 'Jane Smith', '0612345678'),
(5, 'Charlie Customer', '0623456789');

-- Insertion de l'admin
INSERT INTO fd.admin (id_user, name, phone_number) VALUES
(4, 'Alice Admin', '0634567890');

-- Insertion du livreur
INSERT INTO fd.driver (id_user, name, phone_number, vehicle_type, availability) VALUES
(3, 'Bob Driver', '0645678901', 'Scooter', TRUE);

-- Insertion des items
INSERT INTO fd.item (name, item_type, price) VALUES
('Pizza Margherita', 'main', 12.50),
('Pizza 4 Fromages', 'main', 14.00),
('Salade César', 'starter', 8.50),
('Tiramisu', 'dessert', 6.00),
('Coca Cola', 'drink', 3.00),
('Eau Minérale', 'drink', 2.00),
('Burger Classique', 'main', 11.00),
('Frites', 'side', 4.50);

-- Insertion des bundles prédéfinis
INSERT INTO fd.bundle (name, description, bundle_type, price, discount) VALUES
('Menu Pizza', 'Pizza + Boisson + Dessert', 'predefined', 19.00, NULL),
('Menu Burger', 'Burger + Frites + Boisson', 'predefined', 16.00, NULL);

-- Insertion des bundles avec remise
INSERT INTO fd.bundle (name, description, bundle_type, price, discount) VALUES
('Promo 2 Pizzas', 'Achetez 2 pizzas, obtenez 10% de réduction', 'discount', NULL, 0.10),
('Happy Hour', 'Réduction de 20% sur toute commande avant 19h', 'discount', NULL, 0.20);

-- Association items aux bundles prédéfinis
INSERT INTO fd.bundle_item (id_bundle, id_item) VALUES
-- Menu Pizza (bundle 1) : Pizza Margherita + Coca + Tiramisu
(1, 1),
(1, 5),
(1, 4),
-- Menu Burger (bundle 2) : Burger + Frites + Coca
(2, 7),
(2, 8),
(2, 5);

-- Insertion des commandes
INSERT INTO fd.order (id_user, status, address, order_date) VALUES
(1, 'delivered', '10 Rue de Rivoli, 75001 Paris', '2024-10-01 12:30:00'),
(2, 'in_progress', '25 Rue de la République, 69001 Lyon', '2024-10-06 18:45:00'),
(5, 'pending', '50 La Canebière, 13001 Marseille', '2024-10-06 19:15:00');

-- Association commandes aux bundles
INSERT INTO fd.order_bundle (id_order, id_bundle) VALUES
(1, 1), -- Commande 1 : Menu Pizza
(2, 2), -- Commande 2 : Menu Burger
(2, 3), -- Commande 2 : Promo 2 Pizzas
(3, 1); -- Commande 3 : Menu Pizza

-- Insertion des livraisons
INSERT INTO fd.delivery (id_driver, status, delivery_time) VALUES
(3, 'completed', '2024-10-01 13:15:00'),
(3, 'in_progress', NULL),
(NULL, 'pending', NULL);

-- Association livraisons aux commandes
INSERT INTO fd.delivery_order (id_delivery, id_order) VALUES
(1, 1), -- Livraison 1 pour commande 1
(2, 2), -- Livraison 2 pour commande 2
(3, 3); -- Livraison 3 pour commande 3