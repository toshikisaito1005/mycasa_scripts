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



#####################
### Main Procedure
#####################
os.system("rm -rf "+dir_data+galname+"/*"+suffix+"*")

### step 1/10: importfits
print("### step 1/10: importfits")

fitsimages = glob.glob(dir_data+"data/"+galname+"*.fits")
for i in range(len(fitsimages)):
    myim2.eazy_importfits(fitsimages[i],defaultaxes=False)

# find imported images
image_co32 = glob.glob(dir_data+"data/"+galname+"*co32*image*")[0]



### step 2/10: Kelvin to Jansky conversion
print("### step 2/10: Kelvin to Jansky conversion")

bunit = imhead(image_co32,"list")["bunit"]
synsbeam21 = imhead(image_co32,"list")["beammajor"]["value"]
if bunit == "K": # CO(2-1) conversion if bunit = K
    myim2.easy_K2Jy(image_co32,synsbeam21,230.53800)
    image_co32 = image_co32 + ".jy"
else:
    print("# skip easy_K2Jy for the CO(2-1) data")



### step 3/10: imregrid
print("### step 3/10: imregrid")

pbimage = glob.glob(dir_data+"data/"+galname+"*pb.image")[0]
myim2.easy_imregrid(pbimage,image_co32,False) # pbimage
pbimage = pbimage + ".regrid"



### step 4/10: imsmooth
print("### step 4/10: imsmooth")

beam_mask = beam_size * increment_mask # beam size for the masking
myim2.easy_imsmooth(image_co32,beam_mask,False) # co32



### mv the cubes to the working directory
os.system("mkdir "+dir_data+galname)
os.system("mv "+dir_data+"data/"+galname+"*32*smooth "\
          +dir_data+galname+"/"+galname+"_co32_"+suffix+".cube")



### step 6/10: create CO(2-1) cube mask
print("### step 6/10: create CO(2-1) cube mask")

cube_co32 = glob.glob(dir_data+galname+"/"\
                       +galname+"*_co32_"+suffix+".cube")[0]
thres_co32 = rms_co32 * increment_mask * thres_masking
outmask_co32=cube_co32.replace(".cube",".mask")
myim2.createmask(cube_co32,thres_co32,outmask_co32)

beamarea = myim2.beam_area(image_co32,increment_mask)
myim2.remove_smallmask(outmask_co32,beamarea,pixelmin)



### mv to working directory
os.system("rm -rf "+cube_co32)
os.system("mv "+image_co32+" "+cube_co32)

print("### step 9/10: immoments")
myim2.moment_maps(cube_co32,chans,outmask_co32,rms_co32*thres_mom)



### pbmask
print("### step 10/10: pb mask at " + str(pbcut))


mask_pb = dir_data+galname+"/"+galname+"_pb_"+suffix+".mask"
peak = imhead(pbimage,mode="list")["datamax"]
myim2.createmask(pbimage,peak*pbcut,mask_pb)

os.chdir(dir_data+galname)
ia.open(glob.glob("*pb*mask")[0])
ia.calcmask(mask=glob.glob("*pb*mask")[0]+">0",
            name=glob.glob("*pb*mask")[0]+".2")
ia.close()
os.chdir("/Users/saito/data/mycasa_scripts/scripts_image_phangs2")


images_moment = glob.glob(cube_co32 + ".moment*")
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


