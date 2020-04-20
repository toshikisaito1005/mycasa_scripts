import os, sys, glob
import shutil

dir_v3 = "/data/beegfs/astro-storage/groups/schinnerer/PHANGS/ALMA/Compare_v3p4_v4/ngc4303_v3p4/"
dir_v4 = "/data/beegfs/astro-storage/groups/schinnerer/PHANGS/ALMA/Compare_v3p4_v4/ngc4303_v4/"

v3_image    = glob.glob(dir_v3 + "ngc4303_7m_co21.image")[0]
v3_model    = glob.glob(dir_v3 + "ngc4303_7m_co21.model")[0]
v3_psf      = glob.glob(dir_v3 + "ngc4303_7m_co21.psf")[0]
v3_pb       = glob.glob(dir_v3 + "ngc4303_7m_co21.pb")[0]
v3_residual = glob.glob(dir_v3 + "ngc4303_7m_co21.residual")[0]
v3_weight   = glob.glob(dir_v3 + "ngc4303_7m_co21.weight")[0]
v3_mask     = glob.glob(dir_v3 + "ngc4303_7m_co21.mask")[0]
v3_products = [v3_image, v3_model, v3_psf, v3_pb, v3_residual, v3_weight, v3_mask]

v4_image    = glob.glob(dir_v4 + "ngc4303_7m_co21.image")[0]
v4_model    = glob.glob(dir_v4 + "ngc4303_7m_co21.model")[0]
v4_psf      = glob.glob(dir_v4 + "ngc4303_7m_co21.psf")[0]
v4_pb       = glob.glob(dir_v4 + "ngc4303_7m_co21.pb")[0]
v4_residual = glob.glob(dir_v4 + "ngc4303_7m_co21.residual")[0]
v4_weight   = glob.glob(dir_v4 + "ngc4303_7m_co21.weight")[0]
v4_mask     = glob.glob(dir_v4 + "ngc4303_7m_co21.mask")[0]
v4_products = [v4_image, v4_model, v4_psf, v4_pb, v4_residual, v4_weight, v4_mask]

for i in range(len(v3_products)):
    imagename = v3_products[i]
    output = "./" + imagename.split("/")[-1].replace("_7m_co21","_7m_co21_v3")
    os.system("rm -rf " + output)
    shutil.copytree(imagename, output)

for i in range(len(v4_products)):
    imagename = v4_products[i]
    output = "./" + imagename.split("/")[-1].replace("_7m_co21","_7m_co21_v4")
    os.system("rm -rf " + output)
    shutil.copytree(imagename, output)

