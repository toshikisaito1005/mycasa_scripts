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
dir_name = "test0607_feather2merge/"


###############################
### main
###############################
### preparation
# mkdir
dir_working = dir_data + dir_name
os.system("rm -rf " + dir_working)
os.mkdir(dir_working)

# import data
ff_south, pf_south, pb_south = tl.import_data(dir_working,dir_data,projects[0]) # southern mosaic
ff_north, pf_north, pb_north = tl.import_data(dir_working,dir_data,projects[1]) # northern mosaic

# convolved skymodel
skymodel1 = glob.glob(dir_data + "test06/*skymodel")[0]
skymodel2 = dir_working + "test0607_skymodel.smooth_tmp"
os.system("rm -rf " + skymodel2)
imsmooth(imagename = skymodel1,
         targetres = True,
         major = beamsize,
         minor = beamsize,
         pa = "0deg",
         outfile = skymodel2)

skymodel3 = dir_working + "test0607_skymodel.smooth"
imregrid(imagename = skymodel2,
         template = ff_south,
         output = skymodel3)
makemask(mode="delete", inpmask=skymodel3+":mask0")
os.system("rm -rf " + skymodel2)

# featherfirst then merge
tl.merge_pbcored_mosaic(ff_south,
                        ff_north,
                        pb_south,
                        pb_north,
                        output = dir_working + "test0607_featherfirst_then_merge.image")

outfile = dir_working + "test0607_featherfirst_then_merge.diff"
os.system("rm -rf " + outfile)
immath(imagename = [dir_working + "test0607_featherfirst_then_merge.image",skymodel3],
       expr = "IM0-IM1",
       outfile = outfile)

# pbcorrfirst then merge
tl.merge_pbcored_mosaic(pf_south,
                        pf_north,
                        pb_south,
                        pb_north,
                        output = dir_working + "test0607_pbcorrfirst_then_merge.image")

outfile = dir_working + "test0607_pbcorrfirst_then_merge.diff"
os.system("rm -rf " + outfile)
immath(imagename = [dir_working + "test0607_pbcorrfirst_then_merge.image",skymodel3],
       expr = "IM0-IM1",
       outfile = outfile)

# import merge pb from test08
os.system("cp -r " + glob.glob(dir_data + "test08/*12m+7m*.pb")[0] + " " \
          + dir_working + "test0607_12m+7m_merge.pb")

os.system("rm -rf *.last")
for i in range(len(projects)):
    data_copy = dir_working + projects[i] + "_*"
    os.system("rm -rf " + data_copy)
