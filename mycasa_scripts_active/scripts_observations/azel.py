import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.coordinates import get_moon
from astropy.coordinates import get_sun
#plt.ioff()


# set Subaru information
subaru = EarthLocation.from_geodetic(-155.4761*u.deg, 19.825*u.deg,4139*u.m)
utcoffset = -10*u.hour  # Hawaii
time = Time('2021-02-01 23:00:00') - utcoffset


# set target information
arp220 = SkyCoord.from_name('Arp220')

#
midnight = Time('2021-02-01 00:00:00') - utcoffset
delta_midnight = np.linspace(-12, 12, 1000)*u.hour

# set Sun
times_feb = midnight + delta_midnight
frame_feb = AltAz(obstime=times_feb, location=subaru)
sunaltazs_feb = get_sun(times_feb).transform_to(frame_feb)
# set Moon
moon_feb = get_moon(times_feb)
moonaltazs_feb = moon_feb.transform_to(frame_feb)
#
arp220_altazs_feb = arp220.transform_to(frame_feb)

# plot
figure = plt.figure()
plt.plot(np.array(delta_midnight), np.array(sunaltazs_feb.alt), color='r', label='Sun')
plt.plot(np.array(delta_midnight), np.array(moonaltazs_feb.alt), color=[0.75]*3, ls='--', label='Moon')
plt.scatter(np.array(delta_midnight), np.array(arp220_altazs_feb.alt),
            c=np.array(arp220_altazs_feb.az), label='Arp220', lw=0, s=8,
            cmap='viridis')
#plt.fill_between(delta_midnight, 0, 90,
#                 sunaltazs_feb.alt < 0, color='0.5', zorder=0)
#plt.fill_between(delta_midnight, 0, 90,
#                 sunaltazs_feb.alt < -18, color='k', zorder=0)
plt.colorbar().set_label('Azimuth [deg]')
plt.legend(loc='upper left')
plt.xlim([-12, 12])
plt.xticks((np.arange(13)*2-12))
plt.ylim([0, 90])
plt.xlabel('Hours from Hawaii Midnight')
plt.ylabel('Altitude [deg]')
plt.show()
#plt.savefig("test.png", dpi=200)

