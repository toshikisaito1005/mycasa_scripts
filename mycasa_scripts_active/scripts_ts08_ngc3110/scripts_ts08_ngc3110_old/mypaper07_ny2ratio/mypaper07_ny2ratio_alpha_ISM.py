direction="J2000 10:04:02.090 -6.28.29.604"
cl.done()

dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_fits = "../../../ngc3110/ana/data_nyquist/"
data_flux_normal = "ngc3110_flux_contin.txt"
data_flux_co10 = "ngc3110_flux.txt"
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3,4))
d_ra, d_decl = data[:,0], data[:,1]
d_halpha = data[:,2]
d_band3, d_band6 = data[:,3], data[:,4]

data = np.loadtxt(dir_data + data_flux_co10,
                  usecols = (0,1,2,3,4))
d_co10 = data[:,3]
beta = 1.226 * 10 ** 6. / 1.813 / 1.434 / 115.27120 ** 2
jy_co10 = data[:,3] / beta * 113. / 47.115

product_file = dir_data + "ngc3110_alpha_ism.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y co10 ISMmass\n")
f.close()

z = 0.016858
h = 6.626e-27 # erg.s
k = 1.38e-16 # erg/K
nu_obs = 234.6075 / (1 + z) #GHz
Td = 25 # K

alpha_850 = 6.7e+19
factor = h * nu_obs * (1 + z) / (k * Td)
factor_0 = h * nu_obs * (1 + 0) / (k * Td)
gamma_rj = factor / (np.exp(factor) - 1)
gamma_0 = factor_0 / (np.exp(factor_0) - 1)

### nyquist2fits: ISM mass
for i in range(len(data)):
    # ISM mass
    imass = 1.78 * d_band6[i] * (1 + z) ** 4.8 * (352.6970094/234.6075) ** 3.8 * (69.4 / 1000.) ** 2 \
            * (6.7e+19/alpha_850) * gamma_0 / gamma_rj * 10.e+10
    # L'co10
    z1 = 1 + 0.016858
    nu_obs = 115.27120 / z1
    l_co = 3.25e+7 * jy_co10[i] / nu_obs ** 2 * 69.4 ** 2 / z1 ** 2
    flux = imass / l_co
    if l_co == 0.0:
        flux = 0.0
    cl.addcomponent(dir=str(d_ra[i])+"deg, "+str(d_decl[i])+"deg",
                    flux=flux, fluxunit="Jy",
                    freq="234.6075GHz",
                    shape="Gaussian",
                    majoraxis="3.00arcsec",
                    minoraxis="3.00arcsec",
                    positionangle="0.0deg")
    # writing
    f = open(product_file, "a")
    f.write(str(d_ra[i]) + " " + str(d_decl[i])  + " " + str(d_co10[i])  + " " + str(imass) + "\n")
    f.close()

ia.fromshape(dir_fits + "nyquist_alpha_ism.image",
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
exportfits(imagename= dir_fits + 'nyquist_alpha_ism.image',
           fitsimage= dir_fits + 'nyquist_alpha_ism.fits',
           overwrite = True)
ia.close()
