# Sea ice calculations and plots

plot_seaice_extent_fft
    Use this script to make the VRILE files
    
	Plots (1) Raw and filterd sea ice extent as function of year since 1979,
		  (2) Raw and filterd Change in sea ice extent as function of year since 1979 with
		      percentiles overlaid
		  (3) Difference in extent from filtering
		  

plot_seaice_stats
	Plots (1) Number of events vs. year since 1979, 
          (2) Change in SIE distribution decadal comparison
          (3) Accumulated sea ice loss from events
          (4) Percent sea ice extent reduction for warm season
          (5) Sept 1 sea ice extent vs. Sept 1 without VRILE loss
	      (6) Number of events vs. month, 
	      (7) Average change in extent for all events and fractional area loss
	      (8) Average change in extent for all events vs. climatological loss

merge_lists
    Merges the sea ice loss files using the "mean removed" and "bwfitler" methods into a combined file called "allvriles"

print_VRILE_stats
    prints relevant VRILE stats in the format of the paper for quick translation

find_seaice_events
    Prints and plots the top sea ice events from an existing event file

compute_deltaseaice_longterm_means_v2
    Makes daily and monthly longterm climatologies of sea ice extent with errorbars
    
plot_seaice_extent_timeseries_notebook
	Plots average daily change in sea ice extent as a function of day of year

plot_spectra_nsidc
    Updated plots of spectra in sea ice extent, change in extent, red noise, and/or overlays with AO, NAO, PNA 

plot_fft_ao_nao_pna
	**OLD** plots spectrum of change in sea ice extent, and overlays with that of the AO, NAO, and PNA.  For new plots,
     use plot_spectra_nsidc
	

plot_seaice_stats_wrt_longtermmean


plot_seaice_geoph_timeseries
	Plots (1) Sept. min. sea ice extent vs. year and 2nd order fit
	      (2) Sept. min. sea ice extent standardized anomalies
	      (3) JJA 500 hPa geopotential heights vs. year and 2nd order fit
	      (4) JJA 500 hPa geopotential height standardized anomalies 
          
#   NSIDC sea ice extent:
#       ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data
#   NSIDC gridded concentrations:
#       ftp://sidads.colorado.edu/pub/DATASETS/NOAA/G02202_v2/north/
#   http://nsidc.org/data/G02202/versions/2#
#   https://climatedataguide.ucar.edu/search/node/sea%20ice
#   https://climatedataguide.ucar.edu/climate-data/sea-ice-concentration-data-overview-comparison-table-and-graphs
#   
#   NOAA/NSIDC: Concentration estimates are most reliable within the consolidated ice pack during cold, winter 
#   conditions (errors ~5-10%). The estimates are least reliable close to the ice edge and during melt conditions, 
#   where biases may be 20-30%. At any given location (grid cell) errors may be large (>50%) 
#   (https://climatedataguide.ucar.edu/climate-data/sea-ice-concentration-noaansidc-climate-data-record)

	      
