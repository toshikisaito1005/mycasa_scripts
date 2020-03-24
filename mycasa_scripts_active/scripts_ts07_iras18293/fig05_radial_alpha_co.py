import os, re, sys
import math
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import matplotlib.gridspec as gridspec
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts07_iras18293/"
box = "103,115,180,192"
beamarea = 22.382
distance_range = [0.0,2.8]

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
def hist_percent(histo,percent):
    dat_sum = np.sum(histo)
    dat_sum_from_zero,i = 0,0
    while dat_sum_from_zero < dat_sum * percent:
        dat_sum_from_zero += histo[i]
        i += 1
    
    return i

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

def alpha_catom10(Xci,Q10,flux,luminosity): # Alaghband-Zadeh et al. 2013
    A10 = 7.93e-8
    DL = 78.2 # Mpc
    zspec = 0.01818
    MH2 = 1375.8 * DL**2 / (1+zspec) / (Xci/1e-05) / (A10/1e-7) / Q10 * flux
    alpha = MH2/luminosity

    return alpha

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
flux_ci = data2_y1[data2_x > x_sncut/beamarea*2.5]

# gas mass
mass = gas_mass_from_dust_flux(flux_dust,483.37293,zspec,DL*1e-3,20.0)



### alpha_co
ylim = [-0.3,1.7]

plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 16
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:6,0:6])
ax2 = plt.subplot(gs[0:6,6:8])
ax3 = ax2.twinx()

# ax1 scatter
ax1.plot(dist,np.log10(mass/lum_co),".",c="red",markersize=10,alpha=0.5)
ax1.set_xlim(distance_range)
ax1.set_ylim(ylim)
ax1.grid(axis="both")
ax1.set_xlabel("Distance (kpc)")
ax1.set_ylabel(r"log $\alpha_{CO(1-0)}$")

# ax2 histogram
histo = ax2.hist(np.log10(mass/lum_co),range=[-0.5,1.5],bins=60,
                 orientation="horizontal",lw=4,color="red",alpha=0.5,histtype=u'step',
                 weights=lum_co,normed=True)
ax2.tick_params(labelleft=False,labelbottom=False)
ax2.tick_params(bottom=False,left=False,right=True,top=False)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.set_xlim([0,histo[0].max()*1.2])
ax2.set_ylim(ylim)
ax2.grid(axis="y")

# ax3 label in the right
ax3.spines["left"].set_visible(False)
ax3.tick_params(labelleft=False,labelbottom=False)
ax3.set_ylim(ylim)
ax3.set_ylabel(r"log $\alpha_{CO(1-0)}$")

# stats
r_mean = np.mean(np.log10(mass/lum_co))
r_median = np.median(np.log10(mass/lum_co))
r_84 = histo[1][hist_percent(histo[0],0.843)]
r_16 = histo[1][hist_percent(histo[0],0.157)]
ax1.plot(distance_range,[r_84,r_84],"--",color="black",lw=2)
ax1.plot(distance_range,[r_median,r_median],"-",color="black",lw=4)
ax1.plot(distance_range,[r_16,r_16],"--",color="black",lw=2)
ax2.plot([0,histo[0].max()*1.2],[r_84,r_84],"--",color="black",lw=2)
ax2.plot([0,histo[0].max()*1.2],[r_median,r_median],"-",color="black",lw=4)
ax2.plot([0,histo[0].max()*1.2],[r_16,r_16],"--",color="black",lw=2)

# texts
ax1.text(2.45,r_84+0.02,"84%")
ax1.text(2.22,r_median+0.02,"median")
ax1.text(2.45,r_16+0.02,"16%")
step = (ylim[1]-ylim[0]) * 0.1
ax1.text(0.20,ylim[1] - step*1.0, "84% = " + str(np.round(10**r_84,1)))
ax1.text(0.20,ylim[1] - step*1.5, "median = " + str(np.round(10**r_median,1)))
ax1.text(0.20,ylim[1] - step*2.0, "16% = " + str(np.round(10**r_16,1)))

ax1.set_title(r"Radial $\alpha_{CO(1-0)}$")
plt.legend()
plt.savefig(dir_data+"eps/radial_alpha_co.png",dpi=300)


### alpha_ci
ylim = [0.6,2.1]

plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 16
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:6,0:6])
ax2 = plt.subplot(gs[0:6,6:8])
ax3 = ax2.twinx()

# ax1 scatter
ax1.plot(dist,np.log10(mass/lum_ci),".",c="blue",markersize=10,alpha=0.5)
ax1.set_xlim(distance_range)
ax1.set_ylim(ylim)
ax1.grid(axis="both")
ax1.set_xlabel("Distance (kpc)")
ax1.set_ylabel(r"log $\alpha_{[CI](1-0)}$")

# ax2 histogram
histo = ax2.hist(np.log10(mass/lum_ci),range=[-0.5,1.5],bins=60,
                 orientation="horizontal",lw=4,color="blue",alpha=0.5,histtype=u'step',
                 weights=lum_ci,normed=True)
ax2.tick_params(labelleft=False,labelbottom=False)
ax2.tick_params(bottom=False,left=False,right=True,top=False)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.set_xlim([0,histo[0].max()*1.2])
ax2.set_ylim(ylim)
ax2.grid(axis="y")

# ax3 label in the right
ax3.spines["left"].set_visible(False)
ax3.tick_params(labelleft=False,labelbottom=False)
ax3.set_ylim(ylim)
ax3.set_ylabel(r"log $\alpha_{[CI](1-0)}$")

# stats
r_mean = np.mean(np.log10(mass/lum_ci))
r_median = np.median(np.log10(mass/lum_ci))
r_84 = histo[1][hist_percent(histo[0],0.843)]
r_16 = histo[1][hist_percent(histo[0],0.157)]
ax1.plot(distance_range,[r_84,r_84],"--",color="black",lw=2)
ax1.plot(distance_range,[r_median,r_median],"-",color="black",lw=4)
ax1.plot(distance_range,[r_16,r_16],"--",color="black",lw=2)
ax2.plot([0,histo[0].max()*1.2],[r_84,r_84],"--",color="black",lw=2)
ax2.plot([0,histo[0].max()*1.2],[r_median,r_median],"-",color="black",lw=4)
ax2.plot([0,histo[0].max()*1.2],[r_16,r_16],"--",color="black",lw=2)

# texts
ax1.text(2.45,r_84+0.02,"84%")
ax1.text(2.22,r_median+0.02,"median")
ax1.text(2.45,r_16-0.08,"16%")
step = (ylim[1]-ylim[0]) * 0.1
ax1.text(0.20,ylim[1] - step*1.0, "84% = " + str(np.round(10**r_84,1)))
ax1.text(0.20,ylim[1] - step*1.5, "median = " + str(np.round(10**r_median,1)))
ax1.text(0.20,ylim[1] - step*2.0, "16% = " + str(np.round(10**r_16,1)))

ax1.set_title(r"Radial $\alpha_{[CI](1-0)}$")
plt.legend()
plt.savefig(dir_data+"eps/radial_alpha_ci.png",dpi=300)


# alpha_ci heatmap on Q-X plane
list_x = []
list_q = []
list_alpha = []

iterate_x = np.linspace(1e-5, 5e-5, 50)
iterate_q = np.linspace(0.35, 0.50, 50)
#iterate_x = np.linspace(1e-5, 8e-5, 50)
#iterate_q = np.linspace(0.15, 0.55, 50)
for j in range(len(iterate_q)):
    Qrot = iterate_q[j]
    for i in range(len(iterate_x)):
        Xci = iterate_x[i]
        alpha = alpha_catom10(Xci,Qrot,flux_ci.max(),lum_ci.max())
        list_x.append(Xci)
        list_q.append(Qrot)
        list_alpha.append(alpha)

map_X, map_Q = np.meshgrid(iterate_x, iterate_q)
list_x = (np.array(list_x)*1e5).tolist()
map_alpha = np.reshape(list_alpha,(50,50))

fig = plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(111)
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom=0.20, left=0.15, right=0.85, top=0.85)

cscatter = ax1.scatter(list_x,list_q,c=list_alpha,cmap='rainbow',s=60,lw=0,marker='s')
cont = ax1.contour(map_X*1e5,map_Q,map_alpha,linewidths=[2,4,2],levels=[11.7,14.0,17.1],colors=['black'])
cont.clabel(fmt='%1.1f',fontsize=14)
cont2 = ax1.contour(map_X*1e5,map_Q,map_alpha,linewidths=1,levels=[7,8,10,12,14,16,18],colors=['grey'])
cont2.clabel(fmt='%1.1f',fontsize=14)
ax1.set_xlim([min(list_x),max(list_x)])
ax1.set_ylim([min(list_q),max(list_q)])
ax1.set_xlabel('$X_{CI}$/10$^{-5}$')
ax1.set_ylabel('$Q_{10}$')

cbar = plt.colorbar(cscatter)#cax=cax)
cbar.set_label(r"$\alpha_{[CI](1-0)}$")
plt.savefig(dir_data+"eps/heatmap_alpha_ci.png",dpi=300)
plt.savefig(dir_data+"eps/fig06.eps",dpi=300)
