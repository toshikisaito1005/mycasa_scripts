import glob
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
plt.ioff()


#####################
### Main Procedure
#####################
### ngc4321
scale = 103/1.4/1000. #kpc/arcsec
# data stats
dir_data = "../../phangs/co_ratio/ngc4321/"
output = "r21_aperture_vs_beam.txt"
txt_files = glob.glob(dir_data + "ngc4321*.txt")

os.system("rm -rf " + dir_data + output)
f = open(dir_data + output, "a")
f.write("#ap bm int peak\n")
for i in range(len(txt_files)):
    size_ap = str(int(txt_files[i].split("_")[-1].split(".")[0]))
    size_bm = str(int(txt_files[i].split("_")[-2].split("p")[0]))
    data = np.loadtxt(txt_files[i], usecols=(2,3,6,7))
    r_int = data[:,1]/data[:,0]/4.
    r_pea = data[:,3]/data[:,2]/4.
    for j in range(len(r_int)):
        if data[:,0][j] == 0:
            r_int[j] = 0
    for k in range(len(r_pea)):
        if data[:,2][k] == 0:
            r_pea[k] = 0
    
    f.write(size_ap + " " + size_bm + " " \
            + str(np.median(r_int[r_int>0])) + " " \
            + str(np.median(r_pea[r_pea>0])) + " \n")

f.close()

txt_data = glob.glob(dir_data + output)
data = np.loadtxt(txt_data[0], usecols=(0,1,2,3))

# heat map: Rinteg
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=750, linewidth=0,
            c=data[:,2], marker="s")

plt.xlim([1*scale,35*scale])
plt.ylim([1*scale,35*scale])
plt.clim([0.4,0.6])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Beam Size (kpc)")
plt.title("(j) Beam Size vs Aperture Size (NGC 4321)")
cbar=plt.colorbar()
cbar.set_label("Median $R_{21}$", size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04b_i_n4321.png",
            dpi=100)

# plot: Rint vs. aperture size
plt.figure(figsize=(10,8))
plt.xlim([1*scale,35*scale])
plt.ylim([0.40,0.75])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Median $R_{21}$")
plt.title("(k) Median $R_{21}$ vs Aperture Size (NGC 4321)")
plt.rcParams["font.size"] = 18
for i in range(15):
    loc = 2 * i + 4
    select_data = data[data[:,1]==loc]
    plt.plot(select_data[:,0]*scale, select_data[:,2],
             linewidth=3, marker="o", c=cm.rainbow(i/14.),
             alpha=1.0)

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=0, linewidth=0,
            c=data[:,1]*scale, marker=None)
plt.plot(2.3, 0.57, marker="*", markersize=40, color="k", alpha=0.4)
cbar=plt.colorbar()
plt.clim([1*scale,35*scale])
cbar.set_label("Beam Size (kpc)", size=18)

plt.legend(loc="upper left")
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04c_i_n4321.png",
            dpi=100)

# plot: Rint vs. beam size
plt.figure(figsize=(10,8))
plt.xlim([1*scale,35*scale])
plt.ylim([0.40,0.75])
plt.xlabel("Beam Size (kpc)")
plt.ylabel("Median $R_{21}$")
plt.title("(l) Median $R_{21}$ vs Beam Size (NGC 4321)")
plt.rcParams["font.size"] = 18
for i in range(15):
    loc = 2 * i + 4
    select_data = data[data[:,0]==loc]
    select_data2=select_data[np.argsort(select_data[:,1])[::-1]]
    plt.plot(select_data2[:,1]*scale, select_data2[:,2],
             linewidth=3, marker="o", c=cm.rainbow(i/14.),
             alpha=1.0)

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=0, linewidth=0,
            c=data[:,0]*scale, marker=None)
plt.plot(2.3, 0.57, marker="*", markersize=40, color="k", alpha=0.4)
cbar=plt.colorbar()
plt.clim([1*scale,35*scale])
cbar.set_label("Aperture Size (kpc)", size=18)

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04d_i_n4321.png",
            dpi=100)





### ngc3627
scale = 52/1.3/1000. #kpc/arcsec
# data stats
dir_data = "../../phangs/co_ratio/ngc3627/"
output = "r21_aperture_vs_beam.txt"
txt_files = glob.glob(dir_data + "ngc3627*.txt")

os.system("rm -rf " + dir_data + output)
f = open(dir_data + output, "a")
f.write("#ap bm int peak\n")
for i in range(len(txt_files)):
    size_ap = str(int(txt_files[i].split("_")[-1].split(".")[0]))
    size_bm = str(int(txt_files[i].split("_")[-2].split("p")[0]))
    data = np.loadtxt(txt_files[i], usecols=(2,3,6,7))
    r_int = data[:,1]/data[:,0]/4.
    r_pea = data[:,3]/data[:,2]/4.
    for j in range(len(r_int)):
        if data[:,0][j] == 0:
            r_int[j] = 0
    for k in range(len(r_pea)):
        if data[:,2][k] == 0:
            r_pea[k] = 0
    
    f.write(size_ap + " " + size_bm + " " \
            + str(np.median(r_int[r_int>0])) + " " \
            + str(np.median(r_pea[r_pea>0])) + " \n")

f.close()

txt_data = glob.glob(dir_data + output)
data = np.loadtxt(txt_data[0], usecols=(0,1,2,3))

# heat map: Rinteg
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=750, linewidth=0,
            c=data[:,2], marker="s")

plt.xlim([5*scale,39*scale])
plt.ylim([5*scale,39*scale])
#plt.clim([0.56,0.66])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Beam Size (kpc)")
plt.title("(d) Beam Size vs Aperture Size (NGC 3627)")
cbar=plt.colorbar()
cbar.set_label("Median $R_{21}$", size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04b_i_n3627.png",
            dpi=100)

# plot: Rint vs. aperture size
plt.figure(figsize=(10,8))
plt.xlim([5*scale,39*scale])
plt.ylim([0.40,0.80])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Median $R_{21}$")
plt.title("(e) Median $R_{21}$ vs Aperture Size (NGC 3627)")
plt.rcParams["font.size"] = 18
for i in range(15):
    loc = 2 * i + 4
    select_data = data[data[:,1]==loc]
    plt.plot(select_data[:,0]*scale, select_data[:,2],
             linewidth=3, marker="o", c=cm.rainbow(i/14.),
             alpha=1.0)

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=0, linewidth=0,
            c=data[:,1]*scale, marker=None)
plt.plot(1.5, 0.48, marker="*", markersize=40, color="k", alpha=0.4)
cbar=plt.colorbar()
plt.clim([1*scale,35*scale])
cbar.set_label("Beam Size (kpc)", size=18)

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04c_i_n3627.png",
            dpi=100)

# plot: Rint vs. beam size
plt.figure(figsize=(10,8))
plt.xlim([5*scale,39*scale])
plt.ylim([0.40,0.80])
plt.xlabel("Beam Size (kpc)")
plt.ylabel("Median $R_{21}$")
plt.title("(f) Median $R_{21}$ vs Beam Size (NGC 3627)")
plt.rcParams["font.size"] = 18
for i in range(15):
    loc = 2 * i + 4
    select_data = data[data[:,0]==loc]
    select_data2=select_data[np.argsort(select_data[:,1])[::-1]]
    plt.plot(select_data2[:,1]*scale, select_data2[:,2],
             linewidth=3, marker="o", c=cm.rainbow(i/14.),
             alpha=1.0)

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=0, linewidth=0,
            c=data[:,0]*scale, marker=None)
plt.plot(1.5, 0.48, marker="*", markersize=40, color="k", alpha=0.4)
cbar=plt.colorbar()
plt.clim([1*scale,35*scale])
cbar.set_label("Aperture Size (kpc)", size=18)

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04d_i_n3627.png",
            dpi=100)


### ngc0628
scale = 44/1000. #kpc/arcsec
# data stats
dir_data = "../../phangs/co_ratio/ngc0628_old/"
output = "r21_aperture_vs_beam.txt"
txt_files = glob.glob(dir_data + "ngc0628*.txt")

os.system("rm -rf " + dir_data + output)
f = open(dir_data + output, "a")
f.write("#ap bm int peak\n")
for i in range(len(txt_files)):
    size_ap = str(int(txt_files[i].split("_")[-1].split(".")[0]))
    size_bm = str(int(txt_files[i].split("_")[-2].split("p")[0]))
    data = np.loadtxt(txt_files[i], usecols=(2,3,6,7))
    r_int = data[:,1]/data[:,0]/4.
    r_pea = data[:,3]/data[:,2]/4.
    for j in range(len(r_int)):
        if data[:,0][j] == 0:
            r_int[j] = 0
    for k in range(len(r_pea)):
        if data[:,2][k] == 0:
            r_pea[k] = 0

    f.write(size_ap + " " + size_bm + " " \
            + str(np.median(r_int[r_int>0])) + " " \
            + str(np.median(r_pea[r_pea>0])) + " \n")

    #print("size_bms = "+size_bm+" arcsec, R21 = "+str(round(np.mean(r_int[r_int>0]),2))+" +/- "+str(round(np.std(r_int[r_int>0]),2)))

f.close()

txt_data = glob.glob(dir_data + output)
data = np.loadtxt(txt_data[0], usecols=(0,1,2,3))

# heat map: Rinteg
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=750, linewidth=0,
            c=data[:,2], marker="s")

plt.xlim([1*scale,35*scale])
plt.ylim([1*scale,35*scale])
plt.clim([0.56,0.66])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Beam Size (kpc)")
plt.title("(a) Beam Size vs Aperture Size (NGC 0628)")
cbar=plt.colorbar()
cbar.set_label("Median $R_{21}$", size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04b_i_n0628.png",
            dpi=100)

# plot: Rint vs. aperture size
plt.figure(figsize=(10,8))
plt.xlim([1*scale,35*scale])
plt.ylim([0.40,0.75])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Median $R_{21}$")
plt.title("(b) Median $R_{21}$ vs Aperture Size (NGC 0628)")
plt.rcParams["font.size"] = 18
for i in range(15):
    loc = 2 * i + 4
    select_data = data[data[:,1]==loc]
    plt.plot(select_data[:,0]*scale, select_data[:,2],
             linewidth=3, marker="o", c=cm.rainbow(i/14.),
             alpha=1.0)

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=0, linewidth=0,
            c=data[:,1]*scale, marker=None)
plt.plot(1.5, 0.61, marker="*", markersize=40, color="k", alpha=0.4)
cbar=plt.colorbar()
plt.clim([1*scale,35*scale])
cbar.set_label("Beam Size (kpc)", size=18)

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04c_i_n0628.png",
            dpi=100)

# plot: Rint vs. beam size
plt.figure(figsize=(10,8))
plt.xlim([1*scale,35*scale])
plt.ylim([0.40,0.75])
plt.xlabel("Beam Size (kpc)")
plt.ylabel("Median $R_{21}$")
plt.title("(c) Median $R_{21}$ vs Beam Size (NGC 0628)")
plt.rcParams["font.size"] = 18
for i in range(15):
    loc = 2 * i + 4
    select_data = data[data[:,0]==loc]
    select_data2=select_data[np.argsort(select_data[:,1])[::-1]]
    plt.plot(select_data2[:,1]*scale, select_data2[:,2],
             linewidth=3, marker="o", c=cm.rainbow(i/14.),
             alpha=1.0)

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=0, linewidth=0,
            c=data[:,0]*scale, marker=None)
plt.plot(1.5, 0.61, marker="*", markersize=40, color="k", alpha=0.4)
cbar=plt.colorbar()
plt.clim([1*scale,35*scale])
cbar.set_label("Aperture Size (kpc)", size=18)

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04d_i_n0628.png",
            dpi=100)



### ngc4254
scale = 130/1.6/1000. #kpc/arcsec
# data stats
dir_data = "../../phangs/co_ratio/ngc4254/"
output = "r21_aperture_vs_beam.txt"
txt_files = glob.glob(dir_data + "ngc4254*.txt")

os.system("rm -rf " + dir_data + output)
f = open(dir_data + output, "a")
f.write("#ap bm int peak\n")
for i in range(len(txt_files)):
    size_ap = str(int(txt_files[i].split("_")[-1].split(".")[0]))
    size_bm = str(int(txt_files[i].split("_")[-2].split("p")[0]))
    data = np.loadtxt(txt_files[i], usecols=(2,3,6,7))
    r_int = data[:,1]/data[:,0]/4.
    r_pea = data[:,3]/data[:,2]/4.
    for j in range(len(r_int)):
        if data[:,0][j] == 0:
            r_int[j] = 0
    for k in range(len(r_pea)):
        if data[:,2][k] == 0:
            r_pea[k] = 0

    f.write(size_ap + " " + size_bm + " " \
            + str(np.median(r_int[r_int>0])) + " " \
            + str(np.median(r_pea[r_pea>0])) + " \n")

f.close()

txt_data = glob.glob(dir_data + output)
data = np.loadtxt(txt_data[0], usecols=(0,1,2,3))

# heat map: Rinteg
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=750, linewidth=0,
            c=data[:,2], marker="s")

plt.xlim([5*scale,39*scale])
plt.ylim([5*scale,39*scale])
#plt.clim([0.61,0.70])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Beam Size (kpc)")
plt.title("(g) Beam Size vs Aperture Size (NGC 4254)")
cbar=plt.colorbar()
cbar.set_label("Median $R_{21}$", size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04b_i_n4254.png",
            dpi=100)

# plot: Rint vs. aperture size
plt.figure(figsize=(10,8))
plt.xlim([5*scale,39*scale])
plt.ylim([0.40,0.75])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Median $R_{21}$")
plt.title("(h) Median $R_{21}$ vs Aperture Size (NGC 4254)")
plt.rcParams["font.size"] = 18
for i in range(15):
    loc = 2 * i + 4
    select_data = data[data[:,1]==loc]
    plt.plot(select_data[:,0]*scale, select_data[:,2],
             linewidth=3, marker="o", c=cm.rainbow(i/14.),
             alpha=1.0)

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=0, linewidth=0,
            c=data[:,1]*scale, marker=None)
plt.plot(2.3, 0.74, marker="*", markersize=40, color="k", alpha=0.4)
cbar=plt.colorbar()
plt.clim([1*scale,35*scale])
cbar.set_label("Beam Size (kpc)", size=18)

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04c_i_n4254.png",
            dpi=100)

# plot: Rint vs. beam size
plt.figure(figsize=(10,8))
plt.xlim([5*scale,39*scale])
plt.ylim([0.40,0.75])
plt.xlabel("Beam Size (kpc)")
plt.ylabel("Median $R_{21}$")
plt.title("(i) Median $R_{21}$ vs Beam Size (NGC 4254)")
plt.rcParams["font.size"] = 18
for i in range(15):
    loc = 2 * i + 4
    select_data = data[data[:,0]==loc]
    select_data2=select_data[np.argsort(select_data[:,1])[::-1]]
    plt.plot(select_data2[:,1]*scale, select_data2[:,2],
             linewidth=3, marker="o", c=cm.rainbow(i/14.),
             alpha=1.0)

plt.scatter(data[:,0]*scale,data[:,1]*scale,s=0, linewidth=0,
            c=data[:,0]*scale, marker=None)
plt.plot(2.3, 0.74, marker="*", markersize=40, color="k", alpha=0.4)
cbar=plt.colorbar()
plt.clim([1*scale,35*scale])
cbar.set_label("Aperture Size (kpc)", size=18)

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig04d_i_n4254.png",
            dpi=100)
