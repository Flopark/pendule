# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 23:23:25 2026

@author: march
"""

import matplotlib.pyplot as plt
import numpy as np
from IPython import display
import imageio
import os


g = 9.81
l = 10 #cm
t = np.arange(0, 50.1, 0.1) 
w = np.sqrt(g/l)


output_dir = 'anim_pendu'
os.makedirs(output_dir, exist_ok=True)

nb_images = 70
t = np.linspace(0, 10, nb_images)
images = []

for i, temps in enumerate(t):

    plt.figure()
    theta = (np.pi/6) * np.cos(w*temps)
    x = l * np.sin(theta)
    y = -l * np.cos(theta)

    plt.plot([0, x], [0, y], color='blue', linewidth=2) # Add the pendulum bar
    plt.scatter(x, y, s=50) # Plot the pendulum bob
    plt.grid()
    plt.xlabel('x [cm] ')
    plt.ylabel('y [cm] ')
    plt.xlim(-12, 12) 
    plt.ylim(-12, 2) 
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(f'Pendulum at t={temps:.2f}s')
    filename = os.path.join(output_dir, f'frame_{i}.png')
    plt.savefig(filename)
    plt.close()

import imageio.v2 as imageio
for i in range(nb_images):
    filename = os.path.join(output_dir, f'frame_{i}.png')
    images.append(imageio.imread(filename))

imageio.mimsave('pendule.gif', images, duration=10,loop=0)
from IPython.display import Image as IPythonImage
display.display(IPythonImage('pendule.gif'))