import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ngc3110/ana/datacube_LTE/"
box = "45,45,314,314"
pixelmin = 5.

#####################
### Main Procedure
#####################
os.system("rm -rf " + dir_data + "mask2.image")
imagenames = glob.glob(dir_data + "*.image")


### regrid and resize data cubes
for i in range(len(imagenames)):
    output = imagenames[i] + ".regrid"
    os.system("rm -rf " + output)
    imregrid(imagename = imagenames[i],
        template = imagenames[1],
        output = output)
    outfile = imagenames[i] + ".regrid.immath"
    os.system("rm -rf " + outfile)
    immath(imagename = output,
        mode = "evalexpr",
        expr = "IM0",
        box = box,
        outfile = outfile)
    os.system("rm -rf " + output)


### create cube mask for 12CO
imagenames = glob.glob(dir_data + "*.image.regrid.immath")
myim.createmask(dir_data = dir_data,
    imagename = imagenames[0].split("/")[-1],
    thres = -10.,
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


### create cube mask for 13CO
imagenames = glob.glob(dir_data + "*.image.regrid.immath")
myim.createmask(dir_data = dir_data,
    imagename = imagenames[0].split("/")[-1],
    thres = -10.,
    outmask = "mask_13CO.mask")


outmask = dir_data + "mask_13CO.mask"
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
    chans = "14~40",
    mask = "mask_12CO.mask",
    thres = -10.)


### create momement maps for 12co21
myim.moment_maps(dir_data = dir_data,
    imagename = imagenames[1],
    chans = "12~41",
    mask = "mask_12CO.mask",
    thres = -10.)


### create momement maps for 13co10
myim.moment_maps(dir_data = dir_data,
    imagename = imagenames[2],
    chans = "17~38",
    mask = "mask_13CO.mask",
    thres = -10.)


### create momement maps for 13co21
myim.moment_maps(dir_data = dir_data,
    imagename = imagenames[3],
    chans = "16~40",
    mask = "mask_13CO.mask",
    thres = -10.)
