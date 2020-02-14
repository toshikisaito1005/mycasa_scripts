import os
import sys
import glob
import datetime

dir_data = "/Users/saito/data/myproj_published/proj_phangs02_feather/" # laptop
#dir_data = "../" # astro-node7
projs = ["test08"]

for i in range(len(projs)):
    print("### working on " + projs[i])
    vis1 = glob.glob(dir_data + projs[i] + "/" + projs[i] + ".aca.cycle5.ms")[0]
    vis2 = glob.glob(dir_data + projs[i] + "/" + projs[i] + ".alma.cycle5.1.ms")[0]
    vis = [vis1,vis2]

    # 12m+7m
    print("# 12m+7m dirty map...")
    imagename = dir_data + projs[i] + "/" + projs[i] + "_12m+7m_br_dirty"
    os.system("rm -rf " + imagename + "*")
    tclean(vis = vis,
           imagename = imagename,
           field = "",
           specmode = "cube",
           width = 1,
           start = "",
           niter = 0,
           gain = 0.05,
           threshold = "0.2Jy",
           cyclefactor = 4,
           interactive = False,
           imsize = 1024,
           cell = "0.4arcsec",
           phasecenter = "J2000 01:36:41.735 15.46.59.350",
           weighting = "briggs",
           robust = 0.5,
           gridder = "mosaic",
           deconvolver = "multiscale",
           scales = [0,2,5],
           nchan = 1,
           cycleniter = 50,
           usemask = "user",
           pblimit = 0.25)

    # 7m
    print("# 7m-only dirty map...")
    imagename = dir_data + projs[i] + "/" + projs[i] + "_7m_br_dirty"
    os.system("rm -rf " + imagename + "*")
    tclean(vis = vis1,
           imagename = imagename,
           field = "",
           specmode = "cube",
           width = 1,
           start = "",
           niter = 0,
           gain = 0.05,
           threshold = "0.2Jy",
           cyclefactor = 4,
           interactive = False,
           imsize = 512,
           cell = "1.0arcsec",
           phasecenter = "J2000 01:36:41.735 15.46.59.350",
           weighting = "briggs",
           robust = 0.5,
           gridder = "mosaic",
           deconvolver = "multiscale",
           scales = [0,2,5],
           nchan = 1,
           cycleniter = 50,
           usemask = "user")

    # 12m
    print("# 12m-only dirty map...")
    imagename = dir_data + projs[i] + "/" + projs[i] + "_12m_br_dirty"
    os.system("rm -rf " + imagename + "*")
    tclean(vis = vis2,
           imagename = imagename,
           field = "",
           specmode = "cube",
           width = 1,
           start = "",
           niter = 0,
           gain = 0.05,
           threshold = "0.2Jy",
           cyclefactor = 4,
           interactive = False,
           imsize = 1024,
           cell = "0.4arcsec",
           phasecenter = "J2000 01:36:41.735 15.46.59.350",
           weighting = "briggs",
           robust = 0.5,
           gridder = "mosaic",
           deconvolver = "multiscale",
           scales = [0,2,5],
           nchan = 1,
           cycleniter = 50,
           usemask = "user",
           pblimit = 0.25)

os.system("rm -rf *.last")
