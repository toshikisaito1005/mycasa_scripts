import os
import glob
import scripts_phangs_r21 as r21
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ioff()
reload(r21)


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galaxy = ["ngc0628",
          "ngc4321",
          #"ngc4254",
          "ngc3627"]
co10noises = [[0.020,0.020,0.030,0.040,0.050,0.060,0.060,0.070,0.080,0.090,0.095,0.130], # ngc0628
              [0.020,0.020,0.028,0.028,0.035,0.040,0.045,0.050,0.055,0.060,0.060,0.060], # ngc4321
              #[0.030,0.036,0.040,0.045,0.050,0.050,0.055,0.060,0.066,0.080], # ngc4254
              [0.020,0.038,0.045,0.055,0.065,0.065,0.080,0.090,0.100,0.110,0.125,0.150]] # ngc3627
co21noises = [[0.020,0.025,0.030,0.035,0.037,0.060,0.060,0.039,0.040,0.042,0.043,0.055], # ngc0628
              [0.020,0.022,0.026,0.026,0.027,0.028,0.029,0.030,0.030,0.030,0.031,0.050], # ngc4321
              #[0.028,0.030,0.032,0.033,0.033,0.035,0.037,0.038,0.040,0.060], # ngc4254
              [0.020,0.023,0.025,0.027,0.027,0.027,0.028,0.029,0.030,0.031,0.033,0.040]] # ngc3627
"""
co10noises = [[0.020,0.130], # ngc0628
              [0.020,0.060], # ngc4321
              #[0.030,0.080], # ngc4254
              [0.038,0.150]] # ngc3627
co21noises = [[0.025,0.055], # ngc0628
              [0.022,0.050], # ngc4321
              #[0.028,0.060], # ngc4254
              [0.023,0.040]] # ngc3627
"""
beam = [[4.0,6.0,8.0,10.0,12.0,13.6,14.0,16.0,18.0,20.0,22.0,33.0],
        [8.0,10.0,12.0,14.0,15.0,16.0,18.0,20.0,22.0,24.0,26.0,33.0],
        [4.0,6.0,8.0,8.5,10.0,12.0,14.0,16.0,18.0,20.0,22.0,33.0]]
snr_mom = 2.5


#####################
### Main
#####################
#for i in range(len(galaxy)):
list_master = []
for i in [0,1,2]:
    galname = galaxy[i]
    co10images = glob.glob(dir_proj + galname + "_*/co10*cube.image")
    co10images.extend(glob.glob(dir_proj + galname + "_*/co10*cube*p*.image"))
    co21images = glob.glob(dir_proj + galname + "_*/co21*cube.image")
    co21images.extend(glob.glob(dir_proj + galname + "_*/co21*cube*p*.image"))

    list_co10 = []
    list_co21 = []
    for j in range(len(co10images)):
        beamp = co10images[j].split("/")[-1].split("_")[-1].replace(".image","")
        print("# " + galname + " " + beamp)
        # measure noise
        output = dir_proj+"eps/noise_"+galname+"_"+co10images[j].split("/")[-1].replace(".image","").replace("_cube","")+".png"
        co10rms = r21.noisehist(co10images[j],
                                 co10noises[i][j],
                                 output,
                                 snr_mom,
                                 logscale=False,
                                 plotter=False)
        output = dir_proj+"eps/noise_"+galname+"_"+co21images[j].split("/")[-1].replace(".image","").replace("_cube","")+".png"
        co21rms = r21.noisehist(co21images[j],
                                 co21noises[i][j],
                                 output,
                                 snr_mom,
                                 logscale=False,
                                 plotter=False)
        list_co10.append(co10rms)
        list_co21.append(co21rms)
    #
    list_gal = np.c_[beam[i],list_co10,list_co21]
    list_master.append(list_gal)

# plot
list_0628 = list_master[0]
list_3627 = list_master[1]
list_4321 = list_master[2]
np.savetxt(dir_proj + "eps/ngc0628_noise.txt", list_0628)
np.savetxt(dir_proj + "eps/ngc3627_noise.txt", list_3627)
np.savetxt(dir_proj + "eps/ngc4321_noise.txt", list_4321)

fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.10, left=0.19, right=0.99, top=0.90)

ax1.plot(list_0628[:,0], np.log10(list_0628[:,1] * 1.222e6/list_0628[:,0]**2/115.27120**2),
	"-", color=cm.brg(0/2.5), markeredgewidth=0, markersize = 10,
  alpha = 0.5, lw=7, label = "NGC 0628 CO(1-0)")
ax1.plot(list_0628[:,0], np.log10(list_0628[:,2] * 1.222e6/list_0628[:,0]**2/230.53800**2),
	"--", color=cm.brg(0/2.5), markeredgewidth=0, markersize = 10,
  alpha = 0.5, lw=7, label = "NGC 0628 CO(2-1)")

ax1.plot(list_3627[:,0], np.log10(list_3627[:,1] * 1.222e6/list_3627[:,0]**2/115.27120**2),
	"-", color=cm.brg(1/2.5), markeredgewidth=0, markersize = 10,
  alpha = 0.5, lw=7, label = "NGC 3627 CO(1-0)")
ax1.plot(list_3627[:,0], np.log10(list_3627[:,2] * 1.222e6/list_3627[:,0]**2/230.53800**2),
	"--", color=cm.brg(1/2.5), markeredgewidth=0, markersize = 10,
  alpha = 0.5, lw=7, label = "NGC 3627 CO(2-1)")

ax1.plot(list_4321[:,0], np.log10(list_4321[:,1] * 1.222e6/list_4321[:,0]**2/115.27120**2),
	"-", color=cm.brg(2/2.5), markeredgewidth=0, markersize = 10,
  alpha = 0.5, lw=7, label = "NGC 4321 CO(1-0)")
ax1.plot(list_4321[:,0], np.log10(list_4321[:,2] * 1.222e6/list_4321[:,0]**2/230.53800**2),
	"--", color=cm.brg(2/2.5), markeredgewidth=0, markersize = 10,
  alpha = 0.5, lw=7, label = "NGC 4321 CO(2-1)")

ax1.set_xlabel("Beam Size (arcsec)")
ax1.set_ylabel("log rms per pixel (K)")
ax1.set_ylim([10**-3.5,10**0.5])
ax1.set_ylim([-3.5,0.5])
ax1.set_xlim([0,37])

plt.title("(b) log rms vs. Beam Size")
plt.legend()
plt.savefig(dir_proj+"eps/noise_vs_beam.png",dpi=300)


# plot noise histograms
i=0
j=0
galname = galaxy[i]
co10image = glob.glob(dir_proj + galname + "_*/co10*cube.image")[0]
output = dir_proj+"eps/noise_"+galname+"_"+co10image.split("/")[-1].replace(".image","").replace("_cube","")+".png"
co10rms = r21.noisehist_kelvin(co10image,
                        1.222e6/4.0**2/115.27120**2,
                        co10noises[i][j],
                        output,
                        snr_mom,
                        logscale=False,
                        plotter=True,
                        title = "(a) NGC 0628 4.0\" CO(1-0) Cube")

"""
output = dir_proj+"eps/noise_"+galname+"_"+co10image.split("/")[-1].replace(".image","").replace("_cube","")+"_log.png"
co10rms = r21.noisehist_kelvin(co10image,
                        1.222e6/4.0**2/115.27120**2,
                        co10noises[i][j],
                        output,
                        logscale=True,
                        plotter=True)
"""

os.system("rm -rf *.last")
