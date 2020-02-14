import numpy as np
import math
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib.colors as clr
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
plt.ioff()


#####################
### Define Parameters
#####################
cosmo = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)
dir_data = "../../aca_yamashita/"
dir_product = dir_data + "product/"
txt_file = dir_product + "output_size.txt"
product_file1 = dir_product + "output_size_maj.png"
product_file2 = dir_product + "output_size_mean.png"

#####################
### Main Procedure
#####################
# import data
data = np.loadtxt(txt_file, usecols=(1,2,3,4,5), dtype = "S10")

size_maj_all = data[:,1].astype("int") / 1000.
size_maj_ms = size_maj_all[0:34]
size_maj_vv = size_maj_all[34:]

size_min_all = data[:,3].astype("int") / 1000.
size_min_ms = size_min_all[0:34]
size_min_vv = size_min_all[34:]

size_mean_all = (size_maj_all + size_min_all) / 2.
size_mean_ms = (size_maj_ms + size_min_ms) / 2.
size_mean_vv = (size_maj_vv + size_min_vv) / 2.

# plot 1
plt.figure(figsize=(6,6))
plt.rcParams["font.size"] = 12
plt.xlabel(u"Major Axis FWHM (kpc)")
plt.xlim([0,20])
plt.ylim([0,20])
plt.title(u"Major Axis FWHM (kpc)")
plt.hist(size_maj_all, bins=10, range=[0,20],
         color="black", histtype="step", alpha=1.0,
         label = "All")
plt.hist(size_maj_ms, bins=10, range=[0,20],
         color="blue", histtype="stepfilled", alpha=0.4,
         label = "MS galaxies")
plt.hist(size_maj_vv, bins=10, range=[0,20],
         color="red", histtype="stepfilled", alpha=0.4,
         label = "VV galaxies")

plt.legend()
os.system("rm -rf " + product_file1)
plt.savefig(product_file1, dpi=300)

# plot 2
plt.figure(figsize=(6,6))
plt.rcParams["font.size"] = 12
plt.xlabel(u"Geometrical Mean FWHM (kpc)")
plt.xlim([0,20])
plt.ylim([0,20])
plt.title(u"Geometrical Mean FWHM (kpc)")
plt.hist(size_mean_all, bins=10, range=[0,20],
         color="black", histtype="step", alpha=1.0,
         label = "All")
plt.hist(size_mean_ms, bins=10, range=[0,20],
         color="blue", histtype="stepfilled", alpha=0.4,
         label = "MS galaxies")
plt.hist(size_mean_vv, bins=10, range=[0,20],
         color="red", histtype="stepfilled", alpha=0.4,
         label = "VV galaxies")

plt.legend()
os.system("rm -rf " + product_file2)
plt.savefig(product_file2, dpi=300)
