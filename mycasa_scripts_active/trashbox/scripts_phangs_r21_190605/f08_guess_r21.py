import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
import scipy.stats as stats
from scipy.optimize import curve_fit
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
"""
gal = "ngc0628"
scale = 44/1.0/1000. #kpc/arcsec 0628
ra_cnt = 24.174
dec_cnt = 15.783
pa = 21.1
inc = 90-8.7
size = 0.04
apr = 16./8.
vmin=0.1
vmax=0.85
txtfile="../../phangs/co_ratio/"+gal+"_wise/"+gal+"_flux_14p0_14p0_no.txt"
"""
gal = "ngc4321"
scale = 103/1.4/1000. #kpc/arcsec 4321
ra_cnt = 185.729
dec_cnt = 15.8223
pa = 180-157.8
inc = 90-35.1
size = 0.035
apr = 8./8.
vmin=0.0
vmax=0.7
txtfile="../../phangs/co_ratio/"+gal+"_wise/"+gal+"_flux_8p0_8p0_no.txt"


dir_eps="/Users/saito/data/phangs/co_ratio/eps/"
slopes=txtfile.replace(".txt","_linearfit.txt")
beam = 8.0


#####################
### functions
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

#####################
### Main Procedure
#####################
slope = np.loadtxt(slopes)
data = np.loadtxt(txtfile)

##################### data 1
y=data[:,3]/data[:,2]/4.
for i in range(len(y)):
    if data[:,2][i]==0:
        y[i]=-1

r=distance(data[:,0],data[:,1],pa,inc,ra_cnt,dec_cnt,scale)

### plot
# setup
plt.figure(figsize=(10,3))
plt.rcParams["font.size"] = 10
gs = gridspec.GridSpec(nrows=12, ncols=17)
scat1 = plt.subplot(gs[0:9,0:4])
scat2 = plt.subplot(gs[0:9,4:8])
scat3 = plt.subplot(gs[0:9,8:12])
scat4 = plt.subplot(gs[0:9,12:16])

#scat1.set_xticks([])
#scat1.set_yticks([])
scat1.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat1.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(r)*slope[0][1] + slope[0][2]))[data[:,10]>0]
scat1.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat1.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "a) Radius-based $R_{21}$")
scat1.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat2.set_xticks([])
scat2.set_yticks([])
scat2.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat2.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,3])*slope[1][1] + slope[1][2]))[data[:,10]>0]
scat2.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat2.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "b) $I_{CO(2-1)}$-based $R_{21}$")
scat2.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat3.set_xticks([])
scat3.set_yticks([])
scat3.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat3.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,7])*slope[2][1] + slope[2][2]))[data[:,10]>0]
for i in range(len(data_color)):
    if data[:,7][data[:,10]>0][i]==0:
        data_color[i]=0

scat3.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat3.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "c) $T_{CO(2-1)}$-based $R_{21}$")
scat3.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat4.set_xticks([])
scat4.set_yticks([])
scat4.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat4.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,5])*slope[3][1] + slope[3][2]))[data[:,10]>0]
scat4.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat4.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "d) $\sigma$-based $R_{21}$")
scat4.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

scat1.set_xlabel("x-offset (kpc)")
scat1.set_ylabel("y-offset (kpc)")
scat2.set_xlabel("x-offset (kpc)")
scat3.set_xlabel("x-offset (kpc)")
scat4.set_xlabel("x-offset (kpc)")
plt.savefig(dir_eps+"figure8_multiplot1.png",dpi=200)


### plot
# setup
plt.figure(figsize=(10,3))
plt.rcParams["font.size"] = 10
gs = gridspec.GridSpec(nrows=12, ncols=17)
scat1 = plt.subplot(gs[0:9,0:4])
scat2 = plt.subplot(gs[0:9,4:8])
scat3 = plt.subplot(gs[0:9,8:12])
scat4 = plt.subplot(gs[0:9,12:16])

#scat1.set_xticks([])
#scat1.set_yticks([])
scat1.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat1.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,8])*slope[4][1] + slope[4][2]))[data[:,10]>0]
scat1.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat1.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "e) W1-based $R_{21}$")
scat1.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat2.set_xticks([])
scat2.set_yticks([])
scat2.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat2.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,9])*slope[5][1] + slope[5][2]))[data[:,10]>0]
scat2.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat2.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "f) W2-based $R_{21}$")
scat2.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat3.set_xticks([])
scat3.set_yticks([])
scat3.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat3.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,10])*slope[6][1] + slope[6][2]))[data[:,10]>0]
scat3.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat3.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "g) W3-based $R_{21}$")
scat3.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat4.set_xticks([])
scat4.set_yticks([])
scat4.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat4.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,10]/data[:,8])*slope[7][1] + slope[7][2]))[data[:,10]>0]
for i in range(len(data_color)):
    if data[:,8][data[:,10]>0][i]==0:
        data_color[i]=0

scat4.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat4.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "h) W3/W1-based $R_{21}$")
scat4.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

scat1.set_xlabel("x-offset (kpc)")
scat1.set_ylabel("y-offset (kpc)")
scat2.set_xlabel("x-offset (kpc)")
scat3.set_xlabel("x-offset (kpc)")
scat4.set_xlabel("x-offset (kpc)")
plt.savefig(dir_eps+"figure8_multiplot2.png",dpi=200)


### plot
# setup
plt.figure(figsize=(10,3))
plt.rcParams["font.size"] = 10
gs = gridspec.GridSpec(nrows=12, ncols=17)
scat1 = plt.subplot(gs[0:9,0:4])
scat2 = plt.subplot(gs[0:9,4:8])
scat3 = plt.subplot(gs[0:9,8:12])
scat4 = plt.subplot(gs[0:9,12:16])

#scat1.set_xticks([])
#scat1.set_yticks([])
scat1.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat1.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,8]/data[:,7])*slope[8][1] + slope[8][2]))[data[:,10]>0]
for i in range(len(data_color)):
    if data[:,7][data[:,10]>0][i]==0:
        data_color[i]=0

scat1.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat1.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "i) W1/$T_{CO(2-1)}$-based $R_{21}$")
scat1.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat2.set_xticks([])
scat2.set_yticks([])
scat2.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat2.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,9]/data[:,7])*slope[9][1] + slope[9][2]))[data[:,10]>0]
for i in range(len(data_color)):
    if data[:,7][data[:,10]>0][i]==0:
        data_color[i]=0

scat2.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat2.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "j) W2/$T_{CO(2-1)}$-based $R_{21}$")
scat2.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat3.set_xticks([])
scat3.set_yticks([])
scat3.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat3.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,10]/data[:,7])*slope[10][1] + slope[10][2]))[data[:,10]>0]
for i in range(len(data_color)):
    if data[:,7][data[:,10]>0][i]==0:
        data_color[i]=0

scat3.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat3.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "k) W3/$T_{CO(2-1)}$-based $R_{21}$")
scat3.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

#scat4.set_xticks([])
scat4.set_yticks([])
scat4.set_xlim([1*size*scale*3600,-1*size*scale*3600])
scat4.set_ylim([-1*size*scale*3600,1*size*scale*3600])
data_color = (10**(np.log10(data[:,10]/data[:,5])*slope[11][1] + slope[11][2]))[data[:,10]>0]
for i in range(len(data_color)):
    if data[:,7][data[:,10]>0][i]==0:
        data_color[i]=0

scat4.scatter((data[:,0][data[:,10]>0]-ra_cnt)*scale*3600,
              (data[:,1][data[:,10]>0]-dec_cnt)*scale*3600,
              c=data_color,lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",
              marker="h",s=25*size/0.035*apr)

rms = str(np.round(np.sqrt(np.mean((data_color-y[data[:,10]>0])**2)),2))
scat4.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
           "l) W3/$\sigma$-based $R_{21}$")
scat4.text(0.024*scale*3600*size/0.035,0.020*scale*3600*size/0.035,rms)

scat1.set_xlabel("x-offset (kpc)")
scat1.set_ylabel("y-offset (kpc)")
scat2.set_xlabel("x-offset (kpc)")
scat3.set_xlabel("x-offset (kpc)")
scat4.set_xlabel("x-offset (kpc)")
plt.savefig(dir_eps+"figure8_multiplot3.png",dpi=200)


plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 18
#plt.yticks([])
plt.xlim([1*size*scale*3600,-1*size*scale*3600])
plt.ylim([-1*size*scale*3600,1*size*scale*3600])
x_ra = data[:,0][data[:,10]>0]-ra_cnt
y_dec = data[:,1][data[:,10]>0]-dec_cnt
c_val = y[data[:,10]>0]
hcmask = data[:,12][data[:,10]>0]
plt.scatter(x_ra*scale*3600,
            y_dec*scale*3600,
            s=300*size/0.035*apr,c=c_val,
            lw=0,vmin=vmin,vmax=vmax,cmap="rainbow",marker="h")

plt.text(0.032*scale*3600*size/0.035,0.027*scale*3600*size/0.035,
         "m) Observed $R_{21}$")

plt.xlabel("x-offset (kpc)")
plt.ylabel("y-offset (kpc)")
plt.savefig(dir_eps+"figure8_multiplot4.png",dpi=200)
