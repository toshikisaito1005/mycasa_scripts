import os
import re
import sys
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
x_sncut = 0.00075 # rms in Jy/beam # ci_sncut
y1_sncut = 4.37 # log luminsity # co_sncut

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
obsfreq_x = 492.16065100 / (1 + 0.01818) # dust continuum
obsfreq_y1 = 492.16065100 / (1 + 0.01818) # CI
obsfreq_y2 = 115.27120 / (1 + 0.01818) # CO

# flux (Jy.km/s) to luminosity (K.km/spc^2)
eqn_fl2lum_x = 1.197e27 * DL**2 / (1 + zspec)**3
eqn_fl2lum_y1 = 3.25e+7 / obsfreq_y1**2 * DL**2 / (1 + zspec)**3
eqn_fl2lum_y2 = 3.25e+7 / obsfreq_y2**2 * DL**2 / (1 + zspec)**3

# moment-0 maps in Jy/beam.km/s
data_x_org = imval(dir_data + "image_b8contin/b8contin.flux",box=box)["data"]
data_y1_org = imval(dir_data + "image_ci10/ci10.moment0",box=box)["data"]
data_y2_org = imval(dir_data + "image_co10/co10.moment0",box=box)["data"]
data_x = data_x_org.flatten()
data_y1 = data_y1_org.flatten()
data_y2 = data_y2_org.flatten()
data1_x = data_x[data_x>0]
data1_y1 = data_y1[data_x>0]
data1_y2 = data_y2[data_x>0]
data2b_x = data1_x[data1_y1>0] / beamarea
data2b_y1 = data1_y1[data1_y1>0] / beamarea
data2b_y2 = data1_y2[data1_y1>0] / beamarea
data2_x = data2b_x[data2b_y2>0]
data2_y1 = data2b_y1[data2b_y2>0]
data2_y2 = data2b_y2[data2b_y2>0]

# noise maps in Jy.km/s
data_noise_y1_org = imval(dir_data + "image_ci10/ci10.moment0.noise_Jykms",box=box)["data"]
data_noise_y1 = data_noise_y1_org.flatten()
data1_noise_y1 = data_noise_y1[data_x>0]
data2b_noise_y1 = data1_noise_y1[data1_y1>0]
data2_noise_y1 = data2b_noise_y1[data2b_y2>0]

# ra decl
data_ra_org = imval(dir_data + "image_co10/co10.moment0",box=box)["coords"][:,:,0]
data_dec_org = imval(dir_data + "image_co10/co10.moment0",box=box)["coords"][:,:,1]
data_ra = data_ra_org.flatten()
data_dec = data_dec_org.flatten()
data1_ra = data_ra[data_x>0]
data1_dec = data_dec[data_x>0]
data2b_ra = data1_ra[data1_y1>0]
data2b_dec = data1_dec[data1_y1>0]
data2_ra = data2b_ra[data2b_y2>0]
data2_dec = data2b_dec[data2b_y2>0]
ra_co = data2_ra * 180/np.pi
dec_co = data2_dec * 180/np.pi
r_tmp = distance(ra_co, dec_co, 109.90-90, 90, ra_cnt, dec_cnt, 0.365)
r = r_tmp.flatten() # 90-53.737

#
x = (data2_x * eqn_fl2lum_x)[data2_x > x_sncut/beamarea*2.5]
y1 = (data2_y1 * eqn_fl2lum_y1)[data2_x > x_sncut/beamarea*2.5]
y2 = (data2_y2 * eqn_fl2lum_y2)[data2_x > x_sncut/beamarea*2.5]

# plot: CO vs. CI
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)
ax1.grid(which='major',linestyle='--')
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)

#
cbar = ax1.scatter(np.log10(x), y1/y2,
            lw=0,
            c=r[data2_x > x_sncut/beamarea*2.5],
            cmap="rainbow",alpha=0.5,s=60)

cbar.set_clim([0,3.0])

# sensitivity limit
#x = np.arange(4.5, 29.0, 0.1)
#ax1.fill_between(x, 3.0, y1_sncut,
#                 color = "grey", alpha = 0.4, lw = 0)
ax1.axvspan(26.5, np.log10(x_sncut/beamarea*2.5*eqn_fl2lum_x), color = "grey", alpha = 0.4, lw = 0)

#
x_errp = 28.1
y_errp = 0.47
snr_x = np.median(data2_x/(x_sncut/beamarea))
snr_y = np.median(data2_y1/data2_noise_y1)
x_err = np.sqrt(0.05**2+(1.0/snr_x)**2)
y_err = 0.1629001553956515 # np.sqrt(0.20**2+(1.0/snr_y)**2)
ax1.plot([np.log10(10**x_errp*(1-x_err)),np.log10(10**x_errp*(1+x_err))],
         [y_errp,y_errp],
         c = "black",lw = 3)
ax1.plot([x_errp,x_errp],
         [y_errp*(1-y_err),y_errp*(1+y_err)],
         c = "black",lw = 3)

#
nbins = 8
n, _ = np.histogram(np.log10(x), bins=nbins)
sy, _ = np.histogram(np.log10(x), bins=nbins, weights=y1/y2)
sy2, _ = np.histogram(np.log10(x), bins=nbins, weights=y1/y2*y1/y2)
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)
plt.errorbar((_[1:] + _[:-1])/2, mean, yerr=std, fmt='k-', lw=5, capsize = 0)

#
ywidth1 = 0.1 * (np.log10(data2_y1).max() - np.log10(data2_y1).min())
xwidth1 = 0.1 * (np.log10(data2_x[data2_y1 > y1_sncut/beamarea*3.0]).max() - np.log10(data2_x).min())
ax1.set_ylim([-0.05,0.6])
ax1.set_xlim([np.log10(data2_x[data2_y1 > y1_sncut/beamarea*3.0]*eqn_fl2lum_x).min()-ywidth1,
              np.log10(data2_x[data2_y1 > y1_sncut/beamarea*3.0]*eqn_fl2lum_x).max()+ywidth1])

ax1.set_ylabel("$L'_{[C_I](1-0)}$/$L'_{CO(1-0)}$ Ratio")
ax1.set_xlabel(r"log $L_{\nu}$(609 $\mu$m) (erg s$^{-1}$ Hz$^{-1}$)")

plt.text(26.85,
         0.54,
         "(d)", fontsize = 26)
plt.savefig(dir_data+"eps/scatter_cico_dust.png",dpi=300)
