import os, sys, glob
import numpy as np

dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready_bias_cycf/"

imagenames = glob.glob(dir_ready + "ngc4303_7m_co21_*.image")

for i in range(len(imagenames)):
    header = imhead(imagenames[i], mode="list")
    print(imagenames[i].split("/")[-1])
    print("# bmaj = "+str(np.round(header["beammajor"]["value"],2)))
    print("# bmin = "+str(np.round(header["beamminor"]["value"],2)))
