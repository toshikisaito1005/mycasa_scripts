import os, sys, glob
import shutil
import matplotlib.pyplot as plt
plt.ioff()

dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_product = "/Users/saito/data/phangs/compare_v3p4_v4/product/"
galname = "ngc4303"


####################
### main
####################
# mkdir
done = glob.glob(dir_product)
if not done:
	os.mkdir(dir_product)


# get v4 CASA files
v3image = dir_ready + "ngc4303_7m_co21_v3.image"
v4image = dir_ready + "ngc4303_7m_co21_v4.image"


# imhistory v3
print("### imhistory v3")
v3history = imhistory(v3image, mode="list", verbose=False)
output = dir_product + "ngc4303_7m_co21_v3_imhistory.txt"
np.savetxt(output, v3history)


# imhistory v4
print("### imhistory v4")
v4history = imhistory(v4image, mode="list", verbose=False)
output = dir_product + "ngc4303_7m_co21_v4_imhistory.txt"
np.savetxt(output, v4history)

os.system("rm -rf *.last")
