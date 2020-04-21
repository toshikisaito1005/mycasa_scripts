import os, sys, glob
import shutil

dir_v3 = "/data/beegfs/astro-storage/groups/schinnerer/PHANGS/ALMA/Compare_v3p4_v4/ngc4303_v3p4/"
dir_v4_bias_cycf = "/data/beegfs/astro-storage/groups/schinnerer/PHANGS/ALMA/Compare_v3p4_v4/ngc4303_v4_bias_cycf/"

v3_image = glob.glob(dir_v3 + "ngc4303_7m_co21.image")[0]
v4_b6_c1 = glob.glob(dir_v4_bias_cycf + "ngc4303_7m_co21_bias0p6_cycf1p0.image")[0]
v4_b6_c3 = glob.glob(dir_v4_bias_cycf + "ngc4303_7m_co21_bias0p6_cycf3p0.image")[0]
v4_b9_c1 = glob.glob(dir_v4_bias_cycf + "ngc4303_7m_co21_bias0p9_cycf1p0.image")[0]
v4_b9_c3 = glob.glob(dir_v4_bias_cycf + "ngc4303_7m_co21_bias0p9_cycf3p0.image")[0]
v3_products = [v3_image, v4_b6_c1, v4_b6_c3, v4_b9_c1, v4_b9_c3]


for i in range(len(v3_products)):
    imagename = v3_products[i]
    output = "./" + imagename.split("/")[-1].replace("_7m_co21","_7m_co21_v3")
    os.system("rm -rf " + output)
    shutil.copytree(imagename, output)
