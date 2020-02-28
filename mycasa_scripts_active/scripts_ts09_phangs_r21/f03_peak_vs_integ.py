import os
import re
import sys
import glob
import scipy


#####################
### parameters
#####################
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
percents = [0.15,0.025,0.010]

#####################
### Main Procedure
#####################
figure = plt.figure(figsize=(8,8))
histo = []
for i in range(len(gals)):
	galname = gals[i]
	data = np.loadtxt(dir_data + galname + "_parameter_matched_res.txt")

	r21 = data[:,1]
	r21[np.isnan(r21)] = 0
	p21 = data[:,9]
	p21[np.isnan(p21)] = 0
	co21 = data[:,4]
	#
	cut_r21 = (r21 > 0)
	cut_p21 = (p21 > 0)
	cut_co21 = (co21 > co21.max() * percents[i])
	cut_all = np.where((cut_r21) & (cut_p21) & (cut_co21))
	#
	r21 = r21[cut_all]
	p21 = p21[cut_all]
	#
	plt.rcParams["font.size"] = 16
	plt.grid()
	plt.xlim([-1.2,0.7])
	plt.ylim([-1.2,0.7])
	plt.scatter(np.log10(r21), np.log10(p21),
		c=cm.brg(i/2.5), alpha=0.1, lw=0, s=20,
		label = galname.replace("ngc","NGC "))
	plt.plot([-1.2,0.7],[-1.2,0.7],"k-",lw=1)
	plt.plot([-1.2,0.7],[-1.1,0.8],"k--",lw=1)
	plt.plot([-1.2,0.7],[-1.3,0.6],"k--",lw=1)

	histo.extend(p21/r21)

plt.xlabel("log Integrated Intensity Ratio")
plt.ylabel("log Peak Temperature Ratio")
plt.legend(loc = "upper left")
plt.savefig(dir_product+"figure_r21_vs_p21.png",dpi=100)
