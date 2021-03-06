import tensorflow as tf
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.path.append('../')
from segmentation import segment_cell, display, boundary_from_pixelated_mask, smooth_boundary, display_boundary
from molyso.generic.otsu import threshold_otsu
from matplotlib_scalebar.scalebar import ScaleBar

cells = []
for i in range(4):
    cell = np.load("cell_examples/Cell_test_{}.npy".format(i))
    # Remove zeros
    rm_indices = np.where(cell==0.0)[0]
    cell = np.delete(cell, rm_indices, axis=0)
    cells.append(cell)

model = tf.keras.models.load_model('../saved_model/segmentation')

f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey=True)
axes = [ax1, ax2, ax3, ax4]
scalebar = ScaleBar(0.11, 'um', frameon=False, color='w', location=2) # 1 pixel = 0.2 meter
plt.gca().add_artist(scalebar)
title = ['Pixelated Boundary', 'Smoothed Boundary']
colors = ['k', 'r']
width = [1.0, 1.75]
for i, cell in enumerate(cells):
    axes[i].imshow(cell)
    axes[i].axis('off')
    pixelated_mask = segment_cell(cell, model, height=50)
    boundary = boundary_from_pixelated_mask(pixelated_mask)
    smoothed_boundary = smooth_boundary(boundary, 5)
    boundaries = [boundary, smoothed_boundary]
    for j in range(len(boundaries)):
        axes[i].plot(boundaries[j-1][:,0], boundaries[j-1][:,1], colors[j-1], label=title[j-1], linewidth=width[j-1])
# Shrink current axis by 20%
box = ax4.get_position()
ax4.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax4.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

#Pixelation by otsu
f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey=True)
axes = [ax1, ax2, ax3, ax4]
title = ['Pixelated Boundary', 'Smoothed Boundary']
colors = ['r', 'g']
scalebar = ScaleBar(0.11, 'um', frameon=False, color='w', location=2) # 1 pixel = 0.2 meter
plt.gca().add_artist(scalebar)
for i, cell in enumerate(cells):
    axes[i].imshow(cell)
    axes[i].axis('off')
    pixelated_mask = cell > threshold_otsu(cell)
    boundary = boundary_from_pixelated_mask(pixelated_mask)
    smoothed_boundary = smooth_boundary(boundary, 5)
    boundaries = [boundary]#, smoothed_boundary]
    for j in range(len(boundaries)):
        axes[i].plot(boundaries[j][:,0], boundaries[j][:,1], colors[j], label=title[j], linewidth=1.5)
plt.show()
