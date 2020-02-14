import os
import glob
import numpy as np

suffix = "sim04"

imagename = project+"/"+project+".aca.tp.skymodel"
outfile = "/home/saito/Desktop/ssc_test/"+suffix+"/"+suffix+".aca.skymodel"
os.system("rm -rf " + outfile)
imsmooth(imagename = imagename,
         major = "10arcsec",
         minor = "10arcsec",
	 pa = "0deg",
	 outfile = outfile)

"""
sim_model = "/home/saito/Desktop/ssc_test/"+suffix+"/"+suffix+".aca.tp.skymodel"
sim_data = "/home/saito/Desktop/ssc_test/ngc4303_caf/ngc4303_7m+tp+caf_co21_na.image"

bmaj = 8.79
bmin = 5.01
barea = np.round(bmaj * bmin * np.pi / (4 * np.log(2)), 4)

outfile = "/home/saito/Desktop/ssc_test/"+suffix+"/"+suffix+".aca.tp.skymodel_jyperb"
os.system("rm -rf " + outfile)
immath(imagename = sim_model,
       outfile = outfile,
       mode = "evalexpr",
       expr = "IM0*" + str(barea))

bpa = 111.1
imhead(imagename = outfile, mode = "put", hdkey = "beammajor", hdvalue = str(bmaj) + "arcsec")
imhead(imagename = outfile, mode = "put", hdkey = "beamminor", hdvalue = str(bmin) + "arcsec")
imhead(imagename = outfile, mode = "put", hdkey = "beampa", hdvalue = str(bpa) + "deg")
imhead(imagename = outfile, mode = "put", hdkey = "bunit", hdvalue = "Jy/beam")
"""

data2conv_tmp_ = glob.glob("../*_"+suffix+"/*.image")
data2conv = [s for s in data2conv_tmp_ if "_tmp_" not in s]
data2conv.extend(glob.glob("../*_"+suffix+"/*.feather"))

for i in range(len(data2conv)):
    output = data2conv[i].replace(".image","")+".smooth"
    os.system("rm -rf " + output)
    imsmooth(imagename = data2conv[i],
             targetres = True,
	     major = "10arcsec",
	     minor = "10arcsec",
	     pa = "0deg",
	     outfile = output)

    os.system("rm -rf " + output + ".pbcor")
    impbcor(imagename = output,
            pbimage = "../model_7m_"+suffix+"/model_7m_only_co21_br.pb",
	    mode = "divide",
	    outfile = output + ".pbcor")

os.system("rm -rf *.last")

