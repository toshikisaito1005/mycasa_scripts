import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
plt.ioff()

#
data = np.loadtxt("n6240_mom8_data.txt")
dir_product = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/eps/"
#
dist = data[:,0]
co10 = data[:,1]
co21 = data[:,2]

#
fig = plt.figure(figsize=(10,10))                #
ax1 = fig.add_subplot(111)                       #
ax1.grid(which='both',linestyle='--')            #
plt.rcParams["font.size"] = 22                   #
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.85)  #

cscatter = ax1.scatter(np.log10(co10),           #
                       np.log10(co21),           #
                       lw = 0,                   #
                       c = dist,                 #
                       cmap = "jet",             #
                       alpha = 0.5,              #
                       s = 40,                   #
                       norm=Normalize(vmin=0, vmax=7)) #

ax1.plot([-10,10],[-10,10],"k-",lw=2)            #

cbar = plt.colorbar(cscatter)

ax1.set_xlim([-0.7,1.7])                         #
ax1.set_ylim([-0.7,1.7])                         #
cbar.set_clim([0,7])                             #

ax1.set_xlabel("CO(1-0) Brightness Temperature (K)") #
ax1.set_ylabel("CO(2-1) Brightness Temperature (K)") #
cbar.set_label("Distance (kpc)")                 #

plt.savefig(dir_product + "figure_co21_vs_co10.png",dpi=300)
