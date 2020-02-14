import glob
import os
import re
from datetime import datetime

####################################
# Initialize
####################################
import scipy.ndimage

####################################
# main
####################################
prename = imagename
myimage, myflux, mymask, myresidual = prename + ".image", prename + ".pb", prename + ".mask", prename + ".residual"

### Setup stopping criteria with multiplier for rms.
stop = 1.5

### Minimum size multiplier for beam area for removing very small mask regions.
pixelmin = 1.

dirname_script = os.getcwd()
os.chdir(dirname_work)

### Make initial dirty image
os.system("rm -rf "+prename+".* "+prename+"_*")
tclean(vis=vis,
       imagename=prename,
       specmode="cube",
       pblimit=pblimit,
       field=field,
       imsize=imsize,
       cell=cell,
       spw=spw,
       weighting="briggs",
       robust=robust,
       width=width,
       start=start,
       nchan=nchan,
       restfreq=restfreq,
       outframe=outframe,
       veltype="radio",
       mask="",
       niter=0,
       interactive=False,
       deconvolver=deconvolver,
       gridder=gridder,
       phasecenter=phasecenter,
       restoringbeam="common",
       uvtaper = uvtaper)

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
    immath(imagename=[myresidual],
           outfile=threshmask,
           expr="iif(IM0>"+str(thresh)+",1.0,0.0)",
           mask=myflux+">"+str(pblimit))
    if (n==0):
        os.system("cp -r "+threshmask+" "+maskim+".pb")
        print "This is the first loop"
    else:
        makemask(mode="copy",
                 inpimage=myimage,
                 inpmask=[threshmask,mymask],
                 output=maskim)
        imsubimage(imagename=maskim,
                   mask=myflux+">"+str(pblimit),
                   outfile=maskim+".pb")
    print "Combined mask " +maskim+" generated."

    # Remove small masks
    os.system("cp -r "+maskim+".pb "+maskim+".pb.min")
    maskfile=maskim+'.pb.min'
    ia.open(maskfile)
    mask=ia.getchunk()
    labeled,j=scipy.ndimage.label(mask)
    myhistogram=scipy.ndimage.measurements.histogram(labeled,0,j+1,j+1)
    object_slices=scipy.ndimage.find_objects(labeled)
    threshold_area=beamarea*pixelmin
    for i in range(j):
        if myhistogram[i+1]<threshold_area:
            mask[object_slices[i]]=0

    ia.putchunk(mask)
    ia.done()
    print "Small masks removed and "+maskim+".pb.min generated."

    os.system("rm -rf "+mymask+"")
    tclean(vis=vis,
           imagename=prename,
           specmode="cube",
           pblimit=pblimit,
           field = field,
           imsize=imsize,
           cell=cell,
           spw=spw,
           weighting="briggs",
           robust=robust,
           width=width,
           start=start,
           nchan=nchan,
           restfreq=restfreq,
           outframe=outframe,
           veltype="radio",
           mask=maskim+".pb.min",
           scales=scales,
           interactive=False,
           deconvolver=deconvolver,
           niter=1000000,
           threshold=str(thresh)+"Jy/beam",
           phasecenter=phasecenter,
           gridder=gridder,
           gain=0.1,
           smallscalebias=smallscalebias,
           restoringbeam="common",
           uvtaper = uvtaper)

    if thresh==stop*rms: break
    thresh=thresh/2.
    # Run a final time with stop*rms if more than a little above
    # stop*rms. Also make a back-up of next to last image
    if (thresh < stop*rms and thresh*2.>1.05*stop*rms):
        thresh = stop*rms
        os.system("cp -r "+myimage+" "+myimage+str(n))


os.system("rm -rf *.last")
os.chdir(dirname_script)
