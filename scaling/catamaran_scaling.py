import numpy as np

# inputs
total_mass = 45.0 # kg
water_density = 1000.0
total_displacement = total_mass / water_density


# southampton catamaran series
models = np.array(['3b', '4a', '4b', '4c', '5a', '5b', '5c', '6a', '6b', '6c']) # different hull designs
L_model = 1.6 # tested length (m)
L_B = np.array([7.0, 10.4, 9.0, 8.0, 12.8, 11.0, 9.9, 15.1, 13.1, 11.7])
B_T = np.array([2.0, 1.5, 2.0, 2.5, 1.5, 2.0, 2.5, 1.5, 2.0, 2.5])
L_D_1_3 = np.array([6.27, 7.40, 7.41, 7.39, 8.51, 8.50, 8.49, 9.50, 9.50, 9.50])
Cb = 0.397
Cp = 0.693
Cm = 0.565
S = np.array([0.434, 0.348, 0.338, 0.340, 0.282, 0.276, 0.277, 0.240, 0.233, 0.234])
LCB = -6.4

