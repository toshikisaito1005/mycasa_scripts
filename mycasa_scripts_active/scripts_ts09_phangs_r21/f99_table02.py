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
def table03_galname(galname,txtfile1,txtfile2):
	"""
	"""
	table = []
	txtdata1 = np.loadtxt(txtfile1,dtype="str")
	txtdata2 = np.loadtxt(txtfile2,dtype="str")
	for j in range(len(txtdata1)):
		onerow_tmp = extract_onerow(txtdata1[j],txtdata2[j])
		if j==0:
			onerow = galname + " & " + onerow_tmp + " \\\\ \n"
		else:
			onerow = " & " + onerow_tmp + " \\\\ \n"
		table.append(onerow)

	return table

def extract_onegal(txtdata):
	"""
	"""
	txtdata = np.loadtxt(txtfile,dtype="str")[:,1]
	l1 = txtdata[0] + " & " + txtdata[5] + " & " + txtdata[10]
	l2 = txtdata[1] + " & " + txtdata[6] + " & " + txtdata[11]
	l3 = txtdata[2] + " & " + txtdata[7] + " & " + txtdata[12]
	l4 = txtdata[3] + " & " + txtdata[8] + " & " + txtdata[13]
	l5 = txtdata[4] + " & " + txtdata[9] + " & " + txtdata[14]



#####################
### main
#####################
table03 = []
for i in range(len(txtfile1)):
	galname = txtfile1[i].split("_")[1].replace("ngc","NGC ")
	galname2 = txtfile1[i].split("_")[1]
	table = table03_galname(galname, txtfile1[i], txtfile2[i])
	table03.append(table)
	os.system("rm -rf " + txtfile1[i] + " " + txtfile2[i])

np.savetxt("table03.txt",table03,fmt="%s")
