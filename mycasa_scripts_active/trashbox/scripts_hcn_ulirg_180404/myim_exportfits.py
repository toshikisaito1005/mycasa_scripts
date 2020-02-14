import os
import re
import sys
import glob
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = ["../../hcn_ulirgs/hcn_eso148/",
            "../../hcn_ulirgs/hcn_eso286/",
            "../../hcn_ulirgs/hcn_iras05189/",
            "../../hcn_ulirgs/hcn_iras13120/",
            "../../hcn_ulirgs/hcn_irasf12112/",
            "../../hcn_ulirgs/hcn_irasf17208/"]


for i in range(len(dir_data)):
    imagenames = glob.glob(dir_data[i] + "*.moment*")
    for j in range(len(imagenames)):
        fitsimage = dir_data[i] \
            + imagenames[j].split("/")[-1].replace(".image", "") \
            + ".fits"
        os.system("rm -rf " + fitsimage)
        exportfits(imagename = imagenames[j],
            velocity = True,
            fitsimage = fitsimage)
        print(fitsimage)
        os.system("rm -rf " + imagenames[j])

