import os
import glob
import scripts_phangs_r21 as r21


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_ready/"
imagenames = glob.glob(dir_proj + "ngc*co*.image")
imagenames.sort()
noises_byeye = [0.010,0.020, # ngc0628
                0.030,0.020, # ngc3627
                0.025,0.025, # ngc4254
                0.012,0.012] # ngc4321
beams = ["04p0","04p0",
         "08p0","08p0",
         "08p0","08p0",
         "04p0","04p0"]
snr_mom = 2.0
percent = 0.0

done = glob.glob(dir_proj + "../eps/")
if not done:
    os.mkdir(dir_proj + "../eps/")


#####################
### Main
#####################
for i in range(len(imagenames)):
    galname = imagenames[i].split("/")[-1].split("_")[0]
    print("### working on " + imagenames[i].split("/")[-1])
    
    # measure noise
    output = dir_proj+"../eps/noise_"+imagenames[i].split("/")[-1].replace(".image","")+".png"
    noiserms = r21.noisehist(imagenames[i],noises_byeye[i],output)

    # moment map creation
    r21.eazy_immoments(dir_proj,imagenames[i],galname,noiserms,beams[i],snr_mom,percent)

os.system("rm -rf *.last")
