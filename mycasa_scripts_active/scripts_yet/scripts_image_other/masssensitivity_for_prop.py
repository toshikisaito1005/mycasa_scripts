import os
import re
import sys
import glob
import scipy
import numpy as np


### Source Property
sources = [""]
# ngc6240
#z = 0.024480
#D_L = 104.7   # Mpc
# vv114
#z = 0.020067
#D_L = 87.0
# ngc1614
#z = 0.015938
#D_L = 65.0
# ngc3256
#z = 0.009354
#D_L = 38.8
# ngc5257/8
z = 0.022676
D_L = 95.9

### Assumed GMC Property
M_H2 = 3. * 10. ** 6.   # Msun
linewidth = 20.   # km/s
a_co = 0.8
sn_ratio = 5.

### line Property
f_rest = 115.27120


#####################
### Main Procedure
#####################
L_co = M_H2 / a_co
f_obs = f_rest / (1 + z)

Cnst = 3.25 * 10. ** 7. / (f_obs ** 2.) * D_L ** 2. / (1 + z) ** 3.
Sco_dv = L_co / Cnst

peak = Sco_dv / np.sqrt(2 * np.pi * linewidth ** 2.)
sensitivity = round(peak/5. * 1000., 2)

print("To detect " + str(M_H2) + " Msun objects with S/N = " + str(sn_ratio) + ",")
print("You need rms = " + str(sensitivity) + " mJy")
print("Peak = " + str(round(peak * 1000., 2)))
