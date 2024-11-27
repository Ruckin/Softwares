########################################################################################################################
## LOADING THE NECESSARY LIBRARIES FOR DEVELOPING THE EARTH MODEL:
########################################################################################################################
import math
import numpy as np
from tools import Interpolators

########################################################################################################################
## EXAMPLE OF MODEL FOR EARTH:
## THIS EXAMPLE USES THE FLAT EARTH EQUATIONS FOR MODELING THE EARTH
########################################################################################################################
def flatModel_eom(t, x, vmod, amod):
    """ FUNCTION flatModel_eom: Contains the essential elements of a six degree of freedom simulation. The purpose of
                                this function is to allow the numerical approximation of solutions of the governing
                                equations for an aircraft.
                            
        Name convention is like: <variable_name>_coordinate system if applicable>_<units>. For example, the pitch rate,
                                 q, resolved in the body fixed frame, bf, with units of radians per second is named as
                                 <q_b_rps>.
                             
        Arguments used in this functions:
            t       - Scalar vector of time unities [seconds - s].
            x       - State vector at time t [various units], numpy array.
              x[0]  - u_b_mps,   axial velocity of CM wrt inertial CS resolved in the aircraft body fixed CS
              x[1]  - v_b_mps,   lateral velocity of CM wrt inertial CS resolved in the aircraft body fixed CS
              x[2]  - w_b_mps,   vertical velocity of CM wrt inertial CS resolved in the aircraft body fixed CS
              x[3]  - p_b_rps,   roll angular velocity of body fixed CS with respect to inertial CS
              x[4]  - q_b_rps,   pitch angular velocity of body fixed CS with respect to inertial CS
              x[5]  - r_b_rps,   yaw angular velocity of body fixed CS with respect to inertial CS
              x[6]  - phi_rad,   roll angle
              x[7]  - theta_rad, pitch angle
              x[8]  - psi_rad,   yaw angle
              x[9]  - p1_n_m,    x-axis position of the aircraft resolved in NED CS
              x[10] - p2_n_m,    y-axis position of the aircraft resolved in NED CS
              x[11] - p3_n_m,    z-axis position of the aircraft resolved in NED CS
              amod  - Aircraft model data stored as a dictionary containing various parameters.

        Returns:
            dx - The time derivative of each state in x(RHS governing equations).

        History:
            Written by Ben Dickinson - March 2024
                * Six DOF Equations

    """

    # PRELOADING THE SPACE FOR THE TIME DERIVATIVE:
    dx = np.empty((12,), dtype = float)

    # ASSINGING VARIABLE NAME TO THE STATES:
    u_b_mps   = x[0]
    v_b_mps   = x[1]
    w_b_mps   = x[2]
    p_b_rps   = x[3]
    q_b_rps   = x[4]
    r_b_rps   = x[5]
    phi_rad   = x[6]
    theta_rad = x[7]
    psi_rad   = x[8]
    p1_n_m    = x[9]
    p2_n_m    = x[10]
    p3_n_m    = x[11]

    # LOADING THE DATA:
    m_kg       = vmod["m_kg"]
    Jxz_b_kgm2 = vmod["Jxz_b_kgm2"]
    Jxx_b_kgm2 = vmod["Jxx_b_kgm2"]
    Jyy_b_kgm2 = vmod["Jyy_b_kgm2"]
    Jzz_b_kgm2 = vmod["Jzz_b_kgm2"]

    # CORRECTING THE ALTITUDE:
    h_m = -p3_n_m

    #rho_interp_kgpm3 = Interpolators(amod["alt_m"], amod["rho_kgpm3"], h_m)
    rho_interp_kgpm3 = 1.20
    c_interp_mp2     = Interpolators.fastInterp1(amod["alt_m"], amod["c_mps"], h_m)

    # AIR DATA CALCULATION(MACH, AoA, AoS):
    trueAirSpeed_mps = math.sqrt(u_b_mps**2 + v_b_mps**2 + w_b_mps**2)
    qbar_kgpms2      = 0.5*rho_interp_kgpm3*trueAirSpeed_mps**2

    if u_b_mps == 0 and w_b_mps == 0:
        w_over_u = 0
    else:
        w_over_u = w_b_mps/u_b_mps

    if trueAirSpeed_mps == 0 and v_b_mps == 0:
        v_over_VT = 0
    else:
        v_over_VT = v_b_mps/trueAirSpeed_mps

    alpha_rad = math.atan(w_over_u)
    beta_rad = math.asin(v_over_VT)

    # GRAVITY MODEL:
    # FIRST MODEL ACTS NORMAL TO THE EARTH TANGENT CS
    #gz_interp_n_mps2 = Interpolators(amod["alt_m"], amod["g_mps2"], h_m)
    gz_interp_n_mps2 = 9.81

    # RESOLVING GRAVITY IN BODY COORDINATE SYSTEM:
    gx_b_mps2 = -math.sin(theta_rad)*gz_interp_n_mps2
    gy_b_mps2 = math.sin(phi_rad)*math.cos(theta_rad)*gz_interp_n_mps2
    gz_b_mps2 = math.cos(phi_rad)*math.cos(theta_rad)*gz_interp_n_mps2

    # AERODYNAMIC FORCES:
    drag_kgmps2 = vmod(["CD_approx"])*qbar_kgpms2*vmod(["Aref_m2"])
    side_kgmps2 = 0
    lift_kgmps2 = 0

    # EXTERNAL FORCES:
    Fx_b_kgmps2 = -(math.cos(alpha_rad)*math.cos(beta_rad)*drag_kgmps2 - math.cos(alpha_rad)*math.sin(beta_rad)*side_kgmps2 - math.sin(alpha_rad)*lift_kgmps2)
    Fy_b_kgmps2 = -(math.sin(beta_rad)*drag_kgmps2 + math.cos(beta_rad)*side_kgmps2)
    Fz_b_kgmps2 = -(math.sin(alpha_rad)*math.cos(beta_rad)*drag_kgmps2 - math.sin(alpha_rad)*math.sin(beta_rad)*side_kgmps2 + math.cos(alpha_rad)*lift_kgmps2)

    # EXTERNAL MOMENTS:
    l_b_kgm2ps2 = 0
    m_b_kgm2ps2 = 0
    n_b_kgm2ps2 = 0

    # DENOMINATOR IN ROLL AND YAW RATE EQUATIONS:
    Den = Jxx_b_kgm2*Jzz_b_kgm2 - Jxz_b_kgm2

    # CALCULATING THE TIME DERIVATIVE FOR THE STATE VECTOR:
    # x-AXIS (ROLL AXIS) VELOCITY EQUATION
    # STATE: u_b_mps
    dx[0] = 1/m_kg*Fx_b_kgmps2 + gx_b_mps2 - w_b_mps*q_b_rps + v_b_mps*r_b_rps

    # CALCULATING THE TIME DERIVATIVE FOR THE STATE VECTOR:
    # y-AXIS (PITCH AXIS) VELOCITY EQUATION
    # STATE: v_b_mps
    dx[1] = 1/m_kg*Fy_b_kgmps2 + gy_b_mps2 - u_b_mps*r_b_rps + w_b_mps*p_b_rps

    # CALCULATING THE TIME DERIVATIVE FOR THE STATE VECTOR:
    # z-AXIS (YAW AXIS) VELOCITY EQUATION
    # STATE: w_b_mps
    dx[2] = 1/m_kg*Fz_b_kgmps2 + gz_b_mps2 - v_b_mps*p_b_rps + u_b_mps*q_b_rps

    # CALCULATING THE TIME DERIVATIVE FOR THE STATE VECTOR:
    # ROLL EQUATION
    # STATE: p_b_rps
    dx[3] = (Jxz_b_kgm2*(Jxx_b_kgm2 - Jyy_b_kgm2 + Jzz_b_kgm2)*p_b_rps*q_b_rps -
            (Jzz_b_kgm2*(Jzz_b_kgm2 - Jyy_b_kgm2) + Jxz_b_kgm2**2)*q_b_rps*r_b_rps +
            Jxz_b_kgm2*n_b_kgm2ps2)/Den

    # CALCULATING THE TIME DERIVATIVE FOR THE STATE VECTOR:
    # PITCH EQUATION
    # STATE: q_b_rps
    dx[4] = ((Jzz_b_kgm2 - Jxx_b_kgm2)*p_b_rps*r_b_rps - Jxz_b_kgm2*(p_b_rps**2 - r_b_rps) + m_b_kgm2ps2)/Jyy_b_kgm2

    # CALCULATING THE TIME DERIVATIVE FOR THE STATE VECTOR:
    # YAW EQUATION
    # STATE: r_b_rps
    dx[5] = ((Jxx_b_kgm2*(Jxx_b_kgm2 - Jyy_b_kgm2) + Jxz_b_kgm2**2)*p_b_rps*q_b_rps +
            Jxz_b_kgm2*(Jxx_b_kgm2 - Jyy_b_kgm2 + Jzz_b_kgm2)*q_b_rps*r_b_rps + Jxz_b_kgm2*l_b_kgm2ps2 +
            Jxz_b_kgm2*n_b_kgm2ps2)/Den

    # KINEMATICS EQUATIONS:
    # EULER KINEMATICS
    dx[6] = p_b_rps + math.tan(theta_rad)*(math.sin(phi_rad)*q_b_rps + math.cos(phi_rad)*r_b_rps)

    dx[7] = math.cos(phi_rad)*q_b_rps - math.sin(phi_rad)*r_b_rps

    dx[8] = 1/math.cos(theta_rad)*(math.sin(phi_rad)*q_b_rps + math.cos(phi_rad)*r_b_rps)

    # POSITION (NAVIGATION) EQUATIONS:
    dx[9]  = math.cos(theta_rad)*math.cos(phi_rad)*u_b_mps + \
            (-math.cos(phi_rad)*math.sin(psi_rad) + math.sin(phi_rad)*math.sin(theta_rad)*math.cos(psi_rad))*v_b_mps + \
             (math.sin(phi_rad)*math.sin(psi_rad) + math.cos(phi_rad)*math.sin(theta_rad)*math.cos(psi_rad))*w_b_mps

    dx[10] = math.cos(phi_rad)*math.sin(psi_rad)*u_b_mps + \
            (math.cos(phi_rad)*math.cos(psi_rad) + math.sin(phi_rad)*math.sin(theta_rad)*math.sin(psi_rad))*v_b_mps + \
            (-math.sin(phi_rad) * math.cos(psi_rad) + math.cos(phi_rad) * math.sin(theta_rad)*math.sin(psi_rad))*w_b_mps

    dx[11] = -math.sin(theta_rad)*u_b_mps + math.sin(phi_rad)*math.cos(theta_rad)*v_b_mps + \
              math.cos(phi_rad)*math.cos(theta_rad)*w_b_mps

    return dx