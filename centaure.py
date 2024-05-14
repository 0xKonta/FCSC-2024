import base64
import io
from PIL import Image
import socket
from collections import deque
import matplotlib.pyplot as plt
import random
import time
import networkx as nx
import math
from itertools import combinations

def is_black(pixel):
    if isinstance(pixel, int):  
        return pixel == 0
    else:  
        return pixel[:3] == (0, 0, 0)

def update_edges(segment):
    width, height = segment.size
    middle_x, middle_y = width // 2, height // 2
    edge_presence = EdgePresence()
    
    edge_presence.top = is_black(segment.getpixel((middle_x, 0)))
    edge_presence.bottom = is_black(segment.getpixel((middle_x, height - 1)))
    edge_presence.left = is_black(segment.getpixel((0, middle_y)))
    edge_presence.right = is_black(segment.getpixel((width - 1, middle_y)))
    
    edge_presence.top_left_corner = is_black(segment.getpixel((4, 4)))
    edge_presence.top_right_corner = is_black(segment.getpixel((width - 5, 4)))
    edge_presence.bottom_left_corner = is_black(segment.getpixel((4, height - 5)))
    edge_presence.bottom_right_corner = is_black(segment.getpixel((width - 5, height - 5)))
    
    return edge_presence

class EdgePresence:
    def __init__(self):
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False
        self.top_left_corner = False
        self.top_right_corner = False
        self.bottom_left_corner = False
        self.bottom_right_corner = False

    def __str__(self):
        return (
            f"Top: {self.top}, Bottom: {self.bottom}, "
            f"Left: {self.left}, Right: {self.right}, "
            f"Top Left Corner: {self.top_left_corner}, Top Right Corner: {self.top_right_corner}, "
            f"Bottom Left Corner: {self.bottom_left_corner}, Bottom Right Corner: {self.bottom_right_corner}"
        )

def visualiser_graphe(sommets):
    G = nx.Graph()
    
    # Ajouter les sommets au graphe
    for row in sommets:
        for sommet in row:
            G.add_node(sommet.id, pos=(sommet.x, len(sommets) - 1 - sommet.y))
    
    # Ajouter les arêtes au graphe
    for row in sommets:
        for sommet in row:
            for voisin in sommet.voisins:
                G.add_edge(sommet.id, voisin.id)
    
    # Récupérer les positions des sommets
    pos = nx.get_node_attributes(G, 'pos')
    
    # Créer une seule figure et un seul axe
    fig, ax = plt.subplots()
    
    # Dessiner le graphe initial
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, ax=ax)
    labels = {sommet.id: sommet.id for row in sommets for sommet in row}
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', ax=ax)
    
    # Fonction pour mettre à jour la visualisation lors du survol
    def update_hover(event):
        if event.inaxes == ax:
            ax.clear()
            nx.draw_networkx_edges(G, pos, ax=ax)
            
            hover_node = None
            for row in sommets:
                for sommet in row:
                    if abs(sommet.x - event.xdata) < 0.5 and abs(len(sommets) - 1 - sommet.y - event.ydata) < 0.5:
                        hover_node = sommet
                        break
                if hover_node:
                    break
            
            if hover_node:
                hover_nodes = [hover_node.id] + [v.id for v in hover_node.voisins]
                hover_edges = [(hover_node.id, v.id) for v in hover_node.voisins]
                
                node_colors = ['yellow' if n in hover_nodes else 'lightblue' for n in G.nodes]
                nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, ax=ax)
                nx.draw_networkx_edges(G, pos, edgelist=hover_edges, edge_color='r', width=2, ax=ax)
            else:
                nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, ax=ax)
            
            nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', ax=ax)
            ax.set_axis_off()
            fig.canvas.draw_idle()
    
    # Connecter l'événement de survol à la figure unique
    fig.canvas.mpl_connect('motion_notify_event', update_hover)
    
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
    

def creer_graphe(image_matrix):
    sommets = []
    num_rows = len(image_matrix)
    num_cols = len(image_matrix[0])

    # Création des sommets avec les informations sur les arêtes
    for row in range(num_rows):
        sommets_row = []
        for col in range(num_cols):
            edge_presence = image_matrix[row][col]
            sommet = Sommet((row, col), row, col,
                            haut=edge_presence.top,
                            droit=edge_presence.right,
                            bas=edge_presence.bottom,
                            gauche=edge_presence.left,
                            diag_haut_gauche=edge_presence.top_left_corner,
                            diag_haut_droit=edge_presence.top_right_corner,
                            diag_bas_gauche=edge_presence.bottom_left_corner,
                            diag_bas_droit=edge_presence.bottom_right_corner)
            sommets_row.append(sommet)
        sommets.append(sommets_row)

    # Liaison des sommets avec leurs voisins
    for row in range(num_rows):
        for col in range(num_cols):
            edge_presence = image_matrix[col][row]
            sommet_actuel = sommets[row][col]
            
            if not edge_presence.top:
                voisin_haut = sommets[row][(col-1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_haut)

            if not edge_presence.bottom:
                voisin_bas = sommets[row][(col+1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_bas)

            if not edge_presence.left:
                voisin_gauche = sommets[(row-1) % num_rows][col]
                sommet_actuel.ajouter_voisin(voisin_gauche)

            if not edge_presence.right:
                voisin_droite = sommets[(row+1) % num_rows][col]
                sommet_actuel.ajouter_voisin(voisin_droite)

            if not edge_presence.top_left_corner:
                voisin_haut_gauche = sommets[(row-1) % num_rows][(col-1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_haut_gauche)

            if not edge_presence.top_right_corner:
                voisin_haut_droite = sommets[(row+1) % num_rows][(col-1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_haut_droite)

            if not edge_presence.bottom_left_corner:
                voisin_bas_gauche = sommets[(row-1) % num_rows][(col+1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_bas_gauche)

            if not edge_presence.bottom_right_corner:
                voisin_bas_droite = sommets[(row+1) % num_rows][(col+1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_bas_droite)

    return sommets

"""
def creer_graphe(image_matrix):
    sommets = []
    num_rows = len(image_matrix)
    num_cols = len(image_matrix[0])

    for row in range(num_rows):
        sommets_row = []
        for col in range(num_cols):
            sommet = Sommet((row, col),row, col)
            sommets_row.append(sommet)
        sommets.append(sommets_row)

    for row in range(num_rows):
        for col in range(num_cols):
            edge_presence = image_matrix[col][row]
            sommet_actuel = sommets[row][col]
            
            if not edge_presence.top:
                voisin_haut = sommets[row][(col-1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_haut)

            if not edge_presence.bottom:
                voisin_bas = sommets[row][(col+1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_bas)

            if not edge_presence.left:
                voisin_gauche = sommets[(row-1) % num_rows][col]
                sommet_actuel.ajouter_voisin(voisin_gauche)

            if not edge_presence.right:
                voisin_droite = sommets[(row+1) % num_rows][col]
                sommet_actuel.ajouter_voisin(voisin_droite)

            if not edge_presence.top_left_corner:
                voisin_haut_gauche = sommets[(row-1) % num_rows][(col-1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_haut_gauche)

            if not edge_presence.top_right_corner:
                voisin_haut_droite = sommets[(row+1) % num_rows][(col-1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_haut_droite)

            if not edge_presence.bottom_left_corner:
                voisin_bas_gauche = sommets[(row-1) % num_rows][(col+1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_bas_gauche)

            if not edge_presence.bottom_right_corner:
                voisin_bas_droite = sommets[(row+1) % num_rows][(col+1) % num_cols]
                sommet_actuel.ajouter_voisin(voisin_bas_droite)

    return sommets
"""
def creer_graphe_inverse(sommets, num_rows, num_cols):
    # Création du graphe inverse
    graphe_inverse = [[Sommet((row, col), row, col) for col in range(num_cols)] for row in range(num_rows)]

    for row in range(num_rows):
        for col in range(num_cols):
            sommet_actuel = graphe_inverse[row][col]
            sommet_original = sommets[row][col]

            # Pour chaque direction, si l'arête n'existe pas dans le graphe original, l'ajouter dans le graphe inverse
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = (row + dr) % num_rows, (col + dc) % num_cols
                if graphe_inverse[r][c] not in sommet_original.voisins:
                    sommet_actuel.ajouter_voisin(graphe_inverse[r][c])

    return graphe_inverse

from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations
import copy

class Sommet:
    def __init__(self, id, x, y, haut=False, droit=False, bas=False, gauche=False, diag_haut_gauche=False, diag_haut_droit=False, diag_bas_gauche=False, diag_bas_droit=False):
        self.id = id
        self.haut = haut
        self.droit = droit
        self.bas = bas
        self.gauche = gauche
        self.diag_haut_gauche = diag_haut_gauche
        self.diag_haut_droit = diag_haut_droit
        self.diag_bas_gauche = diag_bas_gauche
        self.diag_bas_droit = diag_bas_droit
        self.id = id
        self.x = x
        self.y = y
        self.voisins = set()

    def ajouter_voisin(self, sommet):
        if sommet not in self.voisins:
            self.voisins.add(sommet)
    
    def remove(self, sommet):
        if sommet in self.voisins:
            self.voisins.remove(sommet)
        if self in sommet.voisins:
            sommet.voisins.remove(self)

    def est_circulaire(self, autre, taille):
        return (self.x == 0 and autre.x == taille - 1) or \
               (self.x == taille - 1 and autre.x == 0) or \
               (self.y == 0 and autre.y == taille - 1) or \
               (self.y == taille - 1 and autre.y == 0)
    
    def est_diagonal(self, autre):
        # Une arête est diagonale si la différence absolue entre les coordonnées x
        # est égale à la différence absolue entre les coordonnées y
        return abs(self.x - autre.x) == abs(self.y - autre.y)
    
    def __eq__(self, other):
        # Deux sommets sont considérés égaux s'ils ont le même id
        return self.id == other.id

    def __hash__(self):
        # Le hash d'un sommet est basé sur son id
        return hash(self.id)
    
    
def is_connected(sommets):
    if not sommets or not sommets[0]:
        return True  # Pour un graphe vide ou invalide

    def dfs(sommet, visited):
        if len(visited) / total_sommets >= 0.72:  # Sortie anticipée
            return True
        visited.add(sommet)
        for voisin in sommet.voisins:
            if voisin not in visited:
                if dfs(voisin, visited):  # Propagation de la condition de sortie
                    return True
        return False  # Continue le parcours si pas encore atteint 80%

    total_sommets = len(sommets) * len(sommets)
    visited = set()
    return dfs(sommets[0][0], visited) or len(visited) / total_sommets >= 0.72


def rendre_non_connexe(sommets):
    def retirer_arete(sommet1, sommet2):
        sommet1.voisins.remove(sommet2)
        sommet2.voisins.remove(sommet1)
    
    def restaurer_arete(sommet1, sommet2):
        sommet1.voisins.add(sommet2)
        sommet2.voisins.add(sommet1)

    arêtes = set()
    for row in sommets:
        for sommet in row:
            for voisin in sommet.voisins:
                if sommet.id < voisin.id:  # Éviter les doublons
                    arêtes.add((sommet, voisin))

    for combinaison in combinations(arêtes, 3):
        # Retirer les arêtes sélectionnées
        for sommet1, sommet2 in combinaison:
            retirer_arete(sommet1, sommet2)
        
        if not is_connected(sommets):
            print("Arêtes retirées rendant le graphe non-connexe :", [(s1.id, s2.id) for s1, s2 in combinaison])
            # Restaurer immédiatement les arêtes retirées
            for sommet1, sommet2 in combinaison:
                restaurer_arete(sommet1, sommet2)
            return [(s1.id, s2.id) for s1, s2 in combinaison]
        
        # Si le graphe est encore connexe, restaurer les arêtes retirées
        for sommet1, sommet2 in combinaison:
            restaurer_arete(sommet1, sommet2)

    print("Le graphe reste connexe après toutes les tentatives.")
    return []

def trouver_groupes_aretes(sommets):
    groupes = []
    visites = set()

    def parcourir_groupe(sommet, groupe):
        if sommet in visites:
            return
        visites.add(sommet)
        groupe.append(sommet)
        for voisin in sommet.voisins:
            parcourir_groupe(voisin, groupe)

    for row in sommets:
        for sommet in row:
            if sommet not in visites:
                groupe = []
                parcourir_groupe(sommet, groupe)
                groupes.append(groupe)

    groupes.sort(key=len, reverse=True)
    return groupes

def find_longest_edge_sequence(image_matrix):
    num_rows = len(image_matrix)
    num_cols = len(image_matrix[0])
    
    def dfs(row, col, prev_edge):
        stack = [(row, col, prev_edge, 0)]
        max_length = 0
        
        while stack:
            row, col, prev_edge, length = stack.pop()
            
            if not (0 <= row < num_rows and 0 <= col < num_cols):
                continue
            
            edge_presence = image_matrix[row][col]
            length += 1
            max_length = max(max_length, length)
            
            if prev_edge == 'top':
                if edge_presence.bottom:
                    stack.append((row+1, col, 'bottom', length))
                if edge_presence.bottom_right_corner:
                    stack.append((row+1, col+1, 'bottom_right_corner', length))
            
            elif prev_edge == 'bottom':
                if edge_presence.top:
                    stack.append((row-1, col, 'top', length))
                if edge_presence.top_right_corner:
                    stack.append((row-1, col+1, 'top_right_corner', length))
            
            elif prev_edge == 'left':
                if edge_presence.right:
                    stack.append((row, col+1, 'right', length))
                if edge_presence.bottom_right_corner:
                    stack.append((row+1, col+1, 'bottom_right_corner', length))
            
            elif prev_edge == 'right':
                if edge_presence.left:
                    stack.append((row, col-1, 'left', length))
                if edge_presence.bottom_left_corner:
                    stack.append((row+1, col-1, 'bottom_left_corner', length))
            
            elif prev_edge == 'top_left_corner':
                if edge_presence.bottom_right_corner:
                    stack.append((row+1, col+1, 'bottom_right_corner', length))
            
            elif prev_edge == 'top_right_corner':
                if edge_presence.bottom_left_corner:
                    stack.append((row+1, col-1, 'bottom_left_corner', length))
            
            elif prev_edge == 'bottom_left_corner':
                if edge_presence.top_right_corner:
                    stack.append((row-1, col+1, 'top_right_corner', length))
            
            elif prev_edge == 'bottom_right_corner':
                if edge_presence.top_left_corner:
                    stack.append((row-1, col-1, 'top_left_corner', length))
        
        return max_length
    
    max_length = 0
    
    for row in range(num_rows):
        for col in range(num_cols):
            edge_presence = image_matrix[row][col]
            
            if edge_presence.top:
                max_length = max(max_length, 1 + dfs(row-1, col, 'top'))
            if edge_presence.bottom:
                max_length = max(max_length, 1 + dfs(row+1, col, 'bottom'))
            if edge_presence.left:
                max_length = max(max_length, 1 + dfs(row, col-1, 'left'))
            if edge_presence.right:
                max_length = max(max_length, 1 + dfs(row, col+1, 'right'))
            if edge_presence.top_left_corner:
                max_length = max(max_length, 1 + dfs(row-1, col-1, 'top_left_corner'))
            if edge_presence.top_right_corner:
                max_length = max(max_length, 1 + dfs(row-1, col+1, 'top_right_corner'))
            if edge_presence.bottom_left_corner:
                max_length = max(max_length, 1 + dfs(row+1, col-1, 'bottom_left_corner'))
            if edge_presence.bottom_right_corner:
                max_length = max(max_length, 1 + dfs(row+1, col+1, 'bottom_right_corner'))
                
    return max_length

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('challenges.france-cybersecurity-challenge.fr', 2051))
    
    
    sock.send(b"START\n")

    cpt = 0
    while cpt != 100 :
        start_time = time.time()
        cpt = cpt + 1
        print(str(cpt)+"/100")
        
        data = b""
        while True:
            chunk = sock.recv(4096)
            if b"END MAZE" in chunk:
                data += chunk[:chunk.find(b"END MAZE")+8]
                break
            if b"your solution is incorrect" in chunk:
                print(data)
                break
            data += chunk
            
        b64_data = data.split(b"BEGIN MAZE ------------------------\n")[1].split(b"\n------------------------- END MAZE")[0].strip()

        img_data = base64.b64decode(b64_data)

        img = Image.open(io.BytesIO(img_data))

        left = 64
        top = 128
        right = img.width - 64
        bottom = img.height - 64

        cropped_img = img.crop((left, top, right, bottom))

        #cropped_img.show()

        num_rows = 5
        num_cols = 5
        if cpt >= 6:
            num_rows = 8
            num_cols = 8
        if cpt >= 11:
            num_rows = 10
            num_cols = 10

        segment_width = cropped_img.width // num_cols
        segment_height = cropped_img.height // num_rows

        image_matrix = []
        for row in range(num_rows):
            row_list = []
            for col in range(num_cols):
                left = col * segment_width
                top = row * segment_height
                right = left + segment_width
                bottom = top + segment_height
                
                segment = cropped_img.crop((left, top, right, bottom))
                row_list.append(update_edges(segment))
                
            image_matrix.append(row_list) 

        #print(find_longest_edge_sequence(image_matrix))
        sommets = creer_graphe(image_matrix)
        #graphe_inverse = creer_graphe_inverse(sommets, len(image_matrix), len(image_matrix[0]))
        
        reponse = rendre_non_connexe(sommets)

        #cropped_img.show()
        #visualiser_graphe(graphe_inverse)
        
        end_time = time.time()
        print(f"Size {num_rows}")
        print(f"Temps écoulé : {end_time - start_time:.2f} secondes")
        #chaines_triees = trier_chaines(graphe_inverse)
        #for chaine in chaines_triees:
        #    print(chaine)
        #cropped_img.show()
        
        #visualiser_graphe(graphe_inverse)
        reponse = str(reponse)+"\n"
        reponse = bytes(reponse.encode("utf-8"))
        sock.send(reponse)
        if (end_time - start_time) > 30 :
            cropped_img.show()

        """
        cut_edges = str(cut_edges)+"\n"
        cut_edges = bytes(cut_edges.encode("utf-8"))
        print(cut_edges)

        end_time = time.time()
        print(f"Size {num_rows}")
        print(f"Temps écoulé : {end_time - start_time:.2f} secondes")
        #input("wait")
        sock.send(cut_edges)



    while True:
        buffer = sock.recv(4096)
        if not buffer:
            break
        print("FCSC : ",buffer.decode())
    """
    sock.close()
main()
