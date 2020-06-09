import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)


dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/eps/"


done = glob.glob(dir_data + "../../eps/")
if not done:
    os.mkdir(dir_data + "../../eps/")


#####################
### Main Procedure
#####################
