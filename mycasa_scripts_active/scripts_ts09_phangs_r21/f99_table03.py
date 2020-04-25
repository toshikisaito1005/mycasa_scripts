import os, sys, glob
import numpy as np

data_co21vsco21 = np.loadtxt("table03_ngc0628_co10vsco21.txt",dtype="str")

l1 = [s.replace("00","0") for s in data_co21vsco21[:,0]]
l2 = data_co21vsco21[:,1]
l3a = data_co21vsco21[:,2]
l3b = data_co21vsco21[:,3]
l4a = data_co21vsco21[:,4]