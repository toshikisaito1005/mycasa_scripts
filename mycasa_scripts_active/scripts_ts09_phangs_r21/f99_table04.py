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
		onerow = dataname + " & " + onerow_tmp + " \\\\ \n"
		table.append(onerow)

	return table

def extract_onerow(txtdata):
	"""
	"""
	l1  = txtdata[0].replace("00","0")
	l2a = txtdata[1]
	l2b = txtdata[2]
	l3a = txtdata[3]
	l3b = txtdata[4]
	l4a = txtdata[5]
	l4b = txtdata[6]
	# l1
	if len(l1)==3:
		t1 = "\phantom{0}" + l1
	else:
		t1 = l1
	# l2
	if l2b=="0.00":
		t2 = l2a + " ($<$0.001)"
	else:
		t2 = l2a + " (" + l2b + ")"
	# l3
	t3 = l3a + " $\pm$ " + l3b
	# l4
	if "-" in l4a:
		t4 = l4a.replace("-","$-$") + " $\pm$ " + l4b
	else:
		t4 = "\phantom{$-$}" + l4a + " $\pm$ " + l4b

	onerow = t1+" & "+t2+" & "+t3+" & "+t4+" && "+t5+" & "+t6+" & "+t7
	return onerow


#####################
### main
#####################
table04 = []
for i in range(len(txtfile)):
	#
	txtfile1 = txtfile[i]
	txtfile2 = txtfile[i+1]
	#
	table = table04_galname(txtfile1, txtfile2)
	table04.append(table)
	#os.system("rm -rf " + txtfile1[i] + " " + txtfile2[i])

np.savetxt("table04.txt",table04,fmt="%s")
