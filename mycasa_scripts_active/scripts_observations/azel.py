import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

# set Subaru information
subaru = EarthLocation.from_geodetic(-155.4761*u.deg, 19.825*u.deg,4139*u.m)
utcoffset = -10*u.hour  # Hawaii
time = Time('2021-02-01 23:00:00') - utcoffset

# set target information
arp220 = SkyCoord.from_name('Arp220')

#altaz_arp220 = arp220.transform_to(AltAz(obstime=time,location=subaru))
#print("Arp220's Altitude = {0.alt:.2}".format(altaz_arp220))

midnight = Time('2021-02-01 00:00:00') - utcoffset