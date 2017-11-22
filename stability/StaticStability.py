import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh
import pymesh
import os

# Author: Anurag Makineni (11/22/2017)

class StaticStability:
    def __init__(self):
        pass

    # load an STL into a PyMesh
    def load_mesh(self, fname):
        return pymesh.load_mesh(fname)

    # convert from PyMesh to numpy-stl
    def pyMesh_to_stl(self, mesh_in):
        faces = mesh_in.faces
        vertices = mesh_in.vertices

        temp = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                temp.vectors[i][j] = vertices[f[j], :]
        return temp

    def get_volume(self, mesh_in):
        mesh_in = self.pyMesh_to_stl(mesh_in)
        return mesh_in.get_mass_properties()[0]

    def get_centroid(self, mesh_in):
        mesh_in = self.pyMesh_to_stl(mesh_in)
        return np.array(mesh_in.get_mass_properties()[1])

    def plot_stl(self, mesh_in, hold=False):
        mesh_in = self.pyMesh_to_stl(mesh_in)
        # Create a new plot
        if not hold:
            figure = plt.figure()
            axes = mplot3d.Axes3D(figure)
        else:
            figure = plt.gcf()
            axes = plt.gca()



        # Load the STL files and add the vectors to the plot
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh_in.vectors))

        # Auto scale to the mesh size
        scale = mesh_in.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        # plt.show()

    # axis = 'x', 'y', or 'z'
    # point is the point to rotate about
    # angle (in radians)
    def rotate_mesh(self, mesh_in, point, axis, angle):
        if axis == 'x':
            axis = [1.0, 0.0, 0.0]
        elif axis == 'y':
            axis = [0.0, 1.0, 0.0]
        elif axis == 'z':
            axis = [0.0, 0.0, 1.0]

        mesh_in = self.pyMesh_to_stl(mesh_in)
        mesh_in.rotate(axis, angle, point)

        # convert back to pymesh
        mesh_in.save('temp.stl')
        mesh_out = self.load_mesh('temp.stl')
        os.remove('temp.stl')

        return mesh_out

    def subtract(self, mesh_a, mesh_b):
        return pymesh.boolean(mesh_a, mesh_b, 'difference')


if __name__ == '__main__':
    SS = StaticStability()
    mesh_out = SS.load_mesh('Hull_3B_Full-Scale.stl')
    print SS.get_centroid(mesh_out)
    mesh_a = SS.rotate_mesh(mesh_out, [0,0,0], 'x', np.radians(5.0))
    mesh_b = SS.rotate_mesh(mesh_out, [0,0,0], 'x', np.radians(10.0))
    # SS.plot_stl(mesh_a)
    # SS.plot_stl(mesh_b, hold=True)

    SS.plot_stl(SS.subtract(mesh_b, mesh_a))
    plt.show()