import os
import glob
import scripts_phangs_r21 as r21
reload(r21)


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_ready/"
co10names = glob.glob(dir_proj + "ngc*co10*.image")
co10names.sort()
co21names = glob.glob(dir_proj + "ngc*co21*.image")
co21names.sort()
noises_co10_byeye = [0.010, # ngc0628
                     0.030, # ngc3627
                     #0.025, # ngc4254
                     0.012] # ngc4321
noises_co21_byeye = [0.020, # ngc0628
                     0.020, # ngc3627
                     #0.025, # ngc4254
                     0.012] # ngc4321
beams = ["04p0",
         "08p0",
         #"08p0",
         "04p0"]
#snr_mom = 3.0
percents = [0,0,0]

done = glob.glob(dir_proj + "../eps/")
if not done:
    os.mkdir(dir_proj + "../eps/")


#####################
### Main
#####################
for i in range(len(co21names)):
    galname = co21names[i].split("/")[-1].split("_")[0]
    print("### working on " + galname)
    co10image = co10names[i]
    co21image = co21names[i]

    # measure noise
    output = dir_proj+"../eps/noise_"+co21names[i].split("/")[-1].replace(".image","")+".png"
    co21rms = r21.noisehist(co21image,noises_co21_byeye[i],output,snr_mom)
    
    output = dir_proj+"../eps/noise_"+co10names[i].split("/")[-1].replace(".image","")+".png"
    co10rms = r21.noisehist(co10image,noises_co10_byeye[i],output,snr_mom)

    # moment map creation
    maskname = r21.eazy_immoments(dir_proj,co21image,galname,co21rms,beams[i],snr_mom,percents[i])
    r21.eazy_immoments(dir_proj,co10image,galname,co10rms,beams[i],snr_mom,percents[i],maskname=maskname)


os.system("rm -rf *.last")
