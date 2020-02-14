import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim
import scipy.optimize
from scipy.optimize import curve_fit


dir_data = "../../../ngc3110/ana/data_nyquist/"
ra_center = "10:04:02.090"
dec_center = "-6.28.29.604"
xlim = [-30, 30]
ylim = [30, -30]
value = None


done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")


#####################
### Main Procedure
#####################

### H2mass
# color + contour
imagename_contour = "nyquist_co10_m0.fits"
imagename_color = "nyquist_H2mass.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = ""
colorscale = "rainbow" # "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
#clim = [0., 2.]
title = "$M_{H_2}$"
colorbar_label = ""
output = "../eps/nyquist_H2mass.eps"
myim.fits2eps(dir_data = dir_data,
              imagename_color = imagename_color,
              imagename_contour = imagename_contour,
              ra_center = ra_center,
              dec_center = dec_center,
              title = title,
              colorbar_label = colorbar_label,
              output = output,
              colorscale = colorscale,
              colorlog = colorlog,
              color_contour = color_contour,
              color_beam = color_beam,
              colorbar = colorbar,
              value = value,
              contour = contour,
              xlim = xlim,
              ylim = ylim)


dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_output = "../../../ngc3110/ana/eps/"
data_m_lte = "../gasmass_lte.txt"
data_m_ism = "ngc3110_ISMmass.txt"
data_co10 = "ngc3110_flux.txt"

#####################
### Main Procedure
#####################
# LTE mass
data = np.loadtxt(dir_data + data_m_lte,
                  usecols = (0,1))
d_co10, m_lte = data[:,0], data[:,1]
# NLTE mass
m_radex1 = 51263098.81394617
m_radex2 = 162108152.1703461
# ISM mass
data = np.loadtxt(dir_data + data_m_ism,
                  usecols = (0,1,2))
m_ism = data[:,2]
# CO(1-0) intensity
data = np.loadtxt(dir_data + data_co10,
                  usecols = (0,1,2,3))
d_co10b = data[:,3]

alpha = m_ism / (d_co10b * 795443.)
for i in range(len(d_co10b)):
    if d_co10b[i] == 0:
        alpha[i] = -1
    elif m_ism[i] == 0:
        alpha[i] = -1

def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.xlim([0,5])
plt.ylim([0,25])
plt.xlabel("$M_{ISM}$/$L$'$_{CO(1-0)}$ ($M_{\odot}$ (K km s$^{-1}$ pc$^2$)$^{-1}$)")
plt.ylabel("Count")
#plt.gca().set_aspect('equal', adjustable='box')
dat = plt.hist(alpha, bins=25, histtype="stepfilled",
               alpha = 0.4, color = "skyblue")
popt, pcov = curve_fit(gauss_function, dat[1][2:], dat[0][1:],
                       p0 = [25, 1.2, 0.05],
                       maxfev = 10000)
x = np.linspace(dat[1][1], dat[1][-1], 50)
plt.plot(x,
         gauss_function(x, *popt),
         '-', c="lightcoral", lw=2,
         label = "$\mu$ = " + str(round(popt[1], 1)) + \
             ", $\sigma$ = " + str(round(popt[2], 1)))
plt.legend()
plt.plot([popt[1],popt[1]], [0,25], '--', c="black", lw=3)
plt.savefig("../../../ngc3110/ana/eps/hist_alpha.eps", dpi = 30)
