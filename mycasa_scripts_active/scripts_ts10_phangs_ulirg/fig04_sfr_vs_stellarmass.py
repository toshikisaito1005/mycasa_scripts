from astropy.io import ascii
from astropy.table import QTable
from astroquery.ned import Ned
import astropy.units as u


#####################
### Parameter
#####################
dir_data = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data_other/"

# data.info


#####################
### Main Procedure
#####################
data = ascii.read(dir_data + "apjaaf21at1_mrt.txt")
galnames = data["Name"]

for i in range(len(galnames)):
	result_table = Ned.query_region(galnames[i], radius=30 * u.arcsec)
	print(result_table["Object Name"])