import os
import sys
import glob
import datetime

a=datetime.datetime.now()

# parameter
suffix = "sim04"
galname = "model"
do_steps = [0,1,2,3]
# 0: 7m-only
# 1: CDF (TP as a model)
# 2: CAF (feather)
# 3: CBF (tp2vis)
robust = 0.5
mask = ""
width = "" # "2.6km/s"
chans = "" # "139" # ""
chans_vel = "" # "1561.29km/s" # "1450km/s"
nchan = 1 # 96
niter = 500000 # 1
thres_mask = 1.
thres_clean = "0.3Jy"

#mask = "../"+galname+"_data/"+galname+"_co21_clean_mask.image2"
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
    done = glob.glob("../"+galname+"_7m_"+suffix+"/")
    if not done:
        os.system("mkdir ../"+galname+"_7m_"+suffix+"/")
    else:
        os.system("rm -rf ../"+galname+"_7m_"+suffix+"/*")

if 1 in do_steps:
    done = glob.glob("../"+galname+"_cdf_"+suffix+"/")
    if not done:
        os.system("mkdir ../"+galname+"_cdf_"+suffix+"/")
    else:
        os.system("rm -rf ../"+galname+"_cdf_"+suffix+"/*")

if 2 in do_steps:
    done = glob.glob("../"+galname+"_caf_"+suffix+"/")
    if not done:
        os.system("mkdir ../"+galname+"_caf_"+suffix+"/")
    else:
        os.system("rm -rf ../"+galname+"_caf_"+suffix+"/*")

if 3 in do_steps:
    done = glob.glob("../"+galname+"_cbf_"+suffix+"/")
    if not done:
        os.system("mkdir ../"+galname+"_cbf_"+suffix+"/")
    else:
        os.system("rm -rf ../"+galname+"_cbf_"+suffix+"/*")

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
    outputname_start_tmp = "../"+galname+"_7m_"+suffix+"/_tmp_"+galname+"_tp_co21.startmodel"
    # create TP startmodel
    os.system("rm -rf "+outputname_start_tmp)
    imregrid(imagename = glob.glob("../"+suffix+"/*sd*skymodel")[0],
	     template = outputname_7m+"na.pb",
             output = outputname_start_tmp)
    size_pix = abs(imhead(outputname_start_tmp,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    bmaj = imhead(outputname_start_tmp,mode="list")["beammajor"]["value"] # arcsec
    bmin = imhead(outputname_start_tmp,mode="list")["beamminor"]["value"] # arcsec
    beamarea_tp = (bmaj*bmin*np.pi) / (4*np.log(2)) / area_pix_arcsec

    outputname_start = "../"+galname+"_7m_"+suffix+"/"+galname+"_tp_co21.startmodel"
    os.system("rm -rf "+outputname_start)
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp2"))
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp3"))

    immath(imagename = outputname_start_tmp,
           mode = "evalexpr",
	   expr = "iif(IM0>="+str(thres_mask)+",1.0,0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp3"))

    outputname = "../"+galname+"_7m_"+suffix+"/"+galname+"_7m_only_co21_"
    os.system("rm -rf "+outputname+wt+"*")
    tclean(vis = "../"+suffix+"/"+suffix+".aca.cycle5.ms",
           imagename = outputname+wt,
           field = "",
           specmode = "cube",
           width = width,
           start = chans_vel,
           restfreq = "230.53800GHz",
           outframe = "LSRK",
           niter = niter,
	   gain=0.2,
           threshold = thres_clean,
           cyclefactor = 4,
           interactive = False,
           imsize = 256,
           cell = "1.0arcsec",
           phasecenter = "ICRS 12h21m54.9s +04d28m25s",
           weighting = weighting,
           robust = robust,
           gridder = "mosaic",
           deconvolver = "multiscale",
	   scales = [0,2,5],
           nchan = nchan,
           #cycleniter = 50,
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
    outputname_7m = "../"+galname+"_7m_"+suffix+"/"+galname+"_7m_only_co21_"
    outputname_start_tmp = "../"+galname+"_cdf_"+suffix+"/_tmp_"+galname+"_tp_co21.startmodel"
    # create TP startmodel
    os.system("rm -rf "+outputname_start_tmp)
    imregrid(imagename = glob.glob("../"+suffix+"/*sd*skymodel")[0],
	     template = outputname_7m+wt+".pb",
             output = outputname_start_tmp)

    size_pix = abs(imhead(outputname_start_tmp,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    bmaj = imhead(outputname_start_tmp,mode="list")["beammajor"]["value"] # arcsec
    bmin = imhead(outputname_start_tmp,mode="list")["beamminor"]["value"] # arcsec
    beamarea_tp = (bmaj*bmin*np.pi) / (4*np.log(2)) / area_pix_arcsec

    outputname_start = "../"+galname+"_cdf_"+suffix+"/"+galname+"_tp_co21.startmodel"
    os.system("rm -rf "+outputname_start)
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp2"))
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp3"))
    immath(imagename = [outputname_start_tmp,
                        outputname_7m+wt+".pb"],
           mode = "evalexpr",
	   expr = "iif(IM1>=0.5,IM0*IM1/" + str(beamarea_tp) + ",0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp2"))

    immath(imagename = outputname_start_tmp,
           mode = "evalexpr",
	   expr = "iif(IM0>="+str(thres_mask)+",1.0,0.0)",
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
    outputname = "../"+galname+"_cdf_"+suffix+"/"+galname+"_7m+tp+cdf_co21_"
    os.system("rm -rf "+outputname+wt+"*")
    tclean(vis = "../"+suffix+"/"+suffix+".aca.cycle5.ms",
           imagename = outputname+wt,
           field = "",
           specmode = "cube",
           width = width,
           start = chans_vel,
           restfreq = "230.53800GHz",
           outframe = "LSRK",
           niter = niter,
	   gain=0.2,
           threshold = thres_clean,
           cyclefactor = 4,
           interactive = False,
           imsize = 256,
           cell = "1.0arcsec",
           phasecenter = "ICRS 12h21m54.9s +04d28m25s",
           weighting = "briggs",
           robust = 0.5,
           gridder = "mosaic",
           deconvolver = "multiscale",
	   scales = [0,2],
           nchan = nchan,
           #cycleniter = 50,
           usemask = "user",
           restoringbeam = "common",
           startmodel = outputname_start,
           mask = outputname_start_tmp.replace("tmp","tmp3"))

    outfile = "../"+galname+"_cdf_"+suffix+"/"+galname+"_tp_co21.image.depb"
    os.system("rm -rf " + outfile)
    immath(imagename = [outputname_start_tmp, outputname_7m+wt+".pb"],
           expr = "IM0*IM1",
           outfile= outfile)

    imagename = "../"+galname+"_cdf_"+suffix+"/"+galname+"_7m+tp+cdf_co21_"+wt+".feather"
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
    outputname_7m = "../"+galname+"_7m_"+suffix+"/"+galname+"_7m_only_co21_"
    outputname_start_tmp = "../"+galname+"_caf_"+suffix+"/_tmp_"+galname+"_tp_co21.image"
    # create TP startmodel
    os.system("rm -rf "+outputname_start_tmp)
    imregrid(imagename = glob.glob("../"+suffix+"/*sd*skymodel")[0],
	     template = outputname_7m+wt+".pb",
             output = outputname_start_tmp)

    ####
    ####
    #### immath operand mismatch

    outfile = "../"+galname+"_caf_"+suffix+"/"+galname+"_tp_co21.image.depb"
    os.system("rm -rf " + outfile)
    immath(imagename = [outputname_start_tmp, outputname_7m+wt+".pb"],
           expr = "IM0*IM1",
           outfile= outfile)

    imagename = "../"+galname+"_caf_"+suffix+"/"+galname+"_7m+tp+caf_co21_"+wt+".image"
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

    outputname_7m = "../"+galname+"_7m_"+suffix+"/"+galname+"_7m_only_co21_"
    outputname_start_tmp = "../"+galname+"_cbf_"+suffix+"/_tmp_"+galname+"_tp_co21.startmodel"
    # create TP startmodel
    os.system("rm -rf "+outputname_start_tmp)
    imregrid(imagename = glob.glob("../"+suffix+"/*sd*skymodel")[0],
	     template = outputname_7m+wt+".pb",
	     output = outputname_start_tmp)


    size_pix = abs(imhead(outputname_start_tmp,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    bmaj = imhead(outputname_start_tmp,mode="list")["beammajor"]["value"] # arcsec
    bmin = imhead(outputname_start_tmp,mode="list")["beamminor"]["value"] # arcsec
    beamarea_tp = (bmaj*bmin*np.pi) / (4*np.log(2)) / area_pix_arcsec

    outputname_start = "../"+galname+"_cbf_"+suffix+"/"+galname+"_tp_co21.startmodel"
    os.system("rm -rf "+outputname_start)
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp2"))
    os.system("rm -rf "+outputname_start_tmp.replace("tmp","tmp3"))
    immath(imagename = [outputname_start_tmp,
                        outputname_7m+wt+".pb"],
           mode = "evalexpr",
	   expr = "iif(IM1>=0.5,IM0*IM1/" + str(beamarea_tp) + ",0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp2"))

    immath(imagename = outputname_start_tmp,
           mode = "evalexpr",
	   expr = "iif(IM0>="+str(thres_mask)+",1.0,0.0)",
	   outfile = outputname_start_tmp.replace("tmp","tmp3"))

    outputname = "../"+galname+"_cbf_"+suffix+"/"+galname+"_7m+tp+cbf_co21_"
    os.system("rm -rf "+outputname+wt+"*")
    tclean(vis = ["../"+suffix+"/"+suffix+".aca.cycle5.ms",
                  glob.glob("../"+suffix+"/*tp*.ms")[0]],
           imagename = outputname+wt,
           field = "",
           specmode = "cube",
           width = width,
           start = chans_vel,
           restfreq = "230.53800GHz",
           outframe = "LSRK",
           niter = niter,
	   gain=0.2,
           threshold = thres_clean,
           cyclefactor = 4,
           interactive = False,
           imsize = 256,
           cell = "1.0arcsec",
           phasecenter = "ICRS 12h21m54.9s +04d28m25s",
           weighting = weighting,
           robust = robust,
           gridder = "mosaic",
           deconvolver = "multiscale",
	   scales = [0,4],
           nchan = nchan,
           #cycleniter = 50,
           usemask = "user",
           restoringbeam = "common",
           startmodel = "",
           mask = outputname_start_tmp.replace("tmp","tmp3"))

    os.system("rm -rf "+outputname+wt+".image.pbcor")
    impbcor(imagename = outputname+wt+".image",
            outfile = outputname+wt+".image.pbcor",
	    pbimage = outputname+wt+".pb")

e=datetime.datetime.now()

print("# 7m-only = "+str(b-a))
print("# CDF(TPmodel) and CDF+CAF(TPmodel+father) = "+str(c-b))
print("# CAF(feather) = "+str(d-c))
print("# CBF(tp2vis) = "+str(e-d))

os.system("rm -rf *.last")
