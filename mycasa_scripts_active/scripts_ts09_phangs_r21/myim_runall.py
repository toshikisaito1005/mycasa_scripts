import os

#execfile("myim01_prep.py")
#execfile("myim02_regrid.py")
execfile("myim03a_mom_native.py")
execfile("myim03b_Jy2Kelvin.py")
execfile("myim04_multibeam.py")
execfile("myim05_mom_multibeam.py")
execfile("myim06_r21_map.py")
execfile("myim07_sd_mom.py")
beam = [4.0, 8.0, 4.0]
execfile("myim08_r21_highlowmask.py")
beam = [13.6, 15.0, 8.5]
execfile("myim08_r21_highlowmask.py")
execfile("myim09_convolve_wise.py")
execfile("myim10_extract_param_600pc.py")

os.system("rm -rf tempalte.image")
os.system("rm -rf *.last")
