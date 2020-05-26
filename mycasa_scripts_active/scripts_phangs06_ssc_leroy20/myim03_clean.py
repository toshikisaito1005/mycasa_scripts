import os
import sys
import glob
import datetime
a=datetime.datetime.now()


dir_proj = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/"
robust = 0.5
width = "" # "2.6km/s"
nchan = 1 # 96
niter = 500000
snr = 1.0


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
	thres_clean,
	tpvis=None,
	startmodel="",
	):
	# ms
	if tpvis==None:
		vis = intvis
	else:
		concat(vis = [intvis, tpvis],
			concatvis = vis.replace(".ms",".concatms"),
			freqtol = "50MHz")
		vis = vis.replace(".ms",".concatms")
	#
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
		niter = niter,
		threshold = thres_clean,
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
		startmodel = startmodel,
		mask = hybridmaskimage,
		gain = 0.2,
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
	snr,
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
		thres_clean = str(rms*snr) + "Jy"
	else:
		print("### skip dirty map of " + title)
		os.system("cp -r " + imagename + ".inversemask" + " " + (imagename + ".inversemask").split("/")[-1])
		rms = imstat(imagename=imagename+".image",mask=(imagename+".inversemask").split("/")[-1])["rms"][0]
		os.system("rm -rf " + (imagename+".inversemask").split("/")[-1])
		thres_clean = str(rms*snr) + "Jy"

	return thres_clean

def imaging_caf(
	this_dir_sim,
	galname,
	tpname,
	imagename,
	wt,
	):
	sdimage = this_dir_sim + "/sim_" + galname + ".sd.startmodel_tmp_"
	pbimage = this_dir_sim + "/sim_" + galname + "_7m_" + wt + ".pb"
	os.system("rm -rf " + sdimage)
	imregrid(imagename=tpname, template=pbimage, output=sdimage)
	#
	depbsdimage = this_dir_sim + "/sim_" + galname + ".sd.startmodel.depb"
	os.system("rm -rf " + depbsdimage)
	immath(imagename=[sdimage,pbimage], expr="IM0*IM1", outfile=depbsdimage)
	os.system("rm -rf " + sdimage)
	#
	cafimage = this_dir_sim + "/sim_" + galname + "_feather_" + wt + ".image"
	7mname = this_dir_sim + "/sim_" + galname + "_7m_" + wt + ".image"
	os.system("rm -rf " + cafimage)
	feather(imagename=cafimage, highres=7mname, lowres=depbsdimage)
	#
	os.system("rm -rf " + cafimage + ".pbcor")
	impbcor(imagename=cafimage, outfile=cafimage+".pbcor", pbimage=pbimage)


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
for i in range(len(dir_sim)):
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
		thres_clean = get_dirty_rms(imagename,title,vis,width,start,imsize,phasecenter,weighting,robust,nchan,hybridmaskimage,snr)
		print("# thres_clean = " + thres_clean)
		#
		### imaging 7m-only
		print("### processing 7m-only map of " + title)
		imagename = this_dir_sim + "/sim_" + galname + "_7m_" + wt
		eazy_tclean(vis,imagename,width,start,imsize,phasecenter,weighting,robust,nchan,hybridmaskimage,niter,thres_clean)
		#
		### imaging CAF feather
		print("### processing CAF feather map of " + title)
		imaging_caf(this_dir_sim,galname,tpname,imagename,wt)


