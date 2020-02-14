import re, os, glob
import os.path
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
#matplotlib.use('Agg')

dir_data = "../../hcn_ulirgs/"

dir_fits = glob.glob(dir_data + "hcn_*")
dir_fits.append(dir_fits[0])
dir_fits.append(dir_fits[4])
dir_fits.sort()

target = ["eso148n",
          "eso148s",
          "eso286",
          "irasf05189",
          "iras13120",
          "iras12112n",
          "iras12112s",
          "irasf17207"]

target_ra = ["23h15m46.735s",
             "23h15m46.742s",
             "20h58m26.799s",
             "05h21m01.400s",
             "13h15m06.339s",
             "12h13m46.059s",
             "12h13m45.940s",
             "17h23m21.956s"]

target_decl = ["-59d03m10.022s",
               "-59d03m15.590s",
               "-42d39m00.338s",
               "-25d21m45.284s",
               "-55d09m21.940s",
               "+02d48m41.574s",
               "+02d48m39.178s",
               "-00d17m00.876s"]

for i in range(len(dir_fits)):
    image_spws = glob.glob(dir_fits[i] + "/*spw*.fits")
    region_txt = dir_fits[i] + "/" + target[i] + ".region"
    os.system("rm -rf " + region_txt)
    f = open(region_txt, "w")
    f.write("#CRTFv0\n")
    f.write("global coord=J2000\n")
    f.write("\n")
    f.write("circle[[" + target_ra[i] + ", " + target_decl[i]
            + "], 0.3arcsec]")
    f.write("")
    f.close()
    for j in range(len(image_spws)):
        value = imval(imagename = image_spws[j],
                      region = region_txt)
        value_masked = value["data"] * value["mask"]
        freq_obs = value['coords'][0,0,:,2] #Hz
        product = np.c_[freq_obs, value_masked.sum(axis = (0, 1))]
        product_spw = region_txt.replace(".region",
                                         "_spw" + str(j) + ".txt")
        os.system("rm -rf " + product_spw)
        np.savetxt(product_spw,
                   product,
                   delimiter = " ")

