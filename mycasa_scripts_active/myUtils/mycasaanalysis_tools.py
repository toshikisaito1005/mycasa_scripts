import os
import re
import sys
import glob
import numpy as np


"""
    mycasaanalysis_tools.py
    2018-06-28: refactored by tsaito
    """

k_B = 1.38064852e-16 # erg/K
h_p = 6.6260755e-27 # erg/s
Tbg = 2.73 # K


def partition_func(Trot, datacol, data = "../Qrot_CDMS.txt"):
    """
    Derive partition funcition of a molecule at a given temperature
    using the CDMS table under LTE.  Interpolating 2 nearest values.
    (http://www.astro.uni-koeln.de/site/vorhersagen/catalog/
    partition_function.html)

    Parameters
    ----------
    Trot (K): int, float
        rotation temperature your molecule under LTE
    datacol: int
        column of "../Qrot_CDMS.txt" which contains descrete partition
        functions of your molecule
    data: str
        txt file containing partition function, otherwise use
        "../Qrot_CDMS.txt"

    Returns
    ----------
    Qrot: float
        derived partition function

    reference
    ----------
    Mueller, H. S. P. et al. 2001, A&A, 370, L49
    Mueller, H. S. P. et al. 2005, JMoSt, 742, 215
    """
    table = np.loadtxt(data, usecols = (0,datacol))
    row = np.sum(table[:,0] < Trot) - 1
    t1 = table[:,0][row]
    t2 = table[:,0][row + 1]
    logQ1 = table[:,1][row]
    logQ2 = table[:,1][row + 1]
    a = (logQ1 - logQ2) / (t1 - t2)
    b = (t2*logQ1 - t1*logQ2) / (t2 - t1)
    Qrot = np.exp(a*Trot + b)
    return Qrot


def rot0_13co(Trot, flux_hj, lj_upp = 1, hj_upp = 2):
    """
        input flux density = K.km/s
        """
    Eu = {1: 5.28880, 2: 15.86618, 3: 31.73179, 4: 52.88517, \
        5: 79.32525, 6: 111.05126}
    Snu2 = {1: 0.02436, 2: 0.04869, 3: 0.07297, 4: 0.09717, \
        5: 0.12124, 6: 0.14518} # Debye^2
    y_hj = 3 * k_B * flux_hj / (8 * np.pi * Snu2[hj_upp] * 110.20135 \
           * hj_upp) * 1e32 # cm^2
    b = np.log(y_hj) + Eu[hj_upp] / Trot
    Qrot = partition_func(Trot, datacol = 1)
    exp_rot = np.exp(h_p * 110.20135e+9 * hj_upp / k_B / Trot) - 1.
    exp_bg = np.exp(h_p * 110.20135e+9 * hj_upp / k_B / Tbg) - 1.
    log_Ntot = (b + Qrot - np.log(1 - (exp_rot / exp_bg))) \
               / np.log(10)
    return round(log_Ntot, 2), round(Qrot, 2)


def rot1_13co(flux_lj, flux_hj, lj_upp = 1, hj_upp = 2):
    """
    input flux density = K.km/s
    """
    Eu = {1: 5.28880, 2: 15.86618, 3: 31.73179, 4: 52.88517, \
          5: 79.32525, 6: 111.05126}
    Snu2 = {1: 0.02436, 2: 0.04869, 3: 0.07297, 4: 0.09717, \
            5: 0.12124, 6: 0.14518} # Debye^2
    y_lj = 3 * k_B * flux_lj / (8 * np.pi * Snu2[lj_upp] * 110.20135 \
           * lj_upp) * 1e32 # cm^2
    y_hj = 3 * k_B * flux_hj / (8 * np.pi * Snu2[hj_upp] * 110.20135 \
           * hj_upp) * 1e32 # cm^2
    log_y_lj, log_y_hj = np.log10(y_lj), np.log10(y_hj)
    ln_y_lj, ln_y_hj = np.log(y_lj), np.log(y_hj)
    Trot = (Eu[hj_upp] - Eu[lj_upp]) / (log_y_lj - log_y_hj)
    b = np.log(y_hj) + Eu[hj_upp] / Trot
    Qrot = partition_func(Trot, datacol = 1)
    exp_rot = np.exp(h_p * 110.20135e+9 * hj_upp / k_B / Trot) - 1.
    exp_bg = np.exp(h_p * 110.20135e+9 * hj_upp / k_B / Tbg) - 1.
    log_Ntot = (b + Qrot - np.log(1 - (exp_rot / exp_bg))) \
               / np.log(10)
    return round(Trot, 2), round(log_Ntot, 2), round(Qrot, 2)



