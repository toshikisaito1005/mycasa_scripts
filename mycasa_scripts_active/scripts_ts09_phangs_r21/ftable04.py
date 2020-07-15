import os, sys, glob
import numpy as np


#####################
### parameters
#####################
txtfile = glob.glob("fig_r21_vs_dist*.txt")
txtfile.extend(glob.glob("fig_r21_vs_disp*.txt"))


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
		if j==0:
			onerow = "log " + dataname.replace("d","D").replace("w","W") + " vs. log $R_{21}$ & " + onerow_tmp + " \\\\ \n"
		else:
			onerow = " & " + onerow_tmp + " \\\\ \n"
		table.append(onerow)

	onerow_tmp = extract_onerow(txtdata2[j])
	onerow = " & " + onerow_tmp + " \\\\ \n"
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
	# t0
	t0 = l0.replace("ngc","NGC ").replace("a","A")
	# t1
	if not str(np.round(float(l2),2)).ljust(4,"0")=="0.00":
		if float(l1)<0:
			t1 = "$-$" + l1.replace("-","").ljust(4,"0") + " (" + str(np.round(float(l2),2)).ljust(4,"0") + ")"
		else:
			t1 = "\phantom{$-$}" + l1.ljust(4,"0") + " (" + str(np.round(float(l2),2)).ljust(4,"0") + ")"
	else:
		if float(l1)<0:
			t1 = "$-$" + l1.replace("-","").ljust(4,"0") + " ($<$0.001)"
		else:
			t1 = "\phantom{$-$}" + l1.replace("-","").ljust(4,"0") + " ($<$0.001)"
	# t2
	if float(l3)<0:
		t2 = l3.replace("-","$-$") + " $\pm$ " + l4
	else:
		t2 = "\phantom{$-$}" + l3.replace("-","$-$") + " $\pm$ " + l4
	# t3
	t3 = l5.replace("-","").ljust(4,"0") + " $\pm$ " + l6.ljust(4,"0")

	onerow = t0+" & "+t1+" & "+t2+" & "+t3
	return onerow


#####################
### main
#####################
table04 = []
for i in [0,2,4,6,8]:
	#
	txtfile1 = txtfile[i]
	txtfile2 = txtfile[i+1]
	#
	table = table04_galname(txtfile1, txtfile2)
	table04.append(table)
	os.system("rm -rf " + txtfile1 + " " + txtfile2)

np.savetxt("table04.txt",table04,fmt="%s")
