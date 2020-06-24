import matplotlib
matplotlib.use('Agg')
import netCDF4
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from mpl_toolkits.basemap import Basemap
import numpy as np

data = netCDF4.Dataset('mpas_static.nc','r')
ter = data.variables['ter'][:]
lat = np.degrees(data.variables['latCell'][:])
lon = np.degrees(data.variables['lonCell'][:])
data.close()

data = netCDF4.Dataset('/share/raid4/criedel/MPAS-DART/rundir/mpas_static.nc','r')
ter2 = data.variables['ter'][:]
#lat = np.degrees(data.variables['latCell'][:])
#lon = np.degrees(data.variables['lonCell'][:])
data.close()

fig,ax = plt.subplots(1,2,figsize=(8,8))
levs = np.arange(0,3000+100,100)
m = Basemap(ax=ax[0],projection='npstere',boundinglat=55.0,lon_0=260,resolution='l')
m.drawstates(color='#444444',linewidth=1.0)
m.drawcoastlines(color='#444444',linewidth=1.0)
m.drawcountries(color='#444444',linewidth=1.0)
lats = np.array([60.])
X,Y = m(lon,lat)
mask = np.logical_or(X<1.e20,Y<1.e20)
X = np.compress(mask,X)
Y = np.compress(mask,Y)
triang = tri.Triangulation(X,Y)
caf = plt.tricontourf(triang,ter,levs,extend='max',cmap=plt.get_cmap('jet'))
cbar = m.colorbar(caf,location='bottom')
cbar.set_label('meters',fontsize=7)
cbar.ax.tick_params(labelsize=6)
m = Basemap(ax=ax[1],projection='npstere',boundinglat=55.0,lon_0=260,resolution='l')
m.drawstates(color='#444444',linewidth=1.0)
m.drawcoastlines(color='#444444',linewidth=1.0)
m.drawcountries(color='#444444',linewidth=1.0)
caf2 = plt.tricontourf(triang,ter2,levs,extend='max',cmap=plt.get_cmap('jet'))
cbar2 = m.colorbar(caf2,location='bottom')
cbar2.set_label('meters',fontsize=7)
cbar2.ax.tick_params(labelsize=6)
plt.savefig('test.png',dpi=350,bbox_inches='tight')
