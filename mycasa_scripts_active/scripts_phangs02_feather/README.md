README.md for scripts_phangs02_feather

# History
2019-11-21: start coding

2019-12-05: finish coding

# General

This is a project aiming at test feathering technique for multi-part mosaic data like PHANGS NGC 3627 data. Implemen FeatherFirst (classical feather) and PBcorrFirst (Chris' feather) and some others.

# Memo
1. Input sky model should not be extremely bright (current sky model; total flux is similar to the brightest channel of the PHANGS NGC 0628 CO(2-1) cube).
2. Do not use **uvtaper** parameter in tclean (something is strange...), use imsmooth instead.
3. tclean is not perfect actually. The strongest negative sidelobe level is ~ -3 mJy.

# How to run
```
> execfile("myscript01_*")      # create reference fits file containing a reference corrdinate
> execfile("myscript02_*")      # for test00; create mosaic grids by running simobserve
> sh myscript03_*.sh            # correct the mosaic grids
> execfile("myscript04a_*")     # for test06/07/08; simobserve for model sky
> execfile("myscript05a_*")     # for test06/07; ms2ss-tclean
> execfile("myscript06_*")      # for test06/07; feather for individual mosaics
> execfile("myscript07_*")      # for test06/07; Feather/PBcorrFirst then merge
> execfile("myscript08_*")      # for test06/07/0607; merge then PBcorrFirst
> execfile("myscript09_*")      # create fits files
> execfile("myfig01_images.py") # create png image
> sh myfig02_merge_png.sh         # cleanup png files
```

# Versions
CASA Version 5.4.0-70

# Directory Structure
data/
  - mycasa_scripts_*/ - scripts_phangs02_feather/   # all scripts
  - myproj_*/ - proj_phangs02_feather/ - data_raw/  # all data required
