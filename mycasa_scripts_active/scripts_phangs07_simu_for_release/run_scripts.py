
"""
# done
### two point sources, mfs, large mosaic
this_proj = "sim01"
imsize = 512
this_fov = 120
mapsize=["",""]
#
execfile("myscript01_mocksky.py")
image_mocksky = "simulated_sky.fits"
execfile("myscript02_makems.py")
execfile("myscript03_dirtymap_mfs.py")
"""

"""
# done
### two point sources, mfs, single pointing
this_proj = "sim02"
imsize = 45
this_fov = 30
mapsize=["",""]
#
execfile("myscript01_mocksky.py")
image_mocksky = "simulated_sky.fits"
execfile("myscript02_makems.py")
execfile("myscript03_dirtymap_mfs.py")
"""

"""
# done
### two point sources, cube, single pointing
this_proj = "sim03"
imsize = 45
this_fov = 30
mapsize=["",""]
#
#execfile("myscript01_mocksky.py")
image_mocksky = "simulated_sky.fits"
#execfile("myscript02_makems.py")
execfile("myscript04_dirtymap_cube.py")
"""

this_proj = "sim04"
imsize = 512
this_fov = 120
mapsize=["",""]
image_mocksky = "ngc1097_12m+7m+tp_co21_pbcorr_trimmed_k.fits"
execfile("myscript02_makems.py")
