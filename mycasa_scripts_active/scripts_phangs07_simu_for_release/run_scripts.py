
this_proj = "sim02" # "sim01"
# size of the mocksky in pixel
imsize = 64 # 512
this_mapsize=["",""]

execfile("myscript01_mocksky.py")
execfile("myscript02_makems.py")
execfile("myscript03_dirtymap.py")
