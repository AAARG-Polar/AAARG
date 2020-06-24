import os, sys
import numpy as np
import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as col

import metpy.calc as calc
from metpy.units import units

import colorlib
import matplotlib
matplotlib.use('Agg')
import netCDF4
import matplotlib.tri as tri
import warnings
warnings.filterwarnings("ignore")

#=======================================================================================
# Read in data via thredds
#=======================================================================================


#=======================================================================================
# Create basemap
#=======================================================================================

print("--> Starting Basemap")

use_folder = "sim_24km"#"sim_24km_ac12_thompson"#
title_type = "Kessler"#"Thompson"#

#Create basemap projection
"""
bound_n = 47.2
bound_s = 21.8
bound_w = -121.0
bound_e = -61.5
lat_1 = 35.0
lat_2 = 45.0
lat_0 = 40.0
lon_0 = -99.0
m = Basemap(lat_1=lat_1,lat_2=lat_2,lat_0=lat_0,lon_0=lon_0,llcrnrlat=bound_s,urcrnrlat=bound_n,llcrnrlon=bound_w,urcrnrlon=bound_e,rsphere=(6378137.00,6356752.3142),resolution='h',area_thresh=1200.0,projection='lcc')
"""

"""
m = Basemap(projection='stere',width=10200000*0.35,height=8000000*0.35,lat_ts=-2,lat_0=90,lon_0=360.0-105.0,resolution='l',area_thresh=3500.0)

#=======================================================================================
# Convert lat/lon data to triangulation object
#=======================================================================================

#Create figure
fig = plt.figure(figsize=(14,9),dpi=125)
ax = fig.add_axes([0.05,0.03,0.89,0.90])

#Add geography
m.drawcountries(color='#022400')
m.drawcoastlines(color='#022400')
m.drawstates(color='#022400')

parallels = np.arange(-90,90,20)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=9,linewidth=0.4)
meridians = np.arange(0,360,20)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=9,linewidth=0.4)
m.drawmapboundary(fill_color='#EDFBFF',zorder=-1)
m.fillcontinents(color='#FBF5EA',lake_color='#EDFBFF',zorder=0)

#Plot tracks
color_arr = ['k','r','b','g']
titles = ['ERA-5','Kessler','Thompson','WSM6']
for idx,sim in enumerate(['_era5','','_ac12_thompson','_ac12_wsm6']):
	lat = np.load(f"sim_24km{sim}_lats.npy")
	lon = np.load(f"sim_24km{sim}_lons.npy")
	mslp = np.load(f"sim_24km{sim}_vals.npy")
	
	if sim == '_ac12_wsm6':
		lat = lat[:-1]
		lon = lon[:-1]
		mslp = mslp[:-1]
	
	x,y = m(lon,lat)
	lw = 2.4
	if titles[idx] == 'ERA-5': lw = 3.5
	
	plt.plot(x,y,'-',linewidth=lw,color=color_arr[idx],label=titles[idx])
	plt.plot(x[0],y[0],'D',ms=12,color=color_arr[idx],mec='k',mew=0.5)
	plt.plot(x[4::4],y[4::4],'o',ms=7,color=color_arr[idx],mec='k',mew=0.5)



plt.legend(loc=2,prop={'size':16})

#Save figure and close
#start_date.strftime("%Y-%m-%d_%H")
#strdate = start_date.strftime("%H00 UTC %d %b %Y")
plt.title(f"MPAS Track Comparisons",fontweight='bold',fontsize=16,loc='left')
plt.savefig(f"tracks.png")
plt.close()

#start_date += dt.timedelta(hours=hr_increment)
#hour += hr_increment

#==============================================================
"""


import matplotlib.dates as mdates
fig,ax=plt.subplots(figsize=(12,6),dpi=125)

#Plot tracks
color_arr = ['k','r','b','g']
titles = ['ERA-5','Kessler','Thompson','WSM6']
for idx,sim in enumerate(['_era5','','_ac12_thompson','_ac12_wsm6']):
	x = []
	start_date = dt.datetime(2012,8,4,0)
	end_date = dt.datetime(2012,8,10,0)
	while start_date <= end_date:
		x.append(start_date)
		start_date += dt.timedelta(hours=6)
	y = np.load(f"sim_24km{sim}_vals.npy")
	x = x[:len(y)]
	
	if sim == '_ac12_wsm6':
		x = x[:-1]
		y = y[:-1]
	
	col = color_arr[idx]
	label = titles[idx]
	print(x)
	print(y)

	ax.plot(x,y,'-o',color=col,label=label)
	ax.set_xticks(x[::4])
	ax.set_xticklabels(x[::4])
	myFmt = mdates.DateFormatter('%m-%d/%H')
	ax.xaxis.set_major_formatter(myFmt)

plt.legend(loc=3,prop={'size':10})
plt.grid()
plt.title("ERA-5 Minimum MSLP",fontsize=16,fontweight='bold')
plt.xlabel("Date",fontweight='bold')
plt.ylabel("MSLP (hPa)",fontweight='bold')
plt.savefig("track_mslp.png")
plt.close()