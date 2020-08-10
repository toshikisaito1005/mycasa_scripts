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

#for i in range(len(galnames)):
for i in [0]:
	result_table = Ned.query_region(galnames[i], radius=30 * u.arcsec)
	this_names = result_table["Object Name"]
	this_ngc = [s for s in this_names if "NGC" in s]
	this_eso = [s for s in this_names if "ESO" in s]
	this_ic = [s for s in this_names if "IC" in s]
	this_mcg = [s for s in this_names if "MCG" in s]
	this_iras = [s for s in this_names if "IRAS" in s]
	this_name = np.c_[this_ngc, this_eso, this_ic, this_mcg, this_iras]