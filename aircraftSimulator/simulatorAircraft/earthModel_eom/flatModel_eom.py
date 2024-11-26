########################################################################################################################
## LOADING THE NECESSARY LIBRARIES FOR DEVELOPING THE EARTHO MODEL:
########################################################################################################################
import math
import numpy as np

########################################################################################################################
## EXAMPLE OF MODEL FOR EARTH:
## THIS EXAMPLE USES THE FLAT EARTH EQUATIONS FOR MODELING THE EARTH
########################################################################################################################
def flatModel_eom(t, x, amod):
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
    dx = np.array((12, 1))

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
    m_kg       = amod([m_kg])
    Jxz_b_kgm2 = amod([Jxz_b_kgm2])
    Jxx_b_kgm2 = amod([Jxx_b_kgm2])
    Jyy_b_kgm2 = amod([Jyy_b_kgm2])
    Jzz_b_kgm2 = amod([Jzz_b_kgm2])

    # AIR DATA CALCULATION(Mach, Altitude, AoA, AoS):
    # ATMOSPHERIC MODEL:

    # GRAVITY MODEL:
    # FIRST MODEL ACTS NORMAL TO THE EARTH TANGENT CS
    gz_n_mps2 = 9.81

    # RESOLVING GRAVITY IN BODY COORDINATE SYSTEM:
    gx_b_mps2 = -math.sin(theta_rad)*gz_n_mps2
    gy_b_mps2 = math.sin(phi_rad)*math.cos(theta_rad)*gz_n_mps2
    gz_b_mps2 = math.cos(phi_rad)*math.cos(theta_rad)*gz_n_mps2

    # EXTERNAL FORCES:
    Fx_b_kgmps2 = []
    Fy_b_kgmps2 = []
    Fz_b_kgmps2 = []

    # EXTERNAL MOMENTS:
    l_b_kgm2ps2 = []
    m_b_kgm2ps2 = []
    n_b_kgm2ps2 = []

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
    dx[6] = []
    dx[7] = []
    dx[8] = []

    # POSITION (NAVIGATION) EQUATIONS:
    dx[9]  = []
    dx[10] = []
    dx[11] = []

    return dx