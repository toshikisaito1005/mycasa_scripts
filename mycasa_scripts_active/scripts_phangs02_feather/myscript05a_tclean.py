import os
import sys
import glob
import datetime

dir_data = "/Users/saito/data/myproj_published/proj_phangs02_feather/"
#dir_data = "../"

"""
projs = ["test01","test02","test03","test04","test05"]
masks = [dir_data+"data/ngc0628.mask",
         dir_data+"data/ngc0628.mask",
         dir_data+"data/ngc0628.mask",
         dir_data+"data_model/gauss.mask",
         dir_data+"data_model/gauss.mask"]
thres = [0.005,0.005,0.005,0.2,0.2]
"""

projs = ["test06","test07"]
masks = [dir_data+"data_model/gauss.mask",
         dir_data+"data_model/gauss.mask"]
thres = [0.001,0.001]

for i in range(len(projs)):
    mask = masks[i]
    print("### working on " + projs[i])
    vis1 = glob.glob(dir_data + projs[i] + "/" + projs[i] + ".aca.cycle5.ms")[0]
    vis2 = glob.glob(dir_data + projs[i] + "/" + projs[i] + ".alma.cycle5.1.ms")[0]
    vis = [vis1,vis2]

    # 12m+7m
    print("# multiscale...")
    imagename = dir_data + projs[i] + "/" + projs[i] + "_12m+7m_br"
    os.system("rm -rf " + imagename + "*")
    tclean(vis = vis,
           imagename = imagename,
           field = "",
           specmode = "cube",
           width = 1,
           start = "",
           niter = 100000000,
           gain = 0.3,
           threshold = str(thres[i])+"Jy",
           cyclefactor = 5,
           interactive = False,
           imsize = 1024,
           cell = "0.4arcsec",
           phasecenter = "J2000 01:36:41.735 15.46.59.350",
           weighting = "briggs",
           robust = 0.5,
           gridder = "mosaic",
           deconvolver = "multiscale",
           scales = [0,8,20],
           nchan = 1,
           cycleniter = 30,
           usemask = "user",
           mask = mask,
           pblimit = 0.25)

    print("# singlescale...")
    tclean(vis = vis,
           imagename = imagename,
           field = "",
           specmode = "cube",
           width = 1,
           start = "",
           niter = 100000000,
           gain = 0.1,
           threshold = str(thres[i]/4.)+"Jy",
           cyclefactor = 5,
           interactive = False,
           imsize = 1024,
           cell = "0.4arcsec",
           phasecenter = "J2000 01:36:41.735 15.46.59.350",
           weighting = "briggs",
           robust = 0.5,
           gridder = "mosaic",
           deconvolver = "hogbom",
           nchan = 1,
           cycleniter = 50,
           usemask = "user",
           pblimit = 0.25)

os.system("rm -rf *.last")
