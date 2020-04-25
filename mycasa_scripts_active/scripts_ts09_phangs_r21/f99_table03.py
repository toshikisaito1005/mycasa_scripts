import os, sys, glob
import numpy as np


#####################
### parameters
#####################
txtfile1 = glob.glob("table03_*_co10vsco21.txt")
txtfile2 = glob.glob("table03_*_co21vsr21.txt")


#####################
### functions
#####################
def table03_galname(galname,txtfile1,txtfile2):
	"""
	"""
	table = []
	for i in range(len(txtfile1)):
		txtdata1 = np.loadtxt(txtfile1[i],dtype="str")
		txtdata2 = np.loadtxt(txtfile2[i],dtype="str")
		for j in range(len(txtdata1)):
			onerow_tmp = extract_onerow(txtdata1[j],txtdata2[j])
			if j==0:
				onerow = galname + " & " + onerow_tmp
			else:
				onerow = " & " + onerow_tmp
			table.append(onerow)

	return table

def extract_onerow(txtdata1,txtdata2):
	"""
	"""
	l1  = txtdata1[0].replace("00","0")
	l2  = txtdata1[1]
	l3a = txtdata1[2]
	l3b = txtdata1[3]
	l4a = txtdata1[4]
	l4b = txtdata1[5]
	l5  = txtdata2[1]
	l6a = txtdata2[2]
	l6b = txtdata2[3]
	l7a = txtdata2[4]
	l7b = txtdata2[5]
	# l1
	if len(l1)==3:
		t1 = "\phantom{0}" + l1
	else:
		t1 = l1
	# l2
	t2 = l2
	# l3
	t3 = l3a + " \pm " + l3b
	# l4
	if "-" in l4a:
		t4 = l4a.replace("-","$-$") + " \pm " + l4b
	else:
		t4 = "\phantom{$-$}" + l4a + " \pm " + l4b
	# l5
	if "-" in l5:
		t5 = l5.replace("-","$-$")
	else:
		t5 = "\phantom{$-$}" + l5
	# l6
	if "-" in l6a:
		t6 = l6a.replace("-","$-$") + " \pm " + l6b
	else:
		t6 = "\phantom{$-$}" + l6a + " \pm " + l6b
	# l7
	if "-" in l7a:
		t7 = l7a.replace("-","$-$") + " \pm " + l7b
	else:
		t7 = "\phantom{$-$}" + l7a + " \pm " + l7b

	onerow = t1+" & "+t2+" & "+t3+" & "+t4+" && "+t5+" & "+t6+" & "+t7
	return onerow


#####################
### main
#####################
table03 = []
for i in range(len(txtfile1)):
	galname = txtfile1[i].split("_")[1].replace("ngc","NGC ")
	table = table03_galname(galname, txtfile1, txtfile2)
	table03.append(table)
