import os
import glob
import numpy as np


dir_data = "../../myproj_published/proj_phangs04_school/data_raw/"
galaxy = ["ngc0628", "ngc3627"]
highest_beam = ["53pc", "65pc"]
scale = [47.4, 40]

#####################
### Main Procedure
#####################
# mkdir
dir_working = dir_data + "../data/"
os.system("rm -rf " + dir_working)
os.mkdir(dir_working)

#
for i in range(len(galaxy)):
    # import galname
    galname = galaxy[i]
    print("# working on " + galname)
    
    # casa2fits; moment-0
    fitsimages_12m7mtp = glob.glob(dir_data + galname + "*12m+7m+tp_*broad_mom0*.fits")
    fitsimages_12m7m = glob.glob(dir_data + galname + "*12m+7m_*broad_mom0*.fits")
    fitsimages = np.r_[fitsimages_12m7mtp,fitsimages_12m7m]

    for j in range(len(fitsimages)):
        fitsimage = fitsimages[j]
        beam_tmp = fitsimage.split("/")[-1].split("_")[-1].replace(".fits","")
        beam = beam_tmp.replace("mom0",highest_beam[i]).zfill(5)
        array = fitsimage.split("/")[-1].split("_")[1].replace("+","")
        imagename = dir_working + galname + "_" + array + "_" + beam + ".image_Kelvin"
        
        os.system("rm -rf " + imagename)
        importfits(fitsimage=fitsimage,imagename=imagename)

        # convert Kelvin to jansky
        beam_arcsec = float(beam.replace("pc","")) / scale[i]
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
    fitsimages_12m7mtp = glob.glob(dir_data + galname + "*12m+7m+tp_*broad_emom0*.fits")
    fitsimages_12m7m = glob.glob(dir_data + galname + "*12m+7m_*broad_emom0*.fits")
    fitsimages = np.r_[fitsimages_12m7mtp,fitsimages_12m7m]

    for j in range(len(fitsimages)):
        fitsimage = fitsimages[j]
        beam_tmp = fitsimage.split("/")[-1].split("_")[-1].replace(".fits","")
        beam = beam_tmp.replace("emom0",highest_beam[i]).zfill(5)
        array = fitsimage.split("/")[-1].split("_")[1].replace("+","")
        imagename = dir_working + galname + "_" + array + "_" + beam + ".error_Kelvin"
        
        os.system("rm -rf " + imagename)
        importfits(fitsimage=fitsimage,imagename=imagename)
        
        # convert Kelvin to jansky
        beam_arcsec = float(beam.replace("pc","")) / scale[i]
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
