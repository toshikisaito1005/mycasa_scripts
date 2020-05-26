import os
import sys
import glob
import datetime

a=datetime.datetime.now()

### parameter
do_steps = [2]
robust = 0.5
width = "" # "2.6km/s"
chans = "" # "139" # ""
nchan = 1 # 96
niter = 500000 # 1
snr = 2.0

### function
def dirty_map(
  dir_sim,
  galname,
  wt,
  width,
  start,
  ra,
  dec,
  weighting,
  robust,
  dir_mask,
  imsize):
  outputname = dir_sim + "/dirty_" + galname + "_7m_"+wt
  os.system("rm -rf "+outputname+"*")
    tclean(vis = dir_sim + "/sim_" + galname + ".aca.cycle5.noisy.ms",
           imagename = outputname,
           field = "",
           specmode = "cube",
           width = width,
           start = start,
           restfreq = "230.53800GHz",
           outframe = "LSRK",
           niter = 0,
           threshold = "",
           cyclefactor = 4,
           interactive = False,
           imsize = imsize,
           cell = "1.0arcsec",
           phasecenter = "J2000 "+ra+" "+dec,
           weighting = weighting,
           robust = robust,
           gridder = "mosaic",
           deconvolver = "multiscale",
	       scales = [0,2,5],
           nchan = nchan,
           cycleniter = 50,
           usemask = "user",
           restoringbeam = "common",
           startmodel = "",
           mask = "")

    # masking dirty map
    os.system("rm -rf " + dir_sim + "/_tmp_inverse.mask")
    imregrid(imagename = dir_mask+galname+"_12m+7m+tp_co21_hybridmask.mask",
             template = outputname + ".image",
	     output = dir_sim + "/_tmp_inverse.mask")

    os.system("rm -rf " + dir_sim + "/inverse.mask")
    immath(imagename = dir_sim + "/_tmp_inverse.mask",
           mode = "evalexpr",
	   expr = "iif(IM0>=1,0,1)",
	   outfile = dir_sim + "/inverse.mask")

    os.system("rm -rf " + dir_sim + "/inverse.mask.fits")
    exportfits(imagename = dir_sim + "/inverse.mask",
               fitsimage = dir_sim + "/inverse.mask.fits")

    os.system("rm -rf " + dir_sim + "/inverse.mask")
    os.system("rm -rf inverse.mask")
    importfits(fitsimage = dir_sim + "/inverse.mask.fits",
               imagename = "inverse.mask",
               defaultaxes=True,
               defaultaxesvalues=["RA","Dec","Frequency","Stokes"])
    os.system("rm -rf " + dir_sim + "/inverse.mask.fits")

    rms = imstat(imagename = outputname + ".image",
                 mask = "inverse.mask")["rms"][0]

    return rms



def eazy_tclean(outputname,
                dir_sim,
                galname,
		wt,
		width,
		start,
		niter,
		thres_clean,
		ra,dec,
		weighting,
		robust,
		dir_mask,
		imsize,
		startmodel,
		tpms):
    """
    """
    if tpms==False:
        vis = dir_sim + "/sim_" + galname + ".aca.cycle5.ms"
    elif tpms==True:
        concat(vis = [dir_sim + "/sim_" + galname + ".aca.cycle5.ms",
	              dir_sim + "/sim_" + galname + ".sd.ms"],
               concatvis = dir_sim + "/sim_" + galname + ".concat.ms",
               freqtol = "50MHz")
        vis = dir_sim + "/sim_" + galname + ".concat.ms"

    print(vis)

    outputname = dir_sim + "/sim_" + galname + "_" + outputname + "_"+wt
    os.system("rm -rf "+outputname+"*")
    tclean(vis = vis,
           imagename = outputname,
           field = "",
           specmode = "cube",
           width = width,
           start = start,
           restfreq = "230.53800GHz",
           outframe = "LSRK",
           niter = niter,
	   gain = 0.2,
           threshold = thres_clean,
           cyclefactor = 4,
           interactive = False,
           imsize = imsize,
           cell = "1.0arcsec",
           phasecenter = "J2000 "+ra+" "+dec,
           weighting = weighting,
           robust = robust,
           gridder = "mosaic",
           deconvolver = "multiscale",
	   scales = [0,2,5],
           nchan = nchan,
           #cycleniter = 50,
           usemask = "user",
           restoringbeam = "common",
           startmodel = startmodel,
           mask = dir_mask + galname + "_12m+7m+tp_co21_hybridmask.mask")

    os.system("rm -rf "+outputname+".image.pbcor")
    impbcor(imagename = outputname+".image",
            outfile = outputname+".image.pbcor",
	    pbimage = outputname+".pb")

def def_name(dir_sim,mosaic_def2,robust):
    galname = dir_sim.split("/")[-1]
    start = "" #mosaic_def[:,1][np.where(mosaic_def[:,0]==galname)[0][0]] + "km/s"
    ra = mosaic_def2[:,1][np.where(mosaic_def2[:,0]==galname)[0][0]]
    dec = mosaic_def2[:,2][np.where(mosaic_def2[:,0]==galname)[0][0]]
    if "h" not in ra:
        ra = ra + "deg"
    if "d" not in dec:
        dec = dec + "deg"

    if robust == 2.0:
        weighting = "natural"
        wt = "na"
    elif robust == -2.0:
        weighting = "uniform"
        wt = "un"
    else:
        weighting = "briggs"
        wt = "br"

    return galname, start, ra, dec, weighting, wt

def def_imsize(dir_sim,galname):
    #tpname = dir_sim + "/sim_" + galname + ".sd.image"
    tpname = glob.glob("../phangs_dr1/"+galname+"*.skymodel")[0]
    size_ra = imhead(tpname,mode="list")["shape"][0]
    size_dec = imhead(tpname,mode="list")["shape"][1]
    size_pixel = max(size_ra,size_dec)
    pixel_arcsec = abs(imhead(tpname,mode="list")["cdelt1"]) * 180/np.pi*3600
    size_arcsec = size_pixel * pixel_arcsec
    imsize  = int(np.round(size_arcsec,-1) * 1.4)
    if imsize < 256:
        imsize = 256
    else:
        if imsize < 288:
	    imsize = 288
	else:
	    if imsize < 320:
	        imsize = 320
 	    else:
	        if imsize < 384:
	            imsize = 384
	        else:
		    if imsize < 400:
		        imsize = 400
		    else:
       	                if imsize < 448:
		            imsize = 448
		        else:
		            if imsize < 512:
		                imsize = 512
                            else:
		                if imsize < 576:
			            imsize = 576
			        else:
			            if imsize < 648:
			                imsize = 648
			            else:
				        if imsize < 800:
				            imsize = 800
				        else:
				            imsize = 1024

    return imsize

### main
dir_sim = glob.glob("../sim_phangs/*")
dir_mask = "../phangs_dr1/"

# get systemic velocity definition
mosaic_def_tmp_ = np.loadtxt("../scripts/mosaic_definitions.txt",dtype="S20",usecols=(0,3))
mosaic_def = np.c_[[s.split("_")[0] for s in mosaic_def_tmp_[:,0]],mosaic_def_tmp_[:,1]]

mosaic_def2 = np.loadtxt("../scripts/multipart_fields.txt",dtype="S20",usecols=(0,1,2))
mosaic_def2 = np.r_[np.loadtxt("../scripts/mosaic_definitions.txt",dtype="S20",usecols=(0,1,2)),mosaic_def2]

for i in range(len(dir_sim)):
  """
    # define name
    galname,start,ra,dec,weighting,wt = def_name(dir_sim[i],mosaic_def2,robust)
    title = galname + ", " + str(i) + "/" + str(len(dir_sim) - 1)
    imsize = def_imsize(dir_sim[i],galname)

    ### measure 7m-only rms
    print("### dirty map of " + title)
    rms = dirty_map(dir_sim[i],galname,wt,width,start,ra,dec,
		    weighting,robust,dir_mask,imsize)
  """
  """
    ### model TP data
    tpname = dir_sim[i] + "/sim_" + galname + ".sd.tp2vis.input"

    ### 7m-only clean
    if 0 in do_steps:
        os.system("rm -rf " + dir_sim[i] + "/sim_" + galname + "*_" + wt + ".*")
        print("### start 7m-only tclean for " + title)
        eazy_tclean("7m",
                    dir_sim[i],
                    galname,
		    wt,
		    width,
		    start,
		    niter,
		    str(rms * snr) + "Jy",
		    ra,
		    dec,
                    weighting,
		    robust,
		    dir_mask,
		    imsize,
		    startmodel="",
		    tpms=False)
    """
    """
    ### CAF
    if 1 in do_steps:
	inimodelname = dir_sim[i] + "/sim_" + galname + ".sd.startmodel_tmp_"
	templatename = dir_sim[i]+"/sim_"+galname+"_7m_"+wt+".pb"
        os.system("rm -rf " + inimodelname)
        imregrid(imagename = tpname,
                 template = templatename,
	         output = inimodelname)

        outfile = inimodelname + ".depb"
        os.system("rm -rf " + outfile)
        immath(imagename = [inimodelname, dir_sim[i]+"/sim_"+galname+"_7m_"+wt+".pb"],
               expr = "IM0*IM1",
	       outfile= outfile)

	print("### start CAF for " + title)
        imagename = dir_sim[i]+"/sim_"+galname+"_caf_"+wt+".image"
        os.system("rm -rf " + imagename)
        feather(imagename = imagename,
                highres = dir_sim[i]+"/sim_"+galname+"_7m_"+wt+".image",
	        lowres = outfile)

        os.system("rm -rf "+imagename+".pbcor")
        impbcor(imagename = imagename,
                outfile = imagename+".pbcor",
	        pbimage = dir_sim[i]+"/sim_"+galname+"_7m_"+wt+".pb")
    """
    
    ### CBF
    if 2 in do_steps:
	print("### start CBF for " + title)
        eazy_tclean("cbf",
                    dir_sim[i],
                    galname,
		    wt,
		    width,
		    start,
		    niter,
		    str(rms * snr) + "Jy",
		    ra,
		    dec,
                    weighting,
		    robust,
		    dir_mask,
		    imsize,
		    startmodel="",
		    tpms=True)

    ### CDF
    if 3 in do_steps:
        # define filename
	print("### start CDF for " + title)
        templatename = dir_sim[i]+"/sim_"+galname+"_7m_"+wt+".pb"
        inimodelname = dir_sim[i] + "/sim_" + galname + ".sd.startmodel_tmp_"

        # create TP initial model
        os.system("rm -rf " + inimodelname)
        imregrid(imagename = tpname,
                 template = templatename,
	         output = inimodelname)

        size_pix = abs(imhead(inimodelname,mode="list")["cdelt1"])
        area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
        bmaj = imhead(inimodelname,mode="list")["beammajor"]["value"]
        bmin = imhead(inimodelname,mode="list")["beamminor"]["value"]
        beamarea_tp = (bmaj*bmin*np.pi) / (4*np.log(2)) / area_pix_arcsec

        rms_tp = imstat(imagename = inimodelname,
                        mask = "inverse.mask")["rms"][0]

        os.system("rm -rf " + inimodelname.replace("_tmp_",""))
        expr = "iif(IM0>=" + str(rms_tp) + ",IM0*IM1/" + str(beamarea_tp) + ",0.0)"
        immath(imagename = [inimodelname,
                            dir_sim[i]+"/sim_"+galname+"_7m_"+wt+".pb"],
               mode = "evalexpr",
	       expr = expr,
	       outfile = inimodelname.replace("_tmp_",""))

        imhead(imagename = inimodelname.replace("_tmp_",""),
               mode = "put",
	       hdkey = "bunit",
	       hdvalue = "Jy/pixel")

        eazy_tclean("cdf",
                    dir_sim[i],
                    galname,
		    wt,
		    width,
		    start,
		    niter,
		    str(rms * snr) + "Jy",
		    ra,
		    dec,
                    weighting,
		    robust,
		    dir_mask,
		    imsize,
		    startmodel = inimodelname.replace("_tmp_",""),
		    tpms=False)

        outfile = inimodelname + ".depb"
        os.system("rm -rf " + outfile)
        immath(imagename = [inimodelname, dir_sim[i]+"/sim_"+galname+"_7m_"+wt+".pb"],
               expr = "IM0*IM1",
	       outfile= outfile)

        imagename = dir_sim[i]+"/sim_"+galname+"_cdf_"+wt+".feather"
        os.system("rm -rf " + imagename)
        feather(imagename = imagename,
                highres = dir_sim[i]+"/sim_"+galname+"_cdf_"+wt+".image",
	        lowres = outfile)

        os.system("rm -rf "+imagename+".pbcor")
        impbcor(imagename = imagename,
                outfile = imagename+".pbcor",
	        pbimage = dir_sim[i]+"/sim_"+galname+"_7m_"+wt+".pb")

    os.system("rm -rf " + dir_sim[i] + "/sim_" + galname + "*_" + wt + ".psf")
    os.system("rm -rf " + dir_sim[i] + "/sim_" + galname + "*_" + wt + ".sumwt")
    os.system("rm -rf " + dir_sim[i] + "/sim_" + galname + "*_" + wt + ".weight")
    os.system("rm -rf " + dir_sim[i] + "/dirty_" + galname + "*")

