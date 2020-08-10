from astropy.io import ascii
from astropy.table import QTable
from astroquery.ned import Ned


#####################
### Parameter
#####################
dir_data = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data_other/"

# data.info


#####################
### Main Procedure
#####################
data = ascii.read(dir_data + "apjaaf21at1_mrt.txt")
print(data["Name"])
