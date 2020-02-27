import os

execfile("myim03_mom_native.py")
execfile("myim04_multibeam.py")
execfile("myim05_mom_multibeam.py")
execfile("myim06_r21_map.py")
execfile("myim07_sd_mom.py")
execfile("myim08_r21_highlowmask.py")
execfile("myim09_convolve_wise.py")
execfile("myim10_extract_param_600pc.py")

os.system("rm -rf tempalte.image")
os.system("rm -rf *.last")
