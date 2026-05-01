from cryptography.fernet import Fernet

# Génère une clé sécurisée
key = Fernet.generate_key()
print(f"Ta clé secrète à copier dans tous les scripts : {key.decode()}")