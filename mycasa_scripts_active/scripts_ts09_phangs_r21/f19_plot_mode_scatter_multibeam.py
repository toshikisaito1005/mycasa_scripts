import os, re, sys, glob
import itertools
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy import stats
plt.ioff()

#
import scripts_phangs_r21 as r21


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galname = "ngc0628"
freqco10 = 115.27120
freqco21 = 230.53800
nbins = [40, 30, 20, 10, 10]
percentile = 84

beams = ["04p0","08p0","12p0","16p0","20p0"]


#####################
### functions
#####################


#####################
### functions
#####################