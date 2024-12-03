import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

#print(plt.style.available)

#plt.style.use('seaborn-poster')
plt.style.use('seaborn-v0_8-bright')


class Plotter3D:
    def __init__(self, name):
        self.name = name


    def scatter_points_3d(self, x, y, z, x_title='x', y_title='y', z_title='z'):

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

        print(f"x.shape: {x.shape}, y.shape: {y.shape}, z.shape: {z.shape}")

        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        #plt.show()

        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        ax.grid()

        ax.scatter(x, y, z, c='r', s=50)
        ax.set_title('3D Scatter Plot')

        # Set axes label
        ax.set_xlabel(x_title, labelpad=20)
        ax.set_ylabel(y_title, labelpad=20)
        ax.set_zlabel(z_title, labelpad=20)

        plt.show()

    def scatter_points_2d(self, x, y, x_title='x', y_title='y', plot_title='2D Scatter Plot'):

        x = np.array(x)
        y = np.array(y)

        print(f"x.shape: {x.shape}, y.shape: {y.shape}")


        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes()
        #ax = plt.axes(projection='2d')
        ax.grid()

        ax.scatter(x, y, c='r', s=50)
        ax.set_title(plot_title)

        # Set axes label
        ax.set_xlabel(x_title, labelpad=20)
        ax.set_ylabel(y_title, labelpad=20)

        plt.show()

