import glob
import numpy as np

fidelityimages = glob.glob("../model*sim04/*.accuracy")

for i in range(len(fidelityimages)):
    box_tmp = imhead(fidelityimages[i],mode="list")["shape"]
    box_x = str(box_tmp[0] - 1)
    box_y = str(box_tmp[1] - 1)
    box = "0,0," + box_x + "," + box_y
    fidelity_tmp = imval(fidelityimages[i],box=box)
    x = fidelity_tmp['data'].flatten()
    median_fidelity = np.median(x[x>0])
    print(fidelityimages[i] +', ' + str(median_fidelity))
