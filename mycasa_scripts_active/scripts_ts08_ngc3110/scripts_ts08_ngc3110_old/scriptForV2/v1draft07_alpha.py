import os
import sys
import re
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy
sys.path.append(os.getcwd() + "/../../")
import mycasaanalysis_tools3 as myana
import scipy.optimize
from scipy.optimize import curve_fit

"""
def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
"""

#####################
### Main Procedure
#####################
# import data
txt1 = "/Users/saito/data/ngc3110/ana/other/photmetry/ngc3110_alpha_ism_Tkin.txt"
txt2 = "/Users/saito/data/ngc3110/ana/other/photmetry/ngc3110_alpha_ism_Trot.txt"
txt3 = "/Users/saito/data/ngc3110/ana/other/photmetry/ngc3110_alpha_lte_Tkin.txt"
txt4 = "/Users/saito/data/ngc3110/ana/other/photmetry/ngc3110_alpha_lte_Trot.txt"
txt_master = "/Users/saito/data/ngc3110/ana/other/photmetry/ngc3110_alpha_master.txt"
png1 = "/Users/saito/data/ngc3110/ana/other/photmetry/plot_radial_alpha.png"
png2 = "/Users/saito/data/ngc3110/ana/other/photmetry/hist_alpha.png"

data1 = np.loadtxt(txt1, usecols=(0,1,2,3,4))
data2 = np.loadtxt(txt2, usecols=(3,4))
data3 = np.loadtxt(txt3, usecols=(3,4))
data4 = np.loadtxt(txt4, usecols=(3,4))
d_ra = data1[:,0]
d_decl = data1[:,1]
data_master = np.c_[data1, data2, data3, data4]
np.savetxt(txt_master, data_master)
alpha_average = (data1[:,3] + data2[:,0] + data3[:,0] + data4[:,0]) / 4.

#
plt.figure(figsize=(6,6))
plt.rcParams["font.size"] = 16
#plt.subplots_adjust(bottom = 0.15)
#plt.gca().set_aspect('equal', adjustable='box')
#plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel(u"$\u03b1_{CO}$")
#plt.xlim([1.5e-1, 1.5e+1])
plt.xlim([-0.2, 10.2])
#plt.ylim([0.02, 25])
plt.ylim([0.1, 100])
plt.title(u"Radial $\u03b1_{CO}$")
plt.scatter(data_master[:,2],
            data_master[:,3],
            s = 70,
            alpha = 0.6,
            linewidths=0,
            color = "red",
            label = u"$\u03b1_{ISM}$ with $T_{kin}$")
plt.scatter(data_master[:,2],
            data_master[:,5],
            s = 70,
            alpha = 0.6,
            linewidths=0,
            color = "olive",
            label = u"$\u03b1_{ISM}$ with $T_{rot}$")
plt.scatter(data_master[:,2],
            data_master[:,7],
            s = 70,
            alpha = 0.6,
            linewidths=0,
            color = "cadetblue",
            label = u"$\u03b1_{LTE}$ with $T_{kin}$")
plt.scatter(data_master[:,2],
            data_master[:,9],
            s = 70,
            alpha = 0.6,
            linewidths=0,
            color = "darkorchid",
            label = u"$\u03b1_{LTE}$ with $T_{rot}$")

dist_ave = []
alpha_ave = []
for i in range(len(alpha_average)):
    if alpha_average[i] > 0:
        if alpha_average[i] < 8:
            dist_ave.append(data_master[:,2][i])
            alpha_ave.append(alpha_average[i])

n, _ = np.histogram(np.array(dist_ave), bins=8)
sy, _ = np.histogram(np.array(dist_ave), bins=8,
                     weights=np.array(alpha_ave))
sy2, _ = np.histogram(np.array(dist_ave), bins=8,
                      weights=np.array(alpha_ave)*np.array(alpha_ave))
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)
plt.errorbar((_[1:] + _[:-1])/2, mean, yerr=std, fmt='-',
             capsize=4, ecolor="black", linewidth=3)
plt.plot((_[1:] + _[:-1])/2, mean, color="black", linewidth=3)
#cbar = plt.colorbar()
#cbar.set_label("Deprojected Radius (kpc)")
#plt.clim([0, max(value) * 0.65])

plt.legend(loc="upper left")
os.system("rm -rf " + png1)
plt.savefig(png1, dpi=300)


#
plt.figure(figsize=(6,6))
plt.rcParams["font.size"] = 16
#plt.subplots_adjust(bottom = 0.15)
#plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel(u"$\u03b1_{CO}$")
plt.xlim([0,5])
plt.ylim([0,20])
plt.title(u"Average $\u03b1_{CO}$")
data_hist1 = []
for i in range(len(data_master[:,3])):
    if data_master[:,3][i] > 0:
        data_hist1.append(data_master[:,3][i])

data_hist2 = []
for i in range(len(data_master[:,5])):
    if data_master[:,5][i] > 0:
        data_hist2.append(data_master[:,5][i])

data_hist3 = []
for i in range(len(data_master[:,7])):
    if data_master[:,7][i] > 0:
        data_hist3.append(data_master[:,7][i])

data_hist4 = []
for i in range(len(data_master[:,9])):
    if data_master[:,9][i] > 0:
        data_hist4.append(data_master[:,9][i])

direction="J2000 10:04:02.090 -6.28.29.604"
cl.done()
data_hist5 = []
for i in range(len(alpha_average)):
    if alpha_average[i] > 0:
        if alpha_average[i] < 10:
            data_hist5.append(alpha_average[i])
            cl.addcomponent(dir=str(d_ra[i])+"deg, "+str(d_decl[i])+"deg",
                            flux=alpha_average[i], fluxunit="Jy",
                            freq="234.6075GHz",
                            shape="Gaussian",
                            majoraxis="3.00arcsec",
                            minoraxis="3.00arcsec",
                            positionangle="0.0deg")

dir_fits = "/Users/saito/data/ngc3110/ana/other/photmetry/"
ia.fromshape(dir_fits + "nyquist_alpha_co.image",
             [50,50,1,1],
             overwrite = True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity("1.6arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("151.008708deg", "rad")["value"],
                      qa.convert("-6.474890deg","rad")["value"]],
                     type = "direction")
cs.setreferencevalue("234.6075GHz", "spectral")
cs.setincrement("1GHz", "spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename= dir_fits + 'nyquist_alpha_co.image',
           fitsimage= dir_fits + 'nyquist_alpha_co.fits',
           overwrite = True)
ia.close()

dat = plt.hist(data_hist5, bins=30, range=[0,8],
               color="skyblue", histtype="stepfilled", alpha=1.0)

popt, pcov = curve_fit(gauss_function, dat[1][2:], dat[0][1:],
                       p0 = [25, 1.2, 0.05],
                       maxfev = 10000)

x = np.linspace(dat[1][1], dat[1][-1], 50)
plt.plot(x,
         gauss_function(x, *popt),
         '-', c="black", lw=4,
         label = "$\mu$ = " + str(round(popt[1], 1)) + \
         ", $\sigma$ = " + str(round(popt[2], 1)))

plt.legend()
plt.plot([popt[1],popt[1]], [0,25], '--', c="black", lw=3)
os.system("rm -rf " + png2)
plt.savefig(png2, dpi=300)

