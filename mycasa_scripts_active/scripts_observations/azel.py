import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.coordinates import get_moon
from astropy.coordinates import get_sun
plt.ioff()


# set Subaru information
subaru = EarthLocation.from_geodetic(-155.4761*u.deg, 19.825*u.deg,4139*u.m)
utcoffset = -10*u.hour  # Hawaii
time = Time('2021-02-01 23:00:00') - utcoffset


# set target information
arp220 = SkyCoord.from_name('Arp220')

#
midnight = Time('2021-02-01 00:00:00') - utcoffset
delta_midnight = np.linspace(-12, 12, 1000)*u.hour
#frame_feb = AltAz(obstime=midnight+delta_midnight, location=subaru)
#altazs_arp220_feb = arp220.transform_to(frame_feb)
#altazs_arp220_feb = altazs_arp220_feb.secz

# set Sun
times_feb = midnight + delta_midnight
frame_feb = AltAz(obstime=times_feb, location=subaru)
sunaltazs_feb = get_sun(times_feb).transform_to(frame_feb)
# set Moon
moonaltazs_feb = get_moon(times_feb).transform_to(frame_feb) # times_feb.transform_to(times_feb)
#
arp220_altazs_feb = arp220.transform_to(times_feb)

# plot
plt.figure()
plt.plot(delta_midnight, sunaltazs_feb.alt, color='r', label='Sun')
plt.plot(delta_midnight, moonaltazs_feb.alt, color=[0.75]*3, ls='--', label='Moon')
plt.scatter(delta_midnight, arp220_altazs_feb.alt,
            c=arp220_altazs_feb.az, label='Arp220', lw=0, s=8,
            cmap='viridis')
plt.fill_between(delta_midnight, 0*u.deg, 90*u.deg,
                 sunaltazs_feb.alt < -0*u.deg, color='0.5', zorder=0)
plt.fill_between(delta_midnight, 0*u.deg, 90*u.deg,
                 sunaltazs_feb.alt < -18*u.deg, color='k', zorder=0)
plt.colorbar().set_label('Azimuth [deg]')
plt.legend(loc='upper left')
plt.xlim(-12*u.hour, 12*u.hour)
plt.xticks((np.arange(13)*2-12)*u.hour)
plt.ylim(0*u.deg, 90*u.deg)
plt.xlabel('Hours from Hawaii Midnight')
plt.ylabel('Altitude [deg]')
plt.savefig("test.png")

