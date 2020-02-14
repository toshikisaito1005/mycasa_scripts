import os
import re
import sys
import math
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
import scipy.optimize
from scipy.optimize import curve_fit
from astropy.coordinates import SkyCoord
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts07_iras18293/"
box = "103,115,180,192"
beamarea = 22.382

zspec = 0.01818
DL = 78.2 # Mpc
ci_sncut = 0.00075 # rms in Jy/beam
co_sncut = 5.0 # log luminsity

ra = "18h32m41.1300s"
decl = "-34d11m27.672s"
c = SkyCoord(ra, decl)
ra_cnt = c.ra.degree
dec_cnt = c.dec.degree

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

def function(x, a, b):
    return a * x + b

def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale
    
    return r


#####################
### Main Procedure
#####################
# CI(1-0) observed frequency
obsfreq = 492.16065100 / (1 + 0.01818)
obsfreq_co10 = 115.27120 / (1 + 0.01818)
# flux (Jy.km/s) to luminosity (K.km/spc^2)
eqn_fl2lum = 1.197e27 * DL**2 / (1 + zspec)**3
eqn_fl2lum_co = 3.25e+7 / obsfreq_co10**2 * DL**2 / (1 + zspec)**3

# moment-0 maps in Jy/beam.km/s
data_ci_org = imval(dir_data + "image_ci10/ci10.moment0",box=box)["data"]
data_co_org = imval(dir_data + "image_co10/co10.moment0",box=box)["data"]
data_dust_org = imval(dir_data + "image_b8contin/b8contin.flux",box=box)["data"]
data_ci = data_ci_org.flatten() / beamarea
data_co = data_co_org.flatten() / beamarea
data_dust = data_dust_org.flatten() / beamarea

# ra decl
data_ra_org = imval(dir_data + "image_co10/co10.moment0",box=box)["coords"][:,:,0]
data_dec_org = imval(dir_data + "image_co10/co10.moment0",box=box)["coords"][:,:,1]
data_ra = data_ra_org.flatten()
data_dec = data_dec_org.flatten()
ra_co = data_ra * 180/np.pi
dec_co = data_dec * 180/np.pi
r_tmp = distance(ra_co, dec_co, 109.90-90, 90, ra_cnt, dec_cnt, 0.365)
r = r_tmp.flatten() # 90-53.737

# select data
co_radius = r[data_co>0]
ci_radius = r[data_ci>0]
dust_radius = r[data_dust>0]

co_flux = data_co[data_co>0]
ci_flux = data_ci[data_ci>0]
dust_flux = data_dust[data_dust>0]

# binning
n, _ = np.histogram(co_radius, bins=40, range=[0,4.0])
sy, _ = np.histogram(co_radius, bins=40, weights=co_flux, range=[0,4.0])
sy2, _ = np.histogram(co_radius, bins=40, weights=co_flux**2, range=[0,4.0])
mean = sy / n
bin_co_radius = (_[1:] + _[:-1])/2
bin_co_flux = sy / n / (sy / n).max()
bin_co_err = np.sqrt(sy2/n - mean*mean) / (sy / n).max()

n, _ = np.histogram(ci_radius, bins=30, range=[0,3.0])
sy, _ = np.histogram(ci_radius, bins=30, weights=ci_flux, range=[0,3.0])
sy2, _ = np.histogram(ci_radius, bins=30, weights=ci_flux**2, range=[0,3.0])
mean = sy / n
bin_ci_radius = (_[1:] + _[:-1])/2
bin_ci_flux = sy / n / (sy / n).max()
bin_ci_err = np.sqrt(sy2/n - mean*mean) / (sy / n).max()

n, _ = np.histogram(dust_radius, bins=30, range=[0,3.0])
sy, _ = np.histogram(dust_radius, bins=30, weights=dust_flux, range=[0,3.0])
sy2, _ = np.histogram(dust_radius, bins=30, weights=dust_flux**2, range=[0,3.0])
mean = sy / n
bin_dust_radius = (_[1:] + _[:-1])/2
tmp = sy / n
tmp[np.where(np.isinf(tmp))] = 0
bin_dust_flux = tmp / tmp.max()
bin_dust_err = np.sqrt(sy2/n - mean*mean) / tmp.max()

#
plt.figure()
plt.subplots_adjust(left=0.145, right=0.745)
plt.rcParams["font.size"] = 14
plt.plot(bin_co_radius,bin_co_flux,label="CO $J$ = 1-0",c="red",lw=4,alpha=0.6)
plt.fill_between(bin_co_radius, bin_co_flux-bin_co_err, bin_co_flux+bin_co_err,
                 color = "red", alpha = 0.2, lw = 0)

plt.plot(bin_ci_radius,bin_ci_flux,label="[CI] $J$ = 1-0",c="green",lw=4,alpha=0.6)
plt.fill_between(bin_ci_radius, bin_ci_flux-bin_ci_err, bin_ci_flux+bin_ci_err,
                 color = "green", alpha = 0.2, lw = 0)

plt.plot(bin_dust_radius,bin_dust_flux,label="609$\mu$m Dust",c="blue",lw=4,alpha=0.6)
plt.fill_between(bin_dust_radius, bin_dust_flux-bin_dust_err, bin_dust_flux+bin_dust_err,
                 color = "blue", alpha = 0.2, lw = 0)

#plt.ylim([0,1.1])
plt.ylim([0.015,1.5])
plt.legend()
plt.yscale("log")
plt.xlabel("Distance (kpc)")
plt.ylabel("Normalized Flux")
plt.grid(which = "major")
plt.grid(which = "minor")
plt.title("(d) Normalized Radial Flux Distribution")
plt.savefig(dir_data+"eps/radial_flux.png",dpi=100)

os.system("rm -rf *.last")
