import os
import re
import sys
import glob
import math
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
x_sncut = 0.00075 # rms in Jy/beam
y_sncut = 4.37 # log luminsity

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
# observed frequency
obsfreq_x = 492.16065100 / (1 + 0.01818)
obsfreq_y = 492.16065100 / (1 + 0.01818)

# flux (Jy.km/s) to luminosity (K.km/spc^2)
eqn_fl2lum_x = 1.197e27 * DL**2 / (1 + zspec)**3
eqn_fl2lum_y = 3.25e+7 / obsfreq_y**2 * DL**2 / (1 + zspec)**3

# moment-0 maps in Jy/beam.km/s
data_x_org = imval(dir_data + "image_b8contin/b8contin.flux",box=box)["data"]
data_y_org = imval(dir_data + "image_ci10/ci10.moment0",box=box)["data"]
data_x = data_x_org.flatten()
data_y = data_y_org.flatten()
data1_x = data_x[data_x>0]
data1_y = data_y[data_x>0]
data2_x = data1_x[data1_y>0] / beamarea
data2_y = data1_y[data1_y>0] / beamarea

# ra decl
data_ra_org = imval(dir_data + "image_co10/co10.moment0",box=box)["coords"][:,:,0]
data_dec_org = imval(dir_data + "image_co10/co10.moment0",box=box)["coords"][:,:,1]
data_ra = data_ra_org.flatten()
data_dec = data_dec_org.flatten()
data1_ra = data_ra[data_x>0]
data1_dec = data_dec[data_x>0]
data2_ra = data1_ra[data1_y>0]
data2_dec = data1_dec[data1_y>0]
ra_co = data2_ra * 180/np.pi
dec_co = data2_dec * 180/np.pi
r_tmp = distance(ra_co, dec_co, 109.90-90, 90, ra_cnt, dec_cnt, 0.365)
r = r_tmp.flatten() # 90-53.737

# noise maps in Jy.km/s
data_noise_y_org = imval(dir_data + "image_ci10/ci10.moment0.noise_Jykms",box=box)["data"]
data_noise_y = data_noise_y_org.flatten()
data1_noise_y = data_noise_y[data_x>0]
data2_noise_y = data1_noise_y[data1_y>0]

# plot: CI vs. dust
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)
ax1.grid(which='major',linestyle='--')
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)

#
cbar = ax1.scatter(np.log10((data2_x * eqn_fl2lum_x)[data2_x > x_sncut/beamarea*2.5]),
            np.log10((data2_y * eqn_fl2lum_y)[data2_x > x_sncut/beamarea*2.5]),
            lw=0,c=r[data2_x > x_sncut/beamarea*2.5],cmap="rainbow",alpha=0.5,s=60)

cbar.set_clim([0,3.0])


# sensitivity limit
x = np.arange(26.6, 28.5, 0.1)
ax1.fill_between(x, 3.0, y_sncut,
                 color = "grey", alpha = 0.4, lw = 0)
ax1.axvspan(26.5, np.log10(x_sncut/beamarea*2.5*eqn_fl2lum_x), color = "grey", alpha = 0.4, lw = 0)

# typical error bar
x_errp = 28.1
y_errp = 4.75
snr_x = np.median(data2_x/(x_sncut/beamarea))
snr_y = np.median(data2_y/data2_noise_y)
x_err = np.sqrt(0.05**2+(1.0/snr_x)**2)
y_err = np.sqrt(0.20**2+(1.0/snr_y)**2)
ax1.plot([np.log10(10**x_errp*(1-x_err)),np.log10(10**x_errp*(1+x_err))],
         [y_errp,y_errp],
         c = "black",lw = 3)
ax1.plot([x_errp,x_errp],
         [np.log10(10**y_errp*(1-y_err)),np.log10(10**y_errp*(1+y_err))],
         c = "black",lw = 3)

# linear fit
y_err = np.sqrt(0.20**2+(data2_noise_y[data2_x>data2_x.max()*0.1] * eqn_fl2lum_x)**2)
popt, pcov = curve_fit(function,
                       np.log10(data2_x[data2_x>data2_x.max()*0.1] * eqn_fl2lum_x),
                       np.log10(data2_y[data2_x>data2_x.max()*0.1] * eqn_fl2lum_y),
                       p0 = [1.0,1.0],
                       maxfev = 10000,
                       sigma=np.log10(y_err))
x = np.linspace(np.log10(x_sncut/beamarea*2.5*eqn_fl2lum_x),
                np.log10(data2_x*eqn_fl2lum_x).max(), 50)
plt.plot(x,
         function(x, *popt),
         '--', c="black", lw=6)

print "popt[0] = " + str(popt[0])
print "popt[1] = " + str(popt[1])

# ranges
ywidth1 = 0.1 * (np.log10(data2_y).max() - np.log10(data2_y).min())
xwidth1 = 0.1 * (np.log10(data2_x[data2_y > y_sncut/beamarea*3.0]).max() - np.log10(data2_x).min())
ax1.set_ylim([4.1731141408012267,
              6.5688322008614648])
ax1.set_xlim([np.log10(data2_x[data2_y > y_sncut/beamarea*3.0]*eqn_fl2lum_x).min()-ywidth1,
              np.log10(data2_x[data2_y > y_sncut/beamarea*3.0]*eqn_fl2lum_x).max()+ywidth1])

# annotation
ax1.set_ylabel("log $L'_{[C_I](1-0)}$ (K km s$^{-1}$ pc$^2$)")
ax1.set_xlabel(r"log $L_{\nu}$(609 $\mu$m) (erg s$^{-1}$ Hz$^{-1}$)")
plt.plot([25.8,28.8],[5.0,8.0],"k-",lw=2)
plt.plot([25.8,28.8],[4.69897,7.69897],"k-",lw=2)
plt.plot([25.8,28.8],[4.0,7.0],"k-",lw=2)
plt.text(26.85,6.35,"(b)",fontsize = 26)

plt.savefig(dir_data+"eps/scatter_ci_dust.png",dpi=300)
