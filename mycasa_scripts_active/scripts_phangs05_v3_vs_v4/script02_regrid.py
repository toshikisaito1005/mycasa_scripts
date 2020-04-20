import os, sys, glob


dir_data = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready/"
# v3 channel width = 2.54 km/s
# v4 channel width = 2.22 km/s
# v3 velocity width = 1914.68 ~ 1218.07 km/s (0~279)
# v3 velocity width = 1911.32 ~ 1217.90 km/s (0`312)
# v3 imsize = [255, 255,   0, 274]
# v4 imsize = [255, 255,   0, 312]

####################
### main
####################
done = glob.glob(dir_ready)
if not done:
	os.mkdir(dir_ready)

v3_image = glob.glob(dir_data + "ngc4303_7m_co21_v4.*")




os.system("rm -rf *.last")
