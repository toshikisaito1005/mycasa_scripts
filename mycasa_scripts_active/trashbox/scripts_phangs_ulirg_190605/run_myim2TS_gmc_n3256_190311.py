import glob



unit = 0 # 3 = wrong pb cut?

# 0: non-detection (increment_mask=5.0)
# 1: done (thres_masking=3.5)
# 2: done (pbcut=0.75)
# 3: done (increment_mask=4.0,thres_mom=0.7,pbcut=0.85)
# 4: done (thres_masking=4.5)
# 5: done (thres_masking=5.5)
# 6: done (thres_masking=3.5,pbcut=0.75)
# 7: done (increment_mask=2.0,thres_masking=8.0)



#####################
### Parameter Setup
#####################
# moment map parameter
pixelmin = 30 # 5: increment for removing small masks
increment_mask = 3.0 # 3.0: beam (mask) = beam_size * increment_mask
thres_masking = -30.0 # 2.5: threshold s/n ratio for masking
thres_mom = -30.0 # 1.0: threshold s/n ratio for immoments
pbcut = 0.65 # 0.65: pirmary beam cut
#
dir_data = "/Users/saito/data/ngc3256/"
galnames = ["ngc3256"]
res_highest = [0.22]
chanss = [""]
rms_co32_highs = [0.00035]


#####################
### Main Procedure
#####################
do_step = 11 # two/three-digit number
specific = "a"
# define parameters
if [int(i) for i in str(do_step).zfill(3)][1] == 1:
    galname = galnames[unit]
    chans = chanss[unit]
    rms_co21 = rms_co32_highs[unit] # myim**1
    beam_size = res_highest[unit] # myim**1
    suffix = str(res_highest[unit]).replace(".","p") # myim**1
    print("galname = " + galname)


# run myim scripts
scripts = glob.glob("myim"+str(do_step).zfill(3)+specific+"*.py")

for i in range(len(scripts)):
    print("###################################")
    print("##### run " + scripts[i])
    print("###################################")
    execfile(scripts[i])


