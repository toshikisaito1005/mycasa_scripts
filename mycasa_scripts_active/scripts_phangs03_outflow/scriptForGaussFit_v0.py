import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.ioff()

# import CASA
from taskinit import *
from imval import imval


#####################
### define functions
#####################
def inspec(data):
    """
    import spectrum and estimate rough rms noise
    from a txt file
    """
    # specify datacubes
    txt_spec = glob.glob(data)

    np_spec = np.loadtxt(data)

    # rough noise estimate
    noise = np_spec[0:10][:,1].tolist()
    noise.extend(np_spec[-10:][:,1].tolist())
    rms = np.sqrt(np.mean(np.array(noise)**2))

    return np_spec, rms


def func1(x, a, b, c):
    return a*np.exp(-(x-b)**2/(2*c**2))


def func2(x, a, b, c, d, e, f):
    exp1 = a*np.exp(-(x-b)**2/(2*c**2))
    exp2 = d*np.exp(-(x-e)**2/(2*f**2))
    return exp1 + exp2

def func3(x, a, b, c, d, e, f, g, h, i):
    exp1 = a*np.exp(-(x-b)**2/(2*c**2))
    exp2 = d*np.exp(-(x-e)**2/(2*f**2))
    exp3 = g*np.exp(-(x-h)**2/(2*i**2))
    return exp1 + exp2 + exp3

def do_guess(np_spec):
    """
    guessing inital parameter for fit
    """
    value_hm = np_spec[:,1].max()
    data_x = np_spec[:,0]
    data_y = np_spec[:,1] / value_hm
    guess_fwhm_ch = len(filter(lambda x: x > 0.3, data_y))
    guess_fhwm = guess_fwhm_ch * 2.5 # km/s
    guess_peak = data_y.max()
    guess_pos = np_spec[:,0][np.where(data_y == 1.0)[0][0]]
    guess = [guess_peak, guess_pos, guess_fhwm]

    return guess


def fit_func1(func1, data_x, data_y, guess):
    """
    fit data with func1
    """
    popt, pcov = curve_fit(func1,
                           data_x, data_y,
                           p0=guess)
    best_func = func1(data_x,
                      popt[0], popt[1], popt[2])
    residual = data_y - best_func

    return popt, residual


def fit_func2(func2, data_x, data_y, guess):
    """
    fit data with func2
    """
    popt, pcov = curve_fit(func2,
                           data_x, data_y,
                           p0=guess)
    best_func = func2(data_x,
                      popt[0], popt[1], popt[2],
                      popt[3], popt[4], popt[5])
    residual = data_y - best_func

    return popt, residual


def fit_func3(func3, data_x, data_y, guess):
    """
    fit data with func3
    """
    popt, pcov = curve_fit(func3,
                           data_x, data_y,
                           p0=guess)
    best_func = func3(data_x,
                      popt[0], popt[1], popt[2],
                      popt[3], popt[4], popt[5],
                      popt[6], popt[7], popt[8])
    residual = data_y - best_func

    return popt, residual


def plot_func1(data_x, popt, color, lw = 1, linestyle = "solid"):
    """
    """
    plt.plot(data_x,
             func1(data_x,
                   popt[0], popt[1], popt[2]),
             color = color,
             lw = lw,
             linestyle = linestyle)


def plot_func2(data_x, popt, color, lw = 1, linestyle = "solid"):
    """
    """
    plt.plot(data_x,
             func2(data_x,
                   popt[0], popt[1], popt[2],
                   popt[3], popt[4], popt[5]),
             color = color,
             lw = lw,
             linestyle = linestyle)


def plot_func3(data_x, popt, color, lw = 1, linestyle = "solid"):
    """
    """
    plt.plot(data_x,
             func3(data_x,
                   popt[0], popt[1], popt[2],
                   popt[3], popt[4], popt[5],
                   popt[6], popt[7], popt[8]),
             color = color,
             lw = lw,
             linestyle = linestyle)



def plot_baseline(data_x):
    """
    """
    plt.plot([min(data_x),max(data_x)],
             [0,0],
             color = "grey",
             lw = 1,
             linestyle = "dashed")


def plot_setup(data_x,
               savefig,
               ylim = [-0.1, 1.1],
               xlabel = "Velocity (km s$^{-1}$)",
               ylabel = "Normalized Flux"):
    """
    """
    plt.xlim([min(data_x),max(data_x)])
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(savefig)


#####################
### Main Procedure
#####################
data = glob.glob("products/ngc5643_*arcsec_spec.txt")[0]
np_spec, rms = inspec(data)
data_x = np_spec[:,0]
data_y = np_spec[:,1] / np_spec[:,1].max()


if np_spec[:,1].max() > rms * 5:
    ### single Gauss fit
    # guess and fit
    guess = do_guess(np_spec)
    popt, residual = fit_func1(func1, data_x, data_y, guess)

    # plot
    plt.figure()
    plt.plot(data_x, data_y, color = "grey")
    plot_func1(data_x, popt, "red")
    plt.plot(data_x, residual, color = "blue")
    plot_baseline(data_x)
    plot_setup(data_x, "ngc5643_fit.png")


    ### two Gauss fit if needed
    if residual.max() > rms / np_spec[:,1].max() * 5:
        # guess and fit
        np_residual \
          = np.stack([data_x,
                      residual * np_spec[:,1].max()], 1)
        guess = do_guess(np_residual)
        guess2 = popt.tolist()
        guess2.extend(guess)
        guess2[3] = guess2[3]*np_residual[:,1].max() \
                    / np_spec[:,1].max()
        popt2, residual2 = \
            fit_func2(func2, data_x, data_y, guess2)

        # plot
        plt.figure()
        plt.plot(data_x, data_y, color = "grey")
        popt2a = popt2[0:3]
        popt2b = popt2[-3:]
        plot_func1(data_x, popt2a, "red", linestyle = "dashed")
        plot_func1(data_x, popt2b, "red", linestyle = "dashed")
        plot_func2(data_x, popt2, "red", lw = 2)
        plt.plot(data_x, residual2, color = "blue")
        plot_baseline(data_x)
        plot_setup(data_x, "ngc5643_fit2.png")


        ### three Gauss fit if needed
        if residual2.max() > rms / np_spec[:,1].max() * 3:
            # guess and fit
            np_residual \
              = np.stack([data_x,
                          residual2 * np_spec[:,1].max()], 1)
            guess = do_guess(np_residual)
            guess3 = popt2.tolist()
            guess3.extend(guess)
            guess3[6] = guess3[6]*np_residual[:,1].max() \
                        / np_spec[:,1].max()
            #guess3[8] = 500
            popt3, residual3 = \
                fit_func3(func3, data_x, data_y, guess3)

            # plot
            plt.figure()
            plt.plot(data_x, data_y, color = "grey")
            popt3a = popt3[0:3]
            popt3b = popt3[-6:-3]
            popt3c = popt3[-3:]
            plot_func1(data_x, popt3a, "red",
                       linestyle = "dashed")
            plot_func1(data_x, popt3b, "red",
                       linestyle = "dashed")
            plot_func1(data_x, popt3c, "red",
                       linestyle = "dashed")
            plot_func3(data_x, popt3, "red", lw = 2)
            plt.plot(data_x, residual3, color = "blue")
            plot_baseline(data_x)

            ###
            f1 = func3(data_x, popt3[0], popt3[1], popt3[2],
                       popt3[3], popt3[4], popt3[5],
                       popt3[6], popt3[7], popt3[8])
            f2 = func1(data_x, popt3c[0], popt3c[1], popt3c[2])
            plt.plot(data_x, f2/f1, lw = 1, color = "green", alpha = 0.4)

            vgal_red = data_x[np.where(f2/f1 < 0.9)[0].min()]
            vgal_blue = data_x[np.where(f2/f1 < 0.9)[0].max()]

            plt.plot([vgal_red,vgal_red],
                     [-0.1,1.1],
                     "green",
                     lw = 2,
                     linestyle = "dashed",
                     alpha = 0.4,
                     label = str(round(vgal_red,1)) + " km s$^{-1}$")

            plt.plot([vgal_blue,vgal_blue],
                     [-0.1,1.1],
                     "green",
                     lw = 2,
                     linestyle = "dashed",
                     alpha = 0.4,
                     label = str(round(vgal_blue,1)) + " km s$^{-1}$")
            ###

            plot_setup(data_x, "ngc5643_fit3.png")

            # plot zoom
            plt.figure()
            plt.plot(data_x, data_y, color = "grey")
            popt3a = popt3[0:3]
            popt3b = popt3[-6:-3]
            popt3c = popt3[-3:]
            plot_func1(data_x, popt3a, "red",
                       linestyle = "dashed")
            plot_func1(data_x, popt3b, "red",
                       linestyle = "dashed")
            plot_func1(data_x, popt3c, "red",
                       linestyle = "dashed")
            plot_func3(data_x, popt3, "red", lw = 2)
            plt.plot(data_x, residual3, color = "blue")
            plot_baseline(data_x)

            ###
            plt.plot([vgal_red,vgal_red],
                     [-0.02,0.2],
                     "green",
                     lw = 2,
                     linestyle = "dashed",
                     alpha = 0.4,
                     label = str(round(vgal_red,1)) + " km s$^{-1}$")

            plt.plot([vgal_blue,vgal_blue],
                     [-0.02,0.2],
                     "green",
                     lw = 2,
                     linestyle = "dashed",
                     alpha = 0.4,
                     label = str(round(vgal_blue,1)) + " km s$^{-1}$")

            ###

            plot_setup(data_x, "ngc5643_fit3_zoom.png",
                       ylim = [-0.02, 0.2])


