import os
import sys
import glob
import numpy as np

dir_data = "../"
tpbeam = "28.5arcsec"
chans = "90" # ""
mask_thres = "1" # "20"
mask_thres2 = "1" # "15"

####################
### main
####################
os.system("rm -rf " + dir_data + "data/")
os.system("mkdir " + dir_data + "data/")

# convert to CASA image
fitsimages = glob.glob(dir_data + "data_raw/*.fits")
for i in range(len(fitsimages)):
    imagename1 = fitsimages[i].replace(".fits",".image").replace("_raw","")
    imagename2 = imagename1.replace("_12m+7m+tp_co21","").replace("_strict","")
    importfits(fitsimage = fitsimages[i],
               imagename = imagename2)

# one channel extraction
cubename = glob.glob(dir_data + "data/*pbcorr_round_k.image")[0]
channame = cubename.replace("_pbcorr_round_k","_chan")
os.system("rm -rf " + channame)
immath(imagename = cubename,
       expr = "IM0",
       outfile = channame,
       chans = chans)
os.system("rm -rf " + cubename)

imagename = channame # glob.glob(dir_data + "data/*tpeak.image")[0]
maskname = glob.glob(dir_data + "data/*hybridmask.image")[0]

# create skymodel
bmaj = imhead(imagename,mode="list")["beammajor"]["value"]
factor = 1.222e+6 / bmaj**2 / 230.53800**2

os.system("rm -rf " + maskname.replace(".image",".mask2"))
immoments(imagename = maskname,
          outfile = maskname.replace(".image",".mask2"),
          chans = chans)

outfile1 = imagename.replace(".image",".jyperbeam")
os.system("rm -rf " + outfile1)
expr = "iif(IM1>="+mask_thres+","+"IM0/"+str(factor)+",0.0)"
immath(imagename = [imagename,
                    maskname.replace(".image",".mask2")],
       mode = "evalexpr",
       expr = expr,
       outfile = outfile1)

bmaj = imhead(outfile1,mode="list")["beammajor"]["value"]
size_pix = abs(imhead(outfile1,mode="list")["cdelt1"])
area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
beamarea = (bmaj*bmaj*np.pi) / (4*np.log(2)) / area_pix_arcsec

outfile2 = imagename.replace(".image","_jyperpix.skymodel")
os.system("rm -rf " + outfile2)
expr = "iif(IM0>=0.0001,"+"IM0/"+str(beamarea)+",0.0)"
immath(imagename = outfile1,
       expr = expr,
       outfile = outfile2)

imhead(imagename = outfile2,
       mode = "put",
       hdkey = "bunit",
       hdvalue= "Jy/pixel")

# create TP data used for feathering
outfile1 = imagename.replace(".image",".jypb.smooth_tmp_")
os.system("rm -rf " + outfile1)
imsmooth(imagename = imagename.replace(".image",".jyperbeam"),
         major = tpbeam,
         minor = tpbeam,
         pa = "0deg",
         outfile = outfile1,
         targetres = True)
os.system("rm -rf " + imagename.replace(".image",".jyperbeam"))

cell = np.abs(imhead(outfile1,mode='list')['cdelt1'])*180.*3600./np.pi
nbin = int(float(tpbeam.replace("arcsec","")) / 4.53 / cell)

outfile2 = imagename.replace(".image","_jyperbeam.tpimage")
imrebin(imagename=outfile1,outfile=outfile2,factor=[nbin,nbin])
os.system("rm -rf " + outfile1)

imhead(imagename = outfile2,
       mode = "put",
       hdkey = "bunit",
       hdvalue= "Jy/beam")

# create tclean mask
outfile1 = maskname.replace(".image",".mask2.smooth")
os.system("rm -rf " + outfile1)
imsmooth(imagename = maskname.replace(".image",".mask2"),
         targetres = True,
         major = "3arcsec",
         minor = "3arcsec",
         pa = "0deg",
         outfile = outfile1)

os.system("rm -rf " + maskname.replace(".image",".mask2"))

outfile2 = maskname.replace(".image",".mask").replace("_hybridmask","")
os.system("rm -rf " + outfile2)
immath(imagename = outfile1,
       mode = "evalexpr",
       expr = "iif(IM0>="+mask_thres2+",1.0,0.0)",
       outfile = outfile2)
os.system("rm -rf " + outfile1)

outfile3 = outfile2.replace(".mask","_mask") + ".fits"
os.system("rm -rf " + outfile3)
exportfits(imagename=outfile2,fitsimage=outfile3)

os.system("rm -rf " + outfile2)
importfits(fitsimage = outfile3,
           imagename = outfile2,
           defaultaxes = True,
           defaultaxesvalues=["RA","Dec","Frequency","Stokes"])
os.system("rm -rf " + outfile3)

os.system("rm -rf " + maskname + " " + imagename)
os.system("rm -rf *.last")
