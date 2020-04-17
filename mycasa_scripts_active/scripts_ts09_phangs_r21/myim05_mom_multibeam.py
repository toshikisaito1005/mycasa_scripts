import os
import glob
import scripts_phangs_r21 as r21


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galaxy = ["ngc0628",
          "ngc4321",
          #"ngc4254",
          "ngc3627"]
co10noises = [[0.020,0.030,0.040,0.050,0.060,0.060,0.070,0.080,0.090,0.095,0.130], # ngc0628
              [0.020,0.028,0.028,0.035,0.040,0.045,0.050,0.055,0.060,0.060,0.060], # ngc4321
              #[0.030,0.036,0.040,0.045,0.050,0.050,0.055,0.060,0.066,0.080], # ngc4254
              [0.038,0.045,0.055,0.065,0.065,0.080,0.090,0.100,0.110,0.125,0.150]] # ngc3627
co21noises = [[0.025,0.030,0.035,0.037,0.060,0.060,0.039,0.040,0.042,0.043,0.055], # ngc0628
              [0.022,0.026,0.026,0.027,0.028,0.029,0.030,0.030,0.030,0.031,0.050], # ngc4321
              #[0.028,0.030,0.032,0.033,0.033,0.035,0.037,0.038,0.040,0.060], # ngc4254
              [0.023,0.025,0.027,0.027,0.027,0.028,0.029,0.030,0.031,0.033,0.040]] # ngc3627
"""
co10noises = [[0.020,0.130], # ngc0628
              [0.020,0.060], # ngc4321
              #[0.030,0.080], # ngc4254
              [0.038,0.150]] # ngc3627
co21noises = [[0.025,0.055], # ngc0628
              [0.022,0.050], # ngc4321
              #[0.028,0.060], # ngc4254
              [0.023,0.040]] # ngc3627
"""
snr_mom = 5.0 # 3.0
#percents = [0.15,0.010,0.025]
percents = [0.00,0.00,0.00]

#####################
### Main
#####################
for i in range(len(galaxy)):
    galname = galaxy[i]
    co10images = glob.glob(dir_proj + galname + "_*/co10*cube*p*.image")
    co10images.sort()
    co21images = glob.glob(dir_proj + galname + "_*/co21*cube*p*.image")
    co21images.sort()

    for j in range(len(co10images)):
        beamp = co10images[j].split("/")[-1].split("_")[-1].replace(".image","")
        # measure noise
        output = dir_proj+"eps/noise_"+galname+"_"+co10images[j].split("/")[-1].replace(".image","").replace("_cube","")+".png"
        co10rms = r21.noisehist(co10images[j],
                                 co10noises[i][j],
                                 output)
        output = dir_proj+"eps/noise_"+galname+"_"+co21images[j].split("/")[-1].replace(".image","").replace("_cube","")+".png"
        co21rms = r21.noisehist(co21images[j],
                                 co21noises[i][j],
                                 output)
            
        # moment map creation
        maskname = r21.eazy_immoments(dir_proj + galname + "_co21/",
                                      co21images[j],
                                      galname,
                                      co21rms,
                                      beamp,
                                      snr_mom,
                                      percents[i],
                                      myim="05")
                                 
        r21.eazy_immoments(dir_proj + galname + "_co10/",
                           co10images[j],
                           galname,
                           co10rms,
                           beamp,
                           snr_mom,
                           percents[i],
                           maskname=maskname,
                           myim="05")


os.system("rm -rf *.last")
