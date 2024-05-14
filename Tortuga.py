import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


segments = [(0,2),(0,-2),(1,0),(-1,0),(0,1),(1,0),(0,0),(1,1),(0,-2),(1,0),(-1,0),(0,2),(1,0),(0,0),(2,-2),(-1,0),(0,1),(1,0),(0,1),(-1,0),(0,0),(2,0),(0,-2),(1,0),(-1,0),(0,2),(1,0),(0,0),(3,-2),(-1,0),(0,1),(-1,0),(1,0),(0,1),(1,0),(0,0),(4,-2),(-2,0),(0,0),(0,2),(2,0),(0,-2),(0,1),(-2,0),(0,0),(3,-1),(0,2),(0,0),(3,-2),(-1,0),(-1,1),(0,1),(2,0),(0,-1),(-2,0),(0,0),(3,0),(1,0),(0,-1),(-1,0),(0,2),(1,0),(0,-1),(0,0),(1,1),(1,0),(0,-2),(-1,0),(0,0),(0,1),(1,0),(0,0),(2,1),(0,-2),(-1,1),(2,0),(0,0),(1,-1),(1,0),(-1,2),(0,0),(0,-1),(1,0),(0,0),(1,-1),(1,0),(0,1),(-1,0),(0,1),(1,0),(0,0),(1,0),(1,0),(0,-1),(-1,0),(0,-1),(1,0),(0,0),(1,2),(0,-2),(1,0),(-1,0),(0,2),(1,0),(0,-1),(-1,0),(0,0),(2,1),(1,0),(-1,0),(0,-2),(1,0),(-1,2),(1,0),(0,-2),(0,0),(1,0),(0,1),(1,0),(0,-1),(0,2),(0,0),(2,-2),(1,0),(0,1),(1,0),(-1,0),(0,1),(-1,0)]


def draw_segments(segments):
    fig, ax = plt.subplots()
    current_x, current_y = 0, 0
    skip_next = False  # Contrôle si le prochain segment doit être en blanc

    for dx, dy in segments:
        if (dx, dy) == (0, 0):
            skip_next = True  # Le prochain segment sera en blanc
            continue

        new_x = current_x + dx
        new_y = current_y - dy  # Multiplier par -1 pour inverser verticalement

        # Définir la couleur du segment
        color = 'w' if skip_next else 'b'  # 'w' pour blanc, 'b' pour bleu
        skip_next = False  # Réinitialiser après utilisation

        # Dessiner le segment
        ax.plot([current_x, new_x], [current_y, new_y], color=color)

        # Mise à jour des positions pour le prochain segment
        current_x, current_y = new_x, new_y

    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    plt.show()


draw_segments(segments)
