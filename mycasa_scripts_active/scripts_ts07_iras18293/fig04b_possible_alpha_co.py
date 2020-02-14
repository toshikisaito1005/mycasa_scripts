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
import matplotlib.cm as cm
import matplotlib.patches as pat
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts07_iras18293/"
box = "103,115,180,192"
beamarea = 22.382

zspec = 0.01818
DL = 78.2 # Mpc

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

def function(x, a, b):
    return a * x + b


#####################
### function
#####################
def Q10(r,y1,y2): # Q10 = 0.4
    a = (y2-y1)/(2.5-0.0)
    b = y1
    Q10 = a * r + b

    return Q10

def Xci(r,y1,y2): # Xci = 3e-5
    a = (y2-y1)/(2.5-0.0)
    b = y1
    Xci = a * r + b

    return Xci

A10 = 7.93e-8
def gasmass_catom(DL,zspec,Xci,A10,Q10,flux): # Alaghband-Zadeh et al. 2013
    MH2 = 1375.8 * DL**2 / (1+zspec) / (Xci/1e-05) / (A10/1e-7) / Q10 * flux

    return MH2

def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale
    
    return r

# center
ra = "18h32m41.1300s"
decl = "-34d11m27.672s"
c = SkyCoord(ra, decl)
ra_cnt = c.ra.degree
dec_cnt = c.dec.degree

# CI(1-0) observed frequency
obsfreq = 492.16065100 / (1 + 0.01818)
obsfreq_co10 = 115.27120 / (1 + 0.01818)
# flux (Jy.km/s) to luminosity (K.km/spc^2)
eqn_fl2lum = 3.25e+7 / obsfreq**2 * DL**2 / (1 + zspec)**3
eqn_fl2lum_co = 3.25e+7 / obsfreq_co10**2 * DL**2 / (1 + zspec)**3

#####################
### Main Procedure
#####################

# import moment-0 maps in Jy/beam.km/s
data_ci_org = imval(dir_data + "image_ci10/ci10.moment0",box=box)["data"]
data_co_org = imval(dir_data + "image_co10/co10.moment0",box=box)["data"]
data_ci = data_ci_org.flatten()
data_co = data_co_org.flatten()
data1_ci = data_ci[data_ci>0]
data1_co = data_co[data_ci>0]
data2_ci = data1_ci[data1_co>0] / beamarea # Jy.km/s
data2_co = data1_co[data1_co>0] / beamarea # Jy.km/s
cliplevel = data2_co.max() * 0.1

# importnoise maps in Jy.km/s
data_noiseci_org = imval(dir_data + "image_ci10/ci10.moment0.noise_Jykms",box=box)["data"]
data_noiseco_org = imval(dir_data + "image_co10/co10.moment0.noise_Jykms",box=box)["data"]
data_noiseci = data_noiseci_org.flatten()
data_noiseco = data_noiseco_org.flatten()
data1_noiseci = data_noiseci[data_ci>0]
data1_noiseco = data_noiseco[data_ci>0]
data2_noiseci = data1_noiseci[data1_co>0]
data2_noiseco = data1_noiseco[data1_co>0]

# import ra dec in degree
ra_co_tmp =imval(dir_data+"image_co10/co10.moment0",box=box)["coords"][:,:,0]
dec_co_tmp =imval(dir_data+"image_co10/co10.moment0",box=box)["coords"][:,:,1]
ra_co = ra_co_tmp * 180/np.pi
dec_co = dec_co_tmp * 180/np.pi
r_tmp = distance(ra_co, dec_co, 109.90-90, 90, ra_cnt, dec_cnt, 0.365)
r_tmp2 = r_tmp.flatten() # 90-53.737
r_tmp3 = r_tmp2[data_ci>0]
r = r_tmp3[data1_co>0]

# plot
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)
ax1.grid(which='major',linestyle='--')
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)
#
x = r[data2_co>cliplevel]
q1_values = np.linspace(0.35,0.45,6)
q2_values = np.linspace(0.45,0.35,6)
X1_values = np.linspace(1.5e-5,4.5e-5,6)
X2_values = np.linspace(4.5e-5,1.5e-5,6)

for i in range(len(X1_values)):
    for j in range(len(q1_values)):
        MH2 = gasmass_catom(DL,zspec,
                            Xci(r,X1_values[i],X2_values[i]),
                            A10,
                            Q10(r,q1_values[j],q2_values[j]),
                            data2_ci)
        y = (MH2/(data2_co * eqn_fl2lum_co))[data2_co>cliplevel]
        #ax1.scatter(x,y,lw=0,c="mediumpurple",alpha=0.5,s=60)
        noiseMH2 = gasmass_catom(DL,zspec,
                                 Xci(r,X1_values[i],X2_values[i]),
                                 A10,
                                 Q10(r,q1_values[j],q2_values[j]),
                                 data2_noiseci)
        yerr = (noiseMH2/(data2_co * eqn_fl2lum_co))[data2_co>cliplevel]
        #
        popt, pcov = curve_fit(function,r[data2_co>cliplevel],y,p0 = [1.0,1.0],
                               maxfev = 10000,sigma=yerr)
        x = np.linspace(0.0, 3.0, 50)
        #ax1.scatter(i,j,c=cm.rainbow((popt[0]+2.0)/2.0),s=7050,marker="s",alpha=0.4,lw=0)
        e1 = pat.Ellipse(xy = (i, j),
                         width = 0.8, height = 0.0,
                         alpha = 0.8, angle = np.degrees(np.arctan(popt[0])),
                         color = cm.rainbow((popt[0]+1.7)/1.7),
                         lw = 10)
        ax1.text(i-0.1, j+0.2, str(np.round(popt[0]*-1,2)), fontsize = 18)
        ax1.add_patch(e1)

e2 = pat.Rectangle(xy=(-0.45,-0.45),width=5.9,height=2.9,lw=0,alpha=0.6,color="grey")
ax1.add_patch(e2)
e2 = pat.Rectangle(xy=(-0.4,-0.4),width=2.8,height=5.8,lw=0,alpha=0.6,color="grey")
ax1.add_patch(e2)

# range
xwidth1 = 0.1 * (x.max() - x.min())
#ax1.set_xlim([-0.1,2.8])
#ax1.set_ylim([-0.6,0.75])
ax1.set_xlim([-0.5,5.5])
ax1.set_ylim([-0.5,5.5])
plt.xticks([0,1,2,3,4,5],['-1.20','-0.72','-0.24','0.24','0.72','1.20'])
plt.yticks([0,1,2,3,4,5],['-0.040','-0.024','-0.008','0.008','0.024','0.040'])
#ax1.set_xlabel("Distance from the center (kpc)")
#ax1.set_ylabel(u"log $\u03b1_{CO}$ ($M_{\odot}$(K km s$^{-1}$ pc$^2$)$^{-1}$)")
ax1.set_xlabel("Slope of $X_{CI}$/10$^{-5}$")
ax1.set_ylabel("Slope of $Q_{10}$")
plt.title(u"Radial $\u03b1_{CO}$ Distribution")

# plot eyeguides
peak = (data2_co * eqn_fl2lum_co).max()

plt.savefig(dir_data+"eps/radial_alpha_nonflat.png",dpi=300)

