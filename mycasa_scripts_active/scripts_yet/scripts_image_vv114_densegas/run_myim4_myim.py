import glob



do_step = 11 # two/three-digit number
specific = "b"
unit = 0



#####################
### Parameter Setup
#####################
# moment map parameter
pixelmin = 5 # 5: increment for removing small masks
increment_mask = 2.0 # 3.0: beam (mask) = beam_size * increment_mask
thres_masking = 2.5 # 2.5: threshold s/n ratio for masking
thres_mom = 1.0 # 0.0: threshold s/n ratio for immoments
pbcut = 0.65 # 0.65: pirmary beam cut
sn_ratio = 3.0 # 3.0: threshold for sampling
#
dir_data = "/Users/saito/data/vv114_co43/"
galnames = ["ngc4321"]
ras = ["12h23m01.475s"] # blc
decls = ["+15d47m48.357s"] # blc
chanss = ["23~145"]
velress = [20.0]
fovs = [200]
aperturess_highest = [[3.5]]

#
res_highest = [3.5] # highest matched resolution
#


#####################
### Main Procedure
#####################
# define parameters
if [int(i) for i in str(do_step).zfill(3)][1] == 1:
    galname = galnames[unit]
    ra = ras[unit]
    decl = decls[unit]
    chans = chanss[unit]
    velres = velress[unit]
    fov = fovs[unit]
    suffix = str(res_highest[unit]).replace(".","p") # myim**1
    beam_size = res_highest[unit] # myim**1
    beam_halpha = res_halpha[unit] # myim**2
    rms_co10 = rms_co10_highs[unit] # myim**1, myim**3
    rms_co21 = rms_co21_highs[unit] # myim**1, myim**3
    rms_co10_halpha = rms_co10_halphas[unit] # myim**2
    rms_co21_halpha = rms_co21_halphas[unit] # myim**2
    apertures = aperturess_highest[unit]
    apertures_halpha = aperturess_halpha[unit]
    apertures_wise7p5 = aperturess_wise7p5[unit]
    rms_w1_7p5 = rms_w1_7p5s[unit]
    rms_w2_7p5 = rms_w2_7p5s[unit]
    rms_w3_7p5 = rms_w3_7p5s[unit]
    rms_w1_15p = rms_w1_15ps[unit]
    rms_w2_15p = rms_w2_15ps[unit]
    rms_w3_15p = rms_w3_15ps[unit]
    n_ch = int(chanss[unit].split("~")[1]) - int(chanss[unit].split("~")[0]) + 1
    threesigma_co10 = rms_co10*velres*sqrt(n_ch)*4.
    threesigma_co21 = rms_co21*velres*sqrt(n_ch)*4.
    threesigma8_co10 = rms_co10*4.
    threesigma8_co21 = rms_co21*4.
    aperture_310pc = aperturess_310pc[unit]
    aperture_650pc = aperturess_650pc[unit]
    aperture_1000pc = aperturess_1000pc[unit]

    print("###################################")
    print("##### your parameters")
    print("###################################")
    print("# galname = " + galname)
    print("# ra = " + ra)
    print("# decl = " + decl)
    print("# chans = " + chans)
    print("# velres " + str(velres) + " km/s")
    print("# fov = " + str(fov) + " arcsec")
    print("# suffix = " + suffix)
    print("# beam_size = " + str(beam_size) + " arcsec")
    print("# beam_halpha = " + str(beam_halpha) + " arcsec")
    print("# rms_co10 = " + str(rms_co10) + " Jy")
    print("# rms_co21 = " + str(rms_co21) + " Jy")
    print("# rms_co10_halpha = " + str(rms_co10_halpha) + " Jy")
    print("# rms_co21_halpha = " + str(rms_co21_halpha) + " Jy")
    print("# apertures = " + str(apertures))
    print("# apertures_halpha = " + str(apertures_halpha))
    print("# rms_w1_7p5 = " + str(rms_w1_7p5))
    print("# rms_w2_7p5 = " + str(rms_w2_7p5))
    print("# rms_w3_7p5 = " + str(rms_w3_7p5))
    print("# rms_w1_15p = " + str(rms_w1_15p))
    print("# rms_w2_15p = " + str(rms_w2_15p))
    print("# rms_w3_15p = " + str(rms_w3_15p))
    print("")



# run myim scripts
scripts = glob.glob("myim"+str(do_step).zfill(3)+specific+"*.py")

for i in range(len(scripts)):
    print("###################################")
    print("##### run " + scripts[i])
    print("###################################")
    execfile(scripts[i])
