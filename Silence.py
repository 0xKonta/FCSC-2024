import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Paramètres donnés
salt = base64.b64decode("9Be77hAJpDuviHX1s3iL6Q==")
iterations = 18743
encrypted_message = base64.b64decode("+JIHX/5asdvF2nhKhwtORrG5OvlNvDKP5rZV6vo+lcyoVZbHkIBiACVLlQbv72Wb31Pwvc4vZZAMUIq6VvyYyFr9d8U=")

# Fonction pour générer la clé à partir du mot de passe
def generate_key(passphrase):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        length=16,  # AES 128 bits nécessite une clé de 16 bytes
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())
    return key

# Fonction pour déchiffrer le message
def decrypt_message(key, encrypted_message):
    # AES-CBC nécessite un vecteur d'initialisation de 16 bytes
    iv = encrypted_message[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    return decrypted_message

# Tester tous les mots de passe possibles de 00000 à 99999
for i in range(0,100000):
    passphrase = f"{i:05d}"  # Formatte le nombre en chaîne de 5 chiffres
    key = generate_key(passphrase)
    print(passphrase)
    try:
        decrypted_message = decrypt_message(key, encrypted_message)
        print(f"Passphrase: {passphrase}, Decrypted Message: {decrypted_message}")
        break  # Arrêter si le message est déchiffré avec succès
    except Exception as e:
        continue  # Ignorer les erreurs et continuer avec le prochain mot de passe
