import os
import sys
import glob
import datetime
a=datetime.datetime.now()


dir_proj = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/"
robust = 0.5
width = "" # "2.6km/s"
nchan = 1 # 96


##############################
### def
##############################
def get_info(
	this_dir_sim,
	mosaic_def2,
	robust,
	):
	galname = this_dir_sim.split("/")[-1]
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
	os.system("rm -rf inverse.mask")
	immath(imagename = "_tmp_inverse.mask",
		mode = "evalexpr",
		expr = "iif(IM0>=1,0,1)",
		outfile = "inverse.mask")
	#
	os.system("rm -rf inverse.mask.fits")
	exportfits(imagename = "inverse.mask",
	           fitsimage = "inverse.mask.fits")
	#
	os.system("rm -rf inverse.mask")
	importfits(fitsimage = "inverse.mask.fits",
	           imagename = "inverse.mask",
	           defaultaxes = True,
	           defaultaxesvalues = ["RA","Dec","Frequency","Stokes"])
	#
	os.system("rm -rf inverse.mask.fits")
	#
	rms = imstat(imagename=imagename+".image",mask="inverse.mask")["rms"][0]

	return rms


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

#for i in range(len(dir_sim)):
for i in [0]:
	#
	this_dir_sim = dir_sim[i]
	# get info
	galname, start, ra, dec, weighting, wt = \
	    get_info(this_dir_sim, mosaic_def2, robust)
	phasecenter = "J2000 " + ra + " " + dec
	imsize = def_imsize(this_dir_sim, galname)
	title = galname + ", " + str(i+1) + "/" + str(len(dir_sim))

	### measure 7m-only rms
	print("### dirty map of " + title)
	vis = dir_sim + "/sim_" + galname + ".aca.cycle5.noisy.ms"
	imagename = dir_sim + "/dirty_" + galname + "_7m_" + wt
	hybridmaskimage = glob.glob(dir_mask + galname + "*")[0]
	rms = dirty_map(vis, imagename, width, start, imsize, phasecenter, weighting, robust, nchan, hybridmaskimage)

