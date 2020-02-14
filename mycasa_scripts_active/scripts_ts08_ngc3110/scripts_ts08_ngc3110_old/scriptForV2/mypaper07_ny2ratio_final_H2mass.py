direction="J2000 10:04:02.090 -6.28.29.604"
cl.done()

dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_fits = "../../../ngc3110/ana/data_nyquist/"
data_flux_normal = "ngc3110_flux_sfr.txt"
data_flux_co10 = "ngc3110_flux.txt"
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3))
d_ra, d_decl = data[:,0], data[:,1]
d_halpha, d_vla = data[:,2], data[:,3]

data = np.loadtxt(dir_data + data_flux_co10,
                  usecols = (0,1,2,3))
beta = 1.226 * 10 ** 6. / 1.813 / 1.434 / 115.27120 ** 2
d_co10 = data[:,3] / beta * 113. / 47.115

alpha_co = 1.5

product_file = dir_data + "ngc3110_H2mass.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y H2mass\n")
f.close()

### nyquist2fits: H2 mass
for i in range(len(data)):
    # H2 mass
    z1 = 1 + 0.016858
    nu_obs = 115.27120 / z1
    gmass = 3.25e+7 * d_co10[i] / nu_obs ** 2 * 69.4 ** 2 / z1 ** 2 * alpha_co
    cl.addcomponent(dir=str(d_ra[i])+"deg, "+str(d_decl[i])+"deg",
                    flux=gmass, fluxunit="Jy",
                    freq="234.6075GHz",
                    shape="Point",
                    majoraxis="3.00arcsec",
                    minoraxis="3.00arcsec",
                    positionangle="0.0deg")
    # writing
    f = open(product_file, "a")
    f.write(str(d_ra[i]) + " " + str(d_decl[i])  + " " + str(gmass) + "\n")
    f.close()

ia.fromshape(dir_fits + "nyquist_H2mass.image",
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
exportfits(imagename= dir_fits + 'nyquist_H2mass.image',
           fitsimage= dir_fits + 'nyquist_H2mass.fits',
           overwrite = True)
ia.close()
