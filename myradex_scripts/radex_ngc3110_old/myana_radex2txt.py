import os
import sys
import re
import glob
import numpy as np
import scipy
from pylab import *
import matplotlib.pyplot as plt

#####################
### Main Procedure
#####################
logNH2 = ["22.0", "22.5", "23.0"]

#350.493963711 261.87353297 24.4641248473 19.5843692835

for i in range(len(logNH2)):
    dir_eps = "../../myradex_scripts/radex_ngc3110/"
    data = np.loadtxt("../../myradex_scripts/radex_ngc3110/out_" + logNH2[i] + ".txt",
                      usecols = (0, 1, 2, 3))
    #
    x, y, z1, z2 = data[:,0], data[:,1], data[:,2], data[:,3]
    X = x.reshape(40, 40)
    Y = y.reshape(40, 40)
    Z1 = z1.reshape(40, 40) # CO(2-1)/CO(1-0) = 261.87/350.49
    Z2 = z2.reshape(40, 40) # CO(2-1)/13CO(2-1) = 261.87/19.58
    #
    fig = plt.figure()
    plt.rcParams["font.size"] = 14
    plt.subplots_adjust(bottom = 0.15)
    plt.gca().set_aspect('equal', adjustable='box')
    ax = plt.axes()
    plt.xscale('log')
    plt.title("RADEX Grid @ log($N_{H_2}$/cm$^{-2}$) = " + logNH2[i])
    plt.ylabel("$T_{kin}$ (K)")
    plt.xlabel("$n_{H_2}$ (cm$^{-3}$)")
    plt.ylim([0,160]) #plt.xlim([-10,280])
    # chi_square
    chi_1 = (0.747 - Z1) ** 2. / 0.1 ** 2.
    chi_2 = (13.37 - Z2) ** 2. / 1.0 ** 2.
    chi_low = chi_1 + chi_2
    cont = plt.contourf(Y, X, chi_low, levels=[.0,3.84], colors="pink", linewidths = 1.)
    #plt.pcolormesh(Y, X, chi, cmap = "PuBu")
    plt.plot(Y[np.where(chi_low==chi_low.min())[0],np.where(chi_low==chi_low.min())[1]], X[np.where(chi_low==chi_low.min())[0],np.where(chi_low==chi_low.min())[1]], "D",
             markersize=8, color="red")
    #plt.colorbar()
    #plt.clim(0.,100.)
    ### CO(2-1)/CO(1-0)
    cont = plt.contour(Y, X, Z1, levels=[0.747], colors="blue",
                       label = "CO(2-1)/CO(1-0)")
    cont.clabel(fmt='%1.2f', fontsize=16)
    cont = plt.contour(Y, X, Z1, levels=[0.747-0.1,0.747+0.1],
                       colors="blue",
                       linewidths = 0.5, linestyles = "dashed")
    ### CO(2-1)/13CO(2-1)
    cont = plt.contour(Y, X, Z2, levels=[13.37], colors="green",
                       label = "CO(2-1)/$^{13}$CO(2-1)")
    cont.clabel(fmt='%1.2f', fontsize=16)
    cont = plt.contour(Y, X, Z2, levels=[13.37-1.0,13.37+1.0],
                       colors="green",
                       linewidths = 0.5, linestyles = "dashed")
    #plt.legend(loc='upper left')
    plt.savefig(dir_eps + "plot_radex_" + logNH2[i] + ".eps", dpi=30)

