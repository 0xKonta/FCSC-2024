from scapy.all import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.widgets import Button

# Fonction pour lire et traiter les paquets
def process_packets(filename):
    packets = rdpcap(filename)

    # Filtrer les paquets DMX (port UDP 6454)
    dmx_packets = [p for p in packets if UDP in p and p[UDP].dport == 6454]

    # Extraire les données DMX, le numéro de séquence et l'univers de chaque paquet
    dmx_data = []
    sequence_numbers = []
    universes = []
    for p in dmx_packets:
        # Modifier ici pour correspondre à la structure exacte des paquets
        dmx_data.append(p.load[18:-2])  # Ajustement hypothétique pour extraire les données DMX
        sequence_numbers.append(p.load[-2])
        universes.append(p.load[-1])

    return dmx_data, sequence_numbers, universes

# Fonction pour calculer l'offset DMX
def calculate_dmx_offset(x, y, width=16, start_channel=1, channels_per_pixel=3):
    # Calcul du nombre total de canaux par ligne
    total_channels_per_line = width * channels_per_pixel
    # Initialisation du DMX offset
    offset = 0
    # Gestion du zigzag et des univers multiples
    if y < 10:  # Dans l'univers 1
        if y % 2 == 0:  # Ligne paire (en commençant par 0), de gauche à droite
            offset = y * total_channels_per_line + x * channels_per_pixel
        else:  # Ligne impaire, de droite à gauche
            offset = (y + 1) * total_channels_per_line - (x + 1) * channels_per_pixel
    else:  # Dans l'univers 2 ou plus
        # Calcul du décalage sans tenir compte du changement d'univers
        if (y - 10) % 2 == 0:  # Ligne paire dans le nouvel univers, de gauche à droite
            offset = (y - 10) * total_channels_per_line + x * channels_per_pixel
        else:  # Ligne impaire dans le nouvel univers, de droite à gauche
            offset = ((y - 10) + 1) * total_channels_per_line - (x + 1) * channels_per_pixel
        # Ajustement pour démarrer à 1 dans le nouvel univers
        offset += (start_channel - 1)
    return offset

# Fonction pour créer une matrice de pixels
def create_pixels_matrix(dmx_data):
    pixels = np.zeros((len(dmx_data), 16, 16, 3), dtype=np.uint8)
    for i, data in enumerate(dmx_data):
        for y in range(16):
            for x in range(16):
                offset = calculate_dmx_offset(x, y)
                if 0 <= offset < len(data) - 2:
                    pixels[i, y, x] = [data[offset], data[offset + 1], data[offset + 2]]
    return pixels

# Traitement initial des paquets
dmx_data, sequence_numbers, universes = process_packets(r'capture.pcap')

pixels = create_pixels_matrix(dmx_data)

# Configuration initiale pour l'animation
current_frame = 0
mode = 'auto'  # Les modes peuvent être 'auto' ou 'manual'

# Création de la figure pour l'animation
fig, ax = plt.subplots()
img = ax.imshow(pixels[0])
ax.axis('off')

# Texte pour afficher les informations du pixel
pixel_info_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, color='white', 
                          verticalalignment='top', bbox=dict(facecolor='black', alpha=0.5))

# Mise à jour de l'affichage pour l'animation
def update_display(frame):
    global current_frame
    current_frame = frame % len(pixels)
    img.set_array(pixels[current_frame])

# Gestion du défilement manuel
def on_scroll(event):
    if mode == 'manual':
        global current_frame
        if event.button == 'up':
            update_display(current_frame + 1)
        elif event.button == 'down':
            update_display(current_frame - 1)
        fig.canvas.draw_idle()

# Basculement entre les modes
def toggle_mode(event):
    global mode
    mode = 'auto' if mode == 'manual' else 'manual'
    btn.label.set_text('Mode: Auto' if mode == 'auto' else 'Mode: Manual')
    if mode == 'auto':
        anim.event_source.start()
    else:
        anim.event_source.stop()

# Affichage des informations du pixel au survol de la souris
def on_hover(event):
    if event.inaxes == ax:
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            x, y = int(x), int(y)
            offset = calculate_dmx_offset(x, y)
            pixel_info_text.set_text(f'Pixel ({x}, {y})\nUniverse: {universes[current_frame]}\nDMX Offset: {offset}')
        else:
            pixel_info_text.set_text('')
    else:
        pixel_info_text.set_text('')
    fig.canvas.draw_idle()

# Bouton pour changer de mode
ax_button = plt.axes([0.8, 0.01, 0.18, 0.075])
btn = Button(ax_button, 'Mode: Auto')
btn.on_clicked(toggle_mode)

# Écouteur d'événements pour la molette de la souris
fig.canvas.mpl_connect('scroll_event', on_scroll)

# Écouteur d'événements pour le survol de la souris
fig.canvas.mpl_connect('motion_notify_event', on_hover)

# Animation
anim = animation.FuncAnimation(fig, update_display, frames=len(pixels), interval=50, blit=False)

plt.show()
