import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh
import pymesh


class StaticStability:
    def __init__(self):
        pass

    # load an STL into a PyMesh
    def load_mesh(self, fname):
        return pymesh.load_mesh(fname)

    # convert from PyMesh to numpy-stl
    def convert_mesh(self, mesh_in):
        faces = mesh_in.faces
        vertices = mesh_in.vertices

        temp = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                temp.vectors[i][j] = vertices[f[j], :]

        return temp

    # INPUT is a numpy-stl mesh (not a pymesh)
    def plot_stl(self, mesh_in):
        # Create a new plot
        figure = plt.figure()
        axes = mplot3d.Axes3D(figure)

        # Load the STL files and add the vectors to the plot
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh_in.vectors))

        # Auto scale to the mesh size
        scale = mesh_in.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        plt.show()


if __name__ == '__main__':
    SS = StaticStability()
    mesh_out = SS.load_mesh('Hull_3B_Full-Scale.stl')
    temp = SS.convert_mesh(mesh_out)
    print temp.get_mass_properties()
