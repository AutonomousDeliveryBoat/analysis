import numpy as np
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt

# inputs
total_mass = 50.0 # kg
water_density = 1000.0 # kg / m^3
hull_displacement = total_mass / water_density / 2.0 # displacement of each hull
space_ratio = 0.5 # ratio of hull spacing to length
boat_velocity = np.array([1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0]) # m/s
desired_hull = 0 #index (only used in dimension calculations)
efficiency = 0.7

# hull size calculations
L_calc = 1.83335912186
B_T = 2.0
Cb = 0.397

# resistance table lookup
Fr_table = np.linspace(0.2, 1.0, 17)
space_ratio_table = [0.3, 0.4, 0.5]

# boat 3b appendix table
Cr_table = np.matrix('3.214  2.642  2.555;'
               '3.726  4.019  3.299;'
               '4.750  4.464  3.938;'
               '5.943  5.472  4.803;'
               '7.648  7.085  6.589;'
               '12.569  10.934  9.064;'
               '14.237  12.027  10.112;'
               '12.275  10.538  9.394;'
               '10.089  8.962  8.361;'
               '8.123  7.592  7.488;'
               '6.852  6.642  6.726;'
               '5.934  5.921  6.078;'
               '5.289  5.373  5.537;'
               '4.814  4.949  5.046;'
               '4.452  4.543  4.624;'
               '4.172  4.236  4.335;'
               '3.936  3.996  4.099')

# function that does 2d interpolation on the table
Cr_lookup = interp2d(space_ratio_table, Fr_table, Cr_table, bounds_error=True)

# lookup Cr
Fr = boat_velocity / np.sqrt(9.81 * L_calc)
Cr = Cr_lookup(space_ratio, Fr)[0] / 1000.0

# Reynolds Numbers
Vm = boat_velocity * np.sqrt(1.6 / L_calc)
Re_model = Vm * 1.6 / 1.14E-6
Re_ship = boat_velocity * L_calc / 1.14E-6

C_fm = 0.075 / (np.log10(Re_model) - 2) ** 2
C_fs = 0.075 / (np.log10(Re_ship) - 2) ** 2

Ct = C_fs + Cr

# calculate Cs
Cs = 6.554 - 1.226*B_T + 0.216*B_T**2\
     - 15.409*Cb + 4.468*B_T*Cb - 0.694*(B_T**2)*Cb\
     + 15.404*Cb**2 - 4.527*B_T*(Cb**2) + 0.655*(B_T**2)*(Cb**2)
S = 2*Cs*np.sqrt(hull_displacement * L_calc)

# calculate drag force on hull and power required
Rt = Ct * 0.5 * water_density * boat_velocity**2 * S
P_raw = Rt * boat_velocity
P_actual = P_raw / efficiency

print '###### RESISTANCE PARAMETERS ######'
print 'Rt: ' + str(Rt) + ' N'
print 'Total Propulsive Power: ' + str(P_actual) + ' W'

boat_velocity = np.insert(boat_velocity, 0, [0.0])
P_actual = np.insert(P_actual, 0, [0.0])
plt.plot(boat_velocity, P_actual)
plt.xlabel('Velocity of Full Scale (m/s)')
plt.ylabel('Effective Horsepower')
plt.title('Velocity vs. EHP')
plt.show()