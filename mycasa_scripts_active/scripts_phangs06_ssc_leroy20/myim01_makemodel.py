import os
import sys
import glob
import numpy as np


dir_project = "/Users/saito/data/myproj_active/proj_phangs06_ssc/"
tpbeam = "28.5arcsec"



##############################
### main
##############################
### directories
dir_mask = dir_project + "v3p3_hybridmask/"
dir_data = dir_project + "v3p4_tpeak/"


### get systemic velocity definition
mosaic_def = np.loadtxt("mosaic_definitions.txt",dtype="S20",usecols=(0,3))
mosaic_def = np.c_[[s.split("_")[0] for s in mosaic_def[:,0]], mosaic_def[:,1]]


### convert to CASA image
fitsimages = glob.glob(dir_mask + "*.fits")
fitsimages.extend(glob.glob(dir_data + "*.fits"))
for i in range(len(fitsimages)):
  print("### " + str(i+1) + "/" + str(len(fitsimages)))
  importfits(fitsimage = fitsimages[i],
    imagename = fitsimages[i].replace(".fits",".image"))
  os.system("rm -rf " + fitsimages[i])

os.system("rm -rf " + dir_data + "ngc1300_12m+7m+tp_co21_strict_tpeak.image")
os.system("rm -rf " + dir_data + "ngc4569_12m+7m+tp_co21_strict_tpeak.image")


###
imagenames = glob.glob(dir_data + "*.image")
imagenames.sort()
#
for i in range(len(imagenames)):
  #
  this_image = imagenames[i]
  print("### processing " + this_image.split("/")[-1])
  bmaj = imhead(this_image,mode="list")["beammajor"]["value"]
  factor = 1.222e+6 / bmaj**2 / 230.53800**2
  #
  maskname = glob.glob(dir_mask + this_image.split("/")[-1].split("12m")[0] + "*_hybridmask*")
  if maskname:
    #
    maskname2 = maskname.replace(".image",".mask2")
    os.system("rm -rf " + maskname2)
    immoments(imagename=maskname, outfile=maskname2)
    #
    outfile1 = this_image.replace(".image",".jyperbeam")
    os.system("rm -rf " + outfile1)
    expr = "iif(IM1>=1.0,"+"IM0/"+str(factor)+",0.0)"
    immath(imagename=[this_image,maskname2], mode="evalexpr", expr=expr, outfile=outfile1)
    # skymodel
    bmaj = imhead(outfile1,mode="list")["beammajor"]["value"]
    size_pix = abs(imhead(outfile1,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    beamarea = (bmaj*bmaj*np.pi) / (4*np.log(2)) / area_pix_arcsec
    #
    outfile2 = this_image.replace(".image",".skymodel")
    os.system("rm -rf " + outfile2)
    immath(imagename=outfile1, expr="IM0/"+str(beamarea), outfile=outfile2)
    #
    imhead(imagename=outfile2, mode="put", hdkey="bunit", hdvalue="Jy/pixel")
    imhead(imagename=outfile1,mode="put", hdkey="bunit", hdvalue="Jy/beam")
    #
    outfile3 = this_image.replace(".image",".jypb.smooth_tmp_")
    os.system("rm -rf " + outfile3)
    imsmooth(imagename=outfile1, major=tpbeam, minor=tpbeam, pa="0deg", outfile=outfile3)
    #
    cell = np.abs(imhead(outfile3,mode='list')['cdelt1']) * 180.*3600./np.pi
    nbin = int(28.5 / 4.5 / cell)
    #
    outfile4 = this_image.replace(".image",".jypb.smooth")
    os.system("rm -rf " + outfile4)
    imrebin(imagename=outfile3, outfile=outfile4, factor=[nbin,nbin])
    #
    bmaj = imhead(outfile4,mode="list")["beammajor"]["value"]
    size_pix = abs(imhead(outfile4,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    beamarea = (bmaj*bmaj*np.pi) / (4*np.log(2)) / area_pix_arcsec
    #
    outfile5 = this_image.replace(".image",".jyppix.smooth")
    os.system("rm -rf " + outfile5)
    immath(imagename=outfile4, expr="IM0/"+str(beamarea), outfile=outfile5)



# get PHANGS DR1 moment-8 maps
for i in range(len(imagenames)):
    if maskname:



        imhead(imagename = outfile,
               mode = "put",
	       hdkey = "bunit",
	       hdvalue= "Jy/pixel")

	imhead(imagename = outfile,
	       mode = "del",
	       hdkey = "beammajor")

        os.system("rm -rf " + maskname)
        os.system("rm -rf " + imagenames[i].replace(".image",".jypb.smooth_tmp_"))
	os.system("rm -rf " + maskname.replace(".image",".mask2.smooth"))
        imsmooth(imagename = maskname.replace(".image",".mask2"),
	          targetres = True,
		  major = "3arcsec",
		  minor = "3arcsec",
		  pa = "0deg",
		  outfile = maskname.replace(".image",".mask2.smooth"))

        os.system("rm -rf " + maskname.replace(".image",".mask"))
        immath(imagename = maskname.replace(".image",".mask2.smooth"),
	       mode = "evalexpr",
	       expr = "iif(IM0>=1.0,1.0,0.0)",
	       outfile = maskname.replace(".image",".mask"))
	os.system("rm -rf " + maskname.replace(".image",".mask2*"))
	os.system("rm -rf " + maskname.replace(".image",".mask3*"))

        os.system("rm -rf " + maskname.replace(".image",".mask.fits"))
        exportfits(imagename = maskname.replace(".image",".mask"),
	           fitsimage = maskname.replace(".image",".mask.fits"))

        os.system("rm -rf " + maskname.replace(".image",".mask"))
        importfits(fitsimage = maskname.replace(".image",".mask.fits"),
	           imagename = maskname.replace(".image",".mask"),
		   defaultaxes = True,
		   defaultaxesvalues=["RA","Dec","Frequency","Stokes"])
	os.system("rm -rf " + maskname.replace(".image",".mask.fits"))

    os.system("rm -rf " + imagenames[i])
