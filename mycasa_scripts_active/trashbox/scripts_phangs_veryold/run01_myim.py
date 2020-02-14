import glob



#do_step = 11 # two/three-digit number
#specific = ""
#unit = 0 # 0=n4321, 1=n0628, 2=3627, 3=4254, 4=3351, 5=3110

# done: 11-0

### do_step
# 11: best matched resolution
# 12: 400 pc resolution (galmask resolution)
# 13: 7".5 and 15". resolution (wise data)
# 14: 310 pc resolution
# 2*: plotter

### unit
# 0: n4321(123) 74 pc/", co10=3".9, co21=1".47, 400pc=5".43, 27.0dgr
# 1: n0628(123) 44 pc/", co10=3".5, co21=1".50, 400pc=8".45, 06.5dgr
# 2: n3627(123) 40 pc/", co10=8".0, co21=1".35, 400pc=9".96, 62.0dgr
# 3: n4254(1 3) 81 pc/", co10=8".0, co21=1".57, 400pc=4".91, 27.0dgr
# 4: n3351(1 3) 48 pc/", co10=8".0, co21=1".32, 400pc=8".25, 41.0dgr
# 5: n3110(1  ) 325pc/", co10=1".85,co21=1".85



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
dir_data = "/Users/saito/data/phangs/co_ratio/"
galnames = ["ngc4321",
            "ngc0628",
            "ngc3627",
            "ngc4254",
            "ngc3351",
            "ngc3110"]
ras = ["12h23m01.475s",
       "01h36m50.640s",
       "11h20m19.962s",
       "12h18m57.195s",
       "10h44m00.876s",
       "10h04m04.005s"] # blc
decls = ["+15d47m48.357s",
         "+15d44m57.201s",
         "+12d57m04.073s",
         "+14d23m34.840s",
         "+11d41m31.868s",
         "-06d28m59.025s"] # blc
chanss = ["23~145", "9~61", "25~242", "53~165", "17~179", "14~41"]
velress = [2.5, 2.0, 2.5, 2.5, 2.5, 20]
fovs = [200, 250, 140, 186, 100, 55]
#aperturess_highest = [[4,6,8,10,12,14,16,18,20,22,24,26,28,30,32],
#                      [4,6,8,10,12,14,16,18,20,22,24,26,28,30,32],
#                      [8,10,12,14,16,18,20,22,24,26,28,30,32,34,36],
#                      [8,10,12,14,16,18,20,22,24,26,28,30,32,34,36],
#                      [8,10,12,14],
#                      [2,3,4,5,6,7]]
aperturess_halpha = [[4,6,8,10,12,14,16,18,20],
                     [9,10,12,14,16,18,20,22,24,26,28,30],
                     [10,12,14,16,18,20,22,24,26,28,30],
                     -1,
                     -1,
                     -1]
#
#res_highest = [4.0, 4.0, 8.0, 8.0, 8.0, 2.0] # highest matched resolution
res_halpha = [5.428, 9.0, 10.0, -1, -1, -1] # 400 pc in arcsec
aperturess_wise7p5 = [7.5, 7.5, 8.0, 8.0, 7.5, -1] # 7.5 or res_highest
#
rms_co10_highs = [0.011, 0.010, 0.03, 0.035, 0.075, 0.0011]
rms_co10_halphas = [0.015, 0.030, 0.04, -1, -1, -1]
#
rms_co21_highs = [0.018, 0.014, 0.03, 0.070, 0.110, 0.0011]
rms_co21_halphas = [0.025, 0.080, 0.04, -1, -1, -1]
#
rms_w1_7p5s = [0,0,0,0,0,0]#[0.056, 0.370, 0.230, 0.167, 0, 0]
rms_w1_15ps = [0,0,0,0,0,0]#[0.031, 0.180, 0.110, 0.082, 0, 0]
rms_w2_7p5s = [0,0,0,0,0,0]#[0.033, 0.200, 0.120, 0.089, 0, 0]
rms_w2_15ps = [0,0,0,0,0,0]#[0.018, 0.097, 0.063, 0.044, 0, 0]
rms_w3_7p5s = [0,0,0,0,0,0]#[0.094, 0.088, 0.100, 0.101, 0, 0]
rms_w3_15ps = [0,0,0,0,0,0]#[0.033, 0.029, 0.032, 0.029, 0, 0]
#
aperturess_310pc = [[4.4], [7.3], [8.0], [-1], [-1], [-1]]
aperturess_650pc = [[8.8], [14.8], [16.3], [8.0], [-1], [-1]]
aperturess_1000pc = [[13.6], [22.7], [25.0], [12.3], [-1], [-1]]


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
