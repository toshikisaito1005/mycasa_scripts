import math
import numpy as np

dir_proj = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/"
imageco10 = dir_proj + "image_co10/n6240_co10_mom8_Kelvin.image"
imageco21 = dir_proj + "image_co21/n6240_co21_mom8_Kelvin.image"

###
def distance(x, y):
    ra_cnt = 253.245
    dec_cnt = 2.40111
    scale = 0.48
    x_new = x - ra_cnt
    y_new = y - dec_cnt
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale
    return r

###
length_x = imhead(imageco10,mode="list")["shape"][0] - 1
length_y = imhead(imageco10,mode="list")["shape"][1] - 1

###
box = "0,0,"+str(length_x)+","+str(length_y)

###
valueco10_tmp = imval(imageco10,box=box)["data"]
valueco10 = valueco10_tmp.flatten()

###
valueco21_tmp = imval(imageco21,box=box)["data"]
valueco21 = valueco21_tmp.flatten()

###
cut_zero = np.where((valueco10 > 0) & (valueco21 > 0))
valueco10_cut = valueco10[cut_zero]
valueco21_cut = valueco21[cut_zero]

###
#
valuera_tmp = imval(imageco10,box=box)["coords"][:,:,0] * 180 / np.pi
valuera_tmp2 = valuera_tmp.flatten()
valuera_cut = valuera_tmp2[cut_zero]

#
valuedec_tmp = imval(imageco10,box=box)["coords"][:,:,1] * 180 / np.pi
valuedec_tmp2 = valuedec_tmp.flatten()
valuedec_cut = valuedec_tmp2[cut_zero]

#
valuedist_cut = distance(valuera_cut, valuedec_cut)

#
datatable = np.c_[valuedist_cut,valueco10_cut,valueco21_cut]
np.savetxt("n6240_mom8_data.txt",datatable)

os.system("rm -rf *.last")
