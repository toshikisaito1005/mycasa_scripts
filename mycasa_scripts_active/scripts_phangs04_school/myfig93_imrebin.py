import os
import glob
import numpy as np

dir_data = "../../myproj_published/proj_phangs04_school/data_raw/"
galaxy = ["ngc0628"]
beams = ["500pc"]
scale = [47.4]
imcenter = [24.1738, 15.7825]

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
    for j in range(len(highest_beam)):
        beam = beams[j]
        imagenames = glob.glob(dir_working + galname + "*12m*_" + beam + "*.image")
        imagenames.sort()
        
        # imrebin
        for k in range(len(imagenames)):
            cell = np.abs(imhead(imagenames[k],mode="list")["cdelt1"])*180.*3600./np.pi
            beamsize = imhead(imagenames[k],"list")["beammajor"]["value"]
            nbin = int(float(beamsize) / 4.53 / cell)

            outfile = imagenames[k].replace(".image",".rebin")
            os.system("rm -rf " + outfile)
            imrebin(imagename = imagenames[k],
                    outfile = outfile,
                    factor = [nbin, nbin])

        # imval
        imagenames_12m7mtp = imagenames[1].replace(".image",".rebin")
        x0 = "0"
        x1 = str(imhead(imagenames_12m7mtp,"list")["shape"][0] - 1)
        y0 = "0"
        y1 = str(imhead(imagenames_12m7mtp,"list")["shape"][1] - 1)
        box = x0 + "," + y0 + "," + x1 + "," + y1
        
        data_12m7mtp = imval(imagenames_12m7mtp,box=box)["data"]
        flat_12m7mtp = data_12m7mtp.flatten()

        imagenames_12m7m = imagenames[0].replace(".image",".rebin")
        data_12m7m = imval(imagenames_12m7m,box=box)["data"]
        flat_12m7m = data_12m7m.flatten()
    
        data_radec = imval(imagenames_12m7mtp,box=box)["coords"]
        flat_ra = data_radec[:,:,0].flatten() * 180/np.pi
        flat_dec = data_radec[:,:,1].flatten() * 180/np.pi

        # figure
        fig = plt.figure(figsize=(10,10))
        plt.rcParams["font.size"] = 18
        plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.85)

        # ax1
        ax1 = fig.add_subplot(111)

        plt.scatter((flat_ra - imcenter[0])*60,
                    (flat_dec - imcenter[1])*60,
                    c = flat_12m7mtp - flat_12m7m, # (flat_12m7mtp - flat_12m7m)/flat_12m7mtp*100
                    s = 15, lw = 0, marker = "s", cmap = "rainbow")
        plt.xlim([2.6,-2.6])
        plt.ylim([-2.6,2.6])
        plt.xlabel("x-offset (arcmin)")
        plt.ylabel("y-offset (arcmin)")

        plt.title("12m+7m+TP - 12m+7m")
        plt.legend()
        cbar = plt.colorbar()
        plt.clim(vmin=0, vmax=12)
        cbar.set_label("Jy km s$^{-1}$")
        plt.savefig(dir_product+galname+"_map.png",dpi=100)

os.system("rm -rf *.last")
