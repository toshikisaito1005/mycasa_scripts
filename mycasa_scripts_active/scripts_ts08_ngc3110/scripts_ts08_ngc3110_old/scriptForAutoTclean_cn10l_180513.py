import glob
import os
import re
from datetime import datetime

####################################
# Initialize
####################################
import scipy.ndimage

####################################
# Define clean parameters
####################################
dirname_work = "./"
dirname_script = "./"
vis = "concat_all.ms.contsub"
field = "ngc_3110"
prename1 = "ngc3110_AL3B3_"
prename2 = "cn10l"
prename3 = "_l40_na"
prename = prename1 + prename2 + prename3
imsize = 512
cell = "0.25arcsec" # 1/4 * beam minor axis
pblimit = 0.4
restfreq = "113.14GHz" #CI(1-0) rest frequency
outframe = "LSRK"
spw = ""
width = "40km/s" #km/s
nchan = 25
start = "4500km/s"  #km/s
robust = 2.0
phasecenter = ""
scales = [0,10,25]
smallscalebias = 0.6
rms = 0.0006
#TCLEAN
ud_deconvolver = "multiscale"
ud_gridder = "mosaic"
ud_restoringbeam = "common"

myimage, myflux, mymask, myresidual = prename + ".image", prename + ".pb", prename + ".mask", prename + ".residual"

### Setup stopping criteria with multiplier for rms.
stop = 1.

### Minimum size multiplier for beam area for removing very small mask regions.
pixelmin = 10.

os.chdir(dirname_work)

done = glob.glob(vis + "_" + prename2 + ".split")
if not done:
    split(vis = vis, outputvis = vis + "_" + prename2 + ".split", datacolumn="data", spw = spw)
    os.system("rm -rf " + vis + "_" + prename2 + ".split.listobs")
    listobs(vis + "_" + prename2 + ".split", listfile = vis + "_" + prename2 + ".split.listobs")

vis = vis + "_" + prename2 + ".split"
spw = ""

### Make initial dirty image
os.system("rm -rf "+prename+".* "+prename+"_*")
tclean(vis=vis,imagename=prename,specmode="cube",pblimit=pblimit,field=field,imsize=imsize,cell=cell,spw=spw,weighting="briggs",robust=robust,width=width,start=start,nchan=nchan,restfreq=restfreq,outframe=outframe,veltype="radio",mask="",niter=0,interactive=False,deconvolver=ud_deconvolver,gridder=ud_gridder,restoringbeam=ud_restoringbeam)

os.system("cp -r " + prename + ".image " + prename + ".dirty.image")
os.system("cp -r " + prename + ".pb " + prename + ".dirty.pb")
os.system("cp -r " + prename + ".psf " + prename + ".dirty.psf")
os.system("cp -r " + prename + ".residual " + prename + ".dirty.residual")
os.system("cp -r " + prename + ".sumwt " + prename + ".dirty.sumwt")
os.system("cp -r " + prename + ".weight " + prename + ".dirty.weight")

# Determine the beam area in pixels for later removal of very small mask regions
major=imhead(imagename=myimage,mode="get",hdkey="beammajor")["value"]
minor=imhead(imagename=myimage,mode="get",hdkey="beamminor")["value"]
pixelsize=float(cell.split("arcsec")[0])
beamarea=(major*minor*pi/(4*log(2)))/(pixelsize**2)
print "beamarea in pixels =", beamarea

### Find the peak in the dirty cube.
bigstat=imstat(imagename=myimage)
peak=bigstat["max"][0]
print "peak (Jy/beam) in cube = "+str(peak)
### Sets threshold of first loop, try 2-4. Subsequent loops are set thresh/2.
thresh = peak / 4.

### If True: find the rms in two line-free channels; If False:  Set rms by hand in else statement.
"""
if True:
    chanstat = imstat(imagename = myimage,chans = '4')
    rms1 = chanstat['rms'][0]
    chanstat = imstat(imagename = myimage,chans = '66')
    rms2 = chanstat['rms'][0]
    rms = 0.5*(rms1+rms2)
else:
    rms = 0.0025
"""

print "rms (Jy/beam) in a channel = "+str(rms)

### Automasking loop
os.system("rm -rf "+prename+"_threshmask*")
os.system("rm -rf "+prename+"_fullmask*")
os.system("rm -rf "+prename +".image*")
n=-1
a_0=datetime.now()
while (thresh>=stop*rms):
    n=n+1
    print "clean threshold this loop is", thresh
    threshmask=prename+"_threshmask"+str(n)
    maskim=prename+"_fullmask"+str(n)
    immath(imagename=[myresidual],outfile=threshmask,expr="iif(IM0>"+str(thresh)+",1.0,0.0)",mask=myflux+">"+str(pblimit))
    if (n==0):
        os.system("cp -r "+threshmask+" "+maskim+".pb")
        print "This is the first loop"
    else:
        makemask(mode="copy",inpimage=myimage,inpmask=[threshmask,mymask],output = maskim)
        imsubimage(imagename=maskim,mask=myflux+">"+str(pblimit),outfile=maskim+".pb")
    print "Combined mask " +maskim+" generated."

    # Remove small masks
    os.system("cp -r "+maskim+".pb "+maskim+".pb.min")
    maskfile=maskim+'.pb.min'
    ia.open(maskfile)
    mask=ia.getchunk()
    labeled,j=scipy.ndimage.label(mask)
    myhistogram=scipy.ndimage.measurements.histogram(labeled,0,j+1,j+1)
    object_slices=scipy.ndimage.find_objects(labeled)
    threshold=beamarea*pixelmin
    for i in range(j):
        if myhistogram[i+1]<threshold:
            mask[object_slices[i]]=0

    ia.putchunk(mask)
    ia.done()
    print "Small masks removed and "+maskim+".pb.min generated."

    os.system("rm -rf "+mymask+"")
    tclean(vis=vis,imagename=prename,specmode="cube",pblimit=pblimit,field = field,imsize=imsize,cell=cell,spw=spw,weighting="briggs",robust=robust,width=width,start=start,nchan=nchan,restfreq=restfreq,outframe=outframe,veltype="radio",mask = maskim+".pb.min",scales=scales,interactive=False,niter=10000,threshold=str(thresh)+"Jy/beam",restoringbeam=ud_restoringbeam)

    if thresh==stop*rms: break
    thresh=thresh/2.
    # Run a final time with stop*rms if more than a little above
    # stop*rms. Also make a back-up of next to last image
    if (thresh < stop*rms and thresh*2.>1.05*stop*rms):
        thresh = stop*rms
        os.system("cp -r "+myimage+" "+myimage+str(n))

    #num=1
    #num=num+1
    #a_str(num)=datetime.now()
    #print(str(num)+"th loop takes "+str(e-d))

os.chdir(dirname_script)
