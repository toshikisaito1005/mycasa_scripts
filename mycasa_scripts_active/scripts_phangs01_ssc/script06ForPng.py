import os
import glob
import sys

os.system("rm -rf ../ngc4303*/*.png")
maskimage = "../ngc4303_7m/ngc4303_7m_only_co21_na.mask"

imagenames = glob.glob("../ngc4303*_sim0*/*.smooth.*")
default(imview)
for i in range(len(imagenames)):
    imview(raster = {"file": imagenames[i], "range": [-0.4,2.5], "scaling": -0.5},
           contour = {"file": maskimage, "levels": [1.0]},
	   axes = {"z": "Frequency"},
	   out = imagenames[i]+".png",
	   zoom = {"blc": [19,19], "trc": [235,235]})

imagenames = glob.glob("../ngc4303*_sim0*/*.model")
default(imview)
for i in range(len(imagenames)):
    imview(raster = {"file": imagenames[i], "range": [-0.03,0.15], "scaling": -0.5},
           contour = {"file": maskimage, "levels": [1.0]},
	   axes = {"z": "Frequency"},
	   out = imagenames[i]+".png",
	   zoom = {"blc": [19,19], "trc": [235,235]})

imagenames = glob.glob("../ngc4303*_sim0*/*.accuracy")
default(imview)
for i in range(len(imagenames)):
    imview(raster = {"file": imagenames[i], "range": [0.0,1.0], "scaling": -0.5},
           contour = {"file": maskimage, "levels": [1.0]},
	   axes = {"z": "Frequency"},
	   out = imagenames[i]+".png",
	   zoom = {"blc": [19,19], "trc": [235,235]})

