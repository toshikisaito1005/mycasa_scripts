import os
import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()


dir_data = "../../myproj_published/proj_phangs04_school/data/"
resolution = "500pc"
alpha_co = 4.3


#####################
### Functions
#####################
def beam_area(imagename):
    major = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beammajor")["value"]
    minor = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beamminor")["value"]
    pix = abs(imhead(imagename = imagename,
                     mode = "list")["cdelt1"])

    pixelsize = pix * 3600 * 180 / np.pi
    beamarea_arcsec = major * minor * np.pi/(4 * np.log(2))
    beamarea_pix = beamarea_arcsec / (pixelsize ** 2)
                   
    return beamarea_pix


#####################
### Main Procedure
#####################
dir_working = dir_data + "../products/"
imagenames_12m7mtp = glob.glob(dir_data + "*12m7mtp_" + resolution + ".image_Kelvin")
imagenames_12m7m = glob.glob(dir_data + "*12m7m_" + resolution + ".image_Kelvin")
errornames_12m7mtp = glob.glob(dir_data + "*12m7mtp_" + resolution + ".error_Kelvin")
errornames_12m7m = glob.glob(dir_data + "*12m7m_" + resolution + ".error_Kelvin")

galnames = []
values_12m7mtp = []
values_12m7m = []
snrs_12m7mtp = []
snrs_12m7m = []
for i in range(len(imagenames_12m7mtp)):
    # define imval box
    x = str(imhead(imagenames_12m7mtp[i],"list")["shape"][0] - 1)
    y = str(imhead(imagenames_12m7mtp[i],"list")["shape"][1] - 1)
    box = "0,0," + x + "," + y
    
    # galname
    galname = imagenames_12m7mtp[i].split("/")[-1].split("_")[0]

    # imval
    data_12m7mtp = imval(imagenames_12m7mtp[i],box=box)["data"]
    value_12m7mtp = data_12m7mtp.sum()
    
    error_12m7mtp = imval(errornames_12m7mtp[i],box=box)["data"]
    value_error_12m7mtp = error_12m7mtp.sum()
    
    snr_12m7mtp = value_12m7mtp / value_error_12m7mtp

    data_12m7m = imval(imagenames_12m7m[i],box=box)["data"]
    value_12m7m = data_12m7m.sum()

    error_12m7m = imval(errornames_12m7m[i],box=box)["data"]
    value_error_12m7m = error_12m7m.sum()
    
    snr_12m7m = value_12m7m / value_error_12m7m
    
    #beamarea_pix = beam_area(imagenames_12m7mtp[i])

    galnames.append(galname)
    values_12m7mtp.append(value_12m7mtp)
    values_12m7m.append(value_12m7m)
    snrs_12m7mtp.append(snr_12m7mtp)
    snrs_12m7m.append(snr_12m7m)

data2save = np.c_[galnames,values_12m7mtp,values_12m7m,snrs_12m7mtp,snrs_12m7m]
np.savetxt("total_flux_all_gals_500pc.txt",data2save,fmt="%s",
           header="galname flux_12m7mtp flux_12m7m snr_12m7mtp snr_12m7m")

# plot
fig = plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 22
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)

# ax1
ax1 = fig.add_subplot(111)
ax1.grid(which='major',linestyle='--')
ax1.grid(which='minor',linestyle='--')

xdata = np.array(values_12m7mtp)
ydata = (np.array(values_12m7mtp) - np.array(values_12m7m))/np.array(values_12m7mtp) * 100
ax1.errorbar(np.log10(xdata[np.array(snrs_12m7mtp)>=5]),
             ydata[np.array(snrs_12m7mtp)>=5],
             yerr = ydata[np.array(snrs_12m7mtp)>=5] * np.sqrt(0.1**2+0.1**2),
             marker = "o", markersize = 10, linestyle="", lw = 1, alpha = 1.0, color = "black")

ax1.set_xlim([3.4,6.9])
ax1.set_ylim([0,70])
ax1.set_xlabel("log 12m+7m+TP (K km s$^{-1}$)")
ax1.set_ylabel("Missing flux of 12m+7m (%)")

plt.title("Missing Flux at 500 pc Resolution")
plt.legend(loc = "upper left")
plt.savefig(dir_working+"missing_flux_all_gals.png",dpi=100)

os.system("rm -rf *.last")
