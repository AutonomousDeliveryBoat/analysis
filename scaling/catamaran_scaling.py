import numpy as np
from scipy.interpolate import interp2d

# inputs
total_mass = 50.0 # kg
water_density = 1000.0 # kg / m^3
hull_displacement = total_mass / water_density / 2 # displacement of each hull
space_ratio = 0.5 # ratio of hull spacing to length
boat_velocity = 3.0 # m/s
desired_hull = 0 #index (only used in dimension calculations)
efficiency = 0.75


# southampton catamaran series data
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

# hull size calculations
L_calc = L_D_1_3 * hull_displacement ** (1.0 / 3.0)
B_calc = L_calc / L_B
draft = B_calc / B_T
space_btw_hulls = L_calc * space_ratio
boat_width = B_calc + space_btw_hulls

print '\n###### INPUT PARAMETERS ######'
print "Chosen Hull: " + str(models[desired_hull])
print "Total Mass Displaced: " + str(total_mass) + ' kg'
print "Desired Velocity: " + str(boat_velocity) + ' m/s\n\n'

print '###### SIZE PARAMETERS ######'
print "Total Length: " + str(L_calc[desired_hull]) + ' m'
print "Total Width: " + str(boat_width[desired_hull]) + ' m'
print "Draft: " + str(draft[desired_hull]) + ' m'
print "Hull Width: " + str(B_calc[desired_hull]) + ' m\n\n'

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
Fr = boat_velocity / np.sqrt(9.81 * L_calc[desired_hull])
Cr = Cr_lookup(space_ratio, Fr)[0] / 1000.0

# Reynolds Numbers
Vm = boat_velocity * np.sqrt(1.6 / L_calc[desired_hull])
Re_model = Vm * 1.6 / 1.14E-6
Re_ship = boat_velocity * L_calc[desired_hull] / 1.14E-6

C_fm = 0.075 / (np.log10(Re_model) - 2) ** 2
C_fs = 0.075 / (np.log10(Re_ship) - 2) ** 2

Ct = C_fs + Cr

# calculate Cs
Cs = 6.554 - 1.226*B_T[desired_hull] + 0.216*B_T[desired_hull]**2\
     - 15.409*Cb + 4.468*B_T[desired_hull]*Cb - 0.694*(B_T[desired_hull]**2)*Cb\
     + 15.404*Cb**2 - 4.527*B_T[desired_hull]*(Cb**2) + 0.655*(B_T[desired_hull]**2)*(Cb**2)
S = 2*Cs*np.sqrt(hull_displacement * L_calc[desired_hull])

# calculate drag force on hull and power required
Rt = Ct * 0.5 * water_density * boat_velocity**2 * S
P_raw = Rt * boat_velocity
P_actual = P_raw / efficiency

print '###### DIMENSIONLESS PARAMETERS ######'
print 'Fr: ' + str(Fr)
print 'Cf: ' + str(C_fs)
print 'Cr: ' + str(Cr)
print 'Ct: ' + str(Ct) + '\n\n'

print '###### RESISTANCE PARAMETERS ######'
print 'Rt: ' + str(Rt) + ' N'
print 'Total Propulsive Power: ' + str(P_actual) + ' W'