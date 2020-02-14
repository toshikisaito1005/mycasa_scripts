import glob
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
plt.ioff()


#####################
### Define Functions
#####################


#####################
### Main Procedure
#####################
### ngc4321
scale = 103/1.4/1000. #kpc/arcsec

### weighted
dir_data = "/Users/saito/data/phangs/co_ratio/ngc4321/"

# plot 1
data = np.loadtxt(dir_data + "bm_vs_ap_r21_w2_median.txt")
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

for i in range(16):
    r21_tmp=data[data[:,0]==4+i*2]
    r21=r21_tmp[r21_tmp[:,1].argsort(), :]
    plt.plot(r21[:,1]*scale,
             r21[:,2],
             linewidth=2,
             c=cm.rainbow(i/15.),
             marker="o",
             alpha = 0.6)

plt.scatter([100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
            np.array([4,6,8,10,12,14,16,18,20,22,24,26,28,30,32])*scale,
            c=np.array([4,6,8,10,12,14,16,18,20,22,24,26,28,30,32])*scale,
            cmap="rainbow")

cbar=plt.colorbar()
cbar.set_label("Aperture Size (kpc)", size=18)

plt.xlim([0,35*scale])
plt.ylim([0.28,0.73])
plt.xlabel("Beam Size (kpc)")
plt.ylabel("$\~R_{w^2}$")
plt.text(0 + (35*scale-0*scale)*0.05,
         0.73 - (0.73-0.28)*0.08,
         "(e) $\~R_{w^2}$ vs. Beam Size")
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/f06m_r21_w2_median_vs_bm_n4321.png",
            dpi=100)

# plot 2
data = np.loadtxt(dir_data + "bm_vs_ap_r21_w2_median.txt")
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

for i in range(16):
    r21_tmp=data[data[:,0]==4+i*2]
    r21=r21_tmp[r21_tmp[:,1].argsort(), :]
    plt.plot(r21[:,1]*scale,
             r21[:,3],
             linewidth=2,
             c=cm.gnuplot(i/15.),
             marker="o",
             alpha = 0.6)

plt.scatter([100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
            np.array([4,6,8,10,12,14,16,18,20,22,24,26,28,30,32])*scale,
            c=np.array([4,6,8,10,12,14,16,18,20,22,24,26,28,30,32])*scale,
            cmap="gnuplot")

cbar=plt.colorbar()
cbar.set_label("Aperture Size (kpc)", size=18)

plt.xlim([0,35*scale])
plt.ylim([0.28,0.73])
plt.xlabel("Beam Size (kpc)")
plt.ylabel("$\~M_{w^2}$")
plt.text(0 + (35*scale-0*scale)*0.05,
         0.73 - (0.73-0.28)*0.08,
         "(f) $\~M_{w^2}$ vs. Beam Size")
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/f06n_m21_w2_median_vs_bm_n4321.png",
            dpi=100)

### inverse-weighted
dir_data = "/Users/saito/data/phangs/co_ratio/ngc4321/"

# plot 1
data = np.loadtxt(dir_data + "bm_vs_ap_r21_iw2_median.txt")
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

for i in range(16):
    r21_tmp=data[data[:,0]==4+i*2]
    r21=r21_tmp[r21_tmp[:,1].argsort(), :]
    plt.plot(r21[:,1]*scale,
             r21[:,2],
             linewidth=2,
             c=cm.rainbow(i/15.),
             marker="o",
             alpha = 0.6)

plt.scatter([100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
            np.array([4,6,8,10,12,14,16,18,20,22,24,26,28,30,32])*scale,
            c=np.array([4,6,8,10,12,14,16,18,20,22,24,26,28,30,32])*scale,
            cmap="rainbow")

cbar=plt.colorbar()
cbar.set_label("Aperture Size (kpc)", size=18)

plt.xlim([0,35*scale])
plt.ylim([0.28,0.73])
plt.xlabel("Beam Size (kpc)")
plt.ylabel("$\~R_{1/w^2}$")
plt.text(0 + (35*scale-0*scale)*0.05,
         0.73 - (0.73-0.28)*0.08,
         "(g) $\~R_{1/w^2}$ vs. Beam Size")
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/f06o_r21_iw2_median_vs_bm_n4321.png",
            dpi=100)

# plot 2
data = np.loadtxt(dir_data + "bm_vs_ap_r21_iw2_median.txt")
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

for i in range(16):
    r21_tmp=data[data[:,0]==4+i*2]
    r21=r21_tmp[r21_tmp[:,1].argsort(), :]
    plt.plot(r21[:,1]*scale,
             r21[:,3],
             linewidth=2,
             c=cm.gnuplot(i/15.),
             marker="o",
             alpha = 0.6)

plt.scatter([100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
            np.array([4,6,8,10,12,14,16,18,20,22,24,26,28,30,32])*scale,
            c=np.array([4,6,8,10,12,14,16,18,20,22,24,26,28,30,32])*scale,
            cmap="gnuplot")

cbar=plt.colorbar()
cbar.set_label("Aperture Size (kpc)", size=18)

plt.xlim([0,35*scale])
plt.ylim([0.28,0.73])
plt.xlabel("Beam Size (kpc)")
plt.ylabel("$\~M_{1/w^2}$")
plt.text(0 + (35*scale-0*scale)*0.05,
         0.73 - (0.73-0.28)*0.08,
         "(h) $\~M_{1/w^2}$ vs. Beam Size")
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/f06p_m21_iw2_median_vs_bm_n4321.png",
            dpi=100)
