import os
import sys
import glob
import datetime
a=datetime.datetime.now()


##############################
### parameters
##############################
dir_proj = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/"
robust = 0.5
width = ""
nchan = 1
niter = 500000
skip = ["ngc0628"]
only = ["ngc0628"]


##############################
### def
##############################
def get_info(
	this_dir_sim,
	mosaic_def2,
	robust,
	):
	galname = this_dir_sim.split("/")[-1].split("sim_")[-1]
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

def def_imsize(
	dir_proj,
	galname,
	):
	skymodel = glob.glob(dir_proj+"../v3p4_tpeak/"+galname+"*.skymodel")[0]
	size_ra = imhead(skymodel,mode="list")["shape"][0]
	size_dec = imhead(skymodel,mode="list")["shape"][1]
	size_pixel = max(size_ra, size_dec)
	pixel_arcsec = abs(imhead(skymodel,mode="list")["cdelt1"]) * 180/np.pi*3600
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

def dirty_map(
	vis,
	imagename,
	width,
	start,
	imsize,
	phasecenter,
	weighting,
	robust,
	nchan,
	hybridmaskimage,
	):
	# tclean
	os.system("rm -rf " + imagename + "*")
	tclean(
		vis = vis,
		imagename = imagename,
		field = "",
		specmode = "cube",
		restfreq = "230.53800GHz",
		outframe = "LSRK",
		width = width,
		start = start,
		niter = 0,
		threshold = "",
		cyclefactor = 4,
		interactive = False,
		imsize = imsize,
		cell = "1.0arcsec",
		phasecenter = phasecenter,
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
		mask = "",
		)
	# masking dirty map
	os.system("rm -rf _tmp_inverse.mask")
	imregrid(imagename = hybridmaskimage,
		template = imagename + ".image",
		output = "_tmp_inverse.mask")
	#
	os.system("rm -rf " + imagename + ".inversemask")
	immath(imagename = "_tmp_inverse.mask",
		mode = "evalexpr",
		expr = "iif(IM0>=1,0,1)",
		outfile = imagename + ".inversemask")
	#
	os.system("rm -rf inverse.mask.fits")
	exportfits(imagename = imagename + ".inversemask",
	           fitsimage = "inverse.mask.fits")
	#
	os.system("rm -rf " + imagename + ".inversemask")
	importfits(fitsimage = "inverse.mask.fits",
	           imagename = imagename + ".inversemask",
	           defaultaxes = True,
	           defaultaxesvalues = ["RA","Dec","Frequency","Stokes"])
	os.system("cp -r " + imagename + ".inversemask" + " " + (imagename + ".inversemask").split("/")[-1])
	#
	os.system("rm -rf inverse.mask.fits")
	os.system("rm -rf _tmp_inverse.mask")
	#
	rms = imstat(imagename=imagename+".image",mask=(imagename+".inversemask").split("/")[-1])["rms"][0]
	#
	os.system("rm -rf " + (imagename+".inversemask").split("/")[-1])

	return rms

def eazy_tclean(
	intvis,
	imagename,
	width,
	start,
	imsize,
	phasecenter,
	weighting,
	robust,
	nchan,
	hybridmaskimage,
	niter,
	rms,
	tpvis=None,
	startmodel="",
	):
	# ms
	if tpvis==None:
		vis = intvis
	else:
		concat(vis = [intvis, tpvis],
			concatvis = intvis.replace(".ms",".concatms"),
			freqtol = "50MHz")
		vis = intvis.replace(".ms",".concatms")
	#
	# tclean
	os.system("rm -rf " + imagename + "*")
	print("# multiscale clean down to 4 sigma")
	tclean(
		vis = vis,
		imagename = imagename,
		field = "",
		specmode = "cube",
		restfreq = "230.53800GHz",
		outframe = "LSRK",
		width = width,
		start = start,
		niter = niter,
		threshold = str(rms*4.0) + "Jy",
		cyclefactor = 4,
		interactive = False,
		imsize = imsize,
		cell = "1.0arcsec",
		phasecenter = phasecenter,
		weighting = weighting,
		robust = robust,
		gridder = "mosaic",
		deconvolver = "multiscale",
		scales = [0,2,5],
		nchan = nchan,
		cycleniter = 100,
		usemask = "user",
		restoringbeam = "",
		startmodel = startmodel,
		mask = hybridmaskimage,
		gain = 0.2,
		)
	print("# singlescale clean down to 1.0 sigma")
	tclean(
		vis = vis,
		imagename = imagename,
		field = "",
		specmode = "cube",
		restfreq = "230.53800GHz",
		outframe = "LSRK",
		width = width,
		start = start,
		niter = niter,
		threshold = str(rms*1.0) + "Jy",
		cyclefactor = 4,
		interactive = False,
		imsize = imsize,
		cell = "1.0arcsec",
		phasecenter = phasecenter,
		weighting = weighting,
		robust = robust,
		gridder = "mosaic",
		deconvolver = "hogbom",
		nchan = nchan,
		cycleniter = 100,
		usemask = "user",
		restoringbeam = "",
		gain = 0.1,
		)
	#
	os.system("rm -rf "+imagename+".image.pbcor")
	impbcor(imagename = imagename+".image",
		outfile = imagename+".image.pbcor",
		pbimage = imagename+".pb")

def get_dirty_rms(
	imagename,
	title,
	vis,
	width,
	start,
	imsize,
	phasecenter,
	weighting,
	robust,
	nchan,
	hybridmaskimage,
	):
	done = glob.glob(imagename + ".image")
	if not done:
		print("### processing dirty map of " + title)
		rms = dirty_map(
			vis,
			imagename,
			width,
			start,
			imsize,
			phasecenter,
			weighting,
			robust,
			nchan,
			hybridmaskimage)
	else:
		print("### skip dirty map of " + title)
		os.system("cp -r " + imagename + ".inversemask" + " " + (imagename + ".inversemask").split("/")[-1])
		rms = imstat(imagename=imagename+".image",mask=(imagename+".inversemask").split("/")[-1])["rms"][0]
		os.system("rm -rf " + (imagename+".inversemask").split("/")[-1])

	return rms

def imaging_caf(
	this_dir_sim,
	galname,
	tpname,
	wt,
	):
	sdimage = this_dir_sim + "/sim_" + galname + ".sd.startmodel_tmp_"
	pbimage = this_dir_sim + "/sim_" + galname + "_7m_" + wt + ".pb"
	os.system("rm -rf " + sdimage)
	imregrid(imagename=tpname, template=pbimage, output=sdimage)
	#
	depbsdimage = this_dir_sim + "/sim_" + galname + ".sd.image.depb"
	os.system("rm -rf " + depbsdimage + "_tmp")
	immath(imagename=[sdimage,pbimage], expr="IM0*IM1", outfile=depbsdimage + "_tmp")
	os.system("rm -rf " + sdimage)
	#
	ia.open(depbsdimage + "_tmp")
	ia.replacemaskedpixels(0., update=True)
	ia.close()
	#
	immath(depbsdimage + "_tmp",
		expr = "iif(IM0>=0,IM0,0)",
		outfile = depbsdimage)
	os.system("rm -rf " + depbsdimage + "_tmp")
	#
	cafimage = this_dir_sim + "/sim_" + galname + "_feather_" + wt + ".image"
	intname  = this_dir_sim + "/sim_" + galname + "_7m_" + wt + ".image"
	os.system("rm -rf " + cafimage)
	feather(imagename=cafimage, highres=intname, lowres=depbsdimage)
	#
	os.system("rm -rf " + cafimage + ".pbcor")
	impbcor(imagename=cafimage, outfile=cafimage+".pbcor", pbimage=pbimage)

def imaging_cdf(
	this_dir_sim,
	galname,
	wt,
	tpname,
	vis,
	imagename,
	width,
	start,
	imsize,
	phasecenter,
	weighting,
	robust,
	nchan,
	hybridmaskimage,
	niter,
	rms,
	):
	sdimage = this_dir_sim + "/sim_" + galname + ".sd.startmodel_tmp_"
	pbimage = this_dir_sim + "/sim_" + galname + "_7m_" + wt + ".pb"
	os.system("rm -rf " + sdimage)
	imregrid(imagename=tpname, template=pbimage, output=sdimage)
	#
	size_pix = abs(imhead(sdimage,mode="list")["cdelt1"])
	area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
	bmaj = imhead(sdimage,mode="list")["beammajor"]["value"]
	bmin = imhead(sdimage,mode="list")["beamminor"]["value"]
	beamarea_tp = (bmaj*bmin*np.pi) / (4*np.log(2)) / area_pix_arcsec
	#
	inversemask = this_dir_sim + "/dirty_" + galname + "_7m_" + wt + ".inversemask"
	os.system("cp -r " + inversemask + " " + inversemask.split("/")[-1])
	rms_tp = imstat(imagename=sdimage,mask=inversemask.split("/")[-1])["rms"][0]
	os.system("rm -rf " + inversemask.split("/")[-1])
	#
	tpstartmodel = sdimage.replace("_tmp_","")
	os.system("rm -rf " + tpstartmodel + "_tmp")
	expr = "iif(IM0>=" + str(rms_tp) + ",IM0*IM1/" + str(beamarea_tp) + ",0.0)"
	immath(imagename=[sdimage,pbimage], mode="evalexpr", expr=expr, outfile=tpstartmodel + "_tmp")
	imhead(imagename=tpstartmodel + "_tmp", mode="put", hdkey="bunit", hdvalue="Jy/pixel")
	#
	ia.open(tpstartmodel + "_tmp")
	ia.replacemaskedpixels(0., update=True)
	ia.close()
	immath(imagename = tpstartmodel + "_tmp",
		expr = "iif(IM0>=0,IM0,0)",
		outfile = tpstartmodel)
	os.system("rm -rf " + tpstartmodel + "_tmp")
	#
	eazy_tclean(vis,imagename,width,start,imsize,phasecenter,weighting,robust,nchan,hybridmaskimage,niter,rms,startmodel=tpstartmodel)
	#
	os.system("rm -rf " + imagename + ".image.pbcor")
	impbcor(imagename=imagename+".image", outfile=imagename+".image.pbcor", pbimage=imagename+".pb")


##############################
### main
##############################
# get systemic velocity definition
mosaic_def = np.loadtxt("mosaic_definitions.txt",dtype="S20",usecols=(0,3))
mosaic_def = np.c_[[s.split("_")[0] for s in mosaic_def[:,0]],mosaic_def[:,1]]
mosaic_def2 = np.loadtxt("multipart_fields.txt",dtype="S20",usecols=(0,1,2))
mosaic_def2 = np.r_[np.loadtxt("mosaic_definitions.txt",dtype="S20",usecols=(0,1,2)),mosaic_def2]
#
dir_sim = glob.glob(dir_proj + "*")
dir_mask = dir_proj + "../v3p3_hybridmask/"
#
# apply skip
for i in range(len(skip)):
	dir_sim = [s for s in dir_sim if skip[i] not in s]
#
# apply skip
if only:
	dir_sim = []
	for i in range(len(only)):
		dir_sim.extend(glob.glob(dir_proj + "*" + only[i]))
	dir_sim = np.array(dir_sim)
#
for i in range(len(dir_sim)):
#for i in [1]:
	#
	this_dir_sim = dir_sim[i]
	# get info
	galname, start, ra, dec, weighting, wt = \
	    get_info(this_dir_sim, mosaic_def2, robust)
	phasecenter = "J2000 " + ra + " " + dec
	imsize = def_imsize(dir_proj, galname)
	title = galname + ", " + str(i+1) + "/" + str(len(dir_sim))
	#
	tpname = this_dir_sim + "/sim_" + galname + ".sd.tp2vis.input"
	vis = this_dir_sim + "/sim_" + galname + ".aca.cycle5.noisy.ms"

	hybridmaskimage = glob.glob(dir_mask + galname + "*")
	if hybridmaskimage:
		hybridmaskimage = hybridmaskimage[0]
		### measure 7m-only rms
		imagename = this_dir_sim + "/dirty_" + galname + "_7m_" + wt
		rms = get_dirty_rms(imagename,title,vis,width,start,imsize,phasecenter,weighting,robust,nchan,hybridmaskimage)
		#
		### imaging 7m-only
		imagename = this_dir_sim + "/sim_" + galname + "_7m_" + wt
		done = glob.glob(imagename + ".image")
		if not done:
			print("### processing 7m-only map of " + title)
			eazy_tclean(vis,imagename,width,start,imsize,phasecenter,weighting,robust,nchan,hybridmaskimage,niter,rms)
		else:
			print("### skip 7m-only map of " + title)
		#
		### imaging CAF feather
		print("### processing CAF feather map of " + title)
		imaging_caf(this_dir_sim, galname, tpname, wt)
		#
		### imaging CBF tp2vis
		tpvis = this_dir_sim + "/sim_" + galname + ".sd.ms"
		imagename = this_dir_sim + "/sim_" + galname + "_tp2vis_" + wt
		done = glob.glob(imagename + ".image")
		if not done:
			print("### processing CBF tp2vis map of " + title)
			eazy_tclean(vis,imagename,width,start,imsize,phasecenter,weighting,robust,nchan,hybridmaskimage,niter,rms,tpvis=tpvis)
		else:
			print("### skip CBF tp2vis map of " + title)
		#
		### imaging CDF tpmodel
		imagename = this_dir_sim + "/sim_" + galname + "_tpmodel_" + wt
		done = glob.glob(imagename + ".image")
		if not done:
			print("### processing CDF tpmodel map of " + title)
			imaging_cdf(this_dir_sim,galname,wt,tpname,vis,imagename,width,start,imsize,phasecenter,weighting,robust,nchan,hybridmaskimage,niter,rms)
		else:
			print("### skip CDF tpmodel map of " + title)

os.system("rm -rf *.last")
os.system("rm -rf inverse.mask")
