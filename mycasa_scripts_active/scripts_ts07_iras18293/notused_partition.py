import os
import re
import sys
import glob


#####################
### func
#####################
def partion_func(Tk,nH2):
    """
    following Papadopoulos et al. (2004) prescription
    """
    # define parameters
    g0 = 2. * 0. + 1. # 2J+1; degeneracy factor
    g1 = 2. * 1. + 1. # 2J+1
    g2 = 2. * 2. + 1. # 2J+1
    E1 = 23.6 # K
    E2 = 62.4 # K
    E21 = E2 # K
    n21 = 964. # cm^-3
    gamma20 = 2.0e-10 # cm^3 s^-1
    gamma21 = 7.8e-11 # cm^3 s^-1
    gamma10 = 1.3e-10 # cm^3 s^-1
    C20 = nH2 * gamma20 # s^-1
    C21 = nH2 * gamma21 # s^-1
    C10 = nH2 * gamma10 # s^-1
    n10 = 600. * (1. + g2/g1 * np.exp(-E21/Tk) * gamma21/gamma10)**-1. # cm^-3

    # equation G
    factor1 = 1. + g2/g1 * C21/C10 * np.exp(-E21/Tk)
    factor2 = 1. + g0/g1 * np.exp(E1/Tk)
    factor3 = factor1/factor2 * n10/nH2
    G = 1. + g0/g1 * np.exp(E1/Tk) * factor3
    
    # equation K
    factor1 = g0/g1 * np.exp(E1/Tk) * (1. + g1/g0 * C10/C20 * np.exp(-E1/Tk))
    factor2= g2/g1 * np.exp(-E21/Tk) * (1. + g1/g2 * C10/C21 * np.exp(E21/Tk))
    factor3 = factor2 * (1. + n10/nH2) + factor1

    factor4 = C10/C20 * G * (1. + n21/nH2)
    factor5 = (1. + g1/g0 * np.exp(-E1/Tk)) * factor4
    factor6 = n21/nH2 + g0/g2 * np.exp(E2/Tk) * factor5
    Kparam = 1. + (1. + C20/C21) * factor6 + factor3

    # equation Q10
    factor1 = 1. + g2/g1 * C20/C10 * np.exp(-E21/Tk)
    factor2 = 1. + factor1 * n21 / nH2
    factor3 = 1. + g1/g2 * (1. + C20/C21) * C10/C20 * np.exp(E21/Tk) * factor2
    Q10 = factor3 / Kparam

    return Q10
