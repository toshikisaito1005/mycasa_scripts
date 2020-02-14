direction="J2000 10:04:02.090 -6.28.29.604"
cl.done()

dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_fits = "../../../ngc3110/ana/data_nyquist/"
data_flux_normal = "ngc3110_flux.txt"
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3,4,5,6))
d_ra, d_decl = data[:,0], data[:,1]
d_halpha = data[:,2]
d_co10, d_co21 = data[:,3], data[:,4]
d_13co10, d_13co21 = data[:,5], data[:,6]

### nyquist2fits: 13co21
for i in range(len(data)):
    cl.addcomponent(dir=str(d_ra[i])+"deg, "+str(d_decl[i])+"deg",
                    flux=d_13co21[i], fluxunit="Jy",
                    freq="230.0GHz",
                    shape="Gaussian",
                    majoraxis="3.00arcsec",
                    minoraxis="3.00arcsec",
                    positionangle="0.0deg")

ia.fromshape(dir_fits + "nyquist_13co21_m0.image",
             [400,400,1,1],
             overwrite = True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity("0.2arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("151.008708deg", "rad")["value"],
                      qa.convert("-6.474890deg","rad")["value"]],
                     type = "direction")
cs.setreferencevalue("230GHz", "spectral")
cs.setincrement("1GHz", "spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename= dir_fits + 'nyquist_13co21_m0.image',
           fitsimage= dir_fits + 'nyquist_13co21_m0.fits',
           overwrite = True)
ia.close()
