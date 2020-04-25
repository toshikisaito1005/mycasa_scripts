import os, sys, glob
import numpy as np


#####################
### parameters
#####################
data_co10vsco21 = np.loadtxt("table03_ngc0628_co10vsco21.txt",dtype="str")
data_co21vsr21 = np.loadtxt("table03_ngc0628_co21vsr21.txt",dtype="str")



#####################
### functions
#####################
def table03_builder():
	"""
	"""
	l1  = [s.replace("00","0") for s in txtdata1[:,0]]
	l2  = txtdata1[:,1]
	l3a = txtdata1[:,2]
	l3b = txtdata1[:,3]
	l4a = txtdata1[:,4]
	l4b = txtdata1[:,5]
	l5  = txtdata2[:,1]
	l6a = txtdata2[:,2]
	l6b = txtdata2[:,3]
	l7a = txtdata2[:,4]
	l7b = txtdata2[:,5]

	for i in range(len(l1)):
		# l1
		if len(l1[i])==3:
			t1 = "\phantom{0}" + l1[i]
		else:
			t1 = l1[i]
		# l2
		t2 = l2[i]
		# l3
		t3 = l3a[i] + " \pm " + l3b[i]
		# l4
		if "-" in l4a[i]:
			t4 = l4a[i].replace("-","$-$") + " \pm " + l4b[i]
		else:
			t4 = "\phantom{$-$}" + l4a[i] + " \pm " + l4b[i]
		# l5
		if "-" in l5[i]:
			t5 = l5[i].replace("-","$-$")
		else:
			t5 = "\phantom{$-$}" + l5[i]
		# l6
		if "-" in l6a[i]:
			t6 = l6a[i].replace("-","$-$") + " \pm " + l6b[i]
		else:
			t6 = "\phantom{$-$}" + l6a[i] + " \pm " + l6b[i]
		# l7
		if "-" in l7a[i]:
			t7 = l7a[i].replace("-","$-$") + " \pm " + l7b[i]
		else:
			t7 = "\phantom{$-$}" + l7a[i] + " \pm " + l7b[i]

		onerow = t1+" & "+t2+" & "+t3+" & "+t4+" && "+t5+" & "+t6+" & "+t7


