import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()


dir_data = "/Users/saito/data/myproj_published/proj_phangs02_feather/products/"
box = "155,390,875,640" # around three sourcess
#box = "198,418,400,620" # leftmost source

done = glob.glob(dir_data + "../figures/")
if not done:
    os.mkdir(dir_data + "../figures/")


#####################
### Main Procedure
#####################
data_cl = [s for s in glob.glob(dir_data + "test0607*diff*clip") if not re.search(".fits", s)]
data_cl = [data_cl[0],data_cl[1],data_cl[3],data_cl[2]]
data_all = [s.replace(".clip","") for s in data_cl]
data_all_name = [s.split("/")[-1].replace("test0607_","").replace(".diff.image","").ljust(23," ") for s in data_all]

medians_all, sums_all, noises_all = [], [], []
for i in range(len(data_all)):
    medians_all.append(str(np.round(imstat(data_all[i],box=box)["median"][0],6)).rjust(9," "))
    sums_all.append(str(np.round(imstat(data_all[i],box=box)["sum"][0]/44.2613,3)).rjust(6," "))
    noises_all.append(str(np.round(imstat(data_all[i],box=box)["rms"][0],5)).rjust(7," "))

output = np.c_[data_all_name,medians_all,sums_all,noises_all]
os.system("rm -rf " + "statistics.txt")
header="imagename".ljust(22," ")+"median".rjust(9," ")+"sum".rjust(7," ")+"rms".rjust(8," ")
np.savetxt("statistics.txt",output,fmt="%s",header=header)

os.system("rm -rf *.last")

# plot
plt.figure(figsize=(10,5))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(left=0.3,right=0.95,bottom = 0.15)
labels = output[:,0][::-1]
heights = output[:,2].astype("float64")[::-1]
width = 0.5

left = np.arange(len(heights))
plt.barh(left + width/2,
         heights,
         color='b',
         height=width,
         align="center",
         alpha = 0.4)

plt.yticks(left + width/2, labels)
plt.grid(which="major")
plt.grid(which="minor")
plt.ylim([-0.5,4.0])
plt.plot([0,0],[-0.5,4.0],"k-")
#plt.title("Flux Difference around the Easternmost Source")
plt.title("Flux Difference")
plt.xlabel("Flux in Difference Map (Jy)")
os.system("rm -rf " + dir_data + "../figures/stats.png")
plt.savefig(dir_data + "../figures/fig08.png", dpi=100)
