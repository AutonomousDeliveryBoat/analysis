from StaticStability import StaticStability
import numpy as np
import matplotlib.pyplot as plt

# inputs
CAD_filename = 'Hull_Doubled_Full-Scale.STL'
waterline_filename = 'Water.STL'

rotation_point = [0.0, 0.0, 0.0]
rotation_axis = [1.0, 0.0, 0.0]

boat_mass = 46.0 # kg
max_angle = 20.0 # deg
num_steps = 20 # deg

waterline_level = 140.0 # mm

# computations
stability_model = StaticStability()
mesh_in = stability_model.load_mesh(CAD_filename)

# translate and flip the boat
centroid = stability_model.get_centroid(mesh_in)
mesh_in = stability_model.translate_mesh(mesh_in, [-centroid[0], -centroid[1], 0.0])
mesh_in = stability_model.rotate_mesh(mesh_in, point=None, axis=[1, 0, 0], angle=np.radians(180.0))

i = 0
for theta in np.linspace(0.0, max_angle, num_steps):

    print "Current Angle: " + str(theta) + '\n'

    # rotate the mesh
    rads = np.radians(theta)
    mesh_rot = stability_model.rotate_mesh(mesh_in, point=rotation_point, axis=rotation_axis, angle=rads)

    # only get the submerged section
    water = stability_model.load_mesh(waterline_filename)
    water_centroid = stability_model.get_centroid(water)
    water = stability_model.translate_mesh(water, [-water_centroid[0], -water_centroid[1], -waterline_level])
    submerged = stability_model.subtract(mesh_rot, water)

    # get CB
    CB = stability_model.get_centroid(submerged)

    # plot the boat in 2D
    stability_model.plot_2d(submerged, waterline=-waterline_level)
    plt.scatter(CB[1], CB[2], marker='x', c='r', s=40)
    plt.scatter(rotation_point[1], rotation_point[2], marker='+', c='g', s=80)
    plt.savefig('img/' + str(i) + '.png')
    i += 1