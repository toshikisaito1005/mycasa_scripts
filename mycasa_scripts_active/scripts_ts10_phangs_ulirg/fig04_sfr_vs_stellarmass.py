from astropy.io import ascii
from astropy.table import QTable
from astroquery.ned import Ned
import astropy.units as u


#####################
### Parameter
#####################
dir_data = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data_other/"
galaxy = ['eso297g011', 'eso297g012', 'ic4518e', 'ic4518w', 'eso319',
          'ngc2369', 'mcg02', 'ic5179', 'iras06592',
          'eso267', 'eso557', 'irasf10409', 'ngc5257', 'ngc3110', 'irasf17138',
          'eso507', 'ngc3256', 'ngc1614', 'ngc6240']

# data.info


#####################
### Main Procedure
#####################
#
galname1 = [s.replace("eso","ESO ").replace("ngc","NGC ").replace("mcg","MCG-") for s in galaxy]
galname2 = [s.replace("e","E").replace("w","W").replace("ic","IC") for s in galname1]
galname3 = [s.replace("iras","IRAS ").replace("f","F").replace("g","-G") for s in galname2]
galname4 = [s.replace("319","319-G022").replace("507","507-G070") for s in galname3]
galname5 = [s.replace("557","557-G002").replace("06592","06592-6313") for s in galname4]
galname6 = [s.replace("10409","10409-4556").replace("17138","17138-1017") for s in galname5]
galname = [s.replace("-02"," -02-33-098").replace("267","267-G030") for s in galname6]

#
data = ascii.read(dir_data + "apjaaf21at1_mrt.txt")
galnames = data["Name"]

#for i in range(len(galnames)):
for i in [1]:
	result_table = Ned.query_region(galnames[i], radius=30 * u.arcsec)
	this_names = result_table["Object Name"]
	#
	this_name = []
	for j in ["NGC","ESO","IC","MCG","IRAS"]:
		name = [s for s in this_names if "NGC" in s]
		name = name.sort(lambda x,y: cmp(len(x), len(y)))
	this_name = [s for s in this_names if "NGC" in s]
	this_name = this_name.sort(lambda x,y: cmp(len(x), len(y)))
	#
	this_eso.extend([s for s in this_names if "ESO" in s])
	#
	this_ic.extend([s for s in this_names if "IC" in s])
	#
	this_name.extend([s for s in this_names if "MCG" in s])
	#
	this_name.extend([s for s in this_names if "IRAS" in s])
	#
	this_name = [s for s in this_name if s != []]
	if this_name:
		print(this_name)


