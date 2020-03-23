import os, re, sys
import math
import glob
import numpy as np
import matplotlib.pyplot as plt
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


#####################
### def
#####################
def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale
    
    return r

def sigma_rj(
    tdust, # Kelvin
    nuobs, # GHz
    z, # redshift
    ):
    """
    eq.6 of Scoville et al. 2016
    """
    # Constants
    const_h = 6.626e-34 # m^2 kg s^-1
    const_k = 1.38e-23  # m^2 kg s^-2 K^-1
    #
    part = const_h * nuobs * 1e9 * (1+z) / (const_k * tdust)
    function = part / (np.exp(part) - 1)

    return function

def gas_mass_from_dust_flux(
    flux, # mJy
    nuobs, # GHz
    z, # redshift
    dist, # Gpc
    tdust, # K
    ):
    """
    eq.16 of Scoville et al. 2016
    assumptions:
        dust beta        = 1.8
        rest wavelength  > 250 um 
        alpha850 = 6.7e19
    """
    nu850 = 352.6970094 # GHz
    Sig_rj = sigma_rj(tdust,nuobs,z)
    Sig_0 = sigma_rj(tdust,nu850,0)
    mass = 1.78e10 * flux * (1+z)**-4.8 * (nu850/nuobs)**3.8 * dist**2 * (Sig_rj/Sig_0)

    return mass


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

# noise maps in Jy.km/s
data_noise_y1_org = imval(dir_data + "image_ci10/ci10.moment0.noise_Jykms",box=box)["data"]
data_noise_y1 = data_noise_y1_org.flatten()
data1_noise_y1 = data_noise_y1[data_x>0]
data2b_noise_y1 = data1_noise_y1[data1_y1>0]
data2_noise_y1 = data2b_noise_y1[data2b_y2>0]

#
flux_dust = (data2_x * 1e3)[data2_x > x_sncut/beamarea*2.5] # mJy
lum_dust = (data2_x * eqn_fl2lum_x)[data2_x > x_sncut/beamarea*2.5]
lum_ci = (data2_y1 * eqn_fl2lum_y1)[data2_x > x_sncut/beamarea*2.5]
lum_co = (data2_y2 * eqn_fl2lum_y2)[data2_x > x_sncut/beamarea*2.5]
dist = r[data2_x > x_sncut/beamarea*2.5]

# gas mass
mass_15k = gas_mass_from_dust_flux(flux_dust,483.37293,zspec,DL*1e-3,15.0)
mass_25k = gas_mass_from_dust_flux(flux_dust,483.37293,zspec,DL*1e-3,25.0)
mass_35k = gas_mass_from_dust_flux(flux_dust,483.37293,zspec,DL*1e-3,35.0)

#
plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(left=0.15, right=0.90, bottom=0.10, top=0.85)
ax = plt.subplot(1,1,1)
ax.plot(dist,np.log10(mass_25k/lum_co),".",c="grey",markersize=10,alpha=1.0)

#ax.set_xlim()
#ax.set_ylim([0,10])
#ax.set_xlabel(xlabel)
#ax.set_ylabel("Count")
#ax.set_title(title)
ax.grid()
plt.legend()
plt.savefig(dir_data+"eps/radial_alpha_co.png",dpi=300)

#
plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(left=0.15, right=0.90, bottom=0.10, top=0.85)
ax = plt.subplot(1,1,1)
ax.plot(dist,np.log10(mass_25k/lum_ci),".",c="grey",markersize=10,alpha=1.0)

#ax.set_xlim()
#ax.set_ylim([0,10])
#ax.set_xlabel(xlabel)
#ax.set_ylabel("Count")
#ax.set_title(title)
ax.grid()
plt.legend()
plt.savefig(dir_data+"eps/radial_alpha_ci.png",dpi=300)
