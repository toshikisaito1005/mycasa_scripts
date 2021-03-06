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

### nyquist2fits: band 6/3 ratio
for i in range(len(data)):
    flux = np.log10(d_band6[i]/d_band3[i])/np.log10(234.6075/104.024625)
    if d_band3[i] == 0.0:
        flux = 0.0
    elif str(flux) == "inf":
        flux = 0.0
    elif str(flux) == "-inf":
        flux = 0.0
    cl.addcomponent(dir=str(d_ra[i])+"deg, "+str(d_decl[i])+"deg",
                    flux=flux, fluxunit="Jy",
                    freq="234.6075GHz",
                    shape="Point",
                    majoraxis="3.00arcsec",
                    minoraxis="3.00arcsec",
                    positionangle="0.0deg")

ia.fromshape(dir_fits + "nyquist_R_b6_b3_contin.image",
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
exportfits(imagename= dir_fits + 'nyquist_R_b6_b3_contin.image',
           fitsimage= dir_fits + 'nyquist_R_b6_b3_contin.fits',
           overwrite = True)
ia.close()
