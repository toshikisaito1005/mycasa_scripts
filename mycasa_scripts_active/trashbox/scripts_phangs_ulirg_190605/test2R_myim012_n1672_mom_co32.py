import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim
import mycasaimaging_tools2 as myim2



#####################
### Define Parameters
#####################
dir_data = "/Users/saito/data/phangs_others/outflow_Rebecca/data/"
galname = "ngc1672"
suffix = ""
beam_size = 1.7 # target beam size in arcsec
rms_co32 = 0.0013 # at beam_size
rms_co21 = 0.018 # at beam_size
pixelmin = 5 # increment for removing small masks
increment_mask = 2.0 # beam (mask) = beam_size * increment_mask
thres_masking = 2.5 # threshold s/n ratio for masking
thres_mom = 3.0 # threshold s/n ratio for immoments
chans = "6~56" # channel selection for immoments
pbcut = 0.65 # pirmary beam cut



#####################
### Main Procedure
#####################
### step 1/10: importfits
print("### step 1/10: importfits")

fitsimages = glob.glob(dir_data+"data/"+galname+"*.fits")
for i in range(len(fitsimages)):
    myim2.eazy_importfits(fitsimages[i])

# find imported images
image_co32 = glob.glob(dir_data+"data/"+galname+"*co32*image*")[0]
image_co21 = glob.glob(dir_data+"data/"+galname+"*co21*image*")[0]


"""
### step 2/10: Kelvin to Jansky conversion
print("### step 2/10: Kelvin to Jansky conversion")

bunit = imhead(image_co32,"list")["bunit"]
synsbeam10 = imhead(image_co32,"list")["beammajor"]["value"]
if bunit == "K": # CO(1-0) conversion if bunit = K
    myim2.easy_K2Jy(image_co32,synsbeam10,115.27120)
    image_co32 = image_co32 + ".jy"
else:
    print("# skip easy_K2Jy for the CO(1-0) data")

bunit = imhead(image_co21,"list")["bunit"]
synsbeam21 = imhead(image_co21,"list")["beammajor"]["value"]
if bunit == "K": # CO(2-1) conversion if bunit = K
    myim2.easy_K2Jy(image_co21,synsbeam21,230.53800)
    image_co21 = image_co21 + ".jy"
else:
    print("# skip easy_K2Jy for the CO(2-1) data")
"""


### step 3/10: imregrid
print("### step 3/10: imregrid")
"""
myim2.easy_imregrid(image_co32,image_co21) # co32
image_co32 = image_co32 + ".regrid"
"""
pbimage = glob.glob(dir_data+"data/"+galname+"*.pb")[0]
myim2.easy_imregrid(pbimage,image_co32,False) # pbimage
pbimage = pbimage + ".regrid"



### step 4/10: imsmooth
print("### step 4/10: imsmooth")

beam_mask = beam_size * increment_mask # beam size for the masking
myim2.easy_imsmooth(image_co32,beam_mask,False) # co32
myim2.easy_imsmooth(image_co21,beam_mask,False) # co21



### mv the cubes to the working directory
os.system("mkdir "+dir_data+galname)
os.system("mv "+dir_data+"data/"+galname+"*32*smooth "\
          +dir_data+galname+"/"+galname+"_co32_"+suffix+".cube")
os.system("mv "+dir_data+"data/"+galname+"*21*smooth "\
          +dir_data+galname+"/"+galname+"_co21_"+suffix+".cube")



### step 5/10: create CO(3-2) cube mask
print("### step 5/10: create CO(1-0) cube mask")

cube_co32 = glob.glob(dir_data+galname+"/"\
                      +galname+"*_co32_"+suffix+".cube")[0]
thres_co32 = rms_co32 * increment_mask * 5
outmask_co32=cube_co32.replace(".cube",".mask")
myim2.createmask(cube_co32,thres_co32,outmask_co32)



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
immath(imagename = [outmask_co32, outmask_co21],
       mode = "evalexpr",
       expr = "IM0*IM1",
       outfile = mask_combine)

beamarea = myim2.beam_area(image_co21,increment_mask)
myim2.remove_smallmask(mask_combine,beamarea,pixelmin)


"""
### step 8/10: imsmooth
print("### step 8/10: imsmooth")

myim2.easy_imsmooth(image_co32,beam_size,False) # co32
myim2.easy_imsmooth(image_co21,beam_size,False) # co21
"""


### mv to working directory
os.system("rm -rf "+cube_co32)
os.system("rm -rf "+cube_co21)
os.system("cp -r "+dir_data+"data/"+galname+"*co32* "+cube_co32)

print("### step 9/10: immoments")
myim2.moment_maps(cube_co32,chans,mask_combine,rms_co32*thres_mom)



### pbmask
print("### step 10/10: pb mask at " + str(pbcut))

images_moment = glob.glob(cube_co32 + ".moment*")
images_moment.extend(glob.glob(cube_co21+".moment*"))
for i in range(len(images_moment)):
    os.system("rm -rf " + outfile)
    imagename = images_moment[i]
    outfile = images_moment[i].replace(".ICRS","").replace(".cube.","")
    imregrid(imagename = imagename,
             template = "J2000",
             output = outfile)
    os.system("rm -rf " + imagename)
    

    # exportfits
    os.system("rm -rf " + outfile + ".fits")
    exportfits(imagename = outfile,
               fitsimage = outfile + ".fits",
               velocity = True)


