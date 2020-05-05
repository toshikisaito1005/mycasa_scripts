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

def extract_onerow(txtdata1,txtdata2):
	"""
	"""
	l1  = txtdata1[0].replace("00","0")
	l2a = txtdata1[1]
	l2b = txtdata1[2]
	l3a = txtdata1[3]
	l3b = txtdata1[4]
	l4a = txtdata1[5]
	l4b = txtdata1[6]
	l5a = txtdata2[1]
	l5b = txtdata2[2]
	l6a = txtdata2[3]
	l6b = txtdata2[4]
	l7a = txtdata2[5]
	l7b = txtdata2[6]
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
	# l5
	if "-" in l5a:
		if l5b=="0.00":
			t5 = l5a.replace("-","$-$") + " ($<$0.001)"
		else:
			t5 = l5a.replace("-","$-$") + " (" + l5b + ")"
	else:
		if l5b=="0.00":
			t5 = "\phantom{$-$}" + l5a + " ($<$0.001)"
		else:
			t5 = "\phantom{$-$}" + l5a + " (" + l5b + ")"
	# l6
	if "-" in l6a:
		t6 = l6a.replace("-","$-$") + " $\pm$ " + l6b
	else:
		t6 = "\phantom{$-$}" + l6a + " $\pm$ " + l6b
	# l7
	if "-" in l7a:
		t7 = l7a.replace("-","$-$") + " $\pm$ " + l7b
	else:
		t7 = "\phantom{$-$}" + l7a + " $\pm$ " + l7b

	onerow = t1+" & "+t2+" & "+t3+" & "+t4+" && "+t5+" & "+t6+" & "+t7
	return onerow


#####################
### main
#####################
table03 = []
for i in range(len(txtfile1)):
	galname = txtfile1[i].split("_")[1].replace("ngc","NGC ")
	galname2 = txtfile1[i].split("_")[1]
	table = table03_galname(galname, txtfile1[i], txtfile2[i])
	table03.append(table)
	#os.system("rm -rf " + txtfile1[i] + " " + txtfile2[i])

np.savetxt("table03.txt",table03,fmt="%s")
