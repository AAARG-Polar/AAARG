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
# Read in data
#=======================================================================================

use_folder = "sim_24km_dorian"#"sim_24km_ac12_thompson"
title_type = "Thompson"#"Thompson"

#=======================================================================================
# Read in data
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
#"""
bound_n = 47.2
bound_s = 21.8
bound_w = -121.0
bound_e = -61.5
lat_1 = 35.0
lat_2 = 45.0
lat_0 = 40.0
lon_0 = -99.0
m = Basemap(lat_1=lat_1,lat_2=lat_2,lat_0=lat_0,lon_0=lon_0,llcrnrlat=bound_s,urcrnrlat=bound_n,llcrnrlon=bound_w,urcrnrlon=bound_e,rsphere=(6378137.00,6356752.3142),resolution='h',area_thresh=1200.0,projection='lcc')
#"""

#m = Basemap(projection='stere',width=10200000*0.4,height=8000000*0.4,lat_ts=-2,lat_0=90,lon_0=-105.0,resolution='l',area_thresh=3500.0)

#=======================================================================================
# Convert lat/lon data to triangulation object
#=======================================================================================

X,Y = m(lon,lat)
mask = np.logical_or(X<1.e20,Y<1.e20)
X = np.compress(mask,X)
Y = np.compress(mask,Y)
triang = tri.Triangulation(X,Y)

#=======================================================================================
# Plot with Basemap
#=======================================================================================

init_date = dt.datetime(2019,9,1,18)
init_str = init_date.strftime('%H%M %d %B %Y')

start_date = dt.datetime(2019,9,1,18)
end_date = dt.datetime(2019,9,2,9)
hour = 0
hr_increment = 3

variables = ['mslp','refl','hghtmslp','qpf','ir']

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
    
    todo = 0
    for var in variables:
        if os.path.isfile(f"images/{var}_f{hour}.png") == False: todo += 1
    if todo == 0:
        start_date += dt.timedelta(hours=hr_increment)
        hour += hr_increment
        continue
    
    data = netCDF4.Dataset(f'/share/raid3/tburg/mpas/{use_folder}/diag.{strdate}.00.00.nc','r')
    mslp = data.variables['mslp'][:] * 0.01
    refl = data.variables['refl10cm_1km'][:]
    hght500 = data.variables['height_500hPa'][:] * 0.1
    qpf = data.variables['rainnc'][:] * (1.0 / 25.4)
    ir = data.variables['olrtoa'][:]
    data.close()
    
    ir = np.power(np.divide(ir,5.67*10**-8),0.25)
    ir = ir - 273.15
    
    for var in variables:
        
        if os.path.isfile(f"images/{var}_f{hour}.png") == True:
            continue

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

        #Contour fill mslp
        if var == 'mslp':
            var_title = "MSLP (hPa)"
            save_title = "mslp"
            
            clevs = np.arange(920,1044,4)
            cs = plt.tricontourf(triang,mslp[0,1:],clevs,extend='both',cmap=plt.get_cmap('jet'))
            cbar2 = m.colorbar(cs,size='3%',pad='1%')
            #cbar2.ax.tick_params(labelsize=6)
            
            #Contour label mslp
            clevs = np.arange(920,1044,4)
            cs = plt.tricontour(triang,mslp[0,1:],clevs,linewidths=1.4,colors='k')
            ax.clabel(cs, inline=1, fontsize=11.5, fmt='%d')
            
        #Contour fill mslp
        if var == 'hghtmslp':
            var_title = "500-hPa Height (dam) & MSLP (hPa)"
            save_title = "hghtmslp"
            
            clevs = np.arange(480.0,609.0,3.0)
            clevsbar = np.arange(480.0,606.0,12.0)
            cmap = col.ListedColormap(colorlib.hght(clevs))
            cs = plt.tricontourf(triang,hght500[0,1:],clevs,extend='both',cmap=cmap)
            cbar2 = m.colorbar(cs,size='3%',pad='1%',ticks=clevsbar)
            #cbar2.ax.tick_params(labelsize=6)
            
            #Contour label mslp
            clevs = np.arange(920,1044,4)
            cs = plt.tricontour(triang,mslp[0,1:],clevs,linewidths=1.4,colors='k')
            ax.clabel(cs, inline=1, fontsize=11.5, fmt='%d')
           
        #Contour fill mslp
        if var == 'tpv':
            var_title = "Dynamic Tropopause Theta & MSLP (hPa)"
            save_title = "tpv"
            
            data2 = netCDF4.Dataset(f'/share/raid3/tburg/mpas/{use_folder}/history.{strdate}.00.00.nc','r')
            theta_pv = data2.variables['theta_pv'][:]
            print(np.unique(theta_pv))
            data2.close()
            
            clevs = np.arange(250.0,401.0,0.5)
            clevsbar = np.arange(250.0,410.0,10)
            cmap = col.ListedColormap(colorlib.theta_dt(clevs))
            cs = plt.tricontourf(triang,hght500[0,1:],clevs,extend='both',cmap=cmap)
            
            clevs = np.arange(250.0,800.0,0.5)
            clevsbar = np.arange(250.0,810.0,100)
            cmap = col.ListedColormap(colorlib.theta_dt(clevs))
            cs = plt.tricontourf(triang,hght500[0,1:],clevs,extend='both')
            cbar2 = m.colorbar(cs,size='3%',pad='1%',ticks=clevsbar)
            #cbar2.ax.tick_params(labelsize=6)
            
            #Contour label mslp
            clevs = np.arange(920,1044,4)
            cs = plt.tricontour(triang,mslp[0,1:],clevs,linewidths=1.8,colors='k')
            ax.clabel(cs, inline=1, fontsize=11.5, fmt='%d')
        
        if var == 'refl':
            var_title = "Reflectivity (dBZ)"
            save_title = "refl"
            
            clevs = np.arange(5,76,1)
            clevs2 = np.arange(5,76,5)
            cmap = col.ListedColormap(colorlib.reflectivity(clevs))
            cs = plt.tricontourf(triang,refl[0,1:],clevs,extend='max',cmap=cmap)
            cbar2 = m.colorbar(cs,size='3%',pad='1%',ticks=clevs2)
            
            #Contour label mslp
            clevs = np.arange(920,1044,4)
            plt.tricontour(triang,mslp[0,1:],clevs,linewidths=0.2,colors='k')
        
        if var == 'qpf':
            var_title = "Accumulated Precipitation (in)"
            save_title = "qpf"
            
            clevs = [0,0.01,0.02,0.05,0.10,0.15,0.20,0.25,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1.00,1.10,1.20,1.30,1.40,1.50,1.75,2.00,2.50,3.00,4.00,6.00,8.00,10.00,15.00,20.00,30.00]
            cmap = colorlib.precip()
            norm = col.BoundaryNorm(clevs,cmap.N)
            cs = plt.tricontourf(triang,qpf[0,1:],clevs,extend='max',cmap=cmap,norm=norm)
            cbar2 = m.colorbar(cs,size='3%',pad='1%',ticks=clevs)
        
        if var == 'ir':
            var_title = "Simulated TOA Brightness (deg C)"
            save_title = "ir"
            
            clevs = np.arange(-90,21,1)
            clevsbar = [-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20]
            cmap = col.ListedColormap(colorlib.ir(clevs))
            cs = plt.tricontourf(triang,ir[0,1:],clevs,extend='max',cmap=cmap)
            cbar2 = m.colorbar(cs,size='3%',pad='1%',ticks=clevsbar)
        

        #Save figure and close
        start_date.strftime("%Y-%m-%d_%H")
        strdate = start_date.strftime("%H00 UTC %d %b %Y")
        plt.title(f"24-km MPAS | {title_type} Microphysics | {var_title}\nInit: {init_str} | Hour [{hour}] | Valid: {strdate}",fontweight='bold',fontsize=14,loc='left')
        plt.savefig(f"images/{save_title}_f{hour}.png")
        plt.close()

    #Increment hour
    start_date += dt.timedelta(hours=hr_increment)
    hour += hr_increment
