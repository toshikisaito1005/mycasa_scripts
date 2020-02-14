import os
import sys
import glob

fits_files = glob.glob("*.fits")
for i in range(len(fits_files)):
    print("# convert " + fits_files[i])
    done = glob.glob(fits_files[i].replace("fits","image"))
    if not done:
        importfits(fitsimage = fits_files[i],
                   imagename = fits_files[i].replace("fits","image"))


