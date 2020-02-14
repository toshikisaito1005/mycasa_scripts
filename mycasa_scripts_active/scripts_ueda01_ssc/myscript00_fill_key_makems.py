import os
import sys
import glob
import numpy as np
sys.path.append(os.getcwd())
import toolsJu01Ssc as tl


##############################
### parameter setup
##############################
dir_data = "/Users/saito/data/myproj_published/proj_ju01_ssc/data_raw/" # laptop
#dir_data = "../data_raw/" # astro-node7


##############################
### main
##############################
dir_product = dir_data + "../products/"
done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)

# import keys
key_rawdata_tmp = np.loadtxt("key_rawdata.txt",dtype="S100")
key_rawdata = []
key_galname = []
key_array = []
for i in range(len(key_rawdata_tmp)):
    if ".ms" in key_rawdata_tmp[:,2][i]:
        key_rawdata.append(key_rawdata_tmp[:,2][i])
        key_galname.append(key_rawdata_tmp[:,0][i])
        key_array.append(key_rawdata_tmp[:,1][i])

# plotms to identify strong line(s)
for i in range(len(key_rawdata)):
    vis = dir_data + key_rawdata[i]
    done = glob.glob(vis)
    number = str(i+1) + "/" + str(len(key_rawdata))
    if not done:
        print("# skip "+key_galname[i]+" "+key_array[i]+" ms: " + number)
    else:
        print("# working on "+key_galname[i]+" "+key_array[i]+" ms: " + number)
        spw_co10 = str(tl.find_spw_co10(vis))
        prefix = dir_product + key_galname[i] + "_spw" + spw_co10 + "_" + key_array[i]
        # 12m plotms
        plotfile = prefix + "_amp_vs_chan_" + key_rawdata[i] + ".png"
        tl.eazy_plotms(vis,spw_co10,plotfile,"chan")
        plotfile = prefix + "_amp_vs_freq_" + key_rawdata[i] + ".png"
        tl.eazy_plotms(vis,spw_co10,plotfile,"freq")

os.system("rm -rf *.last")
