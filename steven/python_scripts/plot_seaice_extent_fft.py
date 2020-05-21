#!/usr/bin/env python
# coding: utf-8

# In[1]:


# plot_seaice_extent_fft
#
# Steven Cavallo
# May 2020
#
###########################
# imports
###########################
import matplotlib.pyplot as plt
import numpy as np
import sys, imp
import pylab
import datetime as dt
from datetime import date
import os, datetime
import csv
from scipy.fftpack import fft
from scipy.signal import blackman, butter, lfilter, filtfilt, freqz, periodogram

import weather_modules as wm
import utilities_modules as um

#from mstats import *


# In[2]:


###########################
# User options
###########################
plot_variable = 'dextent_int' # 'extent','dextent', dextent_int, or dextent_diff
plot_spectrum = 'False' 
sum_ndays_post = 0 # Sums final values by the number of days set.  Set to 0 to ignore 
filter_option = 'mean_removed' # options are 'nearby', butterworth', 'mean_removed', and 'none'
number_days_dextent = 3 # 3 is default

years_filter = [1979,2019]

months_filter = [6,8]
#months_filter = [3,5]

dtUniqueCase = 1 # If set to 1, will not count back-to-back daily events as separate events
#percentiles = [25,75]
percentiles = [5,95]
#percentiles = [10,90]
#percentiles = [1,99]
#percentiles = [-0.125,-0.125]

write_events = 'True'
write_events_yearly = 'False'
fpath = '/Users/scavallo/Documents/data/NH_seaice_extent_nrt_1979_2019.csv'
fpath_climo = '/Users/scavallo/Documents/data/NH_seaice_daily_dextent_int_longtermmean_errorbars_1981_2010_3d_new2018.dat'
fpath_climo_monthly = '/Users/scavallo/Documents/data/NH_seaice_monthly_dextent_int_longtermmean_errorbars_1981_2010_3d_new2018.dat'
event_path_yearly = '/Users/scavallo/Documents/data/greatest_seaice_loss_annual_vsyear.dat'

event_path = '/Users/scavallo/Documents/data/seaice_loss/paper_data_1979_2019/rapid_seaice_loss_events_int_withboth_jja_meanremoved_3d_10percentile_dtUnique01.dat'
#event_path = '/Users/scavallo/Documents/data/seaice_loss/paper_data_1979_2019/rapid_seaice_loss_events_int_withboth_jja_meanremoved_3d_10percentile.dat'

label_fontsize = 16
imagedir = '/Users/scavallo/Documents/scripts/python_scripts/images/'

ylims = [-0.4, 0.4]
xlims = [0, 365]


# In[3]:


ab = np.loadtxt(fpath_climo_monthly, skiprows=0)       
#dextent_monthly_percentile = ab[:,9] # 10th percentile
dextent_monthly_percentile = ab[:,7]  # 5th percentile

ab = np.loadtxt(fpath_climo, skiprows=0)       
month_climo = ab[:,0]
day_climo = ab[:,1]
extent_climo = ab[:,2]
dextent_climo = ab[:,3]

if 1 == 1:
    file = open(fpath, 'r')
    data = np.loadtxt(file,skiprows=2, delimiter=',',usecols=(0,1,2,3))
    years = data[:,0].astype(int) #e.g., 1981
    months = data[:,1].astype(int) #e.g., 01
    days=data[:,2].astype(int) #e.g., 01
    extents = data[:,3] #e.g., 11.345 [10^6km^2]    
    
    #convert individual yr,month,day to time values
    nVals = len(extents)
    print(nVals)
    #timeList = [dt.datetime(years[i],months[i],days[i]) for i in xrange(nVals)]; timeList = np.array(timeList)
    timeList = [dt.datetime(years[i],months[i],days[i]) for i in range(nVals)]; timeList = np.array(timeList)
  
    #interpolate to uniform time grid ("daily" values early on are every 2 days)
    tStart = timeList[0]; tEnd = timeList[-1]
    nDays = (tEnd-tStart).total_seconds()/(24*3600); nDays = int(nDays)
    print('{0} days between {1} {2}'.format(nDays, tStart, tEnd))
    times = [tStart+ dt.timedelta(days=i) for i in range(0, nDays)]; times = np.array(times)
  
    dTime = [(a-timeList[0]).total_seconds() for a in timeList]
    dTimeResample = [(a-timeList[0]).total_seconds() for a in times]
    extents = np.interp(dTimeResample, dTime, extents)    
    
    del years, months, days
    years = [i.year for i in times]
    months = [i.month for i in times]
    days = [i.day for i in times]
    
    years = np.array(years)
    months = np.array(months)
    days = np.array(days)

    


# In[4]:


#[inds] = np.where(years==2007)
#[inds] = np.where( (years==2007) & ( (months == 7) | (months == 8) | (months == 9) ) )
#[inds] = np.where( years>1987 )
#[inds] = np.where(years<2016)
[inds] = np.where(years<=years_filter[1])

timefocus = times[inds]
yearfocus = years[inds]
monthfocus = months[inds]
dayfocus = days[inds]
extentfocus = extents[inds]

dextent = np.zeros_like(extentfocus).astype('f')
extent_ref = np.zeros_like(extentfocus).astype('f')
dextent_ref = np.zeros_like(extentfocus).astype('f')
dextent_percentile = np.zeros_like(extentfocus).astype('f')
z0 = np.zeros_like(extentfocus).astype('f')
#dextent[:] = float('NaN')

print(filter_option)
if filter_option == 'mean_removed':
    tt = 0
    while tt < len(dextent):
        mm = monthfocus[tt]
        dd = dayfocus[tt]
        
        [anomind] = np.where( (month_climo == np.int(mm)) & (day_climo == np.int(dd)))
        
        if (not anomind):
            anomind = 1
            extent_anom_now = float('NaN')
            extent_ref_now = float('NaN')
        else:    
            #dextent_anom_now = dextent_nofilt[tt] - dextent_climo[anomind]
            extent_anom_now = extentfocus[tt] - extent_climo[anomind]
            extent_ref_now = extentfocus[tt]
        
        extentfocus[tt] = extent_anom_now
        extent_ref[tt] = extent_ref_now
        
        dextent_percentile[tt] = dextent_monthly_percentile[mm-1]
        tt += 1
    
dextent[1:] = extentfocus[1:] - extentfocus[0:-1]
dextent_ref[1:] = extent_ref[1:] - extent_ref[0:-1]

if ( (plot_variable == 'dextent_int') or (plot_variable == 'mean_removed') ):
    ndays = number_days_dextent
    dextent_int = np.zeros_like(extentfocus).astype('f')
    dextent_ref_int = np.zeros_like(extentfocus).astype('f')
    #dextent_int[:] = float('NaN')
    #dextent_int[1:] = np.diff(extentfocus)
    for ii in range(ndays,len(dextent_int)):
        #print(ii-ndays+1,ii+1)
        #print(dextent[ii-ndays+1:ii+2],np.nansum(dextent[ii-ndays+1:ii+2]))
        sind = ii-ndays+1
        eind = sind+ndays
        dextent_int[ii] = np.nansum(dextent[sind:eind])
        #dextent_int[ii] = np.nansum(dextent[ii-ndays+1:ii+ndays])
        dextent_ref_int[ii] = np.nansum(dextent_ref[sind:eind])
        #dextent_ref_int[ii] = np.nansum(dextent[sind:eind])
        #print(dextent[sind:eind])
        #print(ii,sind,eind)
        
    dextent_int[0:ndays] = dextent_int[ndays]


if ( (plot_variable == 'dextent_diff') or (plot_variable == 'mean_removed') ):
    ndays = number_days_dextent
    dextent_int = np.zeros_like(extentfocus).astype('f')
    dextent_ref_int = np.zeros_like(extentfocus).astype('f')
    
    dextent_int[2:] = extentfocus[2:] - extentfocus[0:-2]
    dextent_int[0:2] = dextent_int[2]
    
    dextent_ref_int[2:] = extent_ref[2:] - extent_ref[0:-2]
    dextent_ref_int[0:2] = dextent_ref[2]    


#indfind = np.where(dextent == np.min(dextent))
#print "The largest decline is on %d/%d/%d of %2.5f" % (monthfocus[indfind], dayfocus[indfind], yearfocus[indfind],percent_change[indfind])

if ( np.size(dayfocus) < 367) :
    dayinds = np.where(dayfocus==1)
    dayplot = (dayfocus[dayinds])
else:
    dayinds = np.where( (monthfocus==1) & (dayfocus==15) )
    dayplot = (yearfocus[dayinds])
    xlims[1] = np.size(dextent)
#dayinds = np.arange(0,len(dayfocus),7)
#print years[dayinds]
#dayplot = (dayfocus[dayinds])  

#print dayplot
#print yearfocus[dayinds]
datesave = []
for ii in range(0,len(dayplot)):
    if ( np.size(dayfocus) < 367) :
        datenow = str(ii+1) + '/ 01'
    else:
        datenow = str(int(dayplot[ii])) 
        
    #datenow = str(int(monthfocus[dayinds[ii]])) + '/' + str(int(dayfocus[dayinds[ii]]))
    datesave.append(datenow)


# In[5]:


# Butterworth filter

if filter_option == 'butterworth':
    #butter_order = 3
    butter_order = 12
    sample_days = 1.0 # days
    lowcut_days = 18.0 # days
    
    #lowcut_days = 120.0
    highcut_days = 2.0 # days

    sample_rate = sample_days*24.0*3600.0 # convert to seconds
    lowcut = lowcut_days*24.0*3600.0 # convert to seconds
    highcut = highcut_days*24.0*3600.0 # convert to seconds

    sample_freq = 1.0/sample_rate
    lowcut_freq = 1.0/lowcut # convert to Hz
    highcut_freq = 1.0/highcut # convert to Hz
    nyq = 0.5*sample_freq


    lowcut = lowcut_freq/nyq
    highcut = highcut_freq/nyq

    #b, a = butter(3,[lowcut,highcut],btype='bandpass')
    #extent_bw = lfilter(b,a,extentfocus)

    b, a = butter(butter_order,lowcut,btype='highpass')
    #b, a = butter(butter_order,lowcut,btype='lowpass')

    
    if plot_variable == 'extent':
        datain = extentfocus
    if plot_variable == 'dextent':
        datain = dextent
    if plot_variable == 'dextent_int':
        datain = dextent_int
    if plot_variable == 'dextent_diff':
        datain = dextent_int        
        
    datain_unfiltered = datain
    datain_mean = np.nanmean(datain)
    #datain = (datain - datain_mean)
    #data_bw = lfilter(b,a,datain)
    data_bw = filtfilt(b,a,datain)
    if plot_variable == 'extent':
        data_bw = data_bw + datain_mean
        extent_bw = data_bw

        dextent_bw = np.zeros_like(extentfocus).astype('f')
        dextent_bw[1:] = extent_bw[1:] - extent_bw[0:-1]            
    if plot_variable == 'dextent':
        extent_bw = extentfocus
        dextent_bw = data_bw
    
        extent_bw = np.zeros_like(extentfocus).astype('f')
        extent_bw[0] = extentfocus[0]
        for ii in range(len(extent_bw)-1):
            extent_bw[ii+1] = extent_bw[ii] + dextent_bw[ii]
    if ( (plot_variable == 'dextent_int') or (plot_variable == 'dextent_diff' ) ):
        extent_bw = extentfocus
        dextent_bw = data_bw
    
        extent_bw = np.zeros_like(extentfocus).astype('f')
        #extent_bw[0] = extentfocus[180]
        extent_bw[0] = np.nanmean(extentfocus)
        for ii in range(len(extent_bw)-1):
            extent_bw[ii+1] = extent_bw[ii] + dextent_bw[ii]          
    
    cornow = np.corrcoef(dextent,dextent_bw)
    print("Correlation between raw and filtered time series is %5.2f" %(cornow[0,1]))
elif filter_option == 'nearby':
    sample_days = 1.0
    smoothing_days = 5.0
    
    npts_smooth = np.int(smoothing_days/sample_days)
    dextent_bw = np.zeros_like(extentfocus).astype('f')
    for ii in range(0,len(dextent)):
        if ii<npts_smooth:
            dextent_bw[ii] = dextent[ii]
        else:   
            dextent_bw[ii] = np.nanmean(dextent[ii-npts_smooth:ii])
    
    extent_bw = extentfocus
    
    #cornow = np.corrcoef(dextent,dextent_bw)
    #print "Correlation between raw and filtered time series is %5.2f" %(cornow[0,1])
elif filter_option == 'mean_removed':
    #datain_mean = np.nanmean(datain)
    #datain = (datain - datain_mean)  
    if plot_variable == 'extent':
        datain = extentfocus
    if plot_variable == 'dextent':
        datain = dextent
    if plot_variable == 'dextent_int':
        datain = dextent_int
    if plot_variable == 'dextent_diff':
        datain = dextent_int 
    datain_unfiltered = dextent_ref_int  
    extent_bw = extentfocus
    dextent_bw = datain
elif filter_option == 'none':
    if plot_variable == 'extent':
        datain = extentfocus
    if plot_variable == 'dextent':
        datain = dextent
    if plot_variable == 'dextent_int':
        datain = dextent_int
    if plot_variable == 'dextent_diff':
        datain = dextent_int 
    datain_unfiltered = datain    
    extent_bw = extentfocus
    dextent_bw = datain


if sum_ndays_post > 0:
    datanew = np.zeros_like(datain).astype('f')
    datanew_bw = np.zeros_like(dextent_bw).astype('f')

    for ii in range(sum_ndays_post,len(datanew)):
        #print(ii-ndays+1,ii+1)
        #print(dextent[ii-ndays+1:ii+2],np.nansum(dextent[ii-ndays+1:ii+2]))
        datanew[ii] = np.nansum(datain[ii-sum_ndays_post+1:ii+2])
        datanew_bw[ii] = np.nansum(dextent_bw[ii-sum_ndays_post+1:ii+2])
    datanew[0:sum_ndays_post] = datanew[sum_ndays_post]    
    datanew_bw[0:sum_ndays_post] = datanew_bw[sum_ndays_post] 
    
    del datain, dextent_bw
    datain = datanew
    dextent_bw = datanew_bw
    del datanew, datanew_bw
    
    #mstats(dextent_bw)
    #mstats(datain)    
    


diff_plot = dextent_bw - dextent

if 1 == 0:
    golden = (pylab.sqrt(5)+1.)/2.
    figprops = dict(figsize=(8., 8./ golden ), dpi=128)    # Figure properties for single and stacked plots
    adjustprops = dict(left=0.15, bottom=0.1, right=0.90, top=0.93, wspace=0.2, hspace=0.2) 

    fig = pylab.figure(**figprops)   # New figure
    ax1 = fig.add_subplot(1, 1, 1)
    w,h = freqz(b,a,worN=2000)
    fhat = (sample_freq*0.5/ np.pi)*w
    per = (1.0/fhat)/(24.0*3600.)
    p1 = ax1.plot(per,abs(h),label='Order = %d' % butter_order)
    ax1.set_xlim(0,50)
    plt.show()




# In[6]:


# FFT 
if plot_spectrum == 'True':
    if plot_variable == 'extent':
        dataspec_bw = extent_bw
        dataspec = datain_unfiltered
        time_step = 24.0*3600.0 # Sample spacing
    if plot_variable == 'dextent':    
        dataspec_bw = dextent_bw
        dataspec = datain_unfiltered
        time_step = 24.0*3600.0 # Sample spacing
    if ( (plot_variable == 'dextent_int') or (plot_variable == 'dextent_diff') ):    
        dataspec_bw = dextent_bw
        dataspec = datain_unfiltered    
        time_step = 24.0*3600.0 # Sample spacing
 

    N = np.size(dataspec) # Sample size
    N = np.int(N)
    w = blackman(N)
    
    #w[:] = 1.0
    
    sample_freq = 1/time_step
    
    datam = (dataspec - np.nanmean(dataspec)) / np.std(dataspec)
    #datam = dataspec
    datam_bw = (dataspec_bw - np.nanmean(dataspec_bw)) / np.std(dataspec_bw)
    
    yf = fft(datam*w)
    yf_bw = fft(datam_bw*w)
    yf_nowindow = fft(datam)
    ypow = np.abs(np.fft.rfft(datam*w))**2.0
    ypow_bw = np.abs(np.fft.rfft(datam_bw*w))**2.0
    ypow_nowind = np.abs(np.fft.rfft(datam))**2.0
    

    xf = np.linspace(0.0,1.0/(2.0*time_step),N/2)
    #xff = np.fft.rfftfreq(datam.size, d=time_step)
    #del xf
    #xf = xff[0:N/2]
    xt = (1.0/xf)/(3600.0*24.0) # Period in Days
    ##########################
    # Red noise spectrum
    ##########################
    if 1 == 0:
        rr = 0.5
        # Create a seris of gaussian-distributed random values from a unit normal
        wr = np.random.randn(N)
        # Initialize an output series
        xr = np.zeros(N)
        # Set the initial value of xr
        xr[0] = wr[0]
        # Populate xr with values tht have lag-1 autocorrelation rr
        sr = (1-rr**2)**0.5
        for ii in range(len(xr)-1):
            xr[ii+1] = rr*xr[ii] + sr*wr[ii+1]
        Nstar = N*(1-rr)/(1+rr)
        datared = (xr - np.nanmean(xr)) / np.std(xr)
        yf_red = fft(datared*w)
        ypow_red = np.abs(np.fft.fft(datared*w))**2    
    else:
        rr = 0.5
        conf = 95
        chunk_length = 2 # days
    
    
        rrr = um.autocorr(datam,2) 
        rr = rrr[1] # 1 time-step autocorrelation    
        print('The one time-step autocorrelation is %5.2f' %(rr))
        
        dof = (2*N)/chunk_length
        xr = np.zeros(N)
        N2 = np.int(N/2)
        for ii in range(N2+1):
            xr[ii] = (1.0-rr**2.0)/(1.0-2.0*rr*np.cos(np.pi*(ii-1.0)/np.float(N2))+rr**2.0)
        
        
        factor = np.sqrt(1.0-(rr**2.0))
        #ypow_red = np.abs(xr)**2.0
        ypow_red = xr
  

        f95 = [3.84,3.00,2.60,2.37,2.21,2.10,2.01,1.94,1.88,1.83,1.75,1.67,1.57,1.52,1.46,1.39,1.38,1.32,1.22,1.00]
        n95 = [1,2,3,4,5,6,7,8,9,10,12,15,20,24,30,40,50,60,120,1000000]
        f99 = [6.63,4.61,3.78,3,32,3.02,2.80,2.64,2.51,2.41,2.31,2.18,2.04,1.88,1.79,1.70,1.59,1.56,1.47,1.32,1.00]
        n99 = n95
        
        if conf==95:
            fstat = f95[-1]
            NF = np.size(f95)
            for ii in range(NF):
                if (dof <= n95[ii]):       
                    fstat = f95[ii-1]+(dof-n95[ii-1])*(f95[ii]-f95[ii-1])/(n95[ii]-n95[ii-1])
                    break   
        elif conf == 99:  
            fstat = f99[-1]
            NF = np.size(f99)
            for ii in range(NF):
                if (dof <= n99[ii]):        
                    fstat = f99[ii-1]+(dof-n99[ii-1])*(f99[ii]-f99[ii-1])/(n99[ii]-n99[ii-1])  
                    break
                 
        print(dof,fstat)    
        ypow_red_sig = fstat*ypow_red

if 1 == 0:
    tt = np.arange(0,len(datam),1)
    golden = (pylab.sqrt(5)+1.)/2.
    figprops = dict(figsize=(8., 8./ golden ), dpi=128)    # Figure properties for single and stacked plots
    adjustprops = dict(left=0.15, bottom=0.1, right=0.90, top=0.93, wspace=0.2, hspace=0.2) 
    fig = pylab.figure(**figprops)   # New figure
    ax1 = fig.add_subplot(1, 1, 1)
    p1 = ax1.plot(tt,datam,'b')
    p1 = ax1.plot(tt,datam*w,'r')
    plt.show()    
    


# In[7]:


t = np.arange(0,len(extentfocus),1)

#upper_lim = 99
#lower_lim = 1
upper_lim = percentiles[1]
lower_lim = percentiles[0]

if percentiles[0] == percentiles[1]:
    lq = percentiles[0]
    uq = percentiles[1]
    lq_bw = percentiles[0]
    uq_bw = percentiles[1]    
    
else:
    uq = np.nanpercentile(dextent, upper_lim)
    lq = np.nanpercentile(dextent, lower_lim)
    uq_bw = np.nanpercentile(dextent_bw, upper_lim)
    lq_bw = np.nanpercentile(dextent_bw, lower_lim)
    
uq_arr = np.zeros_like(dextent).astype('f')
lq_arr = np.zeros_like(dextent).astype('f')
uq_arr[:] = uq
lq_arr[:] = lq

if filter_option == 'mean_removed':
    lq_arr[:] = dextent_percentile
    uq_arr[:] = dextent_percentile

if percentiles[0] == percentiles[1]:
    uinds = np.where(dextent_ref_int<=lq) 
else:
    uinds = np.where(dextent<=lq)
N1 = len(uinds[0][:])


uq_arr_bw = np.zeros_like(dextent_bw).astype('f')
lq_arr_bw = np.zeros_like(dextent_bw).astype('f')
uq_arr_bw[:] = uq_bw
lq_arr_bw[:] = lq_bw

if percentiles[0] == percentiles[1]:
    uinds_bw = np.where(dextent_ref_int<=lq_bw)
else:
    uinds_bw = np.where(dextent_bw<=lq_bw)

N2 = len(uinds_bw[0][:])

print(lq_bw,uq_bw,lq,uq)


# In[8]:


if write_events_yearly == 'True':
    monthMin = months_filter[0]
    monthMax = months_filter[1]
    #monthMin = 6
    #monthMax = 8
    #dtUniqueCase=dt.timedelta(days=5)
    #monthMin = 1
    #monthMax = 12
    dtUniqueCase=dt.timedelta(days=0) 
    
    #candidate cases ------------------------
    vals = dextent_bw
    vals_nofilt = dextent
    thresh = 0.
    thresh_nofilt = 0.
    print(thresh, thresh_nofilt)
    print('{0}% threshold for dExtent: {1}'.format(lower_lim,thresh))
  
    caseDates = timefocus[vals<=thresh]
    caseVals = vals[vals<=thresh]
    #caseVals_nofilt = vals_nofilt[vals_nofilt<=thresh_nofilt]
    caseVals_nofilt = vals_nofilt[vals<=thresh]
    #print caseDates.tolist()
    ncandidates = np.size(caseDates)
    
  
    #filter candidate cases - season, too close in time,... ------------------------
    #get only w/in specified month range
    print('Limiting to months between: ', monthMin, monthMax)
    year1 = years_filter[0]
    year2 = years_filter[1]
    yearnow = year1
    caseDates_yearly = []
    caseVals_yearly = []
    caseVals_nofilt_yearly = []    
    while yearnow <= year2:
        casedate_now = []
        caseval_now = []
        for iCase in range(ncandidates-1):
            casenow = caseDates[iCase]
            casevalnow = caseVals[iCase]
            if ( (casenow.year == yearnow) and (casenow.month>=monthMin) and (casenow.month<=monthMax) ):
                casedate_now.append(casenow)
                caseval_now.append(casevalnow)
        
        [minind] = np.where(caseval_now==np.min(caseval_now))
        caseVals_yearly.append(caseval_now[minind])
        caseDates_yearly.append(casedate_now[minind])        
        
        yearnow += 1
    #print(caseDates_yearly)
    #print(caseVals_yearly)

    yearsprint = [i.year for i in caseDates_yearly]
    monthsprint = [i.month for i in caseDates_yearly]
    daysprint = [i.day for i in caseDates_yearly]
    
    datesprint = []
    for ii in range(0,len(yearsprint)):
        if monthsprint[ii] < 10:
            monthnow = '0' + str(monthsprint[ii])
        else:
            monthnow = str(monthsprint[ii])
        if daysprint[ii] < 10:
            daynow = '0' + str(daysprint[ii])
        else:
            daynow = str(daysprint[ii])            
        datenow = str(yearsprint[ii]) + monthnow + daynow + '00'
        datesprint.append(datenow)

    outfile = open(event_path_yearly,'w')
    wcount = 0
    for ii in range(0,len(caseDates_yearly)):
        print(caseVals_yearly[ii])
        outfile.write('%-10s %7.4f\n' % (datesprint[ii], caseVals_yearly[ii]))
        


# In[9]:


cornow = np.corrcoef(dextent,dextent_bw)
indfind = np.where(dextent == np.min(dextent))
indfind2 = np.where(dextent_bw == np.min(dextent_bw))
percent_change = (dextent / extentfocus)*100
percent_change2 = (dextent_bw / extentfocus)*100
#print "The largest decline is on %d/%d/%d of %2.5f" % (monthfocus[indfind], dayfocus[indfind], yearfocus[indfind],percent_change[indfind])
#print "The largest decline in filtered data is on %d/%d/%d of %2.5f" % (monthfocus[indfind2], dayfocus[indfind2], yearfocus[indfind2],percent_change2[indfind2])
print("Correlation between raw and filtered time series is %5.2f" %(cornow[0,1]))
print('Number of samples below lower threshold is %d for raw data and %d for filtered data' %(N1,N2))


# In[15]:


if write_events == 'True':
    monthMin = months_filter[0]
    monthMax = months_filter[1]
    #monthMin = 6
    #monthMax = 8
    #dtUniqueCase=dt.timedelta(days=5)
    #monthMin = 1
    #monthMax = 12
    #dtUniqueCase=dt.timedelta(days=0) 

    
    vals = dextent_bw
    vals_nofilt = datain_unfiltered #dextent # SMC
    #thresh = np.percentile(vals, lower_lim)
    #thresh_nofilt = np.percentile(vals_nofilt, lower_lim)
    thresh = lq_bw
    thresh_nofilt = lq
    
    if filter_option == 'mean_removed':
        thresh = 9999999.
        thresh_nofilt = 9999999.
    
    #thresh = 0.
    #thresh_nofilt = 0.
    print(thresh, thresh_nofilt)
    print('{0}% threshold for dExtent: {1}'.format(lower_lim,thresh))
  
    caseDates = timefocus[vals<=thresh]
    caseVals = vals[vals<=thresh]

    
    #caseDates_nofilt = timefocus[vals<=thresh_nofilt]
    caseDates_nofilt = timefocus[vals<=thresh]
    caseVals_nofilt = vals_nofilt[vals<=thresh]
    
 
    if filter_option == 'mean_removed':       
        caseThreshes = dextent_percentile[vals<=thresh]
        caseThreshes_nofilt = dextent_percentile[vals<=thresh]
    
    #print caseDates.tolist()
    ncandidates1 = np.size(caseDates)
    ncandidates1_nofilt = np.size(caseDates_nofilt)

    #filter candidate cases - season, too close in time,... ------------------------
    #get only w/in specified month range
    print('Limiting to months between: ', monthMin, monthMax)
    #caseDates = [t0 for t0 in caseDates if ((t0.month>=monthMin) and (t0.month<=monthMax)) ]
    #ncandidates2 = np.size(caseDates)
    print(ncandidates1,ncandidates1_nofilt)

    casedate_now = []
    caseval_now = []
    casedate_now_nofilt = []
    caseval_now_nofilt = [] 
    for iCase in range(ncandidates1-1):
        casenow = caseDates[iCase]
        casevalnow = caseVals[iCase]
        casenow_nofilt = caseDates_nofilt[iCase]
        casevalnow_nofilt = caseVals_nofilt[iCase]
        
        if filter_option == 'mean_removed':
            threshnow = caseThreshes[iCase]
            caseLogic = False
            
            #print('Casevalnow_nofilt is %5.2f and threshnow is %5.2f' %(casevalnow_nofilt, threshnow))
            if (casevalnow_nofilt <= threshnow):
                caseLogic = True
        else:
            caseLogic = True
                
        casenext = caseDates[iCase+1]
        
        
        #if ( (caseDates[iCase+1]-caseDates[iCase] > dtUniqueCase) and (casenow.month>=monthMin) and (casenow.month<=monthMax) and (caseLogic == True)):
        if (  (casenow.month>=monthMin) and (casenow.month<=monthMax) and (caseLogic == True)):
        #if ( (deltadaysnow > 1) and (casenow.month>=monthMin) and (casenow.month<=monthMax) and (caseLogic == True)): 
            
            casedate_now.append(casenow)
            caseval_now.append(casevalnow)
            casedate_now_nofilt.append(casenow_nofilt)
            caseval_now_nofilt.append(casevalnow_nofilt)
            

    ncandidates2 = np.size(casedate_now)
    ncandidates2_nofilt = np.size(casedate_now_nofilt)
    print(ncandidates1,ncandidates2)
    print(ncandidates1_nofilt,ncandidates2_nofilt)

    #take out dates w/ missing values
    validDates = []
    validVals = []
    ind = 0
    for t0 in casedate_now:
        #19870709 is first file in 1987
        if (t0<dt.datetime(1987,1,1) or t0>dt.datetime(1987,7,8) ):
            validDates.append(t0)
            validVals.append(caseval_now[ind])
        ind += 1    
    print('Kept {0}/{1} event dates not known to have missing sea ice values'.format(len(casedate_now),len(validDates)))

    validVals_nofilt = []
    validDates_nofilt = []
    ind = 0
    for t0 in casedate_now_nofilt:
        #19870709 is first file in 1987
        if (t0<dt.datetime(1987,1,1) or t0>dt.datetime(1987,7,8) ):
            validDates_nofilt.append(t0)
            validVals_nofilt.append(caseval_now_nofilt[ind])
        ind += 1    
    print('Kept {0}/{1} event dates not known to have missing sea ice values'.format(len(casedate_now),len(validDates)))    
    
    ncandidates_missingvalues = np.size(validDates)
    
    # Now need to check for back-to-back events
    if 1 == 1:
        validDates_check = []
        validVals_check = []
        validDates_nofilt_check = []
        validVals_nofilt_check = []
        
        count = 0
        for t0 in validDates:
            #print(count,len(validDates))
            if count < len(validDates)-1:
                casenow = validDates[count]
                casenext = validDates[count+1]
         
                aa = date(casenow.year,casenow.month,casenow.day)
                bb = date(casenext.year,casenext.month,casenext.day)
                deltadaysnow = (bb-aa).days
                #print(aa,bb,deltadaysnow,dtUniqueCase)
                
                if (int(deltadaysnow) > dtUniqueCase):
                    validDates_check.append(validDates[count])
                    validVals_check.append(validVals[count])
                    validDates_nofilt_check.append(validDates_nofilt[count])
                    validVals_nofilt_check.append(validVals_nofilt[count])
    
            if count == len(validDates)-1:
                del validDates, validDates_nofilt, validVals, validVals_nofilt
                validDates = validDates_check
                validDates_nofilt = validDates_nofilt_check
                validVals = validVals_check
                validVals_nofilt = validVals_nofilt_check
                
            count += 1
    
    ncandidates_final = np.size(validDates)
    ncandidates_final_nofilt = np.size(validDates_nofilt)
    
    
    print('Number of percentile candidates: %d' %(ncandidates1))
    print('After limiting by missing values: %d' %(ncandidates_missingvalues))
    print('After limiting by month range: %d' %(ncandidates2))
    print('After limiting by adjacent days: %d' %(ncandidates_final))
    #print('After limiting by days apart: %d' %(ncandidates3))
    

    yearsprint = [i.year for i in validDates]
    monthsprint = [i.month for i in validDates]
    daysprint = [i.day for i in validDates]
    
    datesprint = []
    for ii in range(0,len(yearsprint)):
        if monthsprint[ii] < 10:
            monthnow = '0' + str(monthsprint[ii])
        else:
            monthnow = str(monthsprint[ii])
        if daysprint[ii] < 10:
            daynow = '0' + str(daysprint[ii])
        else:
            daynow = str(daysprint[ii])            
        datenow = str(yearsprint[ii]) + monthnow + daynow + '00'
        datesprint.append(datenow)
    
    
    
    #print datesprint   
    outfile = open(event_path,'w')
    wcount = 0
    for ii in range(0,len(datesprint)):
        print(datesprint[ii],validVals[ii])
        outfile.write('%-10s %7.4f %7.4f\n' % (datesprint[ii], validVals[ii], validVals_nofilt[ii]))


# In[11]:


golden = (pylab.sqrt(5)+1.)/2.
figprops = dict(figsize=(8., 8./ golden ), dpi=128)    # Figure properties for single and stacked plots
adjustprops = dict(left=0.15, bottom=0.1, right=0.90, top=0.93, wspace=0.2, hspace=0.2) 
if ( np.size(dayfocus) < 367) :
    rotang = 45
else:
    rotang = 90


# In[12]:


cint1 = 1
yticks1 = np.arange(3,17+(cint1/2),cint1)

fig = pylab.figure(**figprops)   # New figure
ax1 = fig.add_subplot(1, 1, 1)

p1, = ax1.plot(t,extentfocus,'b',linewidth=3.0,label='Extent')
p2, = ax1.plot(t,extent_bw,'r',linewidth=2.0,label='Extent (filtered)')


p3, = ax1.plot(t,z0,'k',linewidth=2.0)


ax1.grid(True, linestyle='-')
ax1.set_ylabel(r'Extent ($\times 10^6$ km$^2$)',fontsize=label_fontsize)
ax1.set_xlabel('Day',fontsize=label_fontsize)

ax1.set_ylim(yticks1[0],yticks1[-1])
ax1.set_yticks(yticks1)
ax1.set_xticks(t[dayinds])
ax1.set_xticklabels(datesave,rotation=rotang,fontsize=14)

#xlims = ax1.get_xlim()
#if ( np.size(dayfocus) < 367) :
ax1.set_xlim(xlims[0],xlims[1])

#legend = ax1.legend(loc='upper left', shadow=True)
legend = ax1.legend(loc='lower left', shadow=True)
#save_name = imagedir + 'sea_ice_extent_noseasonal' + '.png'
save_name = imagedir + 'sea_ice_extent_raw' + '.png'
plt.savefig(save_name, bbox_inches='tight')
#plt.show()


# In[13]:





cint1 = 0.1
yticks1 = np.arange(ylims[0],ylims[1]+(cint1/2),cint1)
yticks2 = np.linspace(-4,4,len(yticks1))



fig = pylab.figure(**figprops)   # New figure
ax1 = fig.add_subplot(1, 1, 1)

p1, = ax1.plot(t,dextent,'b',linewidth=3.0,label='Change in extent')
p2, = ax1.plot(t,dextent_bw,'r',linewidth=1.0,label='Change in extent (filtered)')
#p2a, = ax1.plot(t,uq_arr,'0.3',linewidth=3.0,label='1st/99th percentile')
#p2b, = ax1.plot(t,lq_arr,'0.3',linewidth=3.0,label='5th percentile')
#p2a, = ax1.plot(t,uq_arr_bw,'0.6',linewidth=3.0,label='1st/99th percentile (filtered)')
p2b, = ax1.plot(t,lq_arr_bw,'0.6',linewidth=3.0,label='5th percentile')

p3, = ax1.plot(t,z0,'k',linewidth=2.0)


ax1.grid(True, linestyle='-')
ax1.set_ylabel(r'Change in extent ($\times 10^6$ km$^2$)',fontsize=label_fontsize)
ax1.set_xlabel('Day',fontsize=label_fontsize)

ax1.set_ylim(yticks1[0],yticks1[-1])
ax1.set_yticks(yticks1)
ax1.set_xticks(t[dayinds])
ax1.set_xticklabels(datesave,rotation=rotang,fontsize=14)

#xlims = ax1.get_xlim()
#if ( np.size(dayfocus) < 367) :
ax1.set_xlim(xlims[0],xlims[1])

legend = ax1.legend(loc='upper left', shadow=True)
#legend = ax2.legend(loc='upper right', shadow=True)
save_name = imagedir + 'sea_ice_extent_change_raw' + '.png'
plt.savefig(save_name, bbox_inches='tight')

if 1 == 1:
    fig = pylab.figure(**figprops)   # New figure  
    ax1 = fig.add_subplot(1, 1, 1)

    p1, = ax1.plot(t,diff_plot,'r',linewidth=3.0,label='Filtered minus raw change in extent')  
    p3, = ax1.plot(t,z0,'k',linewidth=2.0)
    
    ax1.grid(True, linestyle='-')
    ax1.set_ylabel(r'Difference in extent ($\times 10^6$ km$^2$)',fontsize=label_fontsize)
    ax1.set_xlabel('Day',fontsize=label_fontsize)

    ax1.set_ylim(yticks1[0],yticks1[-1]) 
    ax1.set_yticks(yticks1) 
    ax1.set_xticks(t[dayinds])
    ax1.set_xticklabels(datesave,rotation=rotang,fontsize=14)  
    ax1.set_xlim(xlims[0],xlims[1])
    
    legend = ax1.legend(loc='lower left', shadow=True)

if plot_spectrum == 'False':
    plt.show()


# In[14]:


if plot_spectrum == 'True':
    fig = pylab.figure(**figprops)   # New figure
    ax1 = fig.add_subplot(1, 1, 1)

    ypow_sig = np.zeros_like(ypow).astype('f')
    ypow_sig[:] = float('NaN')
    testval = 2.0/N*ypow
    #[inds] = np.where(testval>=ypow_red_sig)
    #ypow_sig[inds] = ypow[inds]
    
    #plt.semilogy(xt,2.0/N*np.abs(yf[0:N/2]))
    
    plt.plot(xt,2.0/N*np.abs(ypow[0:N/2]),'b',linewidth=3.0,label='FFT')
    plt.plot(xt[0:N/2],ypow_red[0:N/2],'r',linewidth=2.0,label='Red noise')
    plt.plot(xt[0:N/2],ypow_red_sig[0:N/2],'r--',linewidth=2.0,label='95% red noise')
    #plt.plot(xt[0:N/2],2.0/N*np.abs(ypow_sig[0:N/2]),'g',linewidth=2.0)
    
    #plt.plot(xt,2.0/N*np.abs(ypow_nowind[0:N/2]),'m',linewidth=1.0,label='FFT no window')
    #plt.plot(xt[0:N/2],2.0/N*np.abs(ypow_bw[0:N/2]),'m',linewidth=3.0,label='FFT (filtered)')
    #plt.plot(xf,2.0/N*np.abs(ypow[0:N/2]),'b',linewidth=3.0,label='FFT')
    #plt.plot(xf[0:N/2],ypow_red[0:N/2],'r',linewidth=3.0,label='Red noise')
    #plt.plot(xf[0:N/2],ypow_red_sig[0:N/2],'r--',linewidth=3.0,label='95% red noise')    
    
    ax1.grid(True, linestyle='-')
    if plot_variable == 'extent':
        ax1.set_xlim(0,400)
    if plot_variable == 'dextent':    
        ax1.set_xlim(0,100)
    #ax1.set_xlim(0,lowcut_days)
    
    #ax1.set_ylim(0,10)
    ax1.set_xlim(0,400)
    ax1.set_ylim(0,100)
    #ax1.set_xlim(0,800)    
    ax1.set_ylabel('Power spectral density',fontsize=label_fontsize)
    ax1.set_xlabel('Period (Number of days)',fontsize=label_fontsize)

    plt.show()


# In[ ]:





# In[ ]:




