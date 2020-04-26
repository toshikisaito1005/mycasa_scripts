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
table02 = []
for i in range(len(txtfile)):
	galname = txtfile[i].split("/")[-1].split("_")[0].replace("ngc","NGC ")
	galname2 = txtfile[i].split("/")[-1].split("_")[0]
	l1,l2,l3,l4,l5 = extract_onegal(txtfile[i])

	table03.append(table)
	os.system("rm -rf " + txtfile1[i] + " " + txtfile2[i])

np.savetxt("table03.txt",table03,fmt="%s")
