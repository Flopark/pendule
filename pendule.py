# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 23:23:25 2026

@author: march
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import imageio
import io

# Configuration de la page
st.set_page_config(page_title="Simulateur de Pendule Simple", layout="centered")

st.title("⚖️ Simulateur de Pendule Simple")
st.write("Ajustez les paramètres dans la barre latérale et lancez l'animation.")

# --- Barre latérale pour les paramètres ---
st.sidebar.header("Paramètres Physiques")
g = st.sidebar.slider("Pesanteur (g) [m/s²]", min_value=0.0, max_value=25.0, value=9.81, step=0.1)
l_cm = st.sidebar.slider("Longueur du pendule (L) [cm]", min_value=5.0, max_value=100.0, value=20.0, step=1.0)
theta_deg = st.sidebar.slider("Angle initial [degrés]", min_value=5, max_value=90, value=30)

# Conversion des unités
l_m = l_cm / 100
w = np.sqrt(g / l_m)
theta_max = np.radians(theta_deg)

# --- Paramètres de l'animation ---
nb_images = 60
duree_anim = 5  # secondes

if st.sidebar.button("Lancer l'animation"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    t = np.linspace(0, duree_anim, nb_images)
    images = []

    # Création de la figure
    fig, ax = plt.subplots(figsize=(5, 5))

    for i, temps in enumerate(t):
        # Calcul de la position
        theta = theta_max * np.cos(w * temps)
        x = l_cm * np.sin(theta)
        y = -l_cm * np.cos(theta)

        # Tracé
        ax.clear()
        ax.plot([0, x], [0, y], color='black', linewidth=2, zorder=1)
        ax.scatter(x, y, s=300, color='red', edgecolor='black', zorder=2)
        ax.scatter(0, 0, color='blue', s=50) # Pivot
        
        ax.set_xlim(-l_cm - 5, l_cm + 5)
        ax.set_ylim(-l_cm - 5, 5)
        ax.set_aspect('equal')
        ax.set_title(f"Temps : {temps:.2f}s")
        ax.grid(True, linestyle='--', alpha=0.5)

        # Enregistrement de l'image en mémoire buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        images.append(imageio.v2.imread(buf))
        
        # Mise à jour de la barre de progression
        progress_bar.progress((i + 1) / nb_images)
        status_text.text(f"Génération de l'image {i+1}/{nb_images}...")

    plt.close()
    
    # Création du GIF en mémoire
    status_text.text("Compilation du GIF...")
    gif_buffer = io.BytesIO()
    imageio.mimsave(gif_buffer, images, format='GIF', fps=12, loop=0)
    
    # Affichage du résultat
    st.success("Animation terminée !")
    st.image(gif_buffer, caption=f"Pendule (g={g}, L={l_cm}cm)")

else:
    st.info("Modifiez les paramètres à gauche et cliquez sur 'Lancer l'animation'.")


