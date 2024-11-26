import numpy as np

def foward_Euler(f, t_s, x, h_s):
    """
        PERFORMS FORWARD EULER INTEGRATION TO APPROXIMATE THE SOLUTION OF A DIFFERENTIAL EQUATION

        INPUT ARGUMENTS:
            f:    A FUNCTION REPRESENTING THE RIGHT-HAND SIDE OF THE DIFFERENTIAL EQUATION (dx/dt = f(t, x)).
            t_s : A VECTOR OF POINTS IN TIME AT WHICH NUMERICAL SOLUTION WILL BE APPROXIMATE.
            x:    THE NUMERICALLY APPROXIMATED SOLUTION DATA TO THE DE, f.
            h_s:  THE STEP SIZE IN SECONDS

        OUTPUT ARGUMENTS:
            t_s: A VECTOR OF POINTS IN TIME AT WHICH NUMERICAL SOLUTION WAS APPROXIMATED.
            x:   THE NUMERICALLY APPROXIMATED SOLUTION DATA TO THE DE, f.
    """

    # FOWARD EULER CALCULATION METHOD
    for i in range(1, len(t_s)):
        x[:, i] = x[:, i - 1] + h_s*f(t_s[i - 1], x[:, i - 1]) # EULER FORMULA

    return t_s, x