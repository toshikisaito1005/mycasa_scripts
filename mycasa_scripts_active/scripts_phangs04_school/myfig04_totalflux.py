import os
import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()


dir_data = "../../myproj_published/proj_phangs04_school/data/"
galaxy = ["ngc3627"]
alpha_co = 4.3


#####################
### Main Procedure
#####################
# mkdir
dir_working = dir_data + "../products/"

for i in range(len(galaxy)):
    galname = galaxy[i]
    imagenames_12m7mtp = glob.glob(dir_data + galname + "*12m7mtp_*.image_Kelvin")
    imagenames_12m7m = glob.glob(dir_data + galname + "*12m7m_*.image_Kelvin")
    janskybeams_12m7mtp = glob.glob(dir_data + galname + "*12m7mtp_*.image")
    janskybeams_12m7m = glob.glob(dir_data + galname + "*12m7m_*.image")

    resolution_12m7mtp = []
    flux_12m7mtp = []
    flux_12m7m = []
    fluxjy_12m7mtp = []
    fluxjy_12m7m = []
    for j in range(len(imagenames_12m7mtp)):
        # measure values
        res = str(int(imagenames_12m7mtp[j].split("tp_")[-1].replace("pc.image_Kelvin","")))
        fl1 = str(int(imstat(imagenames_12m7mtp[j])["sum"][0]))
        fl2 = str(int(imstat(imagenames_12m7m[j])["sum"][0]))
        jy1 = str(int(imstat(janskybeams_12m7mtp[j])["flux"][0]))
        jy2 = str(int(imstat(janskybeams_12m7m[j])["flux"][0]))
        
        # merge
        resolution_12m7mtp.append(res)
        flux_12m7mtp.append(fl1)
        flux_12m7m.append(fl2)
        fluxjy_12m7mtp.append(jy1)
        fluxjy_12m7m.append(jy2)
    
    # export txt
    output = np.c_[resolution_12m7mtp,flux_12m7mtp,flux_12m7m]
    output_jy = np.c_[resolution_12m7mtp,fluxjy_12m7mtp,fluxjy_12m7m]
    header = "beamsize(pc) flux_12m7mtp(Jy.km/s) flux_12m7m(Jy.km/s)"
    np.savetxt("total_flux.txt",output,fmt="%s",header=header)

    # plot
    x = output.astype("int64")[:,0]
    y1 = output.astype("int64")[:,1]
    y2 = output.astype("int64")[:,2]
    y1jy = output_jy.astype("int64")[:,1]
    y2jy = output_jy.astype("int64")[:,2]

    fig = plt.figure(figsize=(10,10))
    plt.rcParams["font.size"] = 22
    plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)

    # ax1
    ax1 = fig.add_subplot(111)
    ax1.grid(which='major',linestyle='--')
    ax1.grid(which='minor',linestyle='--')

    ax1.errorbar(x+2, y1/1000000., yerr = y1*0.1/1000000.,
                 ecolor = "red", color ="red", lw = 5, capsize = 0,
                 label = "12m+7m+TP (all structures)")
    ax1.errorbar(x-2, y2/1000000., yerr = y2*0.1/1000000.,
                 ecolor = "blue", color = "blue", lw = 5, capsize = 0,
                 label = "12m+7m (highpass filtered)")

    ax1.set_xlim([0,550])
    ax1.set_ylim([(y2/1000000.).min()*0.7,
                  (y1/1000000.).max()*1.2])
    ax1.set_xlabel("Spatial Resolution (pc)")
    ax1.set_ylabel("Total Flux (10$^6$ K km s$^{-1}$)")
    ax1.set_title(galname.replace("ngc","NGC "))
    """
    # ax2
    factor = 3.25e7 / 230.53800**2 * 9.8**2 / 1e8
    X = x
    Y1 = y1jy * factor * alpha_co
    Y2 = y2jy * factor * alpha_co
    ax2 = ax1.twinx()

    ax2.errorbar(X, Y1, yerr = Y1*0.1,
                 ecolor = "green", color ="green", lw = 15, capsize = 0,
                 alpha = 0)

    ax2.set_xlim([0,550])
    ax2.set_ylim([Y2.min()*0.8,
                  Y1.max()*1.2])
    ax2.set_ylabel("Molecular Gas Mass (10$^{8}$ $M_{\odot}$)")
    """
    ax1.legend(loc="lower left")
    plt.savefig(dir_working+galname+"_totalflux.png",dpi=100)

os.system("rm -rf *.last")
