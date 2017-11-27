import numpy as np
import matplotlib.pyplot as plt

# load data
thetas = np.load('thetas.npy')
righting_moment = np.load('moment.npy')
gravity_moment = np.load('grav.npy')
bouyancy_moment = np.load('bouy.npy')

# conversions
thetas_rad = np.radians(thetas)

# integrate to get energy
energy = np.empty(thetas_rad.shape)

for i in range(0, len(energy)):
    energy[i] = np.trapz(righting_moment[0:i+1], thetas_rad[0:i+1])

plt.plot(thetas, righting_moment)
plt.plot(thetas, energy)
plt.show()
