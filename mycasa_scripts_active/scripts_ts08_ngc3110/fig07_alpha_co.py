import os
import sys
import re
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy
import scipy.optimize
from scipy.optimize import curve_fit


#####################
### def
#####################
def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


#####################
### Main Procedure
#####################
# import data
