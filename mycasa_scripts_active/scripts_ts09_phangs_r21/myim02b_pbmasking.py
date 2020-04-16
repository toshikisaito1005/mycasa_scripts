import os
import glob
import numpy as np
import scripts_phangs_r21 as r21


dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_ready/"


#####################
### Main Procedure
#####################
images = glob.glob(dir_data + "ngc*.image")
pbmasks = glob.glob(dir_data + "ngc*.pbmask")
