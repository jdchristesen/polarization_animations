from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

num_frames = 100


def compute_segs(i):
    x = np.linspace(0, 2, 20)
    y = np.zeros(x.shape)
    z = np.zeros(x.shape)
    u = np.zeros(x.shape) + x
    v = np.cos(2 * np.pi * x + 2 * np.pi * 0.01 * i) + y
    w = np.sin(2 * np.pi * x + 2 * np.pi * 0.01 * i) + z

    # Adding the k-vector
    # x = np.append(np.array([2]), x)
    # y = np.append(np.array([0]), y)
    # z = np.append(np.array([0]), z)
    # u = np.append(np.array([-.5]), u)
    # v = np.append(np.array([0]), v)
    # w = np.append(np.array([0]), w)

    return x, y, z, u, v, w


def compute_reflected_segs(i):
    x = np.linspace(0, 2, 20)
    y = np.zeros(x.shape)
    z = np.zeros(x.shape)
    u = np.zeros(x.shape) + x
    v = np.cos(-2 * np.pi * x + 2 * np.pi * 0.01 * i + np.pi) + y
    w = np.sin(-2 * np.pi * x + 2 * np.pi * 0.01 * i + np.pi) + z

    # Adding the k-vector
    # x = np.append(np.array([0]), x)
    # y = np.append(np.array([0]), y)
    # z = np.append(np.array([0]), z)
    # u = np.append(np.array([2]), u)
    # v = np.append(np.array([0]), v)
    # w = np.append(np.array([0]), w)

    return x, y, z, u, v, w


segs = compute_segs(0)
forward = ax.quiver([], [], [], [], [], [], length=1, colors=['b' for x in segs[0].ravel()])
reflected = ax.quiver([], [], [], [], [], [], length=1, colors=['r' for x in segs[0].ravel()])
summation = ax.quiver([], [], [], [], [], [], length=2, colors=['g' for x in segs[0].ravel()])
scatters = ax.scatter([], [], [], marker='o')


ax.set_xlim([-1, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])


def animate(i):

    computed_segs = np.array(compute_segs(i))
    segs = computed_segs.reshape(6, -1)
    new_segs_l = [[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*segs.tolist())]

    rev_segs = np.array(compute_reflected_segs(i)).reshape(6, -1)
    sum_segs = segs
    sum_segs[4:, :] = sum_segs[4:, :] + rev_segs[4:, :]
    # print(segs.shape)

    new_segs_r = [[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*rev_segs.tolist())]
    new_segs_s = [[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*sum_segs.tolist())]
    # print(sum_segs.shape)
    forward.set_segments(new_segs_l)
    reflected.set_segments(new_segs_r)
    summation.set_segments(new_segs_s)
    scatters._offsets3d = computed_segs[3:]
    return forward, reflected, scatters


ani = FuncAnimation(fig, animate, frames=num_frames, interval=30, blit=False)
# animate(0)
plt.show()