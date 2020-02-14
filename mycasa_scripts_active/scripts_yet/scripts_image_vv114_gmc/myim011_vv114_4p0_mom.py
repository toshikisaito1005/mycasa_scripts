import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim
import mycasaimaging_tools2 as myim2



#####################
### Define Parameters
#####################
dir_data = "../../vv114/"
galname = "vv114"
suffix = "p17"
beam_size = 2.0 # target beam size in arcsec
beam_size32 = 0.17 # target beam size in arcsec
rms_co10 = 0.003 # at beam_size
rms_co32 = 0.0005 # at beam_size
pixelmin = 15 # increment for removing small masks
increment_mask = 1.05 # beam (mask) = beam_size * increment_mask
thres_masking = 2.5 # threshold s/n ratio for masking
thres_mom = 1.0 # threshold s/n ratio for immoments
chans = "4~70" # channel selection for immoments
pbcut = 0.5 # pirmary beam cut



#####################
### Main Procedure
#####################
os.system("rm -rf "+dir_data+galname+"/*"+suffix+"*")

### step 1/10: importfits
print("### step 1/10: importfits")

fitsimages = glob.glob(dir_data+"images/"+galname+"*.fits")
for i in range(len(fitsimages)):
    myim2.eazy_importfits(fitsimages[i])

# find imported images
image_co10 = glob.glob(dir_data+"images/"+galname+"*co10*image*")[0]
image_co32 = glob.glob(dir_data+"images/"+galname+"*co32*image*")[0]



### step 2/10: Kelvin to Jansky conversion
print("### step 2/10: Kelvin to Jansky conversion")

bunit = imhead(image_co10,"list")["bunit"]
synsbeam10 = imhead(image_co10,"list")["beammajor"]["value"]
if bunit == "K": # CO(1-0) conversion if bunit = K
    myim2.easy_K2Jy(image_co10,synsbeam10,115.27120)
    image_co10 = image_co10 + ".jy"
else:
    print("# skip easy_K2Jy for the CO(1-0) data")

bunit = imhead(image_co32,"list")["bunit"]
synsbeam21 = imhead(image_co32,"list")["beammajor"]["value"]
if bunit == "K": # CO(2-1) conversion if bunit = K
    myim2.easy_K2Jy(image_co32,synsbeam21,230.53800)
    image_co32 = image_co32 + ".jy"
else:
    print("# skip easy_K2Jy for the CO(2-1) data")



### step 3/10: imregrid
print("### step 3/10: imregrid")

myim2.easy_imregrid(image_co10,image_co32) # co10
image_co10 = image_co10 + ".regrid"

pbimage = glob.glob(dir_data+"images/"+galname+"*.pb")[0]
myim2.easy_imregrid(pbimage,image_co32,False) # pbimage
pbimage = pbimage + ".regrid"



### step 4/10: imsmooth
print("### step 4/10: imsmooth")

beam_mask = beam_size * increment_mask # beam size for the masking
myim2.easy_imsmooth(image_co10,beam_mask,False) # co10
myim2.easy_imsmooth(image_co32,beam_mask,False) # co32



### mv the cubes to the working directory
os.system("mkdir "+dir_data+galname)
os.system("mv "+dir_data+"images/"+galname+"*10*smooth "\
          +dir_data+galname+"/"+galname+"_co10_"+suffix+".cube")
os.system("mv "+dir_data+"images/"+galname+"*32*smooth "\
          +dir_data+galname+"/"+galname+"_co32_"+suffix+".cube")



### step 5/10: create CO(1-0) cube mask
print("### step 5/10: create CO(1-0) cube mask")

cube_co10 = glob.glob(dir_data+galname+"/"\
                      +galname+"*_co10_"+suffix+".cube")[0]
thres_co10 = rms_co10 * increment_mask * thres_masking
outmask_co10=cube_co10.replace(".cube",".mask")
myim2.createmask(cube_co10,thres_co10,outmask_co10)



### step 6/10: create CO(2-1) cube mask
print("### step 6/10: create CO(2-1) cube mask")

cube_co32 = glob.glob(dir_data+galname+"/"\
                       +galname+"*_co32_"+suffix+".cube")[0]
thres_co32 = rms_co32 * increment_mask * thres_masking
outmask_co32=cube_co32.replace(".cube",".mask")
myim2.createmask(cube_co32,thres_co32,outmask_co32)



### step 7/10: combine masks
print("### step 7/10: combine masks")

mask_combine = dir_data+galname+"/"+galname+"_combine_"+suffix+".mask"
os.system("rm -rf " + mask_combine)
immath(imagename = [outmask_co10, outmask_co32],
       mode = "evalexpr",
       expr = "IM0*IM1",
       outfile = mask_combine)

beamarea = myim2.beam_area(image_co32,increment_mask)
myim2.remove_smallmask(mask_combine,beamarea,pixelmin)



### step 8/10: imsmooth
print("### step 8/10: imsmooth")

myim2.easy_imsmooth(image_co10,beam_size,False) # co10
myim2.easy_imsmooth(image_co32,beam_size32,False) # co32



### mv to working directory
os.system("rm -rf "+cube_co10)
os.system("rm -rf "+cube_co32)
os.system("mv "+dir_data+"images/"+galname+"*10*smooth "+cube_co10)
os.system("mv "+dir_data+"images/"+galname+"*32*smooth "+cube_co32)

print("### step 9/10: immoments")
myim2.moment_maps(cube_co10,chans,mask_combine,rms_co10*thres_mom)
myim2.moment_maps(cube_co32,chans,mask_combine,rms_co32*thres_mom)



### pbmask
print("### step 10/10: pb mask at " + str(pbcut))

mask_pb = dir_data+galname+"/"+galname+"_pb_"+suffix+".mask"
peak = imhead(pbimage,mode="list")["datamax"]
myim2.createmask(pbimage,peak*pbcut,mask_pb)

images_moment = glob.glob(cube_co10 + ".moment*")
images_moment.extend(glob.glob(cube_co32+".moment*"))
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


