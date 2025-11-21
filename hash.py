import random
import string
from src.Service.password_service import PasswordService

def generate_valid_password():
    """
    Génère un mot de passe aléatoire respectant les critères de sécurité
    (Majuscule, minuscule, chiffre, caractère spécial, min 8 caractères).
    """
    length = 12
    # On s'assure d'avoir au moins un caractère de chaque type requis
    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()")
    
    # On complète le reste aléatoirement
    others = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()", k=length - 4))
    
    # On mélange le tout
    password_list = list(upper + lower + digit + special + others)
    random.shuffle(password_list)
    return "".join(password_list)

def main():
    # Instanciation du service
    password_service = PasswordService()
    
    print(f"{'Index':<5} | {'Password (Valid)':<20} | {'Salt (Random)':<64} | {'Hash (SHA-256)':<64}")
    print("-" * 160)

    for i in range(1, 14): # De 1 à 13
        # 1. Génération d'un mot de passe valide
        password = generate_valid_password()
        
        # Vérification par sécurité (optionnel, pour garantir la validité selon le service)
        try:
            password_service.check_password_strength(password)
        except ValueError as e:
            print(f"Erreur de génération : {e}")
            continue

        # 2. Génération du sel via le service
        salt = password_service.create_salt()

        # 3. Hashage du mot de passe avec le sel via le service
        hashed_password = password_service.hash_password(password, salt)

        # Affichage
        print(f"{i:<5} | {password:<20} | {salt:<64} | {hashed_password:<64}")

if __name__ == "__main__":
    main()