
from PIL import Image
import pygame
import sys


chemin_image = r"puzzle-trouble-easy.jpg" 
# Charger l'image et la découper en carrés proportionnels
def charger_et_decouper_image(chemin_image, nb_lignes, nb_colonnes):
    image = Image.open(chemin_image)
    largeur, hauteur = image.size
    taille_carre_largeur = largeur // nb_colonnes
    taille_carre_hauteur = hauteur // nb_lignes
    taille_carre = min(taille_carre_largeur, taille_carre_hauteur)
    
    carrés = []

    for y in range(0, nb_lignes * taille_carre, taille_carre):
        for x in range(0, nb_colonnes * taille_carre, taille_carre):
            carré = image.crop((x, y, x + taille_carre, y + taille_carre))
            carrés.append((carré, (x, y)))

    return carrés, taille_carre

# Initialiser pygame
pygame.init()

# Taille de la grille
nb_lignes, nb_colonnes = 8, 8

carrés, taille_carre = charger_et_decouper_image(chemin_image, nb_lignes, nb_colonnes)

# Définir la taille de la fenêtre
taille_fenetre = (2324, 1024) 
écran = pygame.display.set_mode(taille_fenetre)

# Convertir les carrés PIL en surfaces pygame et stocker leur position initiale
surfaces = [(pygame.image.fromstring(carré.tobytes(), carré.size, carré.mode), pos) for carré, pos in carrés]

carré_selectionné = None
offset_x, offset_y = 0, 0

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i, (surface, pos) in enumerate(surfaces):
                rect = pygame.Rect(pos, (taille_carre, taille_carre))
                if rect.collidepoint(x, y):
                    carré_selectionné = i
                    offset_x = pos[0] - x
                    offset_y = pos[1] - y
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if carré_selectionné is not None:
                surfaces[carré_selectionné] = (surfaces[carré_selectionné][0], (x + offset_x, y + offset_y))
                carré_selectionné = None
        elif event.type == pygame.MOUSEMOTION and carré_selectionné is not None:
            x, y = event.pos
            surfaces[carré_selectionné] = (surfaces[carré_selectionné][0], (x + offset_x, y + offset_y))

    écran.fill((0, 0, 0))  # Effacer l'écran avec du noir

    # Afficher les carrés
    for surface, pos in surfaces:
        écran.blit(surface, pos)

    pygame.display.flip()
