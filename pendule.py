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
st.set_page_config(page_title="Pendule : Terre, Lune ou Soleil", layout="centered")

st.title("⚖️ Simulateur de Pendule Interspatial")
st.write("Comparez le mouvement d'un pendule selon le corps céleste choisi.")

# --- Barre latérale pour les paramètres ---
st.sidebar.header("Configuration")

# Choix de l'astre (Dictionnaire pour mapper le nom à la valeur de g)
astres = {
    "Terre (9.81 m/s²)": 9.81,
    "Lune (1.62 m/s²)": 1.62,
    "Soleil (274.0 m/s²)": 274.0
}

choix_astre = st.sidebar.selectbox("Choisissez la gravité :", list(astres.keys()))
g = astres[choix_astre]

# Longueur du pendule
l_cm = st.sidebar.slider("Longueur du pendule (L) [cm]", min_value=0, max_value=200, value=50)
ang = st.sidebar.slider("Angle initiale [degrés]", min_value=0, max_value=180, value=50)

# Paramètres de simulation
l_m = l_cm / 100
w = np.sqrt(g / l_m)
theta_max = np.radians(ang) 

# Ajustement de la durée selon la gravité (plus court pour le soleil, plus long pour la lune)
if g > 100: # Soleil
    duree_anim = 1  
    nb_images = 40
elif g < 2: # Lune
    duree_anim = 8
    nb_images = 80
else: # Terre
    duree_anim = 4
    nb_images = 60

if st.sidebar.button("Lancer la simulation"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    t = np.linspace(0, duree_anim, nb_images)
    images = []

    fig, ax = plt.subplots(figsize=(5, 5))

    for i, temps in enumerate(t):
        # Equation du mouvement
        theta = theta_max * np.cos(w * temps)
        x = l_cm * np.sin(theta)
        y = -l_cm * np.cos(theta)

        # Dessin
        ax.clear()
        # On trace le support (plafond)
        ax.axhline(0, color='grey', lw=2)
        # La tige
        ax.plot([0, x], [0, y], color='black', linewidth=2, zorder=1)
        # La masse
        ax.scatter(x, y, s=400, color='red', edgecolor='black', zorder=2)
        # Le pivot
        ax.scatter(0, 0, color='blue', s=50, zorder=3)
        
        # Limites dynamiques
        ax.set_xlim(-l_cm - 10, l_cm + 10)
        ax.set_ylim(-l_cm - 10, 10)
        ax.set_aspect('equal')
        ax.set_title(f"Astre : {choix_astre}\nTemps : {temps:.2f}s")
        ax.grid(True, linestyle='--', alpha=0.3)

        # Capture de l'image
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        images.append(imageio.v2.imread(buf))
        
        progress_bar.progress((i + 1) / nb_images)

    plt.close()
    
    # Création du GIF
    status_text.text("Création du GIF en cours...")
    gif_buffer = io.BytesIO()
    # On calcule les FPS pour que le temps de l'animation corresponde au temps réel
    fps_reel = nb_images / duree_anim
    imageio.mimsave(gif_buffer, images, format='GIF', fps=fps_reel, loop=0)
    
    status_text.empty()
    st.success(f"Simulation terminée sur {choix_astre.split(' (')[0]} !")
    st.image(gif_buffer)

    # Petit commentaire physique
    periode = 2 * np.pi * np.sqrt(l_m / g)
    st.info(f"💡 La période d'oscillation théorique est de **{periode:.2f} secondes**.")

else:
    st.info("Sélectionnez un astre et cliquez sur le bouton pour voir la différence de pesanteur.")
