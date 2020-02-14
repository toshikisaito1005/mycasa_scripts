direction="J2000 10:04:02.090 -6.28.29.604"
cl.done()

dir_data = "../../phangs/co_ratio/photmetry/"
dir_fits = "../../phangs/co_ratio/photmetry/"

"""
### nyquist2fits: co21 co10 ratio (no)
data_flux_normal = "m74_flux_no.txt"
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
                    majoraxis="5.00arcsec",
                    minoraxis="5.00arcsec",
                    positionangle="0.0deg")

ia.fromshape(dir_fits + "nyquist_R_co21_co10_no.image",
             [128,128,1,1],
             overwrite = True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity("2.5arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("24.1739deg", "rad")["value"],
                      qa.convert("15.7822deg","rad")["value"]],
                     type = "direction")
cs.setreferencevalue("234.6075GHz", "spectral")
cs.setincrement("1GHz", "spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename= dir_fits + 'nyquist_R_co21_co10_no.image',
           fitsimage= dir_fits + 'nyquist_R_co21_co10_no.fits',
           overwrite = True)
ia.close()

### nyquist2fits: co21 co10 ratio (-2)
data_flux_normal = "m74_flux_-2.txt"
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
                    majoraxis="5.00arcsec",
                    minoraxis="5.00arcsec",
                    positionangle="0.0deg")

ia.fromshape(dir_fits + "nyquist_R_co21_co10_-2.image",
             [128,128,1,1],
             overwrite = True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity("2.5arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("24.1739deg", "rad")["value"],
                      qa.convert("15.7822deg","rad")["value"]],
                     type = "direction")
cs.setreferencevalue("234.6075GHz", "spectral")
cs.setincrement("1GHz", "spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename= dir_fits + 'nyquist_R_co21_co10_-2.image',
           fitsimage= dir_fits + 'nyquist_R_co21_co10_-2.fits',
           overwrite = True)
ia.close()


### nyquist2fits: co21 co10 ratio (0)
data_flux_normal = "m74_flux_0.txt"
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
                    majoraxis="5.00arcsec",
                    minoraxis="5.00arcsec",
                    positionangle="0.0deg")

ia.fromshape(dir_fits + "nyquist_R_co21_co10_0.image",
             [128,128,1,1],
             overwrite = True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity("2.5arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("24.1739deg", "rad")["value"],
                      qa.convert("15.7822deg","rad")["value"]],
                     type = "direction")
cs.setreferencevalue("234.6075GHz", "spectral")
cs.setincrement("1GHz", "spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename= dir_fits + 'nyquist_R_co21_co10_0.image',
           fitsimage= dir_fits + 'nyquist_R_co21_co10_0.fits',
           overwrite = True)
ia.close()
"""


### nyquist2fits: co21 co10 ratio (2)
data_flux_normal = "m74_flux_2.txt"
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
                    majoraxis="5.00arcsec",
                    minoraxis="5.00arcsec",
                    positionangle="0.0deg")

ia.fromshape(dir_fits + "nyquist_R_co21_co10_2.image",
             [128,128,1,1],
             overwrite = True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity("2.5arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("24.1739deg", "rad")["value"],
                      qa.convert("15.7822deg","rad")["value"]],
                     type = "direction")
cs.setreferencevalue("234.6075GHz", "spectral")
cs.setincrement("1GHz", "spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename= dir_fits + 'nyquist_R_co21_co10_2.image',
           fitsimage= dir_fits + 'nyquist_R_co21_co10_2.fits',
           overwrite = True)
ia.close()

