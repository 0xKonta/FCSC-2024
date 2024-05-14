import zipfile

# Remplacez 'archive.zip' par le chemin vers votre fichier zip
chemin_archive = r'archive.zip'

# Ouvrir l'archive en mode lecture
with zipfile.ZipFile(chemin_archive, 'r') as archive:
    # Obtenir la liste des fichiers contenus dans l'archive
    liste_fichiers = archive.namelist()
    print("Liste des fichiers dans l'archive:")
    for fichier in liste_fichiers:
        print(fichier)
    
    # Obtenir des informations détaillées sur chaque fichier
    print("\nInformations détaillées sur les fichiers dans l'archive:")
    for info in archive.infolist():
        print(f"Nom du fichier: {info.filename}")
        print(f"Date et heure de modification: {info.date_time}")
        print(f"Taille compressée: {info.compress_size} octets")
        print(f"Taille réelle: {info.file_size} octets")
        print("-" * 30)


try:
    with zipfile.ZipFile(chemin_archive, 'r') as archive:
        # Récupérer les informations globales de l'archive, y compris les commentaires
        info_globale = archive.comment.decode('utf-8')
        print("Commentaire global de l'archive :")
        print(info_globale)
except zipfile.BadZipFile:
    print("Le fichier n'est pas une archive ZIP valide ou est corrompu.")

import binascii

def afficher_hexadecimal(chemin_fichier):
    try:
        with open(chemin_fichier, 'rb') as fichier:
            contenu = fichier.read()
            hexa = binascii.hexlify(contenu)
            return hexa.decode('utf-8')
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

f = afficher_hexadecimal(chemin_archive)

import binascii

def hex_to_printable_text(hex_string):
    # Convertir la chaîne hexadécimale en bytes
    byte_data = binascii.unhexlify(hex_string)
    # Décoder les bytes en texte, en ignorant les erreurs de décodage
    text = byte_data.decode('utf-8', 'ignore')
    # Filtrer et imprimer uniquement les caractères imprimables
    printable_text = ''.join(char for char in text if char.isprintable())
    print(printable_text)


import zipfile
import datetime
import os

def afficher_metadonnees_zip(chemin_archive):
    # Vérifier si le fichier existe
    if not os.path.exists(chemin_archive):
        print("Le fichier spécifié n'existe pas.")
        return

    # Ouvrir l'archive ZIP en lecture
    with zipfile.ZipFile(chemin_archive, 'r') as zip:
        # Afficher les métadonnées globales de l'archive
        print(f"Commentaire de l'archive: {zip.comment.decode('utf-8')}")
        print(f"Nombre de fichiers dans l'archive: {len(zip.namelist())}")

        # Parcourir chaque fichier dans l'archive
        for info in zip.infolist():
            print(f"\nNom du fichier: {info.filename}")
            print(f"Date de modification: {datetime.datetime(*info.date_time)}")
            print(f"Taille compressée: {info.compress_size} octets")
            print(f"Taille réelle: {info.file_size} octets")
            print(f"Est-ce un dossier: {'Oui' if info.is_dir() else 'Non'}")
            # Afficher les commentaires de fichier, s'ils existent
            commentaire = zip.getinfo(info.filename).comment.decode('utf-8')
            print(f"Commentaire du fichier: {commentaire if commentaire else 'Aucun'}")

afficher_metadonnees_zip(chemin_archive)
