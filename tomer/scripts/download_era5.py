"""
This script uses the CDS API to retrieve ERA-5 data. This assumes that you have the CDS API installed.
Follow the instructions for setting up the CDS API: https://cds.climate.copernicus.eu/api-how-to
The output is saved as a netcdf file using the name requested.
"""

#Import python libraries for dates and CDS API
import datetime as dt
import cdsapi

#Create an instance of a CDS API client
c = cdsapi.Client()

#===================================================================================
# User input - only edit section below
#===================================================================================

#Start and end dates
start_date = "2020-06-01"
end_date = "2020-06-18"

#Specify CDS requested variables to download (check ERA-5 CDS website for list of variables)
#Pressure levels: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=form
#Single levels:   https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form
variables_cds = {
                 'pressure_levels': #List of pressure level variables. If none requested, use an empty list ([]).
                 ['geopotential','temperature','u_component_of_wind','v_component_of_wind'],
    
                 'pressure_levels_hpa': #List of pressure levels in hPa. Ignored if no pressure level data is requested.
                 [250,500,700,850,925],
    
                 'single_levels': #List of single level variables. If none requested, use an empty list ([]).
                 ['mean_sea_level_pressure','2m_temperature','10m_u_component_of_wind','10m_v_component_of_wind'],
}

#PVU surface variables from complete tape ERA-5 archive on ECMWF (warning - will take a while to download!)
#If not necessary, leave 'param' as an empty string ('param':''). This will skip this section.
#URL for variables listing: https://apps.ecmwf.int/data-catalogues/era5/?stream=oper&levtype=pv&expver=1&month=mar&year=2020&type=an&class=ea
variables_pv = {
                 'param': #String of variable IDs separated by a forward slash (/). Check ECMWF ERA-5 website for list.
                 '3.128/54.128/131.128/132.128',
    
                 'levels_pv': #List of PV levels.
                 [2000],
}

#Isentropic variables from complete tape ERA-5 archive on ECMWF (warning - will take a while to download!)
#If not necessary, leave 'param' as an empty string ('param':''). This will skip this section.
#URL for variables listing: https://apps.ecmwf.int/data-catalogues/era5/?stream=oper&levtype=pt&expver=1&month=mar&year=2020&type=an&class=ea
variables_isentropic = {
                 'param': #String of variable IDs separated by a forward slash (/). Check ECMWF ERA-5 website for list.
                 '54.128/60.128/131/132/133.128',
    
                 'levels_kelvin': #List of isentropic levels in Kelvin.
                 [300,310],
}

#Grid resolution in degrees
grid = [0.25,0.25]

#Hour increments (every 1, 3, 6 or 12 hours)
hour_increment = 6

#Data coordinate bounds (longitude from 0 to 360 degrees)
bound_n = 90
bound_s = 20
bound_w = 0
bound_e = 360

#Output file name. If blank, one will be generated.
output_fname = "" #output.nc

"""
Relevant pressure level variables:
'geopotential'
'potential_vorticity'
'relative_humidity'
'specific_humidity'
'temperature','u_component_of_wind'
'v_component_of_wind'
'vertical_velocity'

Relevant single level variables:
'100m_u_component_of_wind'
'100m_v_component_of_wind'
'10m_u_component_of_wind'
'10m_v_component_of_wind'
'2m_dewpoint_temperature'
'2m_temperature'
'convective_available_potential_energy'
'convective_inhibition'
'convective_precipitation'
'convective_snowfall'
'high_cloud_cover'
'land_sea_mask'
'large_scale_precipitation'
'large_scale_snowfall'
'leaf_area_index_high_vegetation'
'leaf_area_index_low_vegetation'
'low_cloud_cover'
'maximum_2m_temperature_since_previous_post_processing'
'mean_sea_level_pressure'
'medium_cloud_cover'
'minimum_2m_temperature_since_previous_post_processing'
'orography'
'precipitation_type'
'sea_ice_cover'
'sea_surface_temperature'
'skin_temperature'
'snow_density'
'snow_depth'
'snowfall'
'soil_temperature_level_1'
'soil_type'
'surface_pressure'
'toa_incident_solar_radiation'
'total_cloud_cover'
'total_column_water_vapour'
'total_precipitation'
'vertical_integral_of_eastward_water_vapour_flux'
'vertical_integral_of_northward_water_vapour_flux'
'zero_degree_level'
"""

#===================================================================================
# Set up variables
#===================================================================================

#Handle dates
sdate = dt.datetime.strptime(start_date,'%Y-%m-%d')
edate = dt.datetime.strptime(end_date,'%Y-%m-%d')
reg_date = dt.datetime.strftime(sdate,'%Y-%m-%d') + "/to/" + dt.datetime.strftime(edate,'%Y-%m-%d')
new_date = dt.datetime.strftime(sdate,'%Y-%m-%d') + "/" + dt.datetime.strftime(edate,'%Y-%m-%d')
yyyy = dt.datetime.strftime(sdate,'%Y')
mm = dt.datetime.strftime(sdate,'%m')

#Format title
use_title = "era_"+dt.datetime.strftime(sdate,'%Y%m')
if output_fname != '': use_title = output_fname + ''

#Get list of days
days = []
idate = dt.datetime.strptime(start_date,'%Y-%m-%d')
while idate <= edate:
    days.append(idate.strftime("%d"))
    idate += dt.timedelta(hours=24)

#Format area
area = [bound_n, bound_w, bound_s, bound_e]
area_old = str(bound_n) + "/" + str(bound_w) + "/" + str(bound_s) + "/" + str(bound_e)

if hour_increment == 12:
    reg_time = ["00:00","12:00"]
    reg_time_old = "00:00:00/12:00:00"
    
if hour_increment == 6:
    reg_time = ["00:00","06:00","12:00","18:00"]
    reg_time_old = "00:00:00/06:00:00/12:00:00/18:00:00"
    
if hour_increment == 3:
    reg_time = ["00:00","03:00","06:00","09:00","12:00","15:00","18:00","21:00"]
    reg_time_old = "00:00:00/03:00:00/06:00:00/09:00:00/12:00:00/15:00:00/18:00:00/21:00:00"

if hour_increment == 1:
    reg_time = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00",
                "10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00",
                "20:00","21:00","22:00","23:00"]
    reg_time_old = "00:00:00/01:00:00/02:00:00/03:00:00/04:00:00/05:00:00/06:00:00/07:00:00/08:00:00/09:00:00/10:00:00/11:00:00/12:00:00/13:00:00/14:00:00/15:00:00/16:00:00/17:00:00/18:00:00/19:00:00/20:00:00/21:00:00/22:00:00/23:00:00"
    
#Old formats
grid_old = f"{grid[0]}/{grid[1]}"

#===================================================================================
# Download data
#===================================================================================

if 'pressure_levels' in variables_cds.keys() and len(variables_cds['pressure_levels']) > 0:
    
    #Pressure levels
    c.retrieve('reanalysis-era5-pressure-levels', {
        'product_type': 'reanalysis',
        'variable': variables_cds['pressure_levels'],
        'pressure_level': [str(i) for i in variables_cds['pressure_levels_hpa']],
        'date': new_date,
        'time': reg_time,
        'format': 'netcdf',
        'area': area,
        'grid': grid,
    }, use_title+".nc")
    
if 'single_levels' in variables_cds.keys() and len(variables_cds['single_levels']) > 0:
    
    #Surface levels
    c.retrieve('reanalysis-era5-single-levels', {
        'product_type': 'reanalysis',
        'variable': variables_cds['single_levels'],
        'date': new_date,
        'time': reg_time,
        'format': 'netcdf',
        'area': area,
        'grid': grid,
    }, use_title+"_sfc.nc")
    
if 'param' in variables_pv.keys() and len(variables_pv['param']) > 0:

    #PV (2 PVU) from old MARS request
    c.retrieve('reanalysis-era5-complete', {
        "class": "ea",
        "dataset": "era5",
        "date": reg_date,
        "expver": "1",
        "levelist": '/'.join([str(i) for i in variables_pv['levels_pv']]),
        "levtype": "pv",
        "param": variables_pv['param'],
        "stream": "oper",
        "time": reg_time_old,
        "type": "an",
        "format": "netcdf",
        "grid": grid_old,
        "area": area_old,
    }, use_title+"_pv.nc")

if 'param' in variables_isentropic.keys() and len(variables_isentropic['param']) > 0:

    #Theta levels from old MARS request
    c.retrieve('reanalysis-era5-complete', {
        "class": "ea",
        "dataset": "era5",
        "date": reg_date,
        "expver": "1",
        "levelist": '/'.join([str(i) for i in variables_isentropic['levels_kelvin']]),
        "levtype": "pt",
        "param": variables_isentropic['param'],
        "stream": "oper",
        "time": reg_time_old,
        "type": "an",
        "format": "netcdf",
        "grid": grid_old,
        "area": area_old,
    }, use_title+"_isen.nc")
    
    #133.128 = q for isentropic level

