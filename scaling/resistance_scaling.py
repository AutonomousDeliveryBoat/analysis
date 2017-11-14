import numpy as np
import matplotlib.pyplot as plt

# Inputs
vel_FS = np.array([])
vel_M = np.array([])
value = 0.2
# while value < 5.75:
#     vel_FS = np.append(vel_FS, [value])
#     value = value + 0.25
while value < 3.2: # set the velocity values we are going to test.
    vel_M = np.append(vel_M, [value])
    value = value + 0.2

L_M = 0.4 # length of the model, in m
C_bM = 0.397
B_M = 0.1 # width of the model, in m
T_M = 0.2

L_FS = 1.83335912186 # length of the full scale boat, in m
C_bFS = 0.397
B_FS = 0.26190844598
T_FS = 1.17858800691

vel_FS = vel_M/np.sqrt(L_M/L_FS) # Make sure vel_FS is between 0 and ~ 5 m/s
R_TM = np.array([]) # input values found from load cell for each velocity
while len(R_TM) < len(vel_FS): # just for testing my code
    R_TM = np.append(R_TM, 1)

# Model properties
rho_M = 1 # water density (temperature dependent) of fluid where model is tested
S_M = 1.025*(1.7*L_M*T_M + C_bM*L_M*B_M) # model wetted surface
nu_M = 1 # fluid viscosity of fluid where model is tested

# Calculating model coefficients
C_TM = R_TM / (0.5*rho_M*np.square(vel_M)*S_M)
R_nm = (vel_M*L_M)/nu_M
C_FM = 0.075 / (np.log10(R_nm)-2)**2

C_R = C_TM - C_FM

# Full scale properties
rho_FS = 1 # water density (temperature dependent) of fluid where full scale is used
S_FS = 1.025*(1.7*L_FS*T_FS + C_bFS*L_FS*B_FS) # full scale wetted surface
nu_FS = 1 # fluid viscosity of fluid where full scale is used

# Calculating full scale coefficients
R_nfs = (vel_FS*L_FS)/nu_FS
C_FFS = 0.075 / (np.log10(R_nfs)-2)**2
C_TS = C_FFS + C_R

R_TS = 0.5*C_TS*rho_FS*np.square(vel_FS)*S_FS

EHP = R_TS*vel_FS/550

plt.plot(vel_FS,EHP)
plt.show()




