import os, sys, glob
import numpy as np

data_co10vsco21 = np.loadtxt("table03_ngc0628_co10vsco21.txt",dtype="str")
data_co21vsr21 = np.loadtxt("table03_ngc0628_co21vsr21.txt",dtype="str")

l1  = [s.replace("00","0") for s in data_co10vsco21[:,0]]
l2  = data_co10vsco21[:,1]
l3a = data_co10vsco21[:,2]
l3b = data_co10vsco21[:,3]
l4a = data_co10vsco21[:,4]
l4b = data_co10vsco21[:,5]
l5  = data_co21vsr21[:,1]
l6a = data_co21vsr21[:,2]
l6b = data_co21vsr21[:,3]
l7a = data_co21vsr21[:,4]
l7b = data_co21vsr21[:,5]

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
	if l5[i]:
		t1 = "\phantom{0}" + l1[i]
	else:
		t1 = l1[i]

	print(t1 + " & " + t2 + " & " + t3 + " & " + t4)
