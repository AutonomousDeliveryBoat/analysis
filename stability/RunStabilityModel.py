from StaticStability import StaticStability
import numpy as np
import matplotlib.pyplot as plt

# inputs
CAD_filename = 'Hull_Doubled_Full-Scale.STL'
waterline_filename = 'Water.STL'

rotation_point = None
rotation_axis = [1.0, 0.0, 0.0]

boat_mass = 46.0 # kg
max_angle = 20.0 # deg
num_steps = 20 # deg

waterline_level = 140.0 # mm

# computations
stability_model = StaticStability()
mesh_in = stability_model.load_mesh(CAD_filename)

# translate boat
centroid = stability_model.get_centroid(mesh_in)
mesh_in = stability_model.translate_mesh(mesh_in, [-centroid[0], -centroid[1], 0.0])

i = 0
for theta in np.linspace(0.0, max_angle, num_steps):

    print "Current Angle: " + str(theta) + '\n'

    # rotate the mesh
    rads = np.radians(theta)
    mesh_rot = stability_model.rotate_mesh(mesh_in, point=rotation_point, axis=rotation_axis, angle=rads)

    # only get the submerged section
    water = stability_model.load_mesh(waterline_filename)
    water_centroid = stability_model.get_centroid(water)
    water = stability_model.translate_mesh(water, [-water_centroid[0], -water_centroid[1], -5.0 * 1000.0 + waterline_level])
    submerged = stability_model.subtract(mesh_rot, water)

    stability_model.plot_2d(stability_model.rotate_mesh(submerged, point=None, axis=[1, 0, 0], angle=np.radians(180.0)), waterline=-waterline_level)
    plt.savefig('img/' + str(i) + '.png')
    i += 1