import glob
sys.path.append(os.getcwd())
import scripts_phangs_r21_plot as r21_plot

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from numpy import linspace, meshgrid
from matplotlib.mlab import griddata
import matplotlib.cm as cm

def coord_rot(x, y, angle):
    tilt_cos = math.cos(math.radians(angle))
    tilt_sin = math.sin(math.radians(angle))
    x_new = (x * tilt_cos - y * tilt_sin)
    y_new = (x * tilt_sin + y * tilt_cos)

    return x_new, y_new

### setup
dir_data = "../../phangs/co_ratio/ngc4321_co/"
xlog=True
ylog=True


### figure 2
txtfiles = [dir_data + "ngc4321_flux_4p0_4p0_no.txt",
            dir_data + "ngc4321_flux_4p0_6p0_no.txt",
            dir_data + "ngc4321_flux_4p0_8p0_no.txt",
            dir_data + "ngc4321_flux_4p0_10p0_no.txt",
            dir_data + "ngc4321_flux_4p0_12p0_no.txt",
            dir_data + "ngc4321_flux_4p0_14p0_no.txt",
            dir_data + "ngc4321_flux_4p0_16p0_no.txt",
            dir_data + "ngc4321_flux_4p0_18p0_no.txt",
            dir_data + "ngc4321_flux_4p0_20p0_no.txt"]

i = 0
data = np.loadtxt(txtfiles[i])
data_z = data[:,3]
#data_z = (data[:,3]/data[:,2]/4.)
clim = [-3,10]
#clim = [0,0.8]
label = "CO(2-1) Flux Density"

ra_cnt = 185.729
dec_cnt = 15.8223
pa = 180-157.8
inc = 35.1


### figure 1
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18
ax = plt.axes()

rot_cos = math.cos(math.radians(pa))
rot_sin = math.sin(math.radians(pa))

x_tmp = data[:,0] - ra_cnt
y_tmp = data[:,1] - dec_cnt

x_tmp2 = (x_tmp * rot_cos - y_tmp * rot_sin)
y_tmp2 = (x_tmp * rot_sin + y_tmp * rot_cos) * 1/math.sin(math.radians(inc))

x, y = coord_rot(x_tmp2, y_tmp2, -pa)

plt.scatter(x_tmp,
            y_tmp,
            s=50 * (1 + i),
            linewidth=0,
            c=data_z,
            marker="o",
            cmap="PuBu")

plt.xlim([0.039,-0.039])
plt.ylim([-0.039,0.039])
plt.clim(clim)
cbar=plt.colorbar()
cbar.set_label(label, size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/test.png",dpi=100)

### figure 2
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18
ax = plt.axes()

for j in range(12):
    c = pat.Circle(xy=(0, 0), radius=0.003*(j+1), fc='g', ec='black', fill=False)
    ax.add_patch(c)

for k in range(4):
    c = pat.Circle(xy=(0, 0), radius=0.009*(k+1), fc='g', ec='black',
                   fill=False, linewidth = 3)
    ax.add_patch(c)

plt.scatter(x,
            y,
            s=110 * (1 + i),
            linewidth=0,
            c=data_z,#/data[:,2]/4.,
            marker="o",
            cmap="PuBu")#Paired")

plt.xlim([0.039,-0.039])
plt.ylim([-0.039,0.039])
plt.clim(clim)
cbar=plt.colorbar()
cbar.set_label(label, size=18)

# spirals
a=0.003
b=0.4
th=np.linspace(0, 500, 10000)
x=a*np.exp(b*th)*np.cos(th)
y=a*np.exp(b*th)*np.sin(th)
plt.plot(x, y, c=cm.gnuplot(4/4.), linewidth=5)

a=0.003
b=0.45
th=np.linspace(0, 500, 10000)
x=a*np.exp(b*th)*np.cos(th)
y=a*np.exp(b*th)*np.sin(th)
plt.plot(x, y, c=cm.gnuplot(3/4.), linewidth=5)

a=0.003
b=0.5
th=np.linspace(0, 500, 10000)
x=a*np.exp(b*th)*np.cos(th)
y=a*np.exp(b*th)*np.sin(th)
plt.plot(x, y, c=cm.gnuplot(2/4.), linewidth=5)

a=0.003
b=0.55
th=np.linspace(0, 500, 10000)
x=a*np.exp(b*th)*np.cos(th)
y=a*np.exp(b*th)*np.sin(th)
plt.plot(x, y, c=cm.gnuplot(1/4.), linewidth=5)

a=0.003
b=0.60
th=np.linspace(0, 500, 10000)
x=a*np.exp(b*th)*np.cos(th)
y=a*np.exp(b*th)*np.sin(th)
plt.plot(x, y, c=cm.gnuplot(0/4.), linewidth=5)


"""
a=0.006
b=0.4
th=np.linspace(0, 500, 10000)
y=-a*np.exp(b*th)*np.cos(th)
x=a*np.exp(b*th)*np.sin(th)
plt.plot(x, y, "green", linewidth=5)
"""

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/test2.png",dpi=100)


### figure 3
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18
ax = plt.axes()

r = np.sqrt(x**2 + y**2)
theta = np.degrees(np.arccos(x/r))

#rot_tilt = [0,0,-15,-65,-75,-90,-100,-110,-125,-200,-210,-210,-210] # both
rot_tilt = [0,0,-20,-65,-75,-100,-120,-125,-140,-175,-190,-190,170] # south-arm

product_file="/Users/saito/data/phangs/co_ratio/ngc4321_co/ngc4321_despiral1.txt"
os.system("rm -rf "+product_file)
data2txt=np.empty([1,3])

for j in range(12):
    c = pat.Circle(xy=(0, 0), radius=0.003*(j+1), fc='g', ec='black', fill=False)
    ax.add_patch(c)
    
    x2 = x[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    y2 = y[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    r2 = r[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    data2 = data_z[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    
    x3_tmp, y3_tmp = coord_rot(x2, y2, rot_tilt[j])
    
    x3, y3 = x3_tmp[y3_tmp>0], y3_tmp[y3_tmp>0]
    #x3, y3 = coord_rot(x3_tmp[y3_tmp>0], y3_tmp[y3_tmp>0], -1*rot_tilt[j])
    
    data3 = data2[y3_tmp>0]
    
    data2txt = np.r_[data2txt,np.c_[x3,y3,data3]]
    
    plt.scatter(x3,
                y3,
                s=110 * (1 + i),
                linewidth=0,
                c=data3,
                marker="o",
                cmap="PuBu")
    plt.clim(clim)

    # plot boundaries
    x_s_tmp = 0
    x_e_tmp = 0
    y_s_tmp = 0.003*(j)
    y_e_tmp = 0.003*(j+1)
 
    # boundary zero
    x0_s, y0_s = coord_rot(x_s_tmp, y_s_tmp, +0-rot_tilt[j])
    x0_e, y0_e = coord_rot(x_e_tmp, y_e_tmp, +0-rot_tilt[j+1])
    plt.plot([x0_s, x0_e],[y0_s, y0_e], color=cm.gnuplot(3/6.), lw=j, alpha=0.8)

    # boundary one
    xr_s, yr_s = coord_rot(x_s_tmp, y_s_tmp, +20-rot_tilt[j])
    xr_e, yr_e = coord_rot(x_e_tmp, y_e_tmp, +20-rot_tilt[j+1])
    plt.plot([xr_s, xr_e],[yr_s, yr_e], color=cm.gnuplot(4/6.), lw=j, alpha=0.8)

    xl_s, yl_s = coord_rot(x_s_tmp, y_s_tmp, -20-rot_tilt[j])
    xl_e, yl_e = coord_rot(x_e_tmp, y_e_tmp, -20-rot_tilt[j+1])
    plt.plot([xl_s, xl_e],[yl_s, yl_e], color=cm.gnuplot(2/6.), lw=j, alpha=0.8)

    # boundary two
    xr_s, yr_s = coord_rot(x_s_tmp, y_s_tmp, +40-rot_tilt[j])
    xr_e, yr_e = coord_rot(x_e_tmp, y_e_tmp, +40-rot_tilt[j+1])
    plt.plot([xr_s, xr_e],[yr_s, yr_e], color=cm.gnuplot(5/6.), lw=j, alpha=0.8)
    
    xl_s, yl_s = coord_rot(x_s_tmp, y_s_tmp, -40-rot_tilt[j])
    xl_e, yl_e = coord_rot(x_e_tmp, y_e_tmp, -40-rot_tilt[j+1])
    plt.plot([xl_s, xl_e],[yl_s, yl_e], color=cm.gnuplot(1/6.), lw=j, alpha=0.8)

    # boundary two
    xr_s, yr_s = coord_rot(x_s_tmp, y_s_tmp, +60-rot_tilt[j])
    xr_e, yr_e = coord_rot(x_e_tmp, y_e_tmp, +60-rot_tilt[j+1])
    plt.plot([xr_s, xr_e],[yr_s, yr_e], color=cm.gnuplot(6/6.), lw=j, alpha=0.8)

    xl_s, yl_s = coord_rot(x_s_tmp, y_s_tmp, -60-rot_tilt[j])
    xl_e, yl_e = coord_rot(x_e_tmp, y_e_tmp, -60-rot_tilt[j+1])
    plt.plot([xl_s, xl_e],[yl_s, yl_e], color=cm.gnuplot(0/6.), lw=j, alpha=0.8)

np.savetxt(product_file, data2txt)

for k in range(4):
    c = pat.Circle(xy=(0, 0), radius=0.009*(k+1), fc='g', ec='black',
                   fill=False, linewidth = 3)
    ax.add_patch(c)


plt.xlim([0.039,-0.039])
plt.ylim([-0.039,0.039])
cbar=plt.colorbar()
cbar.set_label(label, size=18)

plt.savefig("/Users/saito/data/phangs/co_ratio/eps/test3_south.png",dpi=100)

# figure 3 phase
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18
dat = np.loadtxt(product_file)
x_dat=dat[:,0]
y_dat=dat[:,1]
val_dat=dat[:,2]
r_dat=np.sqrt(x_dat**2 + y_dat**2)
th_dat=np.degrees(np.arccos(x_dat/r_dat))
x_bo1=x_dat[np.where((r_dat>=0.009)&(r_dat<0.036))]
y_bo1=y_dat[np.where((r_dat>=0.009)&(r_dat<0.036))]
r_bo12=r_dat[np.where((r_dat>=0.009)&(r_dat<0.036))]
val_bo1=val_dat[np.where((r_dat>=0.009)&(r_dat<0.036))]
th_bo1=(th_dat[np.where((r_dat>=0.009)&(r_dat<0.036))]-90)

r_bo1 = r_bo12[np.where((val_bo1>0)&(th_bo1>-60)&(th_bo1<60))]
x_bo1 = th_bo1[np.where((val_bo1>0)&(th_bo1>-60)&(th_bo1<60))]
y_bo1 = val_bo1[np.where((val_bo1>0)&(th_bo1>-60)&(th_bo1<60))]
plt.scatter(x_bo1,y_bo1,s=110*(1+i),linewidth=0,
            c=y_bo1,marker="o",cmap="PuBu")#hsv")

#
nbins = 12
n, _ = np.histogram(x_bo1[y_bo1<1e7][np.where(r_bo1<0.018)],
                    bins=nbins)
sy, _ = np.histogram(x_bo1[y_bo1<1e7][np.where(r_bo1<0.018)],
                     bins=nbins,
                     weights=y_bo1[y_bo1<1e7][np.where(r_bo1<0.018)])
sy2, _ = np.histogram(x_bo1[y_bo1<1e7][np.where(r_bo1<0.018)],
                      bins=nbins,
                      weights=y_bo1[y_bo1<1e7][np.where(r_bo1<0.018)]*y_bo1[y_bo1<1e7][np.where(r_bo1<0.018)])
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)
plt.plot((_[1:] + _[:-1])/2, mean, "--", c="red", linewidth=8, label="near")
#
n, _ = np.histogram(x_bo1[y_bo1<1e7][np.where((r_bo1>=0.018)&(r_bo1<0.027))],
                    bins=nbins)
sy, _ = np.histogram(x_bo1[y_bo1<1e7][np.where((r_bo1>=0.018)&(r_bo1<0.027))],
                     bins=nbins,
                     weights=y_bo1[y_bo1<1e7][np.where((r_bo1>=0.018)&(r_bo1<0.027))])
sy2, _ = np.histogram(x_bo1[y_bo1<1e7][np.where((r_bo1>=0.018)&(r_bo1<0.027))],
                      bins=nbins,
                      weights=y_bo1[y_bo1<1e7][np.where((r_bo1>=0.018)&(r_bo1<0.027))]*y_bo1[y_bo1<1e7][np.where((r_bo1>=0.018)&(r_bo1<0.027))])
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)
plt.plot((_[1:] + _[:-1])/2, mean, "--", c="green", linewidth=8, label="mid")
#
n, _ = np.histogram(x_bo1[y_bo1<1e7][np.where(r_bo1[y_bo1<1e7]>=0.018)],
                    bins=nbins)
sy, _ = np.histogram(x_bo1[y_bo1<1e7][np.where(r_bo1[y_bo1<1e7]>=0.027)],
                     bins=nbins,
                     weights=y_bo1[y_bo1<1e7][np.where(r_bo1[y_bo1<1e7]>=0.027)])
sy2, _ = np.histogram(x_bo1[y_bo1<1e7][np.where(r_bo1[y_bo1<1e7]>=0.027)],
                      bins=nbins,
                      weights=y_bo1[y_bo1<1e7][np.where(r_bo1[y_bo1<1e7]>=0.027)]*y_bo1[y_bo1<1e7][np.where(r_bo1[y_bo1<1e7]>=0.027)])
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)
plt.plot((_[1:] + _[:-1])/2, mean, "--", c="blue", linewidth=8, label="far")

plt.yscale("log")
label = "$R_{21}$"
ylim = [5e-2,5e+1]
#ylim = [0.1,1.5]
plt.xlim([-70,70])
plt.ylim(ylim)
plt.clim(clim)

plt.plot([-60,-60], ylim, color=cm.gnuplot(0/6.), lw=5, alpha=0.8)
plt.plot([-40,-40], ylim, color=cm.gnuplot(1/6.), lw=5, alpha=0.8)
plt.plot([-20,-20], ylim, color=cm.gnuplot(2/6.), lw=5, alpha=0.8)
plt.plot([0,0], ylim, color=cm.gnuplot(3/6.), lw=5, alpha=0.8)
plt.plot([20,20], ylim, color=cm.gnuplot(4/6.), lw=5, alpha=0.8)
plt.plot([40,40], ylim, color=cm.gnuplot(5/6.), lw=5, alpha=0.8)
plt.plot([60,60], ylim, color=cm.gnuplot(6/6.), lw=5, alpha=0.8)

cbar=plt.colorbar()
cbar.set_label(label, size=18)
plt.legend()
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/test6.png",dpi=100)



### figure 4
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18
ax = plt.axes()

r = np.sqrt(x**2 + y**2)

#rot_tilt = [0,0,-15,-65,-75,-90,-100,-110,-125,-200,-210,-210,195] # both
rot_tilt = [0,0,-15,-65,-75,-75,-70,-95,-110,-225,-225,-225,-205] # north-arm

product_file="/Users/saito/data/phangs/co_ratio/ngc4321_co/ngc4321_despiral2.txt"
os.system("rm -rf "+product_file)
data2txt=np.empty([1,3])

for j in range(12):
    c = pat.Circle(xy=(0, 0), radius=0.003*(j+1), fc='g', ec='black', fill=False)
    ax.add_patch(c)
    
    x2 = x[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    y2 = y[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    data2 = data_z[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    
    x3_tmp, y3_tmp = coord_rot(x2, y2, rot_tilt[j])

    x3, y3 = x3_tmp[y3_tmp<0], y3_tmp[y3_tmp<0]
    #x3, y3 = coord_rot(x3_tmp[y3_tmp<0], y3_tmp[y3_tmp<0], -1*rot_tilt[j])

    data3 = data2[y3_tmp<0]
    
    data2txt = np.r_[data2txt,np.c_[x3,y3,data3]]
    
    plt.scatter(x3,
                y3,
                s=110 * (1 + i),
                linewidth=0,
                c=data3,
                marker="o",
                cmap="PuBu")
    plt.clim(clim)

    # plot boundaries
    x_s_tmp = 0
    x_e_tmp = 0
    y_s_tmp = -0.003*(j)
    y_e_tmp = -0.003*(j+1)
    
    # boundary zero
    x0_s, y0_s = coord_rot(x_s_tmp, y_s_tmp, +0)#-rot_tilt[j])
    x0_e, y0_e = coord_rot(x_e_tmp, y_e_tmp, +0)#-rot_tilt[j+1])
    plt.plot([x0_s, x0_e],[y0_s, y0_e], color=cm.gnuplot(0/3.), lw=j, alpha=0.8)
    
    # boundary one
    xr_s, yr_s = coord_rot(x_s_tmp, y_s_tmp, +20)#-rot_tilt[j])
    xr_e, yr_e = coord_rot(x_e_tmp, y_e_tmp, +20)#-rot_tilt[j+1])
    plt.plot([xr_s, xr_e],[yr_s, yr_e], color=cm.gnuplot(1/3.), lw=j, alpha=0.8)
    
    xl_s, yl_s = coord_rot(x_s_tmp, y_s_tmp, -20)#-rot_tilt[j])
    xl_e, yl_e = coord_rot(x_e_tmp, y_e_tmp, -20)#-rot_tilt[j+1])
    plt.plot([xl_s, xl_e],[yl_s, yl_e], color=cm.gnuplot(1/3.), lw=j, alpha=0.8)
    
    # boundary two
    xr_s, yr_s = coord_rot(x_s_tmp, y_s_tmp, +40)#-rot_tilt[j])
    xr_e, yr_e = coord_rot(x_e_tmp, y_e_tmp, +40)#-rot_tilt[j+1])
    plt.plot([xr_s, xr_e],[yr_s, yr_e], color=cm.gnuplot(2/3.), lw=j, alpha=0.8)
    
    xl_s, yl_s = coord_rot(x_s_tmp, y_s_tmp, -40)#-rot_tilt[j])
    xl_e, yl_e = coord_rot(x_e_tmp, y_e_tmp, -40)#-rot_tilt[j+1])
    plt.plot([xl_s, xl_e],[yl_s, yl_e], color=cm.gnuplot(2/3.), lw=j, alpha=0.8)
    
    # boundary two
    xr_s, yr_s = coord_rot(x_s_tmp, y_s_tmp, +60)#-rot_tilt[j])
    xr_e, yr_e = coord_rot(x_e_tmp, y_e_tmp, +60)#-rot_tilt[j+1])
    plt.plot([xr_s, xr_e],[yr_s, yr_e], color=cm.gnuplot(3/3.), lw=j, alpha=0.8)
    
    xl_s, yl_s = coord_rot(x_s_tmp, y_s_tmp, -60)#-rot_tilt[j])
    xl_e, yl_e = coord_rot(x_e_tmp, y_e_tmp, -60)#-rot_tilt[j+1])
    plt.plot([xl_s, xl_e],[yl_s, yl_e], color=cm.gnuplot(3/3.), lw=j, alpha=0.8)

np.savetxt(product_file, data2txt)

for k in range(4):
    c = pat.Circle(xy=(0, 0), radius=0.009*(k+1), fc='g', ec='black',
                   fill=False, linewidth = 3)
    ax.add_patch(c)

plt.xlim([0.039,-0.039])
plt.ylim([-0.039,0.039])
cbar=plt.colorbar()
cbar.set_label(label, size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/test4_south.png",dpi=100)


### figure 5
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18
ax = plt.axes()

r = np.sqrt(x**2 + y**2)

rot_tilt = [0,0,-15,-65,-75,-90,-100,-110,-125,-200,-210,-210] # both

for j in range(12):
    c = pat.Circle(xy=(0, 0), radius=0.003*(j+1), fc='g', ec='black', fill=False)
    ax.add_patch(c)
    
    x2 = x[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    y2 = y[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    data2 = data_z[np.where((r>=0.003*(j)) & (r<0.003*(j+1)))]
    
    tilt_cos = math.cos(math.radians(rot_tilt[j]))
    tilt_sin = math.sin(math.radians(rot_tilt[j]))

    x3 = (x2 * tilt_cos - y2 * tilt_sin)
    y3 = (x2 * tilt_sin + y2 * tilt_cos)
    
    plt.scatter(x3,
                y3,
                s=110 * (1 + i),
                linewidth=0,
                c=data2,
                marker="o",
                cmap="PuBu")
    plt.clim(clim)


for k in range(4):
    c = pat.Circle(xy=(0, 0), radius=0.009*(k+1), fc='g', ec='black',
                   fill=False, linewidth = 3)
    ax.add_patch(c)

plt.xlim([0.039,-0.039])
plt.ylim([-0.039,0.039])
cbar=plt.colorbar()
cbar.set_label(label, size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/test5_all.png",dpi=100)
