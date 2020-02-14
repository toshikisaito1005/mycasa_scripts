import glob
import numpy as np

imagenames = glob.glob("../sim_phangs/*/*caf*.fidelity")

txtname = "phangs_fidelity.txt"
os.system("rm -rf " + txtname)
f = open(txtname, "w")
f.write("# gal caf_fid cdf_fid 7m_fid circ_diameter model_flux caf_flux cdf_flux 7m_flux cdaf_fid cdaf_flux \n")
for i in range(len(imagenames)):
    galname = imagenames[i].split("/")[2]
    box_tmp = imhead(imagenames[i],mode="list")["shape"]
    box_x = str(box_tmp[0] - 1)
    box_y = str(box_tmp[1] - 1)
    box = "0,0," + box_x + "," + box_y
    dir_data = imagenames[i].split(galname)[0] + galname + "/"

    # caf
    imagename = glob.glob(dir_data+"*caf*.fidelity")[0]
    caf_fidelity_tmp = imval(imagename,box=box)
    x = caf_fidelity_tmp['data'].flatten()
    caf_median_fidelity = str(np.round(np.median(x[x>0]),2))
    # cdf
    imagename = glob.glob(dir_data+"*cdf*br.fidelity")[0]
    cdf_fidelity_tmp = imval(imagename,box=box)
    x = cdf_fidelity_tmp['data'].flatten()
    cdf_median_fidelity = str(np.round(np.median(x[x>0]),2))
    # cdaf
    imagename = glob.glob(dir_data+"*cdf*feather.fidelity")[0]
    cdaf_fidelity_tmp = imval(imagename,box=box)
    x = cdaf_fidelity_tmp['data'].flatten()
    cdaf_median_fidelity = str(np.round(np.median(x[x>0]),2))
    # cbf
    imagename = glob.glob(dir_data+"*cbf*br.fidelity")[0]
    cbf_fidelity_tmp = imval(imagename,box=box)
    x = cbf_fidelity_tmp['data'].flatten()
    cbf_median_fidelity = str(np.round(np.median(x[x>0]),2))
    # 7m
    imagename = glob.glob(dir_data+"*7m*.fidelity")[0]
    aca_fidelity_tmp = imval(imagename,box=box)
    x = aca_fidelity_tmp['data'].flatten()
    aca_median_fidelity = str(np.round(np.median(x[x>0]),2))

    # fidelity image information
    pixel_rad = abs(imhead(imagename,mode="list")["cdelt1"])
    pixelarea_arcsec = np.round(pixel_rad * 180/np.pi*3600,2)**2
    galaxyarea_arcsec = len(x[x>0]) * pixelarea_arcsec
    diameter_arcsec = str(np.round(np.sqrt(galaxyarea_arcsec / np.pi),1)*2)
    print("# working on " + galname + ", " + str(i) + "/" + str(len(imagenames)))

    # skymodel information
    imagename = glob.glob(dir_data+"*skymodel.smooth")[0]
    model_flux = str(np.round(imstat(imagename)["flux"][0],2))
    model_max = str(np.round(imstat(imagename)["max"][0],2))
    imagename = glob.glob(dir_data+"*caf*.smooth.pbcor")[0]
    caf_flux = str(np.round(imstat(imagename)["flux"][0],2))
    caf_max = str(np.round(imstat(imagename)["max"][0],2))
    imagename = glob.glob(dir_data+"*cdf*br.smooth.pbcor")[0]
    cdf_flux = str(np.round(imstat(imagename)["flux"][0],2))
    cdf_max = str(np.round(imstat(imagename)["max"][0],2))
    imagename = glob.glob(dir_data+"*cdf*feather.smooth.pbcor")[0]
    cdaf_flux = str(np.round(imstat(imagename)["flux"][0],2))
    cdaf_max = str(np.round(imstat(imagename)["max"][0],2))
    imagename = glob.glob(dir_data+"*7m*br.smooth.pbcor")[0]
    aca_flux = str(np.round(imstat(imagename)["flux"][0],2))
    aca_max = str(np.round(imstat(imagename)["max"][0],2))
    imagename = glob.glob(dir_data+"*cbf*.smooth.pbcor")[0]
    cbf_flux = str(np.round(imstat(imagename)["flux"][0],2))
    cbf_max = str(np.round(imstat(imagename)["max"][0],2))


    phangs_txt = galname + " " + caf_median_fidelity + " "
    phangs_txt = phangs_txt + cdf_median_fidelity + " "
    phangs_txt = phangs_txt + aca_median_fidelity + " "
    phangs_txt = phangs_txt + diameter_arcsec + " "
    phangs_txt = phangs_txt + model_flux + " " + caf_flux + " "
    phangs_txt = phangs_txt + cdf_flux + " " + aca_flux + " "
    phangs_txt = phangs_txt + cdaf_median_fidelity + " " + cdaf_flux + " "
    phangs_txt = phangs_txt + cbf_median_fidelity + " " + cbf_flux + " "
    phangs_txt = phangs_txt + model_max + " " + caf_max + " "
    phangs_txt = phangs_txt + cdf_max + " " + cdaf_max + " "
    phangs_txt = phangs_txt + aca_max + " " + cbf_max
    f.write(phangs_txt + "\n")

f.close()

