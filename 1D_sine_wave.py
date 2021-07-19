from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation
import numpy as np

fig = plt.figure()
ax = fig.gca()
ax.set_ylim([-2, 2])

x = np.linspace(0, 2, 100)
y = np.sin(2 * np.pi * x)
y2 = np.sin(2 * np.pi * x)
forward, = ax.plot(x, y)
reverse, = ax.plot(x, y2)
summation, = ax.plot(x, y2)


def animate(t):
    y = np.sin(2 * np.pi * x + np.pi * 0.01 * t)
    y2 = np.sin(-2 * np.pi * x + np.pi * 0.01 * t - np.pi)
    forward.set_ydata(y)
    reverse.set_ydata(y2)
    summation.set_ydata(y + y2)
    return forward, reverse, summation


ani = FuncAnimation(fig, animate, frames=200, interval=30, blit=False)

plt.show()