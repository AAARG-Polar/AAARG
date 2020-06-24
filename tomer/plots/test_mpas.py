import os, sys
import xarray as xr
import matplotlib
matplotlib.use('Agg')
import netCDF4
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from mpl_toolkits.basemap import Basemap
import numpy as np

import warnings
warnings.filterwarnings("ignore")

#ds = xr.open_dataset("/share/raid3/tburg/mpas/test_sim2/diag.2019-08-31_03.00.00.nc")
#print(ds)
#ds.close()
#sys.exit()

data = netCDF4.Dataset('/share/raid3/tburg/mpas/sim_24km/x1.1024002.static.nc','r')
ter = data.variables['ter'][:]
lat = np.degrees(data.variables['latCell'][:])
lon = np.degrees(data.variables['lonCell'][:])
data.close()

data = netCDF4.Dataset('/share/raid3/tburg/mpas/test_sim2/diag.2019-09-02_00.00.00.nc','r')
ter2 = data.variables['mslp'][:] * 0.01
#lat = np.degrees(data.variables['latCell'][:])
#lon = np.degrees(data.variables['lonCell'][:])
data.close()

#Create basemap projection
bound_n = 47.2
bound_s = 21.8
bound_w = -121.0
bound_e = -61.5
lat_1 = 35.0
lat_2 = 45.0
lat_0 = 40.0
lon_0 = -99.0
m = Basemap(lat_1=lat_1,lat_2=lat_2,lat_0=lat_0,lon_0=lon_0,llcrnrlat=bound_s,urcrnrlat=bound_n,llcrnrlon=bound_w,urcrnrlon=bound_e,rsphere=(6378137.00,6356752.3142),resolution='l',area_thresh=1200.0,projection='lcc')

X,Y = m(lon,lat)
mask = np.logical_or(X<1.e20,Y<1.e20)
X = np.compress(mask,X)
Y = np.compress(mask,Y)
triang = tri.Triangulation(X,Y)





#"""
fig,ax = plt.subplots(figsize=(12,8),dpi=125)
levs = np.arange(0,3000+100,100)

m.drawstates(color='#444444',linewidth=1.0)
m.drawcoastlines(color='#444444',linewidth=1.0)
m.drawcountries(color='#444444',linewidth=1.0)

caf = plt.tricontourf(triang,ter[1:],levs,extend='max',cmap=plt.get_cmap('jet'))
cbar = m.colorbar(caf,location='bottom')
cbar.set_label('meters',fontsize=7)
cbar.ax.tick_params(labelsize=6)

plt.savefig('test_elev24km.png',dpi=350,bbox_inches='tight')
plt.close()
#"""

"""
fig,ax = plt.subplots(figsize=(12,8),dpi=125)
levs = np.arange(940,1040+5,4)

m.drawstates(color='#444444',linewidth=1.0)
m.drawcoastlines(color='#444444',linewidth=1.0)
m.drawcountries(color='#444444',linewidth=1.0)

caf2 = plt.tricontourf(triang,ter2[0,1:],levs,extend='max',cmap=plt.get_cmap('jet'))
cbar2 = m.colorbar(caf2,location='bottom')
cbar2.set_label('hPa',fontsize=7)
cbar2.ax.tick_params(labelsize=6)

plt.savefig('test_mslp6.png',dpi=350,bbox_inches='tight')
plt.close()
"""
