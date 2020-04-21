import os, sys, glob
import shutil


dir_data = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready_bias_cycf/"
targetbeam = "9.0arcsec"


####################
### main
####################
# mkdir
done = glob.glob(dir_ready)
if not done:
	os.mkdir(dir_ready)


# get v4 CASA files
v3_image = glob.glob(dir_data + "ngc4303_7m_co21_v3.image")
v4_image = glob.glob(dir_data + "ngc4303_7m_co21_bias*.image")
v3_image.sort()
v4_image.sort()


# regrid v4 and move to the ready directory
print("### regrid v4 and mv")
for i in range(len(v4_image)):
	# get names
	imagename = v4_image[i]
	template = v3_image[0]
	output = dir_ready + v4_image[i].split("/")[-1].replace("ngc4303_7m_co21","ngc4303_7m_co21_v4")
	# imregrid
	os.system("rm -rf " + output)
	imregrid(imagename=imagename, template=template, output=output)


# move v3 to the ready directory
print("### mv v3")
for i in range(len(v3_image)):
	imagename = v3_image[0]
	output = dir_ready + imagename.split("/")[-1]
	os.system("rm -rf " + output)
	shutil.copytree(imagename, output)


# smooth v3
print("### smooth v3")
imagename = dir_ready + "ngc4303_7m_co21_v3.image"
outfile = dir_ready + "ngc4303_7m_co21_v3.image.smooth"
os.system("rm -rf " + outfile)
imsmooth(imagename=imagename,targetres=True,major=targetbeam,minor=targetbeam,pa="0deg",outfile=outfile)


# smooth v4
print("### smooth v4")
targetbeam = "9.0arcsec"
imagename = dir_ready + "ngc4303_7m_co21_v4_bias0p6_cycf1p0.image"
outfile = dir_ready + "ngc4303_7m_co21_v4_bias0p6_cycf1p0.image.smooth"
os.system("rm -rf " + outfile)
imsmooth(imagename=imagename,targetres=True,major=targetbeam,minor=targetbeam,pa="0deg",outfile=outfile)

imagename = dir_ready + "ngc4303_7m_co21_v4_bias0p6_cycf3p0.image"
outfile = dir_ready + "ngc4303_7m_co21_v4_bias0p6_cycf3p0.image.smooth"
os.system("rm -rf " + outfile)
imsmooth(imagename=imagename,targetres=True,major=targetbeam,minor=targetbeam,pa="0deg",outfile=outfile)

imagename = dir_ready + "ngc4303_7m_co21_v4_bias0p9_cycf1p0.image"
outfile = dir_ready + "ngc4303_7m_co21_v4_bias0p9_cycf1p0.image.smooth"
os.system("rm -rf " + outfile)
imsmooth(imagename=imagename,targetres=True,major=targetbeam,minor=targetbeam,pa="0deg",outfile=outfile)

imagename = dir_ready + "ngc4303_7m_co21_v4_bias0p9_cycf3p0.image"
outfile = dir_ready + "ngc4303_7m_co21_v4_bias0p9_cycf3p0.image.smooth"
os.system("rm -rf " + outfile)
imsmooth(imagename=imagename,targetres=True,major=targetbeam,minor=targetbeam,pa="0deg",outfile=outfile)
