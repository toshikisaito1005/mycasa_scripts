import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ngc4038/images/"
box = ""
pixelmin = 5.
rms = 0.011

#####################
### Main Procedure
#####################
os.system("rm -rf " + dir_data + "mask2.image")
imagenames = glob.glob(dir_data + "*.image")


### create cube mask for 12CO
myim.createmask(dir_data = dir_data,
    imagename = imagenames[0].split("/")[-1],
    thres = 2.5 * rms,
    outmask = "mask_12CO.mask")


outmask = dir_data + "mask_12CO.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")

major = imhead(imagename = imagenames[0],
               mode = "get",
               hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[0],
               mode = "get",
               hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[0],
                 mode = "list")["cdelt1"])
pixelsize = pix*3600*180 / np.pi
beamarea = (major*minor*np.pi/(4*np.log(2))) / (pixelsize**2)

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

### create momement maps for 12co21
myim.moment_maps(dir_data = dir_data,
    imagename = imagenames[0],
    chans = "55~310",
    mask = "mask_12CO.mask",
    thres = 3. * rms)

os.system("rm -rf " + dir_data + "*immath")
os.system("rm -rf " + dir_data + "*mask*")
