import os, sys
import numpy as np
import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as col
from geopy.distance import great_circle

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

data = netCDF4.Dataset('/share/raid3/tburg/mpas/sim_24km/x1.1024002.static.nc','r')
lat = np.degrees(data.variables['latCell'][:])
lon = np.degrees(data.variables['lonCell'][:])
data.close()

#=======================================================================================
# Create basemap
#=======================================================================================

print("--> Starting Basemap")

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
m = Basemap(projection='stere',width=10200000*0.4,height=8000000*0.4,lat_ts=-2,lat_0=90,lon_0=-105.0,resolution='l',area_thresh=3500.0)

#=======================================================================================
# Convert lat/lon data to triangulation object
#=======================================================================================

X,Y = m(lon,lat)
mask = np.logical_or(X<1.e20,Y<1.e20)
mask = np.logical_or(lat>60.0,lat>61.0)
X = np.compress(mask,X)
Y = np.compress(mask,Y)
lon = np.compress(mask,lon)
lat = np.compress(mask,lat)
triang = tri.Triangulation(X,Y)

#=======================================================================================
# Plot with Basemap
#=======================================================================================

use_folder = "sim_24km_ac12_wsm6"#"sim_24km_ac12_thompson"#
for use_folder in ['sim_24km','sim_24km_ac12_wsm6','sim_24km_ac12_thompson']:

	init_date = dt.datetime(2012,8,3,0)
	init_str = init_date.strftime('%H%M %d %B %Y')

	start_date = dt.datetime(2012,8,4,0)
	end_date = dt.datetime(2012,8,10,0)
	hour = 24
	hr_increment = 6

	start_lat = 68
	start_lon = 130

	lons = []
	lats = []
	vals = []

	while start_date <= end_date:
		
		#Skip if already exists
		"""
		if os.path.isfile(f"images/{variables[0]}_f{hour}.png") == True:
			start_date += dt.timedelta(hours=3)
			hour += 3
			continue
		"""
		
		print(start_date)
		strdate = start_date.strftime("%Y-%m-%d_%H")
		
		data = netCDF4.Dataset(f'/share/raid3/tburg/mpas/{use_folder}/diag.{strdate}.00.00.nc','r')
		mslp = data.variables['mslp'][:] * 0.01
		mslp = np.compress(mask,mslp)
		data.close()
		
		data_mask = np.copy(lat)
		#for i in range(len(lon)):
		#	print(great_circle((lat[i],lon[i]),(start_lat,start_lon)).kilometers)
		dist_arr = np.array([great_circle((lat[i],lon[i]),(start_lat,start_lon)).kilometers for i in range(len(lon))])
		data_mask[lat > -100] = False
		data_mask[dist_arr < 600] = True
		
		mslp = np.ma.masked_where(data_mask == False,mslp)
		mslp_min = np.min(mslp)
		idx = np.where(mslp == mslp_min)
		
		start_lon = lon[idx]
		start_lat = lat[idx]
		lons.append(np.ma.getdata(lon[idx])[0])
		lats.append(np.ma.getdata(lat[idx])[0])
		vals.append(mslp_min)

		start_date += dt.timedelta(hours=hr_increment)
		hour += hr_increment

	print(lons)
	print(lats)
	print(vals)

	np.save(f"{use_folder}_lons.npy",lons)
	np.save(f"{use_folder}_lats.npy",lats)
	np.save(f"{use_folder}_vals.npy",vals)
	
	print("DONE ONE")