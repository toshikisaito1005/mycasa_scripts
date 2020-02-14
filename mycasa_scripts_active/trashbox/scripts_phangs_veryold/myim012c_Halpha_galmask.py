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
dir_mask = dir_data + "galmasks/"
dir_data1 = dir_data + galname + "/"
im_mask = galname+"_400pc_CO95_HA95_overlap_mask.image"

im_co10 = glob.glob(dir_data1+galname+"*co10*"+suffix+"*mom*0")[0]
im_co21 = glob.glob(dir_data1+galname+"*co21*"+suffix+"*mom*0")[0]
m2_co10 = glob.glob(dir_data1+galname+"*co10*"+suffix+"*mom*2")[0]
m2_co21 = glob.glob(dir_data1+galname+"*co21*"+suffix+"*mom*2")[0]
m8_co10 = glob.glob(dir_data1+galname+"*co10*"+suffix+"*mom*8")[0]
m8_co21 = glob.glob(dir_data1+galname+"*co21*"+suffix+"*mom*8")[0]
im_maskin = dir_data1+"halpha_co.maskin"
im_maskout = dir_data1+"halpha_co.maskout"
im_mask = dir_mask+im_mask



### step 1: create 1/0 and 0/1 masks
print("step 1: create 1/0 and 0/1 masks")
os.system("rm -rf " + im_maskin)
os.system("cp -r " + im_mask + " " + im_maskin)
os.system("rm -rf " + im_maskout)
immath(imagename = im_maskin,
       mode = "evalexpr",
       expr = "abs(IM0 - 1)",
       outfile = im_maskout)


### step 2: masking
# moment 0
print("step 2: masking")
outfile = im_co10 + ".maskin"
os.system("rm -rf " + outfile)
immath(imagename = [im_co10, im_maskin],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = im_co10 + ".maskout"
os.system("rm -rf " + outfile)
immath(imagename = [im_co10, im_maskout],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = im_co21 + ".maskin"
os.system("rm -rf " + outfile)
immath(imagename = [im_co21, im_maskin],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = im_co21 + ".maskout"
os.system("rm -rf " + outfile)
immath(imagename = [im_co21, im_maskout],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

### moment 2
outfile = m2_co10 + ".maskin"
os.system("rm -rf " + outfile)
immath(imagename = [m2_co10, im_maskin],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = m2_co10 + ".maskout"
os.system("rm -rf " + outfile)
immath(imagename = [m2_co10, im_maskout],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = m2_co21 + ".maskin"
os.system("rm -rf " + outfile)
immath(imagename = [m2_co21, im_maskin],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = m2_co21 + ".maskout"
os.system("rm -rf " + outfile)
immath(imagename = [m2_co21, im_maskout],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

### moment 8
outfile = m8_co10 + ".maskin"
os.system("rm -rf " + outfile)
immath(imagename = [m8_co10, im_maskin],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = m8_co10 + ".maskout"
os.system("rm -rf " + outfile)
immath(imagename = [m8_co10, im_maskout],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = m8_co21 + ".maskin"
os.system("rm -rf " + outfile)
immath(imagename = [m8_co21, im_maskin],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = m8_co21 + ".maskout"
os.system("rm -rf " + outfile)
immath(imagename = [m8_co21, im_maskout],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

