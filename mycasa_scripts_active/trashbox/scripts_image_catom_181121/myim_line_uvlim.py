import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../iras18293/products/line_uvlim/"
box = ""
pixelmin = 5.
rms_co = 0.0025
rms_co21 = 0.0005
rms_ci = 0.0044

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
               imagename = fitsimages[i].replace(".fits", ".image"))

imagenames = glob.glob(dir_data + "*.image")

### regridding all data into the CI cube
for i in range(4):
    output = imagenames[i] + ".regrid"
    os.system("rm -rf " + output)
    imregrid(imagename = imagenames[i],
             template = imagenames[4],
             output = output)
    os.system("rm -rf " + imagenames[i])
    os.system("mv " + output + " " + imagenames[i])

### create cube mask
# CO(1-0)
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = rms_co * 2.5,
                outmask = "mask_12CO.mask")

outmask = dir_data + "mask_12CO.mask"
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

# CI(1-0)
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = rms_co * 5.,
                outmask = "mask_CI.mask")

outmask = dir_data + "mask_CI.mask"
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

### create momement maps for 12co10
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "18~75",
                 mask = "mask_12CO.mask",
                 thres = rms_co * 3.0)

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[1],
                 chans = "18~75",
                 mask = "mask_12CO.mask",
                 thres = rms_co * 3.0)

### create momement maps for 12co21
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[2],
                 chans = "18~75",
                 mask = "mask_12CO.mask",
                 thres = rms_co * 3.)

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[3],
                 chans = "18~75",
                 mask = "mask_12CO.mask",
                 thres = rms_co * 3.)

### create momement maps for CI10
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[4],
                 chans = "18~75",
                 mask = "mask_CI.mask",
                 thres = rms_ci * 3.5)

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[5],
                 chans = "18~75",
                 mask = "mask_CI.mask",
                 thres = rms_ci * 3.5)

os.system("rm -rf " + dir_data + "mask2.image")

