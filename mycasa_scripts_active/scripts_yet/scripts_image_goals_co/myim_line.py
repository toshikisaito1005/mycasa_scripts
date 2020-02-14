import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/..")
import mycasaimaging_tools as myim


dir_data = "../../proposal/alma_cycle6/"
box = ""
pixelmin = 20.

#####################
### Main Procedure
#####################
os.system("rm -rf " + dir_data + "mask2.image")
os.system("rm -rf " + dir_data + "*moment*")
fitsimages = glob.glob(dir_data + "*.fits")
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = fitsimages[i].replace(".fits", ".image"))

imagenames = glob.glob(dir_data + "*.image")



### create cube mask for 12CO
# ESO 148
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = 0.002 * 7.5,
                outmask = "mask_eso148.mask")

outmask = dir_data + "mask_eso148.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "5~80",
                 mask = "mask_eso148.mask",
                 thres = 0.002 * 6.5)

# ESO 286
myim.createmask(dir_data = dir_data,
                imagename = imagenames[1].split("/")[-1],
                thres = 0.002 * 8.0,
                outmask = "mask_eso286.mask")

outmask = dir_data + "mask_eso286.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[1],
                 chans = "25~106",
                 mask = "mask_eso286.mask",
                 thres = 0.002 * 6.0)

# IRAS 05189
myim.createmask(dir_data = dir_data,
                imagename = imagenames[2].split("/")[-1],
                thres = 0.002 * 2.,
                outmask = "mask_iras05189.mask")

outmask = dir_data + "mask_iras05189.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[2],
                 chans = "25~103",
                 mask = "mask_iras05189.mask",
                 thres = 0.002 * 3.5)

# IRAS 12112
myim.createmask(dir_data = dir_data,
                imagename = imagenames[3].split("/")[-1],
                thres = 0.0025 * 3.5,
                outmask = "mask_iras12112.mask")

outmask = dir_data + "mask_iras12112.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[3],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[3],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[3], mode = "list")["cdelt1"])
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[3],
                 chans = "115~211",
                 mask = "mask_iras12112.mask",
                 thres = 0.002 * 4.5)


# IRAS 13120
myim.createmask(dir_data = dir_data,
                imagename = imagenames[4].split("/")[-1],
                thres = 0.0023 * 4.0,
                outmask = "mask_iras13120.mask")

outmask = dir_data + "mask_iras13120.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[4],
                 chans = "3~103",
                 mask = "mask_iras13120.mask",
                 thres = 0.0023 * 5.0)


# IRAS 17207
myim.createmask(dir_data = dir_data,
                imagename = imagenames[5].split("/")[-1],
                thres = 0.0014 * 2.,
                outmask = "mask_iras17207.mask")

outmask = dir_data + "mask_iras17207.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[5],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[5],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[5], mode = "list")["cdelt1"])
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[5],
                 chans = "26~137",
                 mask = "mask_iras17207.mask",
                 thres = 0.0014 * 3.5)

# NGC 34
myim.createmask(dir_data = dir_data,
                imagename = imagenames[9].split("/")[-1],
                thres = 0.0017 * 3.5,
                outmask = "mask_ngc34.mask")

outmask = dir_data + "mask_ngc34.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[9],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[9],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[9], mode = "list")["cdelt1"])
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[9],
                 chans = "84~234",
                 mask = "mask_ngc34.mask",
                 thres = 0.0017 * 4.0)


# NGC 1614
myim.createmask(dir_data = dir_data,
                imagename = imagenames[6].split("/")[-1],
                thres = 0.0013 * 5.5,
                outmask = "mask_ngc1614.mask")

outmask = dir_data + "mask_ngc1614.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[6],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[6],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[6], mode = "list")["cdelt1"])
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[6],
                 chans = "0~55",
                 mask = "mask_ngc1614.mask",
                 thres = 0.0013 * 7.5)


# NGC 3110
myim.createmask(dir_data = dir_data,
                imagename = imagenames[7].split("/")[-1],
                thres = 0.0011 * 5.5,
                outmask = "mask_ngc3110.mask")

outmask = dir_data + "mask_ngc3110.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[7],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[7],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[7], mode = "list")["cdelt1"])
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[7],
                 chans = "13~42",
                 mask = "mask_ngc3110.mask",
                 thres = 0.0011 * 6.5)


# NGC 3256
myim.createmask(dir_data = dir_data,
                imagename = imagenames[8].split("/")[-1],
                thres = 0.0027 * 6.5,
                outmask = "mask_ngc3256.mask")

outmask = dir_data + "mask_ngc3256.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[8],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[8],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[8], mode = "list")["cdelt1"])
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[8],
                 chans = "0~87",
                 mask = "mask_ngc3256.mask",
                 thres = 0.0027 * 8.0)


# NGC 6240
myim.createmask(dir_data = dir_data,
                imagename = imagenames[10].split("/")[-1],
                thres = 0.0051 * 5.5,
                outmask = "mask_ngc6240.mask")

outmask = dir_data + "mask_ngc6240.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[10],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[10],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[10], mode = "list")["cdelt1"])
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[10],
                 chans = "27~174",
                 mask = "mask_ngc6240.mask",
                 thres = 0.0051 * 8.0)


# VV 114
myim.createmask(dir_data = dir_data,
                imagename = imagenames[11].split("/")[-1],
                thres = 0.0021 * 6.0,
                outmask = "mask_vv114.mask")

outmask = dir_data + "mask_vv114.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[11],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[11],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[11], mode = "list")["cdelt1"])
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[11],
                 chans = "0~59",
                 mask = "mask_vv114.mask",
                 thres = 0.0021 * 10.0)

