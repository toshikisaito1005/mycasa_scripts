import os
import sys
import glob
import datetime

a=datetime.datetime.now()

# parameter
do_steps = [0,1,2,3]
# 0: 7m-only
# 1: CDF (TP as a model)
# 2: CAF (feather)
# 3: CBF (tp2vis)
robust = 2.0
mask = ""
width = "2.6km/s" # "2.6km/s" # 1
chans = "139" # "139" # ""
chans_vel = "1561.29km/s" # "1561.29km/s" # "1450km/s"
nchan = 1 # 1 # 96
niter = 500000 # 1

#mask = "../ngc4303_data/ngc4303_co21_clean_mask.image2"
# step 1 takes ~20 minutes
# step 2 takes ~20 minutes
# step 3 takes less than 1 minute

if robust == 2.0:
    weighting = "natural"
    wt = "na"
elif robust == -2.0:
    weighting = "uniform"
    wt = "un"
else:
    weighting = "briggs"
    wt = "br"

# mkdir
if 0 in do_steps:
    done = glob.glob("../ngc4303_7m/")
    if not done:
        os.system("mkdir ../ngc4303_7m/")
    else:
        os.system("rm -rf ../ngc4303_7m/*")

if 1 in do_steps:
    done = glob.glob("../ngc4303_cdf/")
    if not done:
        os.system("mkdir ../ngc4303_cdf/")
    else:
        os.system("rm -rf ../ngc4303_cdf/*")

if 2 in do_steps:
    done = glob.glob("../ngc4303_caf/")
    if not done:
        os.system("mkdir ../ngc4303_caf/")
    else:
        os.system("rm -rf ../ngc4303_caf/*")

if 3 in do_steps:
    done = glob.glob("../ngc4303_cbf/")
    if not done:
        os.system("mkdir ../ngc4303_cbf/")
    else:
        os.system("rm -rf ../ngc4303_cbf/*")

# deconvolution 7m-only
if 0 in do_steps:
    if robust == 2.0:
        weighting = "natural"
	wt = "na"
    elif robust == -2.0:
        weighting = "uniform"
	wt = "un"
    else:
        weighting = "briggs"
	wt = "br"

    outputname_7m = "../ngc4303_7m/ngc4303_7m_only_co21_"
    outputname_start_tmp = "../ngc4303_7m/_tmp_ngc4303_tp_co21.startmodel"
    # create TP startmodel
    os.system("rm -rf "+outputname_start_tmp)
    imsubimage(imagename = "../ngc4303_data/ngc4303_tp_co21.trans",
               chans = chans,
               outfile = outputname_start_tmp)

    size_pix = abs(imhead(outputname_start_tmp,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    bmaj = imhead(outputname_start_tmp,mode="list")["beammajor"]["value"] # arcsec
    bmin = imhead(outputname_start_tmp,mode="list")["beamminor"]["value"] # arcsec
    beamarea_tp = (bmaj*bmin*np.pi) / (4*np.log(2)) / area_pix_arcsec

    outputname_start = "../ngc4303_7m/ngc4303_tp_co21.startmodel"
    os.system("rm -rf "+outputname_start)
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp2"))
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp3"))

    immath(imagename = outputname_start_tmp,
           mode = "evalexpr",
	   expr = "iif(IM0>=0.5"+",1.0,0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp3"))


    outputname = "../ngc4303_7m/ngc4303_7m_only_co21_"
    os.system("rm -rf "+outputname+wt+"*")
    tclean(vis = "../ngc4303_data/ngc4303_7m_co21.ms",
           imagename = outputname+wt,
           field = "NGC4303",
           specmode = "cube",
           width = width,
           start = chans_vel,
           restfreq = "230.53800GHz",
           outframe = "LSRK",
           niter = niter,
           threshold = "50mJy",
           cyclefactor = 4,
           interactive = False,
           imsize = 256,
           cell = "1.0arcsec",
           phasecenter = 26,
           weighting = weighting,
           robust = robust,
           gridder = "mosaic",
           deconvolver = "multiscale",
	   scales = [0,2],
           nchan = nchan,
           cycleniter = 500,
           usemask = "user",
           restoringbeam = "common",
           startmodel = "",
           mask = outputname_start_tmp.replace("tmp","tmp3"))

    os.system("rm -rf "+outputname+wt+".image.pbcor")
    impbcor(imagename = outputname+wt+".image",
            outfile = outputname+wt+".image.pbcor",
	    pbimage = outputname+wt+".pb")

b=datetime.datetime.now()

### combine TP during deconvolution
if 1 in do_steps:
    outputname_7m = "../ngc4303_7m/ngc4303_7m_only_co21_"
    outputname_start_tmp = "../ngc4303_cdf/_tmp_ngc4303_tp_co21.startmodel"
    # create TP startmodel
    if nchan==1:
        os.system("rm -rf "+outputname_start_tmp)
        imsubimage(imagename = "../ngc4303_data/ngc4303_tp_co21.trans",
                   chans = chans,
                   outfile = outputname_start_tmp)
    else:
        os.system("rm -rf "+outputname_start_tmp)
	imregrid(imagename = "../ngc4303_data/ngc4303_tp_co21.trans",
	         template = outputname_7m+wt+".pb",
		 output = outputname_start_tmp)

    size_pix = abs(imhead(outputname_start_tmp,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    bmaj = imhead(outputname_start_tmp,mode="list")["beammajor"]["value"] # arcsec
    bmin = imhead(outputname_start_tmp,mode="list")["beamminor"]["value"] # arcsec
    beamarea_tp = (bmaj*bmin*np.pi) / (4*np.log(2)) / area_pix_arcsec

    outputname_start = "../ngc4303_cdf/ngc4303_tp_co21.startmodel"
    os.system("rm -rf "+outputname_start)
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp2"))
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp3"))
    immath(imagename = [outputname_start_tmp,
                        outputname_7m+wt+".pb"],
           mode = "evalexpr",
	   expr = "iif(IM1>=0.5,IM0*IM1/" + str(beamarea_tp) + ",0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp2"))

    immath(imagename = outputname_start_tmp.replace("tmp","tmp2"),
           mode = "evalexpr",
	   expr = "iif(IM0>=0.5/"+str(beamarea_tp)+",1.0,0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp3"))

    immath(imagename = outputname_start_tmp.replace("tmp","tmp2"),
           mode = "evalexpr",
	   expr = "iif(IM0>=0.5/"+str(beamarea_tp)+",IM0,0.0)", # TP rms = 0.1 Jy/beam
	   outfile = outputname_start)

    imhead(imagename = outputname_start,
           mode = "put",
	   hdkey = "bunit",
	   hdvalue = "Jy/pixel")

    # tclean
    outputname = "../ngc4303_cdf/ngc4303_7m+tp+cdf_co21_"
    os.system("rm -rf "+outputname+wt+"*")
    tclean(vis = "../ngc4303_data/ngc4303_7m_co21.ms",
           imagename = outputname+wt,
           field = "NGC4303",
           specmode = "cube",
           width = width,
           start = chans_vel,
           restfreq = "230.53800GHz",
           outframe = "LSRK",
           niter = niter,
           threshold = "50mJy",
           cyclefactor = 4,
           interactive = False,
           imsize = 256,
           cell = "1.0arcsec",
           phasecenter = 26,
           weighting = "briggs",
           robust = 0.5,
           gridder = "mosaic",
           deconvolver = "multiscale",
	   scales = [0,2],
           nchan = nchan,
           cycleniter = 500,
           usemask = "user",
           restoringbeam = "common",
           startmodel = outputname_start,
           mask = outputname_start_tmp.replace("tmp","tmp3"))

    outfile = "../ngc4303_cdf/ngc4303_tp_co21.image.depb"
    os.system("rm -rf " + outfile)
    immath(imagename = [outputname_start_tmp, outputname_7m+wt+".pb"],
           expr = "IM0*IM1",
           outfile= outfile)

    imagename = "../ngc4303_cdf/ngc4303_7m+tp+cdf_co21_"+wt+".feather"
    os.system("rm -rf " + imagename)
    feather(imagename = imagename,
            highres = outputname+wt+".image",
	    lowres = outfile)

    os.system("rm -rf "+outputname+wt+".feather.pbcor")
    impbcor(imagename = imagename,
            outfile = imagename+".pbcor",
	    pbimage = outputname+wt+".pb")

c=datetime.datetime.now()

### combine TP after deconvolution
if 2 in do_steps:
    outputname_7m = "../ngc4303_7m/ngc4303_7m_only_co21_"
    outputname_start_tmp = "../ngc4303_caf/_tmp_ngc4303_tp_co21.image"
    # create TP startmodel
    if nchan==1:
        os.system("rm -rf "+outputname_start_tmp)
        imsubimage(imagename = "../ngc4303_data/ngc4303_tp_co21.trans",
                   chans = chans,
                   outfile = outputname_start_tmp)
    else:
        os.system("rm -rf "+outputname_start_tmp)
	imregrid(imagename = "../ngc4303_data/ngc4303_tp_co21.trans",
	         template = outputname_7m+wt+".pb",
		 output = outputname_start_tmp)

    outfile = "../ngc4303_caf/ngc4303_tp_co21.image.depb"
    os.system("rm -rf " + outfile)
    immath(imagename = [outputname_start_tmp, outputname_7m+wt+".pb"],
           expr = "IM0*IM1",
           outfile= outfile)

    imagename = "../ngc4303_caf/ngc4303_7m+tp+caf_co21_"+wt+".image"
    os.system("rm -rf " + imagename)
    feather(imagename = imagename,
            highres = outputname_7m+wt+".image",
	    lowres = outfile)

    impbcor(imagename = imagename,
            outfile = imagename+".pbcor",
            pbimage = outputname_7m+wt+".pb")

d=datetime.datetime.now()

# tp2vis
if 3 in do_steps:
    if robust == 2.0:
        weighting = "natural"
	wt = "na"
    elif robust == -2.0:
        weighting = "uniform"
	wt = "un"
    else:
        weighting = "briggs"
	wt = "br"

    outputname_7m = "../ngc4303_7m/ngc4303_7m_only_co21_"
    outputname_start_tmp = "../ngc4303_cbf/_tmp_ngc4303_tp_co21.startmodel"
    # create TP startmodel
    if nchan==1:
        os.system("rm -rf "+outputname_start_tmp)
        imsubimage(imagename = "../ngc4303_data/ngc4303_tp_co21.trans",
                   chans = chans,
                   outfile = outputname_start_tmp)
    else:
        os.system("rm -rf "+outputname_start_tmp)
	imregrid(imagename = "../ngc4303_data/ngc4303_tp_co21.trans",
	         template = outputname_7m+wt+".pb",
		 output = outputname_start_tmp)


    size_pix = abs(imhead(outputname_start_tmp,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    bmaj = imhead(outputname_start_tmp,mode="list")["beammajor"]["value"] # arcsec
    bmin = imhead(outputname_start_tmp,mode="list")["beamminor"]["value"] # arcsec
    beamarea_tp = (bmaj*bmin*np.pi) / (4*np.log(2)) / area_pix_arcsec

    outputname_start = "../ngc4303_cbf/ngc4303_tp_co21.startmodel"
    os.system("rm -rf "+outputname_start)
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp2"))
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp3"))
    immath(imagename = [outputname_start_tmp,
                        outputname_7m+wt+".pb"],
           mode = "evalexpr",
	   expr = "iif(IM1>=0.5,IM0*IM1/" + str(beamarea_tp) + ",0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp2"))

    immath(imagename = outputname_start_tmp.replace("tmp","tmp2"),
           mode = "evalexpr",
	   expr = "iif(IM0>=0.5/"+str(beamarea_tp)+",1.0,0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp3"))

    outputname = "../ngc4303_cbf/ngc4303_7m+tp+cbf_co21_"
    os.system("rm -rf "+outputname+wt+"*")
    tclean(vis = ["../ngc4303_data/ngc4303_7m_co21.ms",
                  "../ngc4303_data/ngc4303_tp_co21.ms"],
           imagename = outputname+wt,
           field = "",
           specmode = "cube",
           width = width,
           start = chans_vel,
           restfreq = "230.53800GHz",
           outframe = "LSRK",
           niter = niter,
           threshold = "50mJy",
           cyclefactor = 4,
           interactive = False,
           imsize = 256,
           cell = "1.0arcsec",
           phasecenter = 26,
           weighting = weighting,
           robust = robust,
           gridder = "mosaic",
           deconvolver = "multiscale",
	   scales = [0,4],
           nchan = nchan,
           cycleniter = 500,
           usemask = "user",
           restoringbeam = "common",
           startmodel = "",
           mask = outputname_start_tmp.replace("tmp","tmp3"))

    os.system("rm -rf "+outputname+wt+".image.pbcor")
    impbcor(imagename = outputname+wt+".image",
            outfile = outputname+wt+".image.pbcor",
	    pbimage = outputname+wt+".pb")


print(b-a)
print(c-b)
print(d-c)

os.system("rm -rf *.last")
