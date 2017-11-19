import numpy as np
import matplotlib.pyplot as plt

# Inputs
vel_FS = np.array([])
vel_M = np.array([])
value = 0.2
# while value < 5.75:
#     vel_FS = np.append(vel_FS, [value])
#     value = value + 0.25
while value < 3.2:  # set the velocity values we are going to test.
    vel_M = np.append(vel_M, [value])
    value = value + 0.2

# Model properties
L_M = 0.3047  # length of the model, in m
C_bM = 0.397
B_M = 0.041  # width of the model, in m
T_M = 0.041  # draft of model, in m
rho_M = 1000  # water density (temperature dependent) of fluid where model is tested
S_M = 1.025 * (1.7 * L_M * T_M + C_bM * L_M * B_M)  # model wetted surface
nu_M = 8.9e-4  # fluid viscosity of fluid where model is tested

Froude = vel_M / np.sqrt(9.81 * L_M)

# Full scale properties
L_FS = 1.83335912186  # length of full scale boat, in m
C_bFS = 0.397
B_FS = 0.26190844598  # width of full scale boat, in m
T_FS = 0.13095422299  # draft of full scale boat, in m
rho_FS = 1000  # water density (temperature dependent) of fluid where full scale is used
S_FS = 1.025 * (1.7 * L_FS * T_FS + C_bFS * L_FS * B_FS)  # full scale wetted surface
nu_FS = 8.9e-4  # fluid viscosity of fluid where full scale is used

vel_FS = vel_M / np.sqrt(L_M / L_FS)  # Make sure vel_FS is between 0 and ~ 5 m/s
R_TM = np.array([0.2, 0.5, 1.1, 1.8, 2.7, 3.9, 5.3, 6.9, 8.7, 10.7, 13, 15.5, 18.2, 21,
                 24.2])  # input values found from load cell for each velocity
# while len(R_TM) < len(vel_FS): # just for testing my code
#     R_TM = np.append(R_TM, 0.2*0.5*rho_M*np.square(vel_M)*S_M)
# print R_TM

#  Calculating model coefficients
C_TM = R_TM / (0.5 * rho_M * np.square(vel_M) * S_M)
R_nM = (vel_M * L_M) / nu_M
C_FM = 0.075 / (np.log10(R_nM) - 2) ** 2
C_R = C_TM - C_FM

# Calculating full scale coefficients
R_nFS = (vel_FS * L_FS) / nu_FS
C_FFS = 0.075 / (np.log10(R_nFS) - 2) ** 2
C_TS = C_FFS + C_R

R_TS = 0.5 * C_TS * rho_FS * np.square(vel_FS) * S_FS
# R_TS = np.square(vel_FS)

EHP = R_TS * vel_FS

# m = np.array([])
# idx = 0
# while idx < 14:
#     m = np.append(m,[(R_TS[idx+1]-R_TS[idx])/(vel_FS[idx+1]-vel_FS[idx])])
#     idx += 1

plt.plot(vel_FS, EHP)
plt.show()
