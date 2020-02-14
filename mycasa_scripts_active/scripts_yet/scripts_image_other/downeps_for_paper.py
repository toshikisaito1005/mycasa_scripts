import os
import sys
import glob

eps_files_all = glob.glob("*.eps")
eps_files = []
for i in range(len(eps_files_all)):
    if os.path.getsize(eps_files_all[i]) > 1000000:
        eps_files.append(eps_files_all[i])

for i in range(len(eps_files)):
    output_png = eps_files[i].replace(".eps", ".png")
    os.system("rm -rf " + output_png)
    os.system("convert " + eps_files[i] + " " + output_png)
    os.system("rm -rf " + eps_files[i])
    os.system("convert " + output_png + " eps2:" + eps_files[i])
    os.system("rm -rf " + output_png)
