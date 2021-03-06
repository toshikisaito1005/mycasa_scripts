import os


snr_mom = 2.5
nchans = [2.0,3.0,3.0] # ngc0628, ngc3627, ngc4321


"""
print("### running myim01 and myim02")
execfile("myim01_prep.py")
execfile("myim02a_regrid.py")
execfile("myim02b_pbmasking.py")
"""

"""
print("### running myim03")
execfile("myim03a_mom_native.py")
execfile("myim03b_Jy2Kelvin.py")

print("### running myim04")
execfile("myim04_multibeam.py")

print("### running myim05")
execfile("myim05_mom_multibeam.py")

print("### running myim06")
execfile("myim06_r21_map.py")

print("### running myim07")
execfile("myim07_sd_mom.py")

print("### running myim08")
beam = [4.0, 8.0, 4.0]
execfile("myim08_r21_highlowmask.py")
beam = [13.6, 15.0, 8.5]
execfile("myim08_r21_highlowmask.py")

print("### running myim09")
execfile("myim09_convolve_wise.py")

print("### running myim10")
execfile("myim10_extract_param_600pc.py")

print("### running myim11")
execfile("myim11_extract_param_best.py")
"""

print("### running f01")
execfile("f01a_noise.py")
execfile("f01b_flux_growthcurve.py")

print("### running f02")
execfile("f02_images.py")

print("### running f03")
execfile("f03_peak_vs_integ.py")

print("### running f04")
execfile("f04_histograms_600pc.py")

print("### running f05")
execfile("f05_histo_stats.py")

print("### running f06")
execfile("f06_histall.py")

print("### running f07_08")
execfile("f07_08_scatter_and_histo.py")

print("### running f09")
execfile("f09_violins.py")

print("### running f10")
execfile("f10a_r21_highlowmask.py")
execfile("f10b_histo.py")

print("### running f11")
execfile("f11_maskhist.py")

print("### running f12")
execfile("f12_r21_vs_param.py")

print("### tabulate")
execfile("ftable02.py")
execfile("ftable03.py")
execfile("ftable04.py")


print("### cleanup")
os.system("rm -rf tempalte.image")
os.system("rm -rf *.last")
