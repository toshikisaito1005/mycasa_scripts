import numpy as np
import math
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib.colors as clr
plt.ioff()


#####################
### Define Parameters
#####################


#####################
### Main Procedure
#####################
dir_data = "../../aca_yamashita/"
dir_fits = dir_data + "data/"
dir_momnt = dir_data + "moment/"

### moment map creation
os.system("mkdir " + dir_momnt)

# moment 8
fitsfiles = glob.glob(dir_fits + "*.fits")
for i in range(len(fitsfiles)):
    immoments(imagename = fitsfiles[i],
              moments = [8],
              outfile = dir_momnt + fitsfiles[i].split("/")[-1].replace(".fits",".moment8"))
