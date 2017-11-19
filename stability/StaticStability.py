import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh

class StaticStability:
    def __init__(self):
        pass

    def load_stl(self, fname):
        model = mesh.Mesh.from_file(fname)
        return model

    def plot_mesh(self, mesh):
        figure = plt.figure()
        axes = mplot3d.Axes3D(figure)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))
        scale = mesh.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)
        plt.show()


if __name__ == '__main__':
    SS = StaticStability()
    mesh = SS.load_stl('Hull_3B_Full-Scale.stl')
    SS.plot_mesh(mesh)