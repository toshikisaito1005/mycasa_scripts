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
from mpl_toolkits.axes_grid.inset_locator import inset_axes
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts07_iras18293/"
box = "103,115,180,192"
beamarea = 22.382

zspec = 0.01818
DL = 78.2 # Mpc
ci_sncut = 4.37 # log luminsity
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
eqn_fl2lum = 3.25e+7 / obsfreq**2 * DL**2 / (1 + zspec)**3
eqn_fl2lum_co = 3.25e+7 / obsfreq_co10**2 * DL**2 / (1 + zspec)**3

# moment-0 maps in Jy/beam.km/s
data_ci_org = imval(dir_data + "image_ci10/ci10.moment0",box=box)["data"]
data_co_org = imval(dir_data + "image_co10/co10.moment0",box=box)["data"]
data_ci = data_ci_org.flatten()
data_co = data_co_org.flatten()
data1_ci = data_ci[data_ci>0]
data1_co = data_co[data_ci>0]
data2_ci = data1_ci[data1_co>0] / beamarea
data2_co = data1_co[data1_co>0] / beamarea

# noise maps in Jy.km/s
data_noiseci_org = imval(dir_data + "image_ci10/ci10.moment0.noise_Jykms",box=box)["data"]
data_noiseco_org = imval(dir_data + "image_co10/co10.moment0.noise_Jykms",box=box)["data"]
data_noiseci = data_noiseci_org.flatten()
data_noiseco = data_noiseco_org.flatten()
data1_noiseci = data_noiseci[data_ci>0]
data1_noiseco = data_noiseco[data_ci>0]
data2_noiseci = data1_noiseci[data1_co>0]
data2_noiseco = data1_noiseco[data1_co>0]

# ra decl
data_ra_org = imval(dir_data + "image_ci10/ci10.moment0",box=box)["coords"][:,:,0]
data_dec_org = imval(dir_data + "image_ci10/ci10.moment0",box=box)["coords"][:,:,1]
data_ra = data_ra_org.flatten()
data_dec = data_dec_org.flatten()
data1_ra = data_ra[data_ci>0]
data1_dec = data_dec[data_ci>0]
data2_ra = data1_ra[data1_co>0]
data2_dec = data1_dec[data1_co>0]
ra_co = data2_ra * 180/np.pi
dec_co = data2_dec * 180/np.pi
r_tmp = distance(ra_co, dec_co, 109.90-90, 90, ra_cnt, dec_cnt, 0.365)
r = r_tmp.flatten() # 90-53.737


# plot: CO vs. CI
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)
ax1.grid(which='major',linestyle='--')
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)
#
cscatter = ax1.scatter(np.log10(data2_co * eqn_fl2lum_co),
            np.log10(data2_ci * eqn_fl2lum),
            lw=0,c=r,cmap="rainbow",alpha=0.5,s=60) # "mediumpurple"
# sensitivity limit
x = np.arange(4.5, 7.5, 0.1)
ax1.fill_between(x, 4.0, ci_sncut, color = "grey", alpha = 0.4, lw = 0)
ax1.axvspan(4.5, co_sncut, color = "grey", alpha = 0.4, lw = 0)
#
x_errp = 5.7
y_errp = 6.25
snr_x = np.median(data2_co/data2_noiseco)
snr_y = np.median(data2_ci/data2_noiseci)
x_err = np.sqrt(0.05**2+(1.0/snr_x)**2)
y_err = np.sqrt(0.20**2+(1.0/snr_y)**2)
ax1.plot([np.log10(10**x_errp*(1-x_err)),np.log10(10**x_errp*(1+x_err))],
         [y_errp,y_errp],
         c = "black",lw = 3)
ax1.plot([x_errp,x_errp],
         [np.log10(10**y_errp*(1-y_err)),np.log10(10**y_errp*(1+y_err))],
         c = "black",lw = 3)
#
y_err = np.sqrt(0.20**2+(data2_noiseci[data2_co>data2_co.max()*0.1] * eqn_fl2lum_co)**2)
popt, pcov = curve_fit(function,
                       np.log10(data2_co[data2_co>data2_co.max()*0.1] * eqn_fl2lum_co),
                       np.log10(data2_ci[data2_co>data2_co.max()*0.1] * eqn_fl2lum),
                       p0 = [1.0,1.0],
                       maxfev = 10000,
                       sigma=np.log10(y_err))
x = np.linspace(6.0,
                np.log10(data2_co*eqn_fl2lum_co).max(), 50)
plt.plot(x,
         function(x, *popt),
         '--', c="black", lw=6)
#
xwidth1 = 0.1 * (np.log10(data2_co).max() - np.log10(data2_co).min())
ywidth1 = 0.1 * (np.log10(data2_ci).max() - np.log10(data2_ci).min())
ax1.set_xlim([np.log10(data2_co*eqn_fl2lum_co).min()-xwidth1,
              np.log10(data2_co*eqn_fl2lum_co).max()+xwidth1])
ax1.set_ylim([np.log10(data2_ci*eqn_fl2lum).min()-ywidth1,
              np.log10(data2_ci*eqn_fl2lum).max()+ywidth1])

ax1.set_xlabel("log $L'_{CO(1-0)}$ (K km s$^{-1}$ pc$^2$)")
ax1.set_ylabel("log $L'_{[C_I](1-0)}$ (K km s$^{-1}$ pc$^2$)")

plt.plot([3.0,8.0],[3.0,8.0],"k-",lw=2)
plt.plot([3.0,8.0],[2.69897,7.69897],"k-",lw=2)
plt.plot([3.0,8.0],[2.0,7.0],"k-",lw=2)
plt.text(5.72,6.5,"$L'_{[C_I](1-0)}$ = $L'_{CO(1-0)}$", rotation = 45)
plt.text(5.88,6.5,"$L'_{[C_I](1-0)}$ = 0.5 $L'_{CO(1-0)}$", rotation = 45)
plt.text(6.32,6.0,"$L'_{[C_I](1-0)}$ = 0.1 $L'_{CO(1-0)}$", rotation = 45)

#plt.text(5.8,6.42,"log $L'_{[C_I](1-0)}$ = "+str(np.round(popt[0],2))+" log $L'_{CO(1-0)}$ - "+ str(abs(np.round(popt[1],2))), rotation = 54)

plt.text(np.log10(data2_co*eqn_fl2lum_co).max()-xwidth1,
         np.log10(data2_ci*eqn_fl2lum).min()+ywidth1,
         "(a)", fontsize = 26)

cax = fig.add_axes([0.19, 0.52, 0.03, 0.3])
cbar = plt.colorbar(cscatter, cax=cax)
cbar.set_label("Distance (kpc)")
cbar.set_clim([0,3.0])
plt.savefig(dir_data+"eps/scatter_co_ci.png",dpi=300)


# plot: CO/CI vs. CO
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)
ax1.grid(which='major',linestyle='--')
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)
#
ax1.scatter(np.log10(data2_co * eqn_fl2lum_co),
            (data2_ci * eqn_fl2lum)/(data2_co * eqn_fl2lum_co),
            lw=0,c=r,cmap="rainbow",alpha=0.5,s=60)
#
x = np.log10(data2_co * eqn_fl2lum_co)#[data2_co>data2_co.max()*0.1]
y = ((data2_ci * eqn_fl2lum)/(data2_co * eqn_fl2lum_co))#[data2_co>data2_co.max()*0.1]
nbins = 4
n, _ = np.histogram(x, bins=nbins, range=[6.0,7.0])
sy, _ = np.histogram(x, bins=nbins, weights=y, range=[6.0,7.0])
sy2, _ = np.histogram(x, bins=nbins, weights=y*y, range=[6.0,7.0])
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)
plt.errorbar((_[1:] + _[:-1])/2, mean, yerr=std, fmt='k-', lw=5, capsize = 0)
#
n, _ = np.histogram(x, bins=nbins, range=[5.0,6.0])
sy, _ = np.histogram(x, bins=nbins, weights=y, range=[5.0,6.0])
sy2, _ = np.histogram(x, bins=nbins, weights=y*y, range=[5.0,6.0])
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)
plt.errorbar((_[1:] + _[:-1])/2, mean, yerr=std, fmt='k-', lw=2, capsize = 0)
# sensitivity limit
x = np.arange(4.5, 7.5, 0.1)
y = 10**ci_sncut/10**x
ax1.fill_between(x, -0.2, y, color = "grey", alpha = 0.4, lw = 0)
ax1.axvspan(4.5, co_sncut, color = "grey", alpha = 0.4, lw = 0)
#
x_errp = 6.75
y_errp = 0.47
snr_x = np.median(data2_co/data2_noiseco)
snr_y = np.median(data2_ci/data2_noiseci)
x_err = np.sqrt(0.05**2+(1.0/snr_x)**2)
y_err = y_errp * np.sqrt(0.05**2+(1.0/snr_x)**2 + 0.20**2+(1.0/snr_y)**2)
ax1.plot([np.log10(10**x_errp*(1-x_err)),np.log10(10**x_errp*(1+x_err))],
         [y_errp,y_errp],
         c = "black",lw = 3)
ax1.plot([x_errp,x_errp],
         [y_errp*(1-y_err),y_errp*(1+y_err)],
         c = "black",lw = 3)

xwidth1 = 0.1 * (np.log10(data2_co).max() - np.log10(data2_co).min())
ywidth1 = 0.1 * (np.log10(data2_ci).max() - np.log10(data2_ci).min())
ax1.set_xlim([np.log10(data2_co*eqn_fl2lum_co).min()-xwidth1,
              np.log10(data2_co*eqn_fl2lum_co).max()+xwidth1])
ax1.set_ylim([-0.05,0.6])

ax1.set_xlabel("log $L'_{CO(1-0)}$ (K km s$^{-1}$ pc$^2$)")
ax1.set_ylabel("$L'_{[C_I](1-0)}$/$L'_{CO(1-0)}$ Ratio")

# plot Eva's suggestions
ax1.plot([6.0,6.0],
         [-0.05,0.6],linestyle="--",
         c = "black",lw = 5)

plt.text(np.log10(data2_co*eqn_fl2lum_co).min()+xwidth1*0.5,
         0.54,
         "(c)", fontsize = 26)
plt.savefig(dir_data+"eps/scatter_co_ratio.png",dpi=300)
