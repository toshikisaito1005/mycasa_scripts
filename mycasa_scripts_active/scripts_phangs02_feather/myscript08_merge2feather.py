import numpy as np
import os
import glob
sys.path.append(os.getcwd())
import toolsPhangs02Feather as tl


dir_data = "/Users/saito/data/myproj_published/proj_phangs02_feather/"
#dir_data = "../"
projects = ["test06","test07"]
beamsize = "2.5arcsec"
tpbeam = "28.615arcsec"
dir_name = "test0607"


###############################
### main
###############################
### preparation
# mkdir
dir_working = dir_data + dir_name + "_merge2feather/"
os.system("rm -rf " + dir_working)
os.mkdir(dir_working)

# import data
image_south, pb_south = tl.import_data2(dir_working,dir_data,projects[0])
image_north, pb_north = tl.import_data2(dir_working,dir_data,projects[1])
tpimage = dir_working + dir_name + "_skymodel.tpimage"
os.system("cp -r " + glob.glob(dir_data + "data_model/*.tpimage")[0] + " " + tpimage)

# convolved skymodel
skymodel1 = glob.glob(dir_data + projects[0] + "/*skymodel")[0]
skymodel2 = dir_working + dir_name + "_skymodel.smooth_tmp"
imsmooth(imagename = skymodel1,
         targetres = True,
         major = beamsize,
         minor = beamsize,
         pa = "0deg",
         outfile = skymodel2)

skymodel3 = dir_working + dir_name + "_skymodel.smooth"
imregrid(imagename = skymodel2,
         template = image_south,
         output = skymodel3)
makemask(mode="delete", inpmask=skymodel3+":mask0")
os.system("rm -rf " + skymodel2)

# merge 12m+7m image
intimage_pbcor = dir_working + dir_name + "_12m+7m_merge.image.pbcor"
tl.merge_mosaic(image_south,
                 image_north,
                 pb_south,
                 pb_north,
                 output = intimage_pbcor)

tl.addbeamheader_round(intimage_pbcor,beamsize)

outfile = intimage_pbcor.replace(".image.pbcor",".diff")
os.system("rm -rf " + outfile)
immath(imagename = [intimage_pbcor,skymodel3],
       expr = "IM0-IM1",
       outfile = outfile)

# import merge pb from test08
os.system("cp -r " + glob.glob(dir_data + "test08/*12m+7m*.pb")[0] + " " \
          + dir_working + "test0607_12m+7m_merge.pb")

# PbcorrFirst
featherimage1 = intimage_pbcor.replace("12m+7m_merge","merge_then_pbcorrfirst")
featherimage = featherimage1.replace(".pbcor","")
feather(imagename = featherimage,
        highres = intimage_pbcor,
        lowres = tpimage,
        sdfactor = 1.0,
        effdishdiam = -0.1,
        lowpassfiltersd = False)

outfile = featherimage.replace(".image",".diff")
os.system("rm -rf " + outfile)
immath(imagename = [featherimage,skymodel3],
       expr = "IM0-IM1",
       outfile = outfile)


os.system("rm -rf *.last")
for i in range(len(projects)):
    data_copy = dir_working + projects[i] + "_*"
    os.system("rm -rf " + data_copy)
