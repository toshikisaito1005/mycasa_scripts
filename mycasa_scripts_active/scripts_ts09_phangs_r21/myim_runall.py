import os

#execfile("myim01_prep.py")
#execfile("myim02a_regrid.py")
#execfile("myim02b_pbmasking.py")
#execfile("myim03a_mom_native.py")
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
execfile("myim11_extract_param_best.py")

execfile("f01a_noise.py")
execfile("f01b_missingflux.py")
execfile("f02_images.py")
execfile("f03_peak_vs_integ.py")
execfile("f04_histograms_600pc.py")
execfile("f05_histo_stats.py")
execfile("f06_07_scatter_and_histo.py")
execfile("f08_violins.py")

os.system("rm -rf tempalte.image")
os.system("rm -rf *.last")
