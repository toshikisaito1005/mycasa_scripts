import os
import glob
import numpy as np


dir_data = "../../myproj_published/proj_phangs04_school/data_raw/"
scale = [47.4]

#####################
### Main Procedure
#####################
# mkdir
dir_working = dir_data + "../data/"

fitsimages_orig = glob.glob(dir_data + "*12m+7m+tp_*strict_mom0_500pc.fits")

#
for i in range(len(fitsimages_orig)):
    # import galinfo
    galname = fitsimages_orig[i].split("/")[-1].split("_")[0]
    #chans = galinfo[np.where(galinfo[:,0]==galname)][0,1]
    
    # casa2fits; moment-0
    fitsimages_12m7mtp = glob.glob(dir_data + galname + "*12m+7m+tp_*strict_mom0_500pc.fits")
    fitsimages_12m7m = glob.glob(dir_data + galname + "*12m+7m_*strict_mom0_500pc.fits")
    fitsimages = np.r_[fitsimages_12m7mtp,fitsimages_12m7m]

    for j in range(len(fitsimages)):
        fitsimage = fitsimages[j]
        beam = fitsimage.split("/")[-1].split("_")[-1].replace(".fits","")
        array = fitsimage.split("/")[-1].split("_")[1].replace("+","")
        imagename = dir_working + galname + "_" + array + "_" + beam + ".image_Kelvin"
        
        os.system("rm -rf " + imagename)
        importfits(fitsimage=fitsimage,imagename=imagename)

        # convert Kelvin to jansky
        beam_arcsec = imhead(imagename,mode="list")["beammajor"]["value"]
        factor = 1.222e6 / beam_arcsec**2 / 230.53800**2
        outfile = imagename.replace("_Kelvin","")
        os.system("rm -rf " + outfile)
        immath(imagename = imagename,
               expr = "IM0/" + str(factor),
               outfile = outfile)
        #os.system("rm -rf " + imagename)

        imhead(imagename = outfile,
               mode = "put",
               hdkey = "bunit",
               hdvalue = "Jy/beam.km/s")

    # casa2fits; moment-0 error
    fitsimages_12m7mtp = glob.glob(dir_data + galname + "*12m+7m+tp_*strict_emom0_500pc.fits")
    fitsimages_12m7m = glob.glob(dir_data + galname + "*12m+7m_*strict_emom0_500pc.fits")
    fitsimages = np.r_[fitsimages_12m7mtp,fitsimages_12m7m]

    for j in range(len(fitsimages)):
        fitsimage = fitsimages[j]
        beam = fitsimage.split("/")[-1].split("_")[-1].replace(".fits","")
        array = fitsimage.split("/")[-1].split("_")[1].replace("+","")
        imagename = dir_working + galname + "_" + array + "_" + beam + ".error_Kelvin"
        
        os.system("rm -rf " + imagename)
        importfits(fitsimage=fitsimage,imagename=imagename)
        
        # convert Kelvin to jansky
        beam_arcsec = imhead(imagename,mode="list")["beammajor"]["value"]
        factor = 1.222e6 / beam_arcsec**2 / 230.53800**2
        outfile = imagename.replace("_Kelvin","")
        os.system("rm -rf " + outfile)
        immath(imagename = imagename,
               expr = "IM0/" + str(factor),
               outfile = outfile)
        #os.system("rm -rf " + imagename)
               
        imhead(imagename = outfile,
               mode = "put",
               hdkey = "bunit",
               hdvalue = "Jy/beam.km/s")

os.system("rm -rf *.last")
