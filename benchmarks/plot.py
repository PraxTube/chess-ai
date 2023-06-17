import os

import numpy as np
import matplotlib.pyplot as plt

# Define the data
dummy_values = np.array([13, 897, 5, 24, 2.4])
basic_values = np.array([14, 894, 5, 180, 8.4])
advanced_values = np.array([21, 651, 5, 43, 1.13])

total_values = np.vstack((dummy_values, basic_values, advanced_values))
max_values = np.max(total_values, axis=0)
normalized_values = total_values / max_values

categories = [
    f"FEN Conversion\nMax: {max_values[0]} μs",
    f"Legal Move Gen\nMax: {max_values[1]} μs",
    f"Make Move\nMax: {max_values[2]} μs",
    f"Evaluation\nMax: {max_values[3]} μs",
    f"Best Move Gen\nMax: {max_values[4]} ms",
]

# Set the width of each pillar
width = 0.175

# Set the positions of the pillars on the x-axis
x = np.arange(len(categories))

# Create the figure and axis objects
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the pillars
ax.bar(x - width, normalized_values[0], width, label="Dummy AI")
ax.bar(x, normalized_values[1], width, label="Basic AI")
ax.bar(x + width, normalized_values[2], width, label="Advanced AI")

# Set labels, title, and legend
ax.set_ylabel("Normalized Values")
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

script_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(script_dir)
plt.savefig(os.path.join(main_dir, "plot.pdf"), format="pdf")
