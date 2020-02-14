import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../goals_catom/fits/"
box = ""
pixelmin = 5.
rms_n6240 = 0.006
rms_i18293 = 0.003
rms_n5104 = 0.003

#####################
### Main Procedure
#####################
os.system("rm -rf " + dir_data + "*.image")
os.system("rm -rf " + dir_data + "*.immath")
os.system("rm -rf " + dir_data + "*.moment0*")
os.system("rm -rf " + dir_data + "*.moment1*")
os.system("rm -rf " + dir_data + "*.moment2*")
fitsimages = glob.glob(dir_data + "*.fits")

### importfits
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = \
                   fitsimages[i].replace(".fits",
                                         ".image"),
               defaultaxes = True,
               defaultaxesvalues = ['Right Ascension',
                                    'Declination',
                                    'Stokes',
                                    'Frequency'])


imagenames = glob.glob(dir_data + "*.image")


### create cube mask
# IRAS 18293
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = rms_i18293 * 5.,
                outmask = "mask_i18293.mask")

outmask = dir_data + "mask_i18293.mask"
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

### create momement maps for CI10
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[1],
                 chans = "7~35",
                 mask = "mask_i18293.mask",
                 thres = rms_i18293 * 5.5)

# NGC 5104
myim.createmask(dir_data = dir_data,
                imagename = imagenames[2].split("/")[-1],
                thres = rms_n5104 * 3.0,
                outmask = "mask_n5104.mask")

outmask = dir_data + "mask_n5104.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[2],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[2],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[2], mode = "list")["cdelt1"])
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

### create momement maps for CI10
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[3],
                 chans = "3~44",
                 mask = "mask_n5104.mask",
                 thres = rms_n5104 * 3.5)

# NGC 6240
myim.createmask(dir_data = dir_data,
                imagename = imagenames[4].split("/")[-1],
                thres = rms_n6240 * 3.5,
                outmask = "mask_n6240.mask")

outmask = dir_data + "mask_n6240.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[4],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[4],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[4], mode = "list")["cdelt1"])
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

### create momement maps for CI10
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[5],
                 chans = "3~44",
                 mask = "mask_n6240.mask",
                 thres = rms_n6240 * 4.0)

os.system("rm -rf " + dir_data + "mask2.image")

