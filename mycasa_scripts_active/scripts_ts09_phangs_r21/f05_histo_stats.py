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
fig = plt.figure(figsize=(20,5))
ax1 = fig.add_subplot(111)
ax1.grid(which='major',linestyle='--')
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.20, left=0.05, right=0.95, top=0.90)
#
ax1.plot(stats_n0628_no[:,0],stats_n0628_no[:,1]/stats_n0628_no[2][1],
	'-o',alpha=0.4,c=cm.brg(0/2.5),lw=1)
ax1.plot(stats_n0628_wco10[:,0],stats_n0628_wco10[:,1]/stats_n0628_no[2][1],
	'-o',alpha=0.4,c=cm.brg(0/2.5),lw=4)
ax1.plot(stats_n0628_wco21[:,0],stats_n0628_wco21[:,1]/stats_n0628_no[2][1],
	'-o',alpha=0.4,c=cm.brg(0/2.5),lw=7)

ax1.plot(stats_n3627_no[:,0]+1,stats_n3627_no[:,1]/stats_n3627_no[2][1],
	'-o',alpha=0.4,c=cm.brg(1/2.5),lw=1)
ax1.plot(stats_n3627_wco10[:,0]+1,stats_n3627_wco10[:,1]/stats_n3627_no[2][1],
	'-o',alpha=0.4,c=cm.brg(1/2.5),lw=4)
ax1.plot(stats_n3627_wco21[:,0]+1,stats_n3627_wco21[:,1]/stats_n3627_no[2][1],
	'-o',alpha=0.4,c=cm.brg(1/2.5),lw=7)

ax1.plot(stats_n4321_no[:,0]+2,stats_n4321_no[:,1]/stats_n4321_no[2][1],
	'-o',alpha=0.4,c=cm.brg(2/2.5),lw=1)
ax1.plot(stats_n4321_wco10[:,0]+2,stats_n4321_wco10[:,1]/stats_n4321_no[2][1],
	'-o',alpha=0.4,c=cm.brg(2/2.5),lw=4)
ax1.plot(stats_n4321_wco21[:,0]+2,stats_n4321_wco21[:,1]/stats_n4321_no[2][1],
	'-o',alpha=0.4,c=cm.brg(2/2.5),lw=7)

ax1.text(3,1.42,'NGC 0628',horizontalalignment='center')
ax1.text(9,1.42,'NGC 3627',horizontalalignment='center')
ax1.text(15,1.42,'NGC 4321',horizontalalignment='center')

ax1.set_xlim([0.5,17.5])
ax1.set_ylim([0.7,1.5])
ax1.plot([0,18],[1,1],'k-',lw=2)

plt.xticks([1,2,3,4,5,7,8,9,10,11,13,14,15,16,17],["84%","Mean","Median","Mode","16%","84%","Mean","Median","Mode","16%","84%","Mean","Median","Mode","16%"])
plt.xticks(rotation=45)

plt.savefig(dir_product+"stats_histo_600pc.png",dpi=300)
