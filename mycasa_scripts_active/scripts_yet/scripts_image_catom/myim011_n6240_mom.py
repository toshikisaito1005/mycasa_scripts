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
dir_data = "/Users/saito/data/goals_catom/"
galname = "ngc6240"
suffix = "p35"
beam_size = 0.35 # target beam size in arcsec
rms_ci10 = 0.007 # at beam_size
pixelmin = 10 # increment for removing small masks
increment_mask = 3.0 # beam (mask) = beam_size * increment_mask
thres_masking = 4.5 # threshold s/n ratio for masking
thres_mom = 1.0 # threshold s/n ratio for immoments
chans = "15~62" # channel selection for immoments
pbcut = 0.70 # pirmary beam cut



#####################
### Main Procedure
#####################
os.system("rm -rf "+dir_data+galname+"/*"+suffix+"*")

### step 1/10: importfits
print("### step 1/10: importfits")

fitsimages = glob.glob(dir_data+"fits/"+galname+"*.fits")
for i in range(len(fitsimages)):
    myim2.eazy_importfits(fitsimages[i])

# find imported images
image_ci10 = glob.glob(dir_data+"fits/"+galname+"*pbcor.image")[0]



### step 2/10: Kelvin to Jansky conversion
print("### step 2/10: Kelvin to Jansky conversion")

bunit = imhead(image_ci10,"list")["bunit"]
synsbeam10 = imhead(image_ci10,"list")["beammajor"]["value"]
if bunit == "K": # CO(1-0) conversion if bunit = K
    myim2.easy_K2Jy(image_ci10,synsbeam10,115.27120)
    image_ci10 = image_ci10 + ".jy"
else:
    print("# skip easy_K2Jy for the CI(1-0) data")



### step 4/10: imsmooth
print("### step 4/10: imsmooth")

beam_mask = beam_size * increment_mask # beam size for the masking
myim2.easy_imsmooth(image_ci10,beam_mask,False) # ci10



### mv the cubes to the working directory
os.system("mkdir "+dir_data+galname)
os.system("mv "+dir_data+"fits/"+galname+"*10*smooth "\
          +dir_data+galname+"/"+galname+"_ci10_"+suffix+".cube")



### step 5/10: create CO(1-0) cube mask
print("### step 5/10: create CI(1-0) cube mask")

cube_ci10 = glob.glob(dir_data+galname+"/"\
                      +galname+"*_ci10_"+suffix+".cube")[0]
thres_ci10 = rms_ci10 * increment_mask * thres_masking
outmask_ci10=cube_ci10.replace(".cube",".mask")
myim2.createmask(cube_ci10,thres_ci10,outmask_ci10)

beamarea = myim2.beam_area(image_ci10,increment_mask)
myim2.remove_smallmask(outmask_ci10,beamarea,pixelmin)



### step 8/10: imsmooth
print("### step 8/10: imsmooth")

myim2.easy_imsmooth(image_ci10,beam_size,True) # ci10



### mv to working directory
os.system("rm -rf "+cube_ci10)
os.system("mv "+dir_data+"fits/"+galname+"*10*smooth "+cube_ci10)

print("### step 9/10: immoments")
myim2.moment_maps(cube_ci10,chans,outmask_ci10,rms_ci10*thres_mom)



### pbmask
print("### step 10/10: pb mask at " + str(pbcut))

pbimage = glob.glob(dir_data+"fits/"+galname+"*.pb")[0]
mask_pb = dir_data+galname+"/"+galname+"_ci10_"+suffix+"_pb.mask"
peak = imhead(pbimage,mode="list")["datamax"]
myim2.createmask(pbimage,peak*pbcut,mask_pb)

images_moment = glob.glob(cube_ci10 + ".moment*")
for i in range(len(images_moment)):
    outfile = images_moment[i].replace(".cube","")
    os.system("rm -rf " + outfile)
    immath(imagename=[images_moment[i],mask_pb],
           mode="evalexpr",
           expr = "IM0*IM1",
           outfile = outfile)
    os.system("rm -rf " + images_moment[i])
    os.system("rm -rf " + outfile + ".2")
    imregrid(imagename = outfile,
                 template = "J2000",
                 output = outfile + ".2")
    os.system("rm -rf " + outfile)

    # exportfits
    os.system("rm -rf " + outfile + ".fits")
    exportfits(imagename = outfile + ".2",
               fitsimage = outfile + ".fits",
               velocity = True)
    os.system("mv " + outfile + ".2 " + outfile)


