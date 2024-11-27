## CODE DEVELOP FOR AN AIRCRAFT SIMULATOR IN PYTHON FOLLOWING BEN DICKINSON FROM YOUTUBE TUTORIAL SINCE MARCH 2024.
## THIS IS THE MAIN FILE RESPONSIBLE FOR CONTROLLING ALL THE SIMULATION WITH INITIAL CONDITIONS, MODELS OF GRAVITY AND
## ATMOSPHERE, CONFIGURATIONS FOR THE AIRCRAFT, TYPE OF AIRCRAFT, AND SUBSYSTEMS IMPLEMENTED AS WELL THE INTEGRATION
## METHODS AND PLOTTING ALL THE RESULTS.
## FREDERICO CASARA ANTONIAZZI - 26/11/2024

## LOADING THE LIBRARIES:
import math
import ussa1976
import numpy as np
import matplotlib.pyplot as plt

## IMPORTING THE METHODS AND MODELS:
from tools import Interpolators
from vehicleModels import spheres
from earthModel_eom import flatEarth
from integrationMethods import numericalIntegration

########################################################################################################################
## BEGIN OF THE CODE:
########################################################################################################################

# ATMOSPHERIC DATA:
atmosphere = ussa1976.compute()

# GET ESSENTIAL GRAVITY AND ATMOSPHERIC DATA
alt_m     = atmosphere["z"].values
rho_kgpm3 = atmosphere["rho"].values
c_mps     = atmosphere["cs"].values
g_mps2    = ussa1976.core.compute_gravity(alt_m)

amod = {"alt_m"     : alt_m,
        "rho_kgpm3" : rho_kgpm3,
        "c_mps"     : c_mps,
        "g_mps2"    : g_mps2}

# DEFINING THE VEHICLE:
vmod = spheres.bowlingBall()

## INITIALIZATION:
u0_b_mps   = 0.001 # AVOIDS DIVIDING BY ZERO
v0_b_mps   = 0
w0_b_mps   = 0
p0_b_rps   = 0
q0_b_rps   = 0
r0_b_rps   = 0
phi0_rad   = 0*math.pi/180
theta0_rad = -90*math.pi/180
psi0_rad   = 0
p10_n_m    = 0
p20_n_m    = 0
p30_n_m    = -10000

x0 = np.array([
u0_b_mps,
v0_b_mps,
w0_b_mps,
p0_b_rps,
q0_b_rps,
r0_b_rps,
phi0_rad,
theta0_rad,
psi0_rad,
p10_n_m,
p20_n_m,
p30_n_m
])

x0 = x0.transpose()
nx0 = x0.size

# SETTING THE TIME CONDITIONS:
t0_s = 0.0
tf_s = 100
h_s = 0.01

## SEOND PART:

t_s = np.arange(t0_s, tf_s + h_s, h_s)
nt_s = t_s.size
x = np.empty((nx0, nt_s), dtype = float)

x[:, 0] = x0

t_s, x = numericalIntegration.forward_Euler(flatEarth.flatModel_eom, t_s, x, h_s, vmod, amod)

trueAirSpeed_mps = np.zeros((nt_s, 1))
for i, element in enumerate(t_s):
        trueAirSpeed_mps[i, 0] = math.sqrt(x[0, i]**2 + x[1, i]**2 + x[2, i]**2)

Altitude_m = np.zeros((nt_s, 1))
Cs_mps = np.zeros((nt_s, 1))
Rho_kgm3 = np.zeros((nt_s, 1))

for i, element in enumerate(t_s):
        Altitude_m[i, 0] = -x[11, i]
        Cs_mps[i, 0] = Interpolators.fastInterp1(amod["alt_m"], amod["c_mps"], Altitude_m[i, 0])
        Rho_kgm3[i, 0] = Interpolators.fastInterp1(amod["alt_m"], amod["rho_kgm3"], Altitude_m[i, 0])

# CALCULATING THE ANGLE OF ATTACK(AoA):
alpha_rad = np.zeros((t_s, 1))
for i, element in enumerate(t_s):
        if x[0, i] == 0 and x[2, i] == 0:
                w_over_v = 0
        else:
                w_over_v = x[2, i]/x[0, i]

        alpha_rad[i, 0] = math.atan(w_over_v)

# CALCULANTING THE ANGLE OF SIDE SLIPE:
beta_rad = np.zeros((t_s, 1))
for i, element in enumerate(t_s):
        if x[i, 0] == 0 and trueAirSpeed_mps[i, 0] == 0:
                v_over_VT = 0
        else:
                v_over_VT = x[1, i]/trueAirSpeed_mps[i, 0]

        beta_rad[i, 0] = math.asin(v_over_VT)

# CALCULATING THE MACH NUMBER:
Mach = np.zeros((t_s, 1))
for i, element in enumerate(t_s):
        Mach[i, 0] = trueAirSpeed_mps[i, 0]/Cs_mps[i, 0]

## PLOTTING THE RESULTS:

fig, axes = plt.subplots(2, 4, figsize=(10, 6))
fig.set_facecolor('black')

# AXIAL VELOCITY PLOT: u_b_mps
axes[0, 0].plot(t_s, x[0, :], color = 'yellow')
axes[0, 0].set_xlabel('Time / [s]', color = 'white')
axes[0, 0].set_ylabel('u / [m/s]', color = 'white')
axes[0, 0].set_facecolor('black')
axes[0, 0].grid(True)
axes[0, 0].tick_params(colors = 'white')

# LATERAL VELOCITY PLOT: v_b_mps
axes[0, 1].plot(t_s, x[1, :], color = 'yellow')
axes[0, 1].set_xlabel('Time / [s]', color = 'white')
axes[0, 1].set_ylabel('v / [m/s]', color = 'white')
axes[0, 1].set_facecolor('black')
axes[0, 1].grid(True)
axes[0, 1].tick_params(colors = 'white')

# VELOCITY PLOT: z_b_mps
axes[0, 2].plot(t_s, x[2, :], color = 'yellow')
axes[0, 2].set_xlabel('Time / [s]', color = 'white')
axes[0, 2].set_ylabel('w / [m/s]', color = 'white')
axes[0, 2].set_facecolor('black')
axes[0, 2].grid(True)
axes[0, 2].tick_params(colors = 'white')

# ROLL RATE PLOT: p_b_rps
axes[0, 3].plot(t_s, x[6, :], color = 'yellow')
axes[0, 3].set_xlabel('Time / [s]', color = 'white')
axes[0, 3].set_ylabel('phi / [rad]', color = 'white')
axes[0, 3].set_facecolor('black')
axes[0, 3].grid(True)
axes[0, 3].tick_params(colors = 'white')

# PITCH RATE PLOT: q_b_rps
axes[1, 0].plot(t_s, x[3, :], color = 'yellow')
axes[1, 0].set_xlabel('Time / [s]', color = 'white')
axes[1, 0].set_ylabel('p / [rps]', color = 'white')
axes[1, 0].set_facecolor('black')
axes[1, 0].grid(True)
axes[1, 0].tick_params(colors = 'white')

# YAW RATE PLOT: r_b_rps
axes[1, 1].plot(t_s, x[4, :], color = 'yellow')
axes[1, 1].set_xlabel('Time / [s]', color = 'white')
axes[1, 1].set_ylabel('q / [rps]', color = 'white')
axes[1, 1].set_facecolor('black')
axes[1, 1].grid(True)
axes[1, 1].tick_params(colors = 'white')

# ROLL ANGLE PLOT: phi_rad
axes[1, 2].plot(t_s, x[5, :], color = 'yellow')
axes[1, 2].set_xlabel('Time / [s]', color = 'white')
axes[1, 2].set_ylabel('r / [rps]', color = 'white')
axes[1, 2].set_facecolor('black')
axes[1, 2].grid(True)
axes[1, 2].tick_params(colors = 'white')

# PITCH ANGLE PLOT: theta_rad
axes[1, 3].plot(t_s, x[7, :], color = 'yellow')
axes[1, 3].set_xlabel('Time / [s]', color = 'white')
axes[1, 3].set_ylabel('theta / [rad]', color = 'white')
axes[1, 3].set_facecolor('black')
axes[1, 3].grid(True)
axes[1, 3].tick_params(colors = 'white')
"""
# YAW ANGLE PLOT: psi_rad
axes[2, 0].plot(t_s, x[8, :], color = 'yellow')
axes[2, 0].set_xlabel('Time / [s]', color = 'white')
axes[2, 0].set_ylabel('psi / [rad]', color = 'white')
axes[2, 0].set.facecolor('black')
axes[2, 0].grid(True)
axes[2, 0].tick_params(colors = 'white')

## POSITION(NOT YET IMPLEMENTED)

# PITCH ANGLE PLOT: theta_rad
axes[2, 1].plot(t_s, x[8, :], color = 'yellow')
axes[2, 1].set_xlabel('Time / [s]', color = 'white')
axes[2, 1].set_ylabel('theta / [rad]', color = 'white')
axes[2, 1].set.facecolor('black')
axes[2, 1].grid(True)
axes[2, 1].tick_params(colors = 'white')
# PITCH ANGLE PLOT: theta_rad
axes[2, 2].plot(t_s, x[8, :], color = 'yellow')
axes[2, 2].set_xlabel('Time / [s]', color = 'white')
axes[2, 2].set_ylabel('theta / [rad]', color = 'white')
axes[2, 2].set.facecolor('black')
axes[2, 2].grid(True)
axes[2, 2].tick_params(colors = 'white')
# PITCH ANGLE PLOT: theta_rad
axes[2, 2].plot(t_s, x[8, :], color = 'yellow')
axes[2, 2].set_xlabel('Time / [s]', color = 'white')
axes[2, 2].set_ylabel('theta / [rad]', color = 'white')
axes[2, 2].set.facecolor('black')
axes[2, 2].grid(True)
axes[2, 2].tick_params(colors = 'white')
"""
#SHOWING
plt.tight_layout()
plt.savefig('savedGraphs/sphereTest1.png')
plt.show()
