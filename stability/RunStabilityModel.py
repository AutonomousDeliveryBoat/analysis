from StaticStability import StaticStability
import numpy as np
import matplotlib.pyplot as plt

# files
CAD_filename = 'Hull_Doubled_Full-Scale.STL'
waterline_filename = 'Water.STL'

# computations
stability_model = StaticStability()
mesh_in = stability_model.load_mesh(CAD_filename)

# translate and flip the boat
centroid = stability_model.get_centroid(mesh_in)
mesh_in = stability_model.translate_mesh(mesh_in, [-centroid[0], -centroid[1], 0.0])
mesh_in = stability_model.rotate_mesh(mesh_in, point=None, axis=[1, 0, 0], angle=np.radians(180.0))

# inputs
rotation_point = [0.0, 0.0, np.min(mesh_in.vertices[:, 2])]
center_of_gravity = [0.0, 0.0, 0.0] # np.average(mesh_in.vertices[:, 2])
rotation_axis = [1.0, 0.0, 0.0]

boat_mass = 46.0  # kg
max_angle = 80.0  # deg
num_steps = 40  # deg
thetas = np.linspace(0.0, max_angle, num_steps)
np.save('thetas.npy', thetas)

waterline_level = 136.9  # m

# get vector from rotation point to CG
r_cg =  np.array(center_of_gravity) - np.array(rotation_point)

# empty matrices for  plotting
CG_y = []
CG_z = []

CB_y = []
CB_z = []

gravity_moment_arr = []
bouyancy_moment_arr = []
righting_moment_arr = []

i = 0
for theta in thetas:
    print "Current Angle: " + str(theta)

    # construct rotation matrix
    rads = np.radians(theta)
    R = np.array([[1, 0, 0], [0, np.cos(-rads), -np.sin(-rads)], [0, np.sin(-rads), np.cos(-rads)]])

    # rotate the mesh
    mesh_rot = stability_model.rotate_mesh(mesh_in, point=rotation_point, axis=rotation_axis, angle=rads)

    # only get the submerged section
    water = stability_model.load_mesh(waterline_filename)

    waterline_level, submerged = stability_model.calculate_waterline(mesh_rot, boat_mass, water, waterline_level)
    print "Waterline Level: " + str(waterline_level) + " mm"


    # get CB
    CB = stability_model.get_centroid(submerged)
    r_cb_rot = np.array(CB) - np.array(rotation_point)
    B_force = stability_model.get_volume(submerged)/1E9 * 1000.0 * 9.81

    # get CG
    r_cg_rot = np.dot(R, r_cg)
    CG = r_cg_rot + np.array(rotation_point)

    # calculate moment due to gravity
    gravity_moment = r_cg_rot[1]/1000.0 * -(boat_mass * 9.81)
    bouyancy_moment = r_cb_rot[1]/1000.0 * B_force
    righting_moment = gravity_moment + bouyancy_moment
    print "Gravity Moment: " + str(gravity_moment) + ' N-m'
    print "Bouyancy Moment: " + str(bouyancy_moment) + ' N-m'
    print "Righting Moment: " + str(righting_moment) + ' N-m'

    # save CG and CB
    CB_y.append(CB[1])
    CB_z.append(CB[2])
    CG_y.append(CG[1])
    CG_z.append(CG[2])

    # save moments
    righting_moment_arr.append(righting_moment)
    bouyancy_moment_arr.append(bouyancy_moment)
    gravity_moment_arr.append(gravity_moment)

    # plot the boat in 2D
    stability_model.plot_2d(mesh_rot, waterline=-waterline_level)

    plt.scatter(CB[1], CB[2], marker='x', c='r', s=40)
    plt.scatter(rotation_point[1], rotation_point[2], marker='+', c='g', s=80)
    plt.scatter(CG[1], CG[2], marker='+', c='k', s=80)

    plt.quiver(CB[1], CB[2], 0, B_force, color='r')
    plt.quiver(CG[1], CG[2], 0, -boat_mass * 9.81, color='k')

    plt.plot(CB_y, CB_z, 'r')
    plt.plot(CG_y, CG_z, 'k')
    plt.savefig('img/' + str(i) + '.png')
    plt.close()
    i += 1

    print "Current Displacement: " + str(stability_model.get_volume(submerged)/1E9 * 1000.0) + '\n'

np.save('moment.npy', righting_moment_arr)
np.save('grav.npy', gravity_moment_arr)
np.save('bouy.npy', bouyancy_moment_arr)

plt.figure()
plt.plot(thetas, righting_moment_arr)
plt.xlabel('Theta (deg)')
plt.ylabel('Righting Moment (N-m)')
plt.savefig('img/righting_moment.png')
plt.show()
