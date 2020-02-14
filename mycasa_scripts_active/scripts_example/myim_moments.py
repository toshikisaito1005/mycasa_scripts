import os, re, sys, glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../data/" # relative path to your data
pixelmin = 5. # remove small mask reions smaller than beamsize * pixelmin
imagename = "hogehoge.image" # your CASA cube name
rms = 0.001
threshold_mask = 2. #threshold for masking: rms * threshold_mask
chans = "10~20" # select channnels for immoments
threshold_moment = 3. # thrshold for immomenths: rms * threshold_moment


#####################
### Main Procedure
#####################

### create cube mask
myim.createmask(dir_data = dir_data,
    imagename = imagename,
    thres = rms * threshold_mask,
    outmask = "datacube.mask")


outmask = dir_data + "datacube.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = dir_data + imagename,
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = dir_data + imagename,
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = dir_data + imagename, mode = "list")["cdelt1"])
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


### create momement maps
myim.moment_maps(dir_data = dir_data,
    imagename = dir_data + imagename,
    chans = chans,
    mask = "datacube.mask",
    thres = rms * threshold_moment)


