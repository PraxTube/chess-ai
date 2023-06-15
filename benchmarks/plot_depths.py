import os

import numpy as np
import matplotlib.pyplot as plt

# Sample data
x = np.array([1, 2, 3, 4, 5], dtype=int)
time_dummy = np.array([1, 20, 440, 1345, 9170]) / 1000
time_basic = np.array([8, 162, 2046, 7449, 54721]) / 1000
time_advanced = np.array([1, 22, 245, 1966, 28678]) / 1000

node_dummy = np.array([20, 420, 9322, 28414, 189904]) / 1000
node_basic = np.array([20, 420, 1303, 10672, 34688]) / 1000
node_advanced = np.array([20, 420, 3053, 28090, 336520]) / 1000

dummy_color = "blue"
basic_color = "red"
advanced_color = "green"

# Create the plot
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# Plot the first dataset with the left y-axis
ax1.plot(x, time_dummy, label="Dummy AI", linestyle="--", marker=".", color=dummy_color)
ax1.plot(x, time_basic, label="Basic AI", linestyle="--", marker=".", color=basic_color)
ax1.plot(
    x,
    time_advanced,
    label="Advanced AI",
    color=advanced_color,
    linestyle="--",
    marker=".",
)
ax1.set_ylabel("Time in s")

# Plot the second dataset with the right y-axis
ax2.plot(x, node_dummy, label="Dummy AI", color=dummy_color, linestyle="--", marker=".")
ax2.plot(x, node_basic, label="Basic AI", color=basic_color, linestyle="--", marker=".")
ax2.plot(
    x,
    node_advanced,
    label="Advanced AI",
    color=advanced_color,
    linestyle="--",
    marker=".",
)

ax2.set_xlabel("Depth")
ax2.set_ylabel("(kilo) Nodes searched")

ax1.legend()
ax2.legend()

xticks = range(1, len(x) + 1)
plt.xticks(xticks, xticks)

plt.tight_layout()

script_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(script_dir)
plt.savefig(os.path.join(main_dir, "plot-depths.pdf"), format="pdf")
