import random

# --- Variables Globales Corrigées ---
# (pop_db s'arrête à 11 pour les items et 5 pour les bundles)
next_item_id = 13
next_bundle_id = 6
# Doit suivre l'ID maximum des articles pour les associations de bundles
max_item_id = 11


def generate_bulk_items(db_connector, item_count=5000):
    """
    Génère et insère un grand nombre d'articles en une seule requête (bulk insert).
    """
    # Indique que nous MODIFIONS ces variables globales
    global next_item_id, max_item_id

    print(f"Génération de {item_count} articles...")
    realistic_dishes = [
        {"name": "Classic Burger", "type": "main"},
        {"name": "Pad Thai", "type": "main"},
        {"name": "Carbonara Pasta", "type": "main"},
        {"name": "Bolognese Lasagna", "type": "main"},
        {"name": "Roast Chicken", "type": "main"},
        {"name": "Grilled Steak", "type": "main"},
        {"name": "Cantonese Fried Rice", "type": "main"},
        {"name": "Caesar Salad", "type": "starter"},
        {"name": "Soup of the Day", "type": "starter"},
        {"name": "Bruschetta", "type": "starter"},
        {"name": "Beef Carpaccio", "type": "starter"},
        {"name": "Gazpacho", "type": "starter"},
        {"name": "Tiramisu", "type": "dessert"},
        {"name": "Chocolate Mousse", "type": "dessert"},
        {"name": "Crème Brûlée", "type": "dessert"},
        {"name": "Apple Tart", "type": "dessert"},
        {"name": "Panna Cotta", "type": "dessert"},
        {"name": "Fresh Orange Juice", "type": "drink"},
        {"name": "Coffee", "type": "drink"},
        {"name": "Green Tea", "type": "drink"},
        {"name": "Homemade Lemonade", "type": "drink"},
        {"name": "Strawberry Smoothie", "type": "drink"},
        {"name": "French Fries", "type": "side"},
        {"name": "Grilled Vegetables", "type": "side"},
        {"name": "Mashed Potatoes", "type": "side"},
        {"name": "Steamed Rice", "type": "side"},
        {"name": "Green Salad", "type": "side"},
        {"name": "Onion Rings", "type": "side"},
        {"name": "Garlic Bread", "type": "side"},
    ]

    complete_list = realistic_dishes * (item_count // len(realistic_dishes) + 1)
    random.shuffle(complete_list)
    items_sql_values = []

    for i in range(item_count):
        # CORRECTION: Faute de frappe (item_next_id -> next_item_id)
        item_id = next_item_id + i

        dish = complete_list[i]
        name = dish["name"].replace("'", "''")
        item_type = dish["type"]
        price = round(random.uniform(3.5, 25.0), 2)
        stock = random.randint(0, 100)
        availability = "TRUE" if stock > 0 else "FALSE"

        items_sql_values.append(f"({item_id}, '{name}', '{item_type}', {price}, {stock}, {availability})")

    full_query = "INSERT INTO fd.item (id_item, name, item_type, price, stock, availability) VALUES "
    full_query += ", ".join(items_sql_values)
    full_query += ";"

    try:
        db_connector.sql_query(full_query, return_type=None)
        print(f"{item_count} articles ajoutés avec succès.")

        # CORRECTION: Mettre à jour les variables globales
        next_item_id += item_count
        max_item_id = next_item_id - 1  # Met à jour l'ID max pour la prochaine fonction

    except Exception as e:
        print(f"Erreur lors de l'insertion de masse des articles : {e}")
        raise


def generate_discounted_bundles(db_connector, bundle_count=1000):
    """
    Génère et insère un grand nombre de "discounted bundles".
    """
    # Indique que nous MODIFIONS cette variable globale
    global next_bundle_id

    print(f"Génération de {bundle_count} bundles de réduction...")
    realistic_bundles = [
        {"name": "Lunch Deal", "types": ["main", "drink"]},
        {"name": "Full Menu", "types": ["starter", "main", "dessert"]},
        {"name": "Duo Offer", "types": ["main", "main"]},
        {"name": "Sweet Break", "types": ["drink", "dessert"]},
        {"name": "Healthy Menu", "types": ["starter", "main"]},
        {"name": "Kids Menu", "types": ["main", "drink", "dessert"]},
        {"name": "Quick Bite", "types": ["starter", "main"]},
        {"name": "Coffee & Cake", "types": ["drink", "dessert"]},
        {"name": "Snack Combo", "types": ["starter", "drink"]},
        {"name": "Classic Trio", "types": ["main", "side", "drink"]},
        {"name": "Family Pack", "types": ["main", "main", "side"]},
        {"name": "Gourmet Selection", "types": ["starter", "main", "dessert", "drink"]},
        {"name": "Express Menu", "types": ["main", "side"]},
        {"name": "Light Meal", "types": ["starter", "drink"]},
        {"name": "Dessert Lover Pack", "types": ["dessert", "dessert", "drink"]},
        {"name": "Brunch Formula", "types": ["main", "drink", "side"]},
        {"name": "Couple Menu", "types": ["starter", "main", "main", "drink"]},
        {"name": "Student Deal", "types": ["main", "drink"]},
        {"name": "Afterwork Pack", "types": ["drink", "drink", "side"]},
        {"name": "Balanced Plate", "types": ["starter", "main", "side"]},
        {"name": "Premium Menu", "types": ["starter", "main", "dessert", "side"]},
        {"name": "Weekend Special", "types": ["main", "main", "dessert"]},
        {"name": "Tea Time Set", "types": ["drink", "dessert"]},
        {"name": "Energy Combo", "types": ["drink", "drink", "main"]},
        {"name": "Comfort Meal", "types": ["main", "side", "dessert"]},
        {"name": "Sharing Board", "types": ["starter", "starter", "drink"]},
        {"name": "Double Delight", "types": ["dessert", "drink"]},
        {"name": "Light & Fresh", "types": ["starter", "side"]},
        {"name": "Deli Box", "types": ["main", "dessert"]},
        {"name": "Full Experience", "types": ["starter", "main", "side", "dessert", "drink"]},
    ]

    liste_complete = realistic_bundles * (bundle_count // len(realistic_bundles) + 1)
    random.shuffle(liste_complete)
    bundle_sql_values = []

    for i in range(bundle_count):
        bundle_id = next_bundle_id + i
        bundle_data = liste_complete[i]
        name = bundle_data["name"].replace("'", "''")
        bundle_type = "discount"
        discount = round(random.uniform(0.05, 0.50), 2)
        types_list = bundle_data["types"]
        formatted_types = ", ".join([f"'{t}'" for t in types_list])
        sql_array = f"ARRAY[{formatted_types}]"

        bundle_sql_values.append(f"({bundle_id}, '{name}', '', '{bundle_type}', {sql_array}, NULL, {discount})")

    full_query = "INSERT INTO fd.bundle (id_bundle, name, description, bundle_type, required_item_types, price, discount) VALUES "
    full_query += ", ".join(bundle_sql_values)
    full_query += ";"

    try:
        db_connector.sql_query(full_query, return_type=None)
        print(f"{bundle_count} bundles de réduction ajoutés avec succès.")

        # CORRECTION: Mettre à jour la variable globale
        next_bundle_id += bundle_count

    except Exception as e:
        print(f"Erreur lors de l'insertion de masse des bundles : {e}")
        raise


# CORRECTION: La fonction a été dés-indentée
def generate_predefined_bundles(db_connector, bundle_count=500, items_per_bundle=3):
    """
    Génère des bundles prédéfinis (menus) et les associe à des articles
    dans fd.bundle_item.
    """
    # Indique que nous LISONS max_item_id et MODIFIONS next_bundle_id
    global next_bundle_id, max_item_id

    print(f"Génération de {bundle_count} bundles prédéfinis...")
    realistic_names = [
        "Classic Menu",
        "Express Formula",
        "Pizza Menu",
        "Burger Menu",
        "Evening Offer",
        "Student Menu",
        "Family Menu",
        "Chef’s Selection",
        "Lunch Special",
        "Brunch Menu",
        "Kids Menu",
        "Healthy Choice",
        "Gourmet Menu",
        "Weekend Deal",
        "Daily Special",
        "Sweet Break",
        "Snack Combo",
        "Couple Menu",
        "Happy Hour Offer",
        "Comfort Menu",
        "Signature Menu",
        "Light Meal",
        "Tasting Menu",
        "Sharing Menu",
        "Premium Menu",
        "Morning Deal",
        "Grab & Go",
        "Dinner Box",
        "Full Experience",
        "Seasonal Menu",
    ]

    bundle_sql_values = []
    bundle_item_sql_values = []

    for i in range(bundle_count):
        bundle_id = next_bundle_id + i
        name = random.choice(realistic_names)
        bundle_type = "predefined"
        price = round(random.uniform(15.0, 25.0), 2)

        bundle_sql_values.append(f"({bundle_id}, '{name}', '', '{bundle_type}', NULL, {price}, NULL)")

        for _ in range(items_per_bundle):
            # CORRECTION: Utilise la variable globale max_item_id
            random_item_id = random.randint(1, max_item_id)
            bundle_item_sql_values.append(f"({bundle_id}, {random_item_id})")

    next_bundle_id += bundle_count

    bundle_query = "INSERT INTO fd.bundle (id_bundle, name, description, bundle_type, required_item_types, price, discount) VALUES "
    bundle_query += ", ".join(bundle_sql_values) + ";"

    bundle_item_query = "INSERT INTO fd.bundle_item (id_bundle, id_item) VALUES "
    bundle_item_query += ", ".join(bundle_item_sql_values) + ";"

    try:
        print(f"Insertion de {len(bundle_sql_values)} bundles prédéfinis...")
        db_connector.sql_query(bundle_query, return_type=None)

        print(f"Insertion de {len(bundle_item_sql_values)} associations bundle-item...")
        db_connector.sql_query(bundle_item_query, return_type=None)

        print("Bundles prédéfinis ajoutés avec succès.")

    except Exception as e:
        print(f"Erreur lors de l'insertion de masse des bundles prédéfinis : {e}")
        raise
