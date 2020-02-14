import glob

cubes = glob.glob("../*/ngc4303_*_na*.pbcor")
cubes.append("../ngc4303_cdf/_tmp_ngc4303_tp_co21.startmodel")

for i in range(len(cubes)):
    outfile=cubes[i].replace(".image.pbcor","").replace(".startmodel","")+".moment0"
    os.system("rm -rf "+outfile)
    immoments(imagename=cubes[i],
              moments=[0],
	      chans="5~80",
	      outfile=outfile)

cubes = glob.glob("../*/ngc4303_*_na.image")

for i in range(len(cubes)):
    imsmooth(imagename=cubes[i],
             targetres=True,
	     major="10arcsec",
	     minor="10arcsec",
	     pa="0deg",
	     outfile=cubes[i]+".smooth")

