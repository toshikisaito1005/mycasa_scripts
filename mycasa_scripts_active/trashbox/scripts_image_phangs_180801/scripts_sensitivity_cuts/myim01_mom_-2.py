import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../phangs/co_ratio/"
rms_co10 = 0.01
rms_co21 = 0.03
pixelmin = 5.

#####################
### Main Procedure
#####################
fitsimages = glob.glob(dir_data + "m74*.fits")


### importfits
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = fitsimages[i].replace(".fits", ".image"),
               defaultaxes = True,
               defaultaxesvalues = ['Right Ascension',
                                    'Declination',
                                    'Stokes',
                                    'Frequency'])

imagenames = glob.glob(dir_data + "m74*.image")


### imregrid
os.system("rm -rf " + imagenames[1] + ".regrid")
imregrid(imagename = imagenames[1],
         template = imagenames[0],
         output = imagenames[1] + ".regrid")
os.system("rm -rf " + imagenames[1])
imagenames[1] = imagenames[1] + ".regrid"


### imsmooth
for i in range(len(imagenames)):
    os.system("rm -rf " + imagenames[i] + ".smooth")
    imsmooth(imagename = imagenames[i],
             kernel = "gauss",
             major = "3.2arcsec",
             minor = "3.2arcsec",
             pa = "0.0deg",
             targetres = True,
             outfile = imagenames[i] + ".smooth")
    os.system("rm -rf " + imagenames[i])


### create cube mask
imagenames = glob.glob(dir_data + "m74*.smooth")

# co10
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = rms_co10 * -2.0,
                outmask = "mask_12CO10.mask")


outmask = dir_data + "mask_12CO10.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[0],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[0],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[0], mode = "list")["cdelt1"])
pixelsize = pix * 3600 * 180 / np.pi
beamarea = (major * minor * np.pi/(4 * np.log(2))) / (pixelsize ** 2)
ia.open(outmask)
mask = ia.getchunk()
labeled, j = scipy.ndimage.label(mask)
myhistogram = scipy.ndimage.measurements.histogram(labeled, 0, j+1 , j+1)
object_slices = scipy.ndimage.find_objects(labeled)
threshold = beamarea * pixelmin
for i in range(j):
    if myhistogram[i + 1] < threshold:
        mask[object_slices[i]] = 0
ia.putchunk(mask)
ia.done()


# co21
myim.createmask(dir_data = dir_data,
                imagename = imagenames[1].split("/")[-1],
                thres = rms_co21 * -2.0,
                outmask = "mask_12CO21.mask")


outmask = dir_data + "mask_12CO21.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[1], mode = "list")["cdelt1"])
pixelsize = pix * 3600 * 180 / np.pi
beamarea = (major * minor * np.pi/(4 * np.log(2))) / (pixelsize ** 2)
ia.open(outmask)
mask = ia.getchunk()
labeled, j = scipy.ndimage.label(mask)
myhistogram = scipy.ndimage.measurements.histogram(labeled, 0, j+1 , j+1)
object_slices = scipy.ndimage.find_objects(labeled)
threshold = beamarea * pixelmin
for i in range(j):
    if myhistogram[i + 1] < threshold:
        mask[object_slices[i]] = 0
ia.putchunk(mask)
ia.done()


### create momement maps for 12co10
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "16~32",
                 mask = "mask_12CO10.mask",
                 thres = rms_co10 * -2.0)


### create momement maps for 12co21
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[1],
                 chans = "16~32",
                 mask = "mask_12CO21.mask",
                 thres = rms_co21 * -2.0)

