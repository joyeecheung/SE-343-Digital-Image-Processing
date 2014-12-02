#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm


def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    M, N = 100, 100
    u, v = np.arange(M), np.arange(N)
    U, V = np.meshgrid(u, v)

    def H(u, v):
        return 2 - 2 * np.cos(2 * np.pi * (u - M / 2.0) / M)

    zs = np.array([H(u, v) for u, v in zip(np.ravel(U), np.ravel(V))])
    Z = zs.reshape(U.shape)
    ax.set_xlabel('u')
    ax.set_ylabel('v')
    ax.set_zlabel('H(u, v)')

    ax.plot_surface(
        U, V, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)

    plt.savefig('exercise-1-4.png')

if __name__ == "__main__":
    main()
