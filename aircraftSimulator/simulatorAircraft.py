## CODE DEVELOP FOR AN AIRCRAFT SIMULATOR IN PYTHON FOLLOWING BEN DICKINSON FROM YOUTUBE TUTORIAL SINCE MARCH 2024.
## THIS IS THE MAIN FILE RESPONSIBLE FOR CONTROLLING ALL THE SIMULATION WITH INITIAL CONDITIONS, MODELS OF GRAVITY AND
## ATMOSPHERE, CONFIGURATIONS FOR THE AIRCRAFT, TYPE OF AIRCRAFT, AND SUBSYSTEMS IMPLEMENTED AS WELL THE INTEGRATION
## METHODS AND PLOTTING ALL THE RESULTS.
## FREDERICO CASARA ANTONIAZZI - 26/11/2024

## LOADING THE LIBRARIES:
import math
import numpy as np
import matplotlib.pyplot as plt

## IMPORTING THE METHODS AND MODELS:
from integrationMethods import forwardEuler
from earthModel_eom import flatModel_eom

########################################################################################################################
## BEGIN OF THE CODE:
########################################################################################################################

## INITIALIZATION:
u0_b_mps   = []
v0_b_mps   = []
w0_b_mps   = []
p0_b_rps   = []
q0_b_rps   = []
r0_b_rps   = []
phi0_rad   = []
theta0_rad = []
psi0_rad   = []
p10_n_m    = []
p20_n_m    = []
p30_n_m    = []

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
tf_s = 10
h_s = 0.01

## SEOND PART:

t_s = np.arange(t0_s, tf_s + h_s, h_s)
nt_s = t_s.size
x = np.empty((nx0, nt_s), dtype = float)

x[:, 0] = x0

t_s, x = forwardEuler.foward_Euler(flatModel_eom, t_s, x, h_s)

## PLOTTING THE RESULTS:

fig, (ax1, ax2) = plt.subplot(1, 2, figsize=(10, 6))

ax1.plot(t_s, x[0, :], label='Line 1')
ax1.set_xlabel('Time / [s]')
ax1.set_ylabel('Line 1 Value')
ax1.set.Title('Line 1')
ax1.grid(True)

ax2.plot(t_s, x[1, :], label='Line 2')
ax2.set_xlabel('Time / [s]')
ax2.set_ylabel('Line 2 Value')
ax2.set.Title('Line 2')
ax2.grid(True)

#SHOWING
plt.show()




