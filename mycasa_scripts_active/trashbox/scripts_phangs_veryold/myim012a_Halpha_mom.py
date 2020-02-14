import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim
import mycasaimaging_tools2 as myim2
import mycasaimaging_Nyquist as Nyq
from astropy import units as u
from astropy.coordinates import SkyCoord



#####################
### Define Parameters
#####################
suffix = "Halpha"
beam_size = beam_halpha
rms_co10 = rms_co10_halpha
rms_co21 = rms_co21_halpha



#####################
### Main Procedure
#####################
os.system("rm -rf "+dir_data+galname+"/*"+suffix+"*")

### step 1/10: importfits
print("### step 1/10: importfits")

fitsimages = glob.glob(dir_data+"data/"+galname+"*.fits")
for i in range(len(fitsimages)):
    myim2.eazy_importfits(fitsimages[i])

# find imported images
image_co10 = glob.glob(dir_data+"data/"+galname+"*co10*image*")[0]
image_co21 = glob.glob(dir_data+"data/"+galname+"*co21*image*")[0]



### step 2/10: Kelvin to Jansky conversion
print("### step 2/10: Kelvin to Jansky conversion")

bunit = imhead(image_co10,"list")["bunit"]
synsbeam10 = imhead(image_co10,"list")["beammajor"]["value"]
if bunit == "K": # CO(1-0) conversion if bunit = K
    myim2.easy_K2Jy(image_co10,synsbeam10,115.27120)
    image_co10 = image_co10 + ".jy"
else:
    print("# skip easy_K2Jy for the CO(1-0) data")

bunit = imhead(image_co21,"list")["bunit"]
synsbeam21 = imhead(image_co21,"list")["beammajor"]["value"]
if bunit == "K": # CO(2-1) conversion if bunit = K
    myim2.easy_K2Jy(image_co21,synsbeam21,230.53800)
    image_co21 = image_co21 + ".jy"
else:
    print("# skip easy_K2Jy for the CO(2-1) data")



### step 3/10: imregrid
print("### step 3/10: imregrid")

myim2.easy_imregrid(image_co10,image_co21) # co10
image_co10 = image_co10 + ".regrid"

pbimage = glob.glob(dir_data+"data/"+galname+"*.pb")[0]
myim2.easy_imregrid(pbimage,image_co21,False) # pbimage
pbimage = pbimage + ".regrid"



### step 4/10: imsmooth
print("### step 4/10: imsmooth")

beam_mask = beam_size * increment_mask # beam size for the masking
myim2.easy_imsmooth(image_co10,beam_mask,False) # co10
myim2.easy_imsmooth(image_co21,beam_mask,False) # co21



### mv the cubes to the working directory
os.system("mkdir "+dir_data+galname)
os.system("mv "+dir_data+"data/"+galname+"*10*smooth "\
          +dir_data+galname+"/"+galname+"_co10_"+suffix+".cube")
os.system("mv "+dir_data+"data/"+galname+"*21*smooth "\
          +dir_data+galname+"/"+galname+"_co21_"+suffix+".cube")



### step 5/10: create CO(1-0) cube mask
print("### step 5/10: create CO(1-0) cube mask")

cube_co10 = glob.glob(dir_data+galname+"/"\
                      +galname+"*_co10_"+suffix+".cube")[0]
thres_co10 = rms_co10 * increment_mask * thres_masking
outmask_co10=cube_co10.replace(".cube",".mask")
myim2.createmask(cube_co10,thres_co10,outmask_co10)



### step 6/10: create CO(2-1) cube mask
print("### step 6/10: create CO(2-1) cube mask")

cube_co21 = glob.glob(dir_data+galname+"/"\
                       +galname+"*_co21_"+suffix+".cube")[0]
thres_co21 = rms_co21 * increment_mask * thres_masking
outmask_co21=cube_co21.replace(".cube",".mask")
myim2.createmask(cube_co21,thres_co21,outmask_co21)



### step 7/10: combine masks
print("### step 7/10: combine masks")

mask_combine = dir_data+galname+"/"+galname+"_combine_"+suffix+".mask"
os.system("rm -rf " + mask_combine)
immath(imagename = [outmask_co10, outmask_co21],
       mode = "evalexpr",
       expr = "IM0*IM1",
       outfile = mask_combine)

beamarea = myim2.beam_area(image_co21,increment_mask)
myim2.remove_smallmask(mask_combine,beamarea,pixelmin)



### step 8/10: immoments
print("### step 8/10: immoments")

myim2.easy_imsmooth(image_co10,beam_size,True) # co10
myim2.easy_imsmooth(image_co21,beam_size,True) # co21



### mv to working directory
os.system("rm -rf "+cube_co10)
os.system("rm -rf "+cube_co21)
os.system("mv "+dir_data+"data/"+galname+"*10*smooth "+cube_co10)
os.system("mv "+dir_data+"data/"+galname+"*21*smooth "+cube_co21)

myim2.moment_maps(cube_co10,chans,mask_combine,rms_co10*thres_mom)
myim2.moment_maps(cube_co21,chans,mask_combine,rms_co21*thres_mom)



### pbmask
print("### step 9/10: pb mask at " + str(pbcut))
print("### step 10/10: exportfits")

mask_pb = dir_data+galname+"/"+galname+"_pb_"+suffix+".mask"
peak = imhead(pbimage,mode="list")["datamax"]
myim2.createmask(pbimage,peak*pbcut,mask_pb)

images_moment = glob.glob(cube_co10 + ".moment*")
images_moment.extend(glob.glob(cube_co21+".moment*"))
for i in range(len(images_moment)):
    outfile = images_moment[i].replace(".cube","")
    os.system("rm -rf " + outfile)
    immath(imagename=[images_moment[i],mask_pb],
           mode="evalexpr",
           expr = "IM0*IM1",
           outfile = outfile)
    os.system("rm -rf " + images_moment[i])

    # exportfits
    os.system("rm -rf " + outfile + ".fits")
    exportfits(imagename = outfile,
               fitsimage = outfile + ".fits",
               velocity = True)


