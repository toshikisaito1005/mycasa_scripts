import os, sys, glob
import numpy as np


#####################
### parameters
#####################
dir_txt = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
txtfile = glob.glob(dir_txt + "ngc*_stats_600pc.txt")


#####################
### functions
#####################
def extract_onegal(txtdata):
	"""
	"""
	txtdata = np.loadtxt(txtdata,dtype="str")[:,1]
	l1 = txtdata[0] + " & " + txtdata[5] + " & " + txtdata[10]
	l2 = txtdata[1] + " & " + txtdata[6] + " & " + txtdata[11]
	l3 = txtdata[2] + " & " + txtdata[7] + " & " + txtdata[12]
	l4 = txtdata[3] + " & " + txtdata[8] + " & " + txtdata[13]
	l5 = txtdata[4] + " & " + txtdata[9] + " & " + txtdata[14]

	return l1, l2, l3, l4, l5


#####################
### main
#####################
list_l1 = []
list_l2 = []
list_l3 = []
list_l4 = []
list_l5 = []
for i in range(len(txtfile)):
	galname = txtfile[i].split("/")[-1].split("_")[0].replace("ngc","NGC ")
	galname2 = txtfile[i].split("/")[-1].split("_")[0]
	l1,l2,l3,l4,l5 = extract_onegal(txtfile[i])
	list_l1.append(l1)
	list_l2.append(l2)
	list_l3.append(l3)
	list_l4.append(l4)
	list_l5.append(l5)

np.r_["84\% & "   + " && ".join(list_l1) + " \\\\ \n",
	  "Mean & "   + " && ".join(list_l2) + " \\\\ \n",
	  "Median & " + " && ".join(list_l3) + " \\\\ \n",
	  "Mode & "   + " && ".join(list_l4) + " \\\\ \n",
	  "16\% & "   + " && ".join(list_l5)]


np.savetxt("table03.txt",table03,fmt="%s")
