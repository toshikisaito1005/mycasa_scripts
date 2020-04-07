import os
import sys
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()

#####################
### parameters
#####################
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"


#####################
### Main Procedure
#####################
### import data
data = np.loadtxt("ngc0628_stats_600pc.txt")
stats_n0628_no = data[0:5]
stats_n0628_wco10 = data[5:10]
stats_n0628_wco21 = data[10:15]

data = np.loadtxt("ngc3627_stats_600pc.txt")
stats_n3627_no = data[0:5]
stats_n3627_wco10 = data[5:10]
stats_n3627_wco21 = data[10:15]

data = np.loadtxt("ngc4321_stats_600pc.txt")
stats_n4321_no = data[0:5]
stats_n4321_wco10 = data[5:10]
stats_n4321_wco21 = data[10:15]


### plot
# setup
fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(111)
ax1.grid(which='major',linestyle='--')
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)
#
ax1.plot(stats_n0628_no[:,0],stats_n0628_no[:,1],'-o',alpha=0.4,c=cm.brg(0/2.5),lw=1)
ax1.plot(stats_n0628_wco10[:,0],stats_n0628_wco10[:,1],'-o',alpha=0.4,c=cm.brg(0/2.5),lw=4)
ax1.plot(stats_n0628_wco21[:,0],stats_n0628_wco21[:,1],'-o',alpha=0.4,c=cm.brg(0/2.5),lw=7)
ax1.plot(stats_n3627_no[:,0],stats_n3627_no[:,1],'-o',alpha=0.4,c=cm.brg(1/2.5),lw=1)
ax1.plot(stats_n3627_wco10[:,0],stats_n3627_wco10[:,1],'-o',alpha=0.4,c=cm.brg(1/2.5),lw=4)
ax1.plot(stats_n3627_wco21[:,0],stats_n3627_wco21[:,1],'-o',alpha=0.4,c=cm.brg(1/2.5),lw=7)
ax1.plot(stats_n4321_no[:,0],stats_n4321_no[:,1],'-o',alpha=0.4,c=cm.brg(2/2.5),lw=1)
ax1.plot(stats_n4321_wco10[:,0],stats_n4321_wco10[:,1],'-o',alpha=0.4,c=cm.brg(2/2.5),lw=4)
ax1.plot(stats_n4321_wco21[:,0],stats_n4321_wco21[:,1],'-o',alpha=0.4,c=cm.brg(2/2.5),lw=7)

ax1.set_xlim([0,16])
ax1.set_ylim([0.3,1.1])

ax1.set_xticklabels([1,2],["84%","Mean"])

plt.savefig(dir_product+"stats_histo_600pc.png",dpi=300)


