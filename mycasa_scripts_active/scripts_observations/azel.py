import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
plt.ioff()


# set Subaru information
subaru = EarthLocation.from_geodetic(-155.4761*u.deg, 19.825*u.deg,4139*u.m)
utcoffset = -10*u.hour  # Hawaii
time = Time('2021-02-01 23:00:00') - utcoffset


# set target information
arp220 = SkyCoord.from_name('Arp220')

#
midnight = Time('2021-02-01 00:00:00') - utcoffset
delta_midnight = np.linspace(-2, 10, 100)*u.hour
frame_feb = AltAz(obstime=midnight+delta_midnight, location=subaru)
altazs_arp220_feb = arp220.transform_to(frame_feb)
altazs_arp220_feb = altazs_arp220_feb.secz

# plot
