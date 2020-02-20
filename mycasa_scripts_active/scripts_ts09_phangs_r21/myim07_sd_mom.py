import os
import sys
import glob


dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_other/"
dir_empire = dir_data + "empire_co10/"
dir_heracles = dir_data + "heracles_co21/"

chans_co10 = ["89~98",
              "61~117",
              "80~108",
              "74~107"]

######
fits_co10 = glob.glob(dir_empire + "*.fits")
fits_co21 = glob.glob(dir_heracles + "*.fits")

for i in range(len(fits_co10)):
    os.system("rm -rf " + fits_co10[i].replace(".fits",".image"))
    importfits(fitsimage = fits_co10[i],
               imagename = fits_co10[i].replace(".fits",".image"))

    os.system("rm -rf " + fits_co10[i].replace(".fits",".image_Jypb"))
    expr = "IM0/1.222e6*25.649*25.649*115.27120*115.27120"
    immath(imagename = fits_co10[i].replace(".fits",".image"),
           mode = "evalexpr",
           expr = expr,
           outfile = fits_co10[i].replace(".fits",".image_Jypb"))
    os.system("rm -rf " + fits_co10[i].replace(".fits",".image"))

    imhead(imagename = fits_co10[i].replace(".fits",".image_Jypb"),
           mode = "put",
           hdkey = "bunit",
           hdvalue = "Jy/beam")

    imsmooth(imagename = fits_co10[i].replace(".fits",".image_Jypb"),
             targetres = True,
             major = "33.0arcsec",
             minor = "33.0arcsec",
             pa = "0deg",
             outfile = fits_co10[i].replace(".fits",".smooth"))

    os.system("rm -rf " + fits_co10[i].replace(".fits",".moment0"))
    immoments(imagename = fits_co10[i].replace(".fits",".smooth"),
              moments = [0],
              chans = chans_co10[i],
              outfile = fits_co10[i].replace(".fits",".moment0"))
    os.system("rm -rf " + fits_co10[i].replace(".fits",".smooth"))

for i in range(len(fits_co21)):
    os.system("rm -rf " + fits_co21[i].replace(".fits",".image"))
    importfits(fitsimage = fits_co21[i],
               imagename = fits_co21[i].replace(".fits",".image"))
        
    os.system("rm -rf " + fits_co21[i].replace(".fits",".image_Jypb"))
    expr = "IM0/1.222e6*33.0*33.0*230.53800*230.53800"
    immath(imagename = fits_co21[i].replace(".fits",".image"),
           mode = "evalexpr",
           expr = expr,
           outfile = fits_co21[i].replace(".fits",".image_Jypb"))
    os.system("rm -rf " + fits_co21[i].replace(".fits",".image"))
               
    imhead(imagename = fits_co21[i].replace(".fits",".image_Jypb"),
           mode = "put",
           hdkey = "bunit",
           hdvalue = "Jy/beam")

    os.system("rm -rf " + fits_co21[i].replace(".fits",".regrid"))
    imregrid(imagename = fits_co21[i].replace(".fits",".image_Jypb"),
             template = fits_co10[i].replace(".fits",".image_Jypb"),
             output = fits_co21[i].replace(".fits",".regrid"),
             asvelocity = True)

    os.system("rm -rf " + fits_co21[i].replace(".fits",".moment0_tmp"))
    immoments(imagename = fits_co21[i].replace(".fits",".regrid"),
              moments = [0],
              chans = chans_co10[i],
              outfile = fits_co21[i].replace(".fits",".moment0_tmp"))

    velres = abs(imhead(fits_co10[i].replace(".fits",".image_Jypb"),"list")["cdelt3"])
    velres2 = str(velres*3.e8/115.27120e9)
    os.system("rm -rf " + fits_co21[i].replace(".fits",".regrid"))
    os.system("rm -rf " + fits_co21[i].replace(".fits",".moment0"))
    #os.system("rm -rf " + fits_co10[i].replace(".fits",".image_Jypb"))
    immath(imagename = fits_co21[i].replace(".fits",".moment0_tmp"),
           expr = "IM0/238.538e9*3e8/"+velres2,
           outfile = fits_co21[i].replace(".fits",".moment0"))
    os.system("rm -rf " + fits_co21[i].replace(".fits",".moment0_tmp"))
    #os.system("rm -rf " + fits_co21[i].replace(".fits",".image_Jypb"))

fits_sd_co10 = glob.glob(dir_empire + "*.moment0")
fits_sd_co10.sort()
fits_sd_co21 = glob.glob(dir_heracles + "*.moment0")
fits_sd_co21.sort()


#####
for i in range(len(fits_sd_co10)):
    os.system("rm -rf " + fits_sd_co10[i] + ".fits")
    exportfits(imagename = fits_sd_co10[i],
               fitsimage = fits_sd_co10[i] + ".fits")
        
    os.system("rm -rf " + fits_sd_co10[i])
    importfits(fitsimage = fits_sd_co10[i] + ".fits",
               imagename = fits_sd_co10[i],
               defaultaxes = True,
               defaultaxesvalues = ['Right Ascension',
                                    'Declination',
                                    'Frequency',
                                    'Stokes'])
    os.system("rm -rf " + fits_sd_co10[i] + ".fits")
               
    os.system("rm -rf " + fits_sd_co10[i] + ".regrid_tmp")
    galname = fits_sd_co10[i].split("/empire_co10/")[1].split("_")[0]
    imregrid(imagename = fits_sd_co10[i],
             template = glob.glob(dir_data+"../"+galname+"_co10/*co10*33p0*moment0")[0],
             output = fits_sd_co10[i] + ".regrid_tmp")

    os.system("rm -rf " + fits_sd_co10[i] + ".regrid")
    immath(imagename = [fits_sd_co10[i] + ".regrid_tmp",
                        glob.glob(dir_data+"../"+galname+"_co10/*co10*33p0*moment0")[0]],
           expr = "iif(IM1>0,IM0,0.0)",
           outfile = fits_sd_co10[i] + ".regrid")
    os.system("rm -rf " + fits_sd_co10[i] + ".regrid_tmp")
    os.system("rm -rf " + fits_sd_co10[i])
               
    # co21
    os.system("rm -rf " + fits_sd_co21[i] + ".fits")
    exportfits(imagename = fits_sd_co21[i],
               fitsimage = fits_sd_co21[i] + ".fits",
               dropstokes = True,
               dropdeg = True)
               
    os.system("rm -rf " + fits_sd_co21[i])
    importfits(fitsimage = fits_sd_co21[i] + ".fits",
               imagename = fits_sd_co21[i],
               defaultaxes = True,
               defaultaxesvalues = ['0deg',
                                    '0deg',
                                    '1GHz',
                                    'I'])
    os.system("rm -rf " + fits_sd_co21[i] + ".fits")
               
    os.system("rm -rf " + fits_sd_co21[i] + ".regrid_tmp")
    galname = fits_sd_co21[i].split("/heracles_co21/")[1].split("_")[0]
    imregrid(imagename = fits_sd_co21[i],
             axes = [0,1],
             template = glob.glob(dir_data+"../"+galname+"_co21/*co21*33p0*moment0")[0],
             output = fits_sd_co21[i] + ".regrid_tmp")
               
    os.system("rm -rf " + fits_sd_co21[i] + ".regrid")
    immath(imagename = [fits_sd_co21[i] + ".regrid_tmp",
                        glob.glob(dir_data+"../"+galname+"_co21/*co21*33p0*moment0")[0]],
           expr = "iif(IM1>0,IM0,0.0)",
           outfile = fits_sd_co21[i] + ".regrid")
    os.system("rm -rf " + fits_sd_co21[i] + ".regrid_tmp")
    os.system("rm -rf " + fits_sd_co21[i])

os.system("rm -rf *.last")
