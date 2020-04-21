import os, sys, glob
import shutil
import matplotlib.pyplot as plt
plt.ioff()


dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_product = "/Users/saito/data/phangs/compare_v3p4_v4/product/"
casalog_v3 = ""
casalog_v4 = ""
v3_output = dir_product + "ngc4303_v3_tcleancall.txt"
v4_output = dir_product + "ngc4303_v4_tcleancall.txt"


####################
### main
####################
# mkdir
done = glob.glob(dir_product)
if not done:
	os.mkdir(dir_product)


# read v3 CASA log
with open(casalog_v3) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]
v3_tcleanlog = np.array([line for line in lines_strip if "tclean(" in line])
os.system("rm -rf " + v3_output)
np.savetxt(v3_output, v3_tcleanlog)


# read v4 CASA log
with open(casalog_v4) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]
v4_tcleanlog = np.array([line for line in lines_strip if "tclean(" in line])
os.system("rm -rf " + v4_output)
np.savetxt(v4_output, v4_tcleanlog)


"""
### script04_imhistory.py
### did not work because of no histories in the header.


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
"""

os.system("rm -rf *.last")
