import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh
import pymesh
import os
from scipy.optimize import least_squares


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

    def stl_to_pyMesh(self, mesh_in):
        # convert back to pymesh
        mesh_in.save('temp.stl')
        mesh_out = self.load_mesh('temp.stl')
        os.remove('temp.stl')
        return mesh_out

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
            axes = plt.gca()

        # Load the STL files and add the vectors to the plot
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh_in.vectors))

        # Auto scale to the mesh size
        scale = mesh_in.points.flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        plt.show()

    def plot_2d(self, mesh_in, waterline=0.0):
        plt.figure()
        verticies = mesh_in.vertices
        plt.scatter(verticies[:, 1], verticies[:, 2])
        plt.plot([-800, 800], [waterline, waterline])
        plt.axis('equal')
        plt.xlim([-1000.0, 1000.0])
        plt.ylim([-1000.0, 1000.0])

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

        return self.stl_to_pyMesh(mesh_in)

    def subtract(self, mesh_a, mesh_b):
        return pymesh.boolean(mesh_a, mesh_b, operation='difference', engine='cgal')

    def translate_mesh(self, mesh_in, translation):
        mesh_in = self.pyMesh_to_stl(mesh_in)
        mesh_in.translate(translation)

        return self.stl_to_pyMesh(mesh_in)

    def calculate_waterline(self, mesh_in, displacement, water_mesh, waterline_init):
        self.mesh_in = mesh_in
        self.displacement = displacement
        self.water_mesh = water_mesh
        error, submerged = self.get_error(waterline_init)
        waterline = waterline_init

        i = 1
        while abs(error) > 0.1:
            waterline = waterline - 1.0 * error
            error, submerged = self.get_error(waterline)
            print "Iteration: " + str(i) + ", Error: " + str(error)
            i += 1

        return waterline, submerged



    def get_error(self, waterline):
        water_centroid = self.get_centroid(self.water_mesh)
        water = self.translate_mesh(self.water_mesh, [-water_centroid[0], -water_centroid[1], -waterline])
        submerged = self.subtract(self.mesh_in, water)
        return self.displacement - self.get_volume(submerged)/1E9 * 1000.0, submerged

if __name__ == '__main__':
    SS = StaticStability()
    mesh_out = SS.load_mesh('Hull_Doubled_Full-Scale.stl')
    centroid = SS.get_centroid(mesh_out)
    mesh_out = SS.rotate_mesh(SS.translate_mesh(mesh_out, [-centroid[0], -centroid[1], 0.0]), point=None,
                              axis=[1, 0, 0], angle=np.radians(10.0))
    print SS.get_volume(mesh_out) / 1.0E9

    water = SS.load_mesh('Water.STL')
    water_centroid = SS.get_centroid(water)
    water = SS.translate_mesh(water, [-water_centroid[0], -water_centroid[1], -140.0])
    # submerged = SS.subtract(mesh_out, water)
    # print SS.get_volume(submerged) / 1.0E9 * 1000.0
    # print SS.get_centroid(submerged)
    # SS.plot_2d(SS.rotate_mesh(submerged, point=None, axis=[1, 0, 0], angle=np.radians(180.0)), waterline=-140.0)
    SS.plot_stl(water)
    plt.show()
