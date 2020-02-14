direction="J2000 10:04:02.090 -6.28.29.604"
cl.done()

dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_fits = "../../../ngc3110/ana/data_nyquist/"
data_flux_normal = "ngc3110_flux_contin.txt"
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3,4))
d_ra, d_decl = data[:,0], data[:,1]
d_halpha = data[:,2]
d_band3, d_band6 = data[:,3], data[:,4]

product_file = dir_data + "ngc3110_ISMmass.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y ISMmass\n")
f.close()

z = 0.016858
h = 6.626e-27 # erg.s
k = 1.38e-16 # erg/K
nu_obs = 234.6075 / (1 + z) #GHz
Td = 25 # K

alpha_850 = 6.7e+19
factor = h * nu_obs * (1 + z) / (k * Td)
factor_0 = h * 353.  * (1 + 0) / (k * Td)
gamma_rj = factor / (np.exp(factor) - 1)
gamma_0 = factor_0 / (np.exp(factor_0) - 1)

### nyquist2fits: ISM mass
for i in range(len(data)):
    imass = 1.78 * d_band6[i] * (1 + z) ** 4.8 * (352.6970094/234.6075) ** 3.8 * (69.4 / 1000.) ** 2 \
            * (6.7e+19/alpha_850) * gamma_0 / gamma_rj * 10.e+10
    cl.addcomponent(dir=str(d_ra[i])+"deg, "+str(d_decl[i])+"deg",
                    flux=imass, fluxunit="Jy",
                    freq="234.6075GHz",
                    shape="Gaussian",
                    majoraxis="3.00arcsec",
                    minoraxis="3.00arcsec",
                    positionangle="0.0deg")
    # writing
    f = open(product_file, "a")
    f.write(str(d_ra[i]) + " " + str(d_decl[i])  + " " + str(imass) + "\n")
    f.close()

ia.fromshape(dir_fits + "nyquist_ISMmass.image",
             [50,50,1,1],
             overwrite = True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity("1.6arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("151.008708deg", "rad")["value"],
                      qa.convert("-6.474890deg","rad")["value"]],
                     type = "direction")
cs.setreferencevalue("234.6075GHz", "spectral")
cs.setincrement("1GHz", "spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename= dir_fits + 'nyquist_ISMmass.image',
           fitsimage= dir_fits + 'nyquist_ISMmass.fits',
           overwrite = True)
ia.close()
