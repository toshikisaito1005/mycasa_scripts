import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ioff()


#####
dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/"
dir_gals = glob.glob(dir_data + "sim_*/")
dir_gals.sort()


for i in range(len(dir_gals)):
    imagenames = glob.glob(dir_gals[i] + "*_br.smooth")
    skymodel = glob.glob(dir_gals[i] + "*_skymodel_regrid.smooth")[0]
    for j in range(len(imagenames)):
        outfile = imagenames[j].replace(".smooth",".fidelity")
        os.system("rm -rf " + outfile)
        print("# processing " + outfile.split("/")[-1])
        immath(imagename=[imagenames[j],skymodel], expr="abs(IM1)/abs(IM1-IM0)", outfile=outfile)
