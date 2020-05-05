import os, sys, glob
import numpy as np


#####################
### parameters
#####################
txtfile = glob.glob("fig_r21_vs_*.txt")


#####################
### functions
#####################
def table04_galname(txtfile1,txtfile2):
	"""
	"""
	table = []
	dataname = txtfile1.split("_vs_")[1].replace(".txt","").replace("_all","")
	txtdata1 = np.loadtxt(txtfile1,dtype="str")
	txtdata2 = np.loadtxt(txtfile2,dtype="str")
	for j in range(len(txtdata1)):
		onerow_tmp = extract_onerow(txtdata1[j])
		onerow = "log " + dataname.replace("d","D").replace("w","WISE") + " & " + onerow_tmp + " \\\\ \n"
		table.append(onerow)

	onerow_tmp = extract_onerow(txtdata2[j])
	onerow = dataname + " & " + onerow_tmp + " \\\\ \n"
	table.append(onerow)

	return table

def extract_onerow(txtdata):
	"""
	"""
	l0 = txtdata[0]
	l1 = txtdata[1]
	l2 = txtdata[2]
	l3 = txtdata[3]
	l4 = txtdata[4]
	l5 = txtdata[5]
	l6 = txtdata[6]
	# l0
	t0 = l0.replace("ngc","NGC ").replace("a","A")
	# l1
	t1 = l1.zfill(4)

	onerow = t1+" & "+t2+" & "+t3+" & "+t4
	return onerow


#####################
### main
#####################
table04 = []
for i in [0,2,4,6]:
	#
	txtfile1 = txtfile[i]
	txtfile2 = txtfile[i+1]
	#
	table = table04_galname(txtfile1, txtfile2)
	table04.append(table)
	#os.system("rm -rf " + txtfile1[i] + " " + txtfile2[i])

np.savetxt("table04.txt",table04,fmt="%s")
