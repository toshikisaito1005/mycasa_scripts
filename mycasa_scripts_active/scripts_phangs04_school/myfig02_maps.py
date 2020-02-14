import os
import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "../../myproj_published/proj_phangs04_school/data_raw/"
galaxy = ["ngc0628"]
beams = ["060pc"]
scale = [47.4]
imcenter = [24.1738, 15.7825]
vmin = 0
vmax = 20
cbarlabel = "K km s$^{-1}$"

#####################
### Main Procedure
#####################
# mkdir
dir_working = dir_data + "../data/"
dir_product = dir_data + "../products/"
done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)

for i in range(len(galaxy)):
    galname = galaxy[i]
    for j in range(len(beams)):
        beam = beams[i]
        imagenames = glob.glob(dir_working + galname + "*12m*_" + beam + "*.image_Kelvin")
        imagenames.sort()

        # imval
        imagenames_12m7mtp = imagenames[1]
        x = str(imhead(imagenames_12m7mtp,"list")["shape"][0] - 1)
        y = str(imhead(imagenames_12m7mtp,"list")["shape"][1] - 1)
        box = "0,0," + x + "," + y
        
        data_12m7mtp = imval(imagenames_12m7mtp,box=box)["data"]
        flat_12m7mtp = data_12m7mtp.flatten()

        imagenames_12m7m = imagenames[0]
        data_12m7m = imval(imagenames_12m7m,box=box)["data"]
        flat_12m7m = data_12m7m.flatten()
    
        data_radec = imval(imagenames_12m7mtp,box=box)["coords"]
        flat_ra = data_radec[:,:,0].flatten() * 180/np.pi
        flat_dec = data_radec[:,:,1].flatten() * 180/np.pi

        # figure 1
        fig = plt.figure(figsize=(10,10))
        plt.rcParams["font.size"] = 22
        plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.85)

        # ax1
        ax1 = fig.add_subplot(111)

        plt.scatter((flat_ra - imcenter[0])*60,
                    (flat_dec - imcenter[1])*60,
                    c = flat_12m7mtp,
                    s = 15, lw = 0, marker = "s", cmap = "rainbow")
        plt.xlim([2.6,-2.6])
        plt.ylim([-2.6,2.6])
        plt.xlabel("x-offset (arcmin)")
        plt.ylabel("y-offset (arcmin)")

        plt.title("12m+7m+TP (NGC 0628)")
        plt.legend()
        plt.grid()
        cbar = plt.colorbar()
        plt.clim(vmin=vmin, vmax=vmax)
        cbar.set_label(cbarlabel)
        plt.savefig(dir_product+galname+"_12m7mtp.png",dpi=100)
        
        # figure 1 zoom
        fig = plt.figure(figsize=(10,10))
        plt.rcParams["font.size"] = 22
        plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.85)
        
        # ax1 zoom
        ax1 = fig.add_subplot(111)
        
        plt.scatter((flat_ra - imcenter[0])*60,
                    (flat_dec - imcenter[1])*60,
                    c = flat_12m7mtp,
                    s = 15, lw = 0, marker = "s", cmap = "rainbow")
        plt.xlim([0,-1])
        plt.ylim([0,1])
        plt.xlabel("x-offset (arcmin)")
        plt.ylabel("y-offset (arcmin)")

        plt.title("12m+7m+TP (NGC 0628)")
        plt.legend()
        plt.grid()
        cbar = plt.colorbar()
        plt.clim(vmin=vmin, vmax=vmax)
        cbar.set_label(cbarlabel)
        plt.savefig(dir_product+galname+"_12m7mtp_zoom.png",dpi=100)

        # figure 2
        fig = plt.figure(figsize=(10,10))
        plt.rcParams["font.size"] = 22
        plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.85)
        
        # ax1
        ax1 = fig.add_subplot(111)
        
        plt.scatter((flat_ra - imcenter[0])*60,
                    (flat_dec - imcenter[1])*60,
                    c = flat_12m7m,
                    s = 15, lw = 0, marker = "s", cmap = "rainbow")
        plt.xlim([2.6,-2.6])
        plt.ylim([-2.6,2.6])
        plt.xlabel("x-offset (arcmin)")
        plt.ylabel("y-offset (arcmin)")

        plt.title("12m+7m (NGC 0628)")
        plt.legend()
        plt.grid()
        cbar = plt.colorbar()
        plt.clim(vmin=vmin, vmax=vmax)
        cbar.set_label(cbarlabel)
        plt.savefig(dir_product+galname+"_12m7m.png",dpi=100)
        
        # figure 2 zoom
        fig = plt.figure(figsize=(10,10))
        plt.rcParams["font.size"] = 22
        plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.85)
        
        # ax1 zoom
        ax1 = fig.add_subplot(111)
        
        plt.scatter((flat_ra - imcenter[0])*60,
                    (flat_dec - imcenter[1])*60,
                    c = flat_12m7m,
                    s = 15, lw = 0, marker = "s", cmap = "rainbow")
        plt.xlim([0,-1])
        plt.ylim([0,1])
        plt.xlabel("x-offset (arcmin)")
        plt.ylabel("y-offset (arcmin)")

        plt.title("12m+7m (NGC 0628)")
        plt.legend()
        plt.grid()
        cbar = plt.colorbar()
        plt.clim(vmin=vmin, vmax=vmax)
        cbar.set_label(cbarlabel)
        plt.savefig(dir_product+galname+"_12m7m_zoom.png",dpi=100)

os.system("rm -rf *.last")
