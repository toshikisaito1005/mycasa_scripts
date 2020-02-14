import os
import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()


dir_data = "../../myproj_published/proj_phangs04_school/data/"
galaxy = ["ngc0628"]
beams = ["60pc"]
alpha_co = 4.3


#####################
### Main Procedure
#####################
dir_working = dir_data + "../products/"

for i in range(len(galaxy)):
    # import data
    galname = galaxy[i]
    beam = beams[i]
    print("# working on " + galname + " data at " + beam)
    
    imagenames_12m7mtp = glob.glob(dir_data + galname + "*12m7mtp_*"+beam+"*.image_Kelvin")[0]
    errornames_12m7mtp = glob.glob(dir_data + galname + "*12m7mtp_*"+beam+"*.error_Kelvin")[0]
    imagenames_12m7m = glob.glob(dir_data + galname + "*12m7m_*"+beam+"*.image_Kelvin")[0]
    errornames_12m7m = glob.glob(dir_data + galname + "*12m7m_*"+beam+"*.image_Kelvin")[0]

    # define imval box
    x = str(imhead(imagenames_12m7mtp,"list")["shape"][0] - 1)
    y = str(imhead(imagenames_12m7mtp,"list")["shape"][1] - 1)
    box = "0,0," + x + "," + y

    # imval
    data_12m7mtp = imval(imagenames_12m7mtp,box=box)["data"]
    flat_12m7mtp = data_12m7mtp.flatten()
    
    error_12m7mtp = imval(errornames_12m7mtp,box=box)["data"]
    flat_error_12m7mtp = error_12m7mtp.flatten()
    
    data_12m7m = imval(imagenames_12m7m,box=box)["data"]
    flat_12m7m = data_12m7m.flatten()
    
    error_12m7m = imval(errornames_12m7m,box=box)["data"]
    flat_error_12m7m = error_12m7m.flatten()
    
    data_radec = imval(imagenames_12m7mtp,box=box)["coords"]
    flat_ra = data_radec[:,:,0].flatten()
    flat_dec = data_radec[:,:,1].flatten()
    
    flat_snr_12m7mtp = flat_12m7mtp/flat_error_12m7mtp
    flat_snr_12m7mtp[np.where(np.isnan(flat_snr_12m7mtp))]=0
    
    # plot
    fig = plt.figure(figsize=(10,10))
    plt.rcParams["font.size"] = 22
    plt.subplots_adjust(bottom=0.15, left=0.15, right=0.85, top=0.85)

    # ax1
    ax1 = fig.add_subplot(111)
    ax1.grid(which='major',linestyle='--')
    ax1.grid(which='minor',linestyle='--')
    
    ax1.plot([-2.5,4.2],
             [np.log10(0.1*10**-2.5),np.log10(0.1*10**4.2)],
             "-",color="black",lw=3,alpha=0.5, zorder=1)
    ax1.plot([-2.5,4.2],
             [np.log10(0.5*10**-2.5),np.log10(0.5*10**4.2)],
             "-",color="black",lw=5,alpha=0.5, zorder=1)
    ax1.plot([-2.5,4.2],
             [-2.5,4.2],
             "-",color="black",lw=10,alpha=0.5, zorder=1)

    ax1.text(1.6, 2.0, "1:1", rotation = 45)
    ax1.text(1.6, 1.4, "1:0.5", rotation = 45)
    ax1.text(1.6, 0.7, "1:0.1", rotation = 45)
        
    ax1.scatter(np.log10(flat_12m7mtp[flat_snr_12m7mtp<5.]),
                np.log10(flat_12m7m[flat_snr_12m7mtp<5.]),
                lw = 0, alpha = 0.2, s = 10, color = "blue",
                label = "S/N < 5", zorder=2)
        
    ax1.scatter(np.log10(flat_12m7mtp[flat_snr_12m7mtp>=5.]),
                np.log10(flat_12m7m[flat_snr_12m7mtp>=5.]),
                lw = 0, alpha = 0.2, s = 50, color = "red",
                label = "S/N $\geqq$ 5", zorder=3)

    ax1.set_xlim([-2.5,2.5])
    ax1.set_ylim([-2.5,2.5])
    ax1.set_xlabel("12m+7m+TP (K km s$^{-1}$)")
    ax1.set_ylabel("12m+7m (K km s$^{-1}$)")


    plt.title("12m+7m+TP vs 12m+7m (NGC 0628)")
    plt.legend(loc = "upper left")
    plt.savefig(dir_working+galname+"_scatter.png",dpi=100)

os.system("rm -rf *.last")
