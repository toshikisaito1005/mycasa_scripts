import glob
import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.cm as cm
plt.ioff()


# GMC position map
dir_data = "/Users/saito/data/phangs_ulirg/catalogues/"
galnames = ["ngc1614", # z = 0.01594
            "irasf13373a", # ngc 5258, z = 0.02254
            "irasf13373b", # ngc 5257, z = 0.02268
            "ngc3110", # z = 0.01686
            "ngc6240", # z = 0.02448
            ]
filenames = [dir_data+"ngc1614_co21_native_props.fits",
             dir_data+"irasf13373a_co21_native_props.fits",
             dir_data+"irasf13373b_co21_native_props.fits",
             dir_data+"ngc3110_co21_native_props.fits",
             dir_data+"ngc6240_co21_native_props.fits"]
ctr_ra = [68.5001,204.99,204.971,151.009,253.245]
ctr_decl = [-8.57918,0.830823,0.840137,-6.47487,2.40105]
scales = [305., 326., 483., 184., 444., 444., 600.]
size = [0.002, 0.0045, 0.004, 0.0035, 0.0018]

#for i in range(len(filenames)):
for i in [0,1,2,3,4]:
    # moment-0
    dir_gal = dir_data.replace("catalogues/","")+galnames[i]+"/"
    fitsdata = glob.glob(dir_gal+"*.moment0")[0]
    image_r = imhead(fitsdata,mode="list")["shape"][0] - 1
    image_t = imhead(fitsdata,mode="list")["shape"][1] - 1
    data_m0 = imval(fitsdata,box="0,0,"+str(image_r)+","+str(image_t))
    m0_ra = data_m0["coords"][:,:,0].flatten()*180/np.pi - ctr_ra[i]
    m0_decl = data_m0["coords"][:,:,1].flatten()*180/np.pi - ctr_decl[i]
    m0_flux = data_m0["data"].flatten()

    # cprops
    hdu_list = fits.open(filenames[i], memmap=True)
    data = Table(hdu_list[1].data)
    
    data_x = data["XCTR_DEG"][~np.isnan(data["RAD_PC"])] - ctr_ra[i]
    data_y = data["YCTR_DEG"][~np.isnan(data["RAD_PC"])] - ctr_decl[i]
    data_rad = data["RAD_PC"][~np.isnan(data["RAD_PC"])]
    data_s2n = data["S2N"][~np.isnan(data["RAD_PC"])]
    data_pa = data["POSANG"][~np.isnan(data["RAD_PC"])] * 180 / np.pi
    data_height = data["FWHM_MAJ_DC"][~np.isnan(data["RAD_PC"])]
    data_width = data["FWHM_MIN_DC"][~np.isnan(data["RAD_PC"])]

    x = data_x[data_s2n>4.]
    y = data_y[data_s2n>4.]
    s = data_rad[data_s2n>4.]

    ell_height = data_height[data_s2n>4.] / scales[i] / 3600.
    ell_width = data_width[data_s2n>4.] / scales[i] / 3600.
    ell_pa = data_pa[data_s2n>4.]
    np.log10(m0_flux)[~np.isnan(np.log10(m0_flux))] = 0
    np.log10(m0_flux)[~np.isinf(np.log10(m0_flux))] = 0

    # plot
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    plt.rcParams["font.size"] = 18
    ax.set_xlabel("R.A. (deg)")
    ax.set_ylabel("Decl. (deg)")
    ax.set_ylim([size[i]*-1,size[i]])
    ax.set_xlim([size[i],size[i]*-1])

    ax.scatter(m0_ra,#[m0_flux>0],
               m0_decl,#[m0_flux>0],
               c=np.log10(m0_flux),#np.log10(m0_flux[m0_flux>0]),
               cmap="rainbow",
               marker="s",
               lw=0,
               s=3.0)

    for j in range(len(x)):
        c = pat.Ellipse(xy = (x[j], y[j]),
                        width = ell_width[j],
                        height = ell_height[j],
                        angle = 90-ell_pa[j],
                        color = "grey",
                        fill=False)
        ax.add_patch(c)

    plt.legend()
    saveeps = filenames[i].replace("catalogues/","eps/")
    plt.savefig(saveeps.replace("_native_props.fits","_gmc_map.png"),
                dpi=400)

