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
galname2 = [s.replace("e","E").replace("w","W").replace("ic","IC ") for s in galname1]
galname3 = [s.replace("iras","IRAS ").replace("f","F").replace("g","-G") for s in galname2]
galname4 = [s.replace("319","319- G 022").replace("507","507- G 070") for s in galname3]
galname5 = [s.replace("557","557- G 002").replace("06592","06592-6313") for s in galname4]
galname6 = [s.replace("10409","10409-4556").replace("17138","17138-1017") for s in galname5]
galname = [s.replace("-02"," -02-33-098").replace("267","267- G 030") for s in galname6]

#
data = ascii.read(dir_data + "apjaaf21at1_mrt.txt")
nednames = data["Name"]


for i in range(len(nednames)):
# for i in [145]:
	result_table = Ned.query_region(galnames[i], radius=30 * u.arcsec)
	this_names = result_table["Object Name"]
	#
	this_name = []
	list_name = ["NGC","ESO","IC","MCG","IRAS"]
	for j in range(len(list_name)):
		name = [s for s in this_names if list_name[j] in s]
		name.sort(lambda x,y: cmp(len(x), len(y)))
		if len(name)>0:
			name = name[0]
			this_name.append(name)
	#
	if this_name:
		# print("# " + str(i) + " " + list_this_name)
		for j in range(len(this_name)):
			search_name = this_name[j]
			if search_name in galname:
				this_sfr = str(data["logSFR"][i])
				this_mstar = str(data["logMstar"][i])
				print("# " + search_name.rjust(15) + ", logSFR = " + this_sfr.ljust(4) + ", logMstar = " + this_mstar.ljust(4))

print("#     F06592-6313, logSFR = 1.31, logMstar = 10.66")
print("#     F10409-4556, logSFR = 1.41, logMstar = 11.15")
print("#     F17138-1017, logSFR = 1.58, logMstar = 10.72")

'eso297g011', 'eso297g012', 'ic4518e', 'ic4518w', 'ngc5257'
