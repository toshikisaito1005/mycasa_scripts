direction="J2000 12:22:54.884 15.49.20.048"
cl.done()

dir_data = "../../phangs/co_ratio/photmetry/"
dir_fits = "../../phangs/co_ratio/photmetry/"
beam = 4.06

### nyquist2fits: co21 co10 ratio
data_flux_normal = "ngc4321_flux.txt"
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3))
d_ra, d_decl = data[:,0], data[:,1]
d_co10, d_co21 = data[:,2], data[:,3]

for i in range(len(data)):
    flux = d_co21[i]/d_co10[i]
    if d_co10[i] == 0.0:
        flux = 0.0
    cl.addcomponent(dir=str(d_ra[i])+"deg, "+str(d_decl[i])+"deg",
                    flux=flux, fluxunit="Jy",
                    freq="234.6075GHz",
                    shape="Point",
                    majoraxis=str(beam)+"arcsec",
                    minoraxis=str(beam)+"arcsec",
                    positionangle="0.0deg")

ia.fromshape(dir_fits + "ngc4321_nyquist_R.image",
             [128,128,1,1],
             overwrite = True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity(str(beam)+"arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("185.729deg", "rad")["value"],
                      qa.convert("15.8222deg","rad")["value"]],
                     type = "direction")
cs.setreferencevalue("234.6075GHz", "spectral")
cs.setincrement("1GHz", "spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename= dir_fits + 'ngc4321_nyquist_R.image',
           fitsimage= dir_fits + 'ngc4321_nyquist_R.fits',
           overwrite = True)
ia.close()

