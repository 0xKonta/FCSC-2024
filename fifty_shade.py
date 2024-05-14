import base64

# Contenu encodé en Base64 du fichier de licence
encoded_license = """
TmFtZTogV2FsdGVyIFdoaXRlIEp1bmlvcgpTZXJpYWw6IDFkMTE3YzVhLTI5N2QtNGNlNi05MTg2LWQ0Yjg0ZmI3ZjIzMApUeXBlOiAxCg==
"""

# Décodage du contenu
decoded_license = base64.b64decode(encoded_license).decode('utf-8')


def generate_key(name, serial, type):
    # Ici, vous devez implémenter la logique pour générer la clé basée sur le nom, le numéro de série et le type.
    # Cette partie dépend de la manière dont le binaire valide la clé.
    key = f"{name}-{serial}-{type}"
    return key


import hashlib

def hash_data(data):
    # Créer un nouvel objet hash SHA-256
    hash_obj = hashlib.sha256()
    
    # Mettre à jour l'objet hash avec les données (qui doivent être des bytes)
    hash_obj.update(data.encode('utf-8'))
    
    # Obtenir le digest haché en hexadécimal
    hash_digest = hash_obj.hexdigest()
    
    return hash_digest




def validate(arg1, arg2):
    # Compute SHA-256 hash of arg2
    arg2_hash = hashlib.sha256(arg2.encode()).digest()
    
    var_ch = 1
    for var_10h in range(3):
        var_14h = 0
        var_20h = var_10h
        while var_20h < len(arg1):
            var_14h += ord(arg1[var_20h])
            var_20h += 3
        
        var_24h = (var_14h * 0x13 + 0x37) % 0x7f
        var_2ch = (arg2_hash[var_10h] * 0x37 + 0x13) % 0x7f
        var_ch &= (var_24h == var_2ch)
    
    return var_ch


#print("Result:", result)

import hashlib
import uuid

def generate_arg2(arg1):
    arg2 = str(uuid.uuid4())
    
    # Vérifier si cet arg2 fonctionne avec arg1
    return arg2, validate(arg1, arg2)

def generate_valid_strings(arg2_hash):
    valid_strings = []
    # Nous limitons la recherche à des chaînes de longueur 3 pour simplifier
    for i in range(32, 127):  # Caractères imprimables ASCII
        for j in range(32, 127):
            for k in range(32, 127):
                arg1 = chr(i) + chr(j) + chr(k)
                if validate(arg1, arg2_hash):
                    print(arg1)
                    valid_strings.append(arg1)
    return valid_strings


# Exemple d'utilisation
arg1 = "Walter White Junior"
#for i in range(0,30000000):
#    arg2, c = generate_valid_strings(arg1)


import socket

# Paramètres de connexion
serveur = 'challenges.france-cybersecurity-challenge.fr'
port = 2250

import socket
import re

def get_rep(n):
    for i in range(0,100000000):
        arg2, c = generate_arg2(n)
        if c == 1:
            return arg2

def creer_licence_base64(nom, reponse):
    # Création du contenu de la licence
    contenu = f"Name: {nom}\nSerial: {reponse}\nType: 1337\n"
    
    # Encodage en base64
    contenu_base64 = base64.b64encode(contenu.encode()).decode()
    
    # Préparation du format final avec les marqueurs de début et de fin
    debut = "----BEGIN WHITE LICENSE----\n"
    fin = "\n-----END WHITE LICENSE-----"
    
    # Ajout des retours à la ligne pour que la longueur de la ligne base64 ne dépasse pas celle du marqueur de début
    max_length = len(debut.strip())
    lignes_base64 = [contenu_base64[i:i+max_length] for i in range(0, len(contenu_base64), max_length)]
    contenu_base64_avec_retours = "\n".join(lignes_base64)
    
    # Assemblage final de la licence
    licence_complete = debut + contenu_base64_avec_retours + fin
    
    return licence_complete

serveur = 'challenges.france-cybersecurity-challenge.fr'
port = 2250

#print(creer_licence_base64("Walter White Junior","1d117c5a-297d-4ce6-9186-d4b84fb7f230"))

# Création d'un socket

import socket
import re



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((serveur, port))
    
    received_data = ""  # Accumuler les données reçues pour la recherche
    for _ in range(50):  # Répéter l'opération 50 fois
        while True:
            donnees = s.recv(1024)
            if not donnees:
                break
            
            received_data += donnees.decode('utf-8')
            print("Données reçues:", received_data)
            name = None
            for fdsf in received_data.split('\n'):
                if "Give me a valid" in fdsf:
                    name = fdsf.split(': ')[1]
            if name:
                print(name)
                print("Nom d'utilisateur trouvé:", name)
                
                reponse = get_rep(name)
                reponse = creer_licence_base64(name, reponse)
                print("Réponse envoyée:", reponse)
                
                message = (reponse + "\n").encode('utf-8')
                s.sendall(message)
                s.sendall(("\n").encode('utf-8'))
                
                received_data = ""  # Réinitialiser les données accumulées après traitement
                break
            
    while True:
        donnees_suivantes = s.recv(1024)
        if not donnees_suivantes:
            break
        print("Données suivantes reçues:", donnees_suivantes.decode('utf-8'))

