direction="J2000 10:04:02.090 -6.28.29.604"
cl.done()

dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_fits = "../../../ngc3110/ana/data_nyquist/"
data_flux_normal = "ngc3110_flux_sfr.txt"
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3))
d_ra, d_decl = data[:,0], data[:,1]
d_halpha, d_vla = data[:,2], data[:,3]


product_file = dir_data + "ngc3110_sfr.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y SFR\n")
f.close()

### nyquist2fits: SFR density
for i in range(len(data)):
    lumi_hlpha = d_halpha[i] * 36.5 * 4. * np.pi \
                 * (69.4 * 10 ** 6. * 3. * 10. ** 18.) ** 2.
    lumi_vla = d_vla[i] / 26.7658 * 1.e-23 * (4. * np.pi * (69.4 * 1000000. * 3086000000000000000.) ** 2.)
    flux1 = (lumi_hlpha + 0.39e+13 * lumi_vla) / 10. ** 41.27 # sfr
    flux = (flux1 / ((3. * 0.325 / 2.) ** 2 * np.pi))
    if d_halpha[i] < 2.2e-19:
        flux = 0.0
    cl.addcomponent(dir=str(d_ra[i])+"deg, "+str(d_decl[i])+"deg",
                    flux=flux, fluxunit="Jy",
                    freq="234.6075GHz",
                    shape="Gauss",
                    majoraxis="3.00arcsec",
                    minoraxis="3.00arcsec",
                    positionangle="0.0deg")
    # writing
    f = open(product_file, "a")
    f.write(str(d_ra[i]) + " " + str(d_decl[i])  + " " + str(flux) + "\n")
    f.close()

ia.fromshape(dir_fits + "nyquist_corr_sfr_density.image",
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
exportfits(imagename= dir_fits + 'nyquist_corr_sfr_density.image',
           fitsimage= dir_fits + 'nyquist_corr_sfr_density.fits',
           overwrite = True)
ia.close()
