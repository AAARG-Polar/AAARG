#!/usr/bin/env python
# coding: utf-8

# In[1]:


# plot_seaice_stats_wrt_longtermmean
#
# Steven Cavallo
# May 2020
#######################################
import numpy as np
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import os, datetime, pylab
import pylab as P
from scipy.signal import butter, lfilter, filtfilt
from matplotlib.ticker import FormatStrFormatter


from mstats import *
import utilities_modules as um


# In[2]:


num_cases = 2
#fpath_cases = '/Users/scavallo/Documents/data/seaice_loss/5percentile_2017/rapid_seaice_loss_events_int_withboth_annual_bwfilter_3d.dat'
fpath_cases = '/Users/scavallo/Documents/data/seaice_loss/paper_data_1979_2019/rapid_seaice_loss_events_int_withboth_annual_bwfilter_3d_5percentile.dat'
fpath_cases2 = '/Users/scavallo/Documents/data/seaice_loss/paper_data_1979_2019/rapid_seaice_loss_events_int_withboth_annual_meanremoved_3d_5percentile.dat'
#fpath_cases = '/Users/scavallo/Documents/data/seaice_loss/5percentile_2017/rapid_seaice_loss_events_int_withboth_annual_3d.dat'
#fpath_cases = '/Users/scavallo/Documents/data/seaice_loss/1percentile/rapid_seaice_loss_events_int_withboth_annual_2d.dat'
fpath_climo = '/Users/scavallo/Documents/data/NH_seaice_daily_dextent_int_longtermmean_errorbars_1981_2010_3d.dat'
fpath_climo_monthly = '/Users/scavallo/Documents/data/NH_seaice_monthly_dextent_int_longtermmean_errorbars_1981_2010_3d.dat'
fpath_record_monthly = '/Users/scavallo/Documents/data/NH_seaice_monthly_dextent_int_longtermmean_errorbars_1979_2019_3d.dat'
fpath_recent_monthly = '/Users/scavallo/Documents/data/NH_seaice_monthly_dextent_int_longtermmean_errorbars_2010_2019_3d.dat'
#imagedir = '/Users/scavallo/Documents/Work/Research/Proposals/ONR_Polar_DRI_2017/presentations/golden_cases/images/'
#imagedir = '/Users/scavallo/Documents/Work/Research/Proposals/ONR_Polar_DRI_2017/presentations/images/'
#imagedir = '/Users/scavallo/Documents/Work/Research/Presentations/ONR_2016/images/'
#imagedir = '/Users/scavallo/Documents/Work/Research/Presentations/AMS_2017_polar/images/'
imagedir = '/Users/scavallo/Documents/scripts/python_scripts/images/'
#imagedir = '/Users/scavallo/Documents/Work/Research/Papers/Nature_geoscience_vRILE/images_working/'
plot_option = 1 # 1 for histogram, 2 for probability density function
npasses_smooth = 1
label_fontsize = 16
read_and_plot_errorbars = 'True'
bw_filt_climo = 'False'
figdescript = '5percentile'

labeltext_climo = r'$\Delta$SIE_climatology' # 1981-2010
labeltext_record = r'$\Delta$SIE$_{record}$' # 1979-2018
labeltext_meanplusbw = r'$\Delta$SIE$_{total}$'
labeltext_bw = r'$\Delta$SIE$_{bwfilt}$'
labeltext_friendly = r'$\Delta$SIE$_{VRILE}$'


# In[3]:


# read climo
#    Column 1 = month
#    Column 2 = day
#    Column 3 = Extent climatology (no filter)
#    Column 4 = dextent climatology (no filter)
#    Column 5 = Extent climatology (butterworth filter)
#    Column 6 = dextent climatology (butterworth filter)
ab = np.loadtxt(fpath_climo, skiprows=0)       
month_climo = ab[:,0]
day_climo = ab[:,1]
extent_climo = ab[:,2]
dextent_climo = ab[:,3]
if read_and_plot_errorbars == 'True':
    #dextent_climo_ll = ab[:,4]
    #dextent_climo_ul = ab[:,5]
    del ab
    ab = np.loadtxt(fpath_climo_monthly, skiprows=0)       
    month_climo_monthly = ab[:,0]
    extent_climo_monthly = ab[:,1]
    dextent_climo_monthly = ab[:,2]
    dextent_climo_monthly_ll_0 = ab[:,3]
    dextent_climo_monthly_ul_100 = ab[:,4]
    dextent_climo_monthly_ll_1 = ab[:,5]
    dextent_climo_monthly_ul_99 = ab[:,6]
    dextent_climo_monthly_ll_5 = ab[:,7]
    dextent_climo_monthly_ul_95 = ab[:,8]


# In[4]:


if read_and_plot_errorbars == 'True':
    del ab
    ab = np.loadtxt(fpath_record_monthly, skiprows=0)       
    month_record_monthly = ab[:,0]
    extent_record_monthly = ab[:,1]
    dextent_record_monthly = ab[:,2]
    dextent_record_monthly_ll_0 = ab[:,3]
    dextent_record_monthly_ul_100 = ab[:,4]
    dextent_record_monthly_ll_1 = ab[:,5]
    dextent_record_monthly_ul_99 = ab[:,6]
    dextent_record_monthly_ll_5 = ab[:,7]
    dextent_record_monthly_ul_95 = ab[:,8]
    
    del ab
    ab = np.loadtxt(fpath_recent_monthly, skiprows=0)       
    month_recent_monthly = ab[:,0]
    extent_recent_monthly = ab[:,1]
    dextent_recent_monthly = ab[:,2]
    dextent_recent_monthly_ll_0 = ab[:,3]
    dextent_recent_monthly_ul_100 = ab[:,4]
    dextent_recent_monthly_ll_1 = ab[:,5]
    dextent_recent_monthly_ul_99 = ab[:,6]
    dextent_recent_monthly_ll_5 = ab[:,7]
    dextent_recent_monthly_ul_95 = ab[:,8]


# In[5]:


# read cases
print(fpath_cases)
aa = np.loadtxt(fpath_cases, skiprows=0)       
datelist = aa[:,0]
dextent = aa[:,1]
dextent_nofilt = aa[:,2]

ncases = np.size(datelist)
print(ncases)
tt = 0

years_start = []
months_start = []
days_start = []
mmdd_start = []
dextent_anom = []
while tt < ncases:

    datestrinit = str(datelist[tt])	
    yyyy = datestrinit[0:4]
    mm = datestrinit[4:6]
    dd = datestrinit[6:8]
    hh = datestrinit[8:10]
    mmdd = datestrinit[4:8]
    
    years_start.append(yyyy)
    months_start.append(mm)
    days_start.append(dd)
    mmdd_start.append(mmdd)
    
    [anomind] = np.where( (month_climo == np.int(mm)) & (day_climo == np.int(dd)))
    #numinds = np.size(anomind)
    #print(anomind)
    if (not anomind):
        anomind = 1
        dextent_anom_now = float('NaN')
    else:    
        #dextent_anom_now = dextent_nofilt[tt] - dextent_climo[anomind]
        dextent_anom_now = dextent[tt] - dextent_climo[anomind]
    dextent_anom.append(dextent_anom_now)
    
       
    tt += 1

dextent_anom = np.array(dextent_anom).astype(np.float)

if num_cases == 2:
    print(fpath_cases2)
    aa = np.loadtxt(fpath_cases2, skiprows=0)       
    datelist_case2 = aa[:,0]
    dextent_case2 = aa[:,1]
    dextent_nofilt_case2 = aa[:,2]

    ncases_case2 = np.size(datelist_case2)
    print(ncases_case2)
    tt = 0

    years_start_case2 = []
    months_start_case2 = []
    days_start_case2 = []
    mmdd_start_case2 = []
    dextent_anom_case2 = []
    while tt < ncases_case2:

        datestrinit = str(datelist_case2[tt])	
        yyyy = datestrinit[0:4]
        mm = datestrinit[4:6]
        dd = datestrinit[6:8]
        hh = datestrinit[8:10]
        mmdd = datestrinit[4:8]
    
        years_start_case2.append(yyyy)
        months_start_case2.append(mm)
        days_start_case2.append(dd)
        mmdd_start_case2.append(mmdd)
    
        [anomind] = np.where( (month_climo == np.int(mm)) & (day_climo == np.int(dd)))
        #numinds = np.size(anomind)
        #print(anomind)
        if (not anomind):
            anomind = 1
            dextent_anom_now = float('NaN')
        else:    
            #dextent_anom_now = dextent_nofilt[tt] - dextent_climo[anomind]
            dextent_anom_now = dextent_case2[tt] - dextent_climo[anomind]
        dextent_anom_case2.append(dextent_anom_now)
    
       
        tt += 1

    dextent_anom_case2 = np.array(dextent_anom_case2).astype(np.float)


# In[6]:


month_start_inds = np.array([0,31,60,91,121,152,182,213,244,274,305,335])
ndays_month =      np.array([31,29,31,30,31,30,31,31,30,31,30,31])
month_end_inds = month_start_inds + ndays_month


# In[7]:


years_plot = np.array(years_start)
months_plot = np.array(months_start).astype(int)
days_plot = np.array(days_start)
mmdd_plot = np.array(mmdd_start)

#month_start_inds = np.array([0,31,60,91,121,152,182,213,244,274,305,335])
#ndays_month =      np.array([31,29,31,30,31,30,31,31,30,31,30,31])
#month_end_inds = month_start_inds + ndays_month

dextent_months = np.zeros(len(ndays_month))
dextent_months_nofilt = np.zeros(len(ndays_month))
dextent_months_nofilt_ul = np.zeros(len(ndays_month))
dextent_months_nofilt_ll = np.zeros(len(ndays_month))
dextent_months_ul = np.zeros(len(ndays_month))
dextent_months_ll = np.zeros(len(ndays_month))
dextent_months_anom = np.zeros(len(ndays_month))
dextent_months_anom_ul = np.zeros(len(ndays_month))
dextent_months_anom_ll = np.zeros(len(ndays_month))
ul = 0
ll = 100
for tt in range(1,13):
    [inds3] = np.where(months_plot == tt)
    dextent_months[tt-1] = np.nanmean(dextent[inds3])
    dextent_months_nofilt[tt-1] = np.nanmean(dextent_nofilt[inds3])
    try:
        dextent_months_ll[tt-1] = np.percentile(dextent[inds3], ll)
        dextent_months_ul[tt-1] = np.percentile(dextent[inds3], ul)    
        dextent_months_nofilt_ll[tt-1] = np.percentile(dextent_nofilt[inds3], ll)
        dextent_months_nofilt_ul[tt-1] = np.percentile(dextent_nofilt[inds3], ul)           
    except:
        dextent_months_ll[tt-1] = float('NaN')
        dextent_months_ul[tt-1] = float('NaN')
        dextent_months_nofilt_ll[tt-1] = float('NaN')
        dextent_months_nofilt_ul[tt-1] = float('NaN')        
    dextent_months_anom[tt-1] = np.nanmean(dextent_anom[inds3])
    try:
        dextent_months_anom_ll[tt-1] = np.percentile(dextent_anom[inds3], ll)
        dextent_months_anom_ul[tt-1] = np.percentile(dextent_anom[inds3], ul)
    except:
        dextent_months_anom_ll[tt-1] = float('NaN')
        dextent_months_anom_ul[tt-1] = float('NaN')
    #dextent_months_anom_ll[tt-1] = np.min(dextent_anom[inds3])
    #dextent_months_anom_ul[tt-1] = np.max(dextent_anom[inds3])

#perc_area = np.abs(dextent_months/extent_monthly_climo)

dextent_months_climo = np.zeros(len(ndays_month))
dextent_months_climo_ul = np.zeros(len(ndays_month))
dextent_months_climo_ll = np.zeros(len(ndays_month))
ul = 0
ll = 100
for tt in range(1,13):
    [inds3] = np.where(month_climo == tt)
    #print(tt)
    #print(tt)
    #mstats(dextent_climo[inds3])
    dextent_months_climo[tt-1] = np.nanmean(dextent_climo[inds3])
    dextent_months_climo_ll[tt-1] = np.percentile(dextent_climo[inds3], ll)
    dextent_months_climo_ul[tt-1] = np.percentile(dextent_climo[inds3], ul)



        


# In[8]:


if num_cases == 2:
    years_plot_case2 = np.array(years_start_case2)
    months_plot_case2 = np.array(months_start_case2).astype(int)
    days_plot_case2 = np.array(days_start_case2)
    mmdd_plot_case2 = np.array(mmdd_start_case2)



    dextent_months_case2 = np.zeros(len(ndays_month))
    dextent_months_nofilt_case2 = np.zeros(len(ndays_month))
    dextent_months_nofilt_ul_case2 = np.zeros(len(ndays_month))
    dextent_months_nofilt_ll_case2 = np.zeros(len(ndays_month))
    dextent_months_ul_case2 = np.zeros(len(ndays_month))
    dextent_months_ll_case2 = np.zeros(len(ndays_month))
    dextent_months_anom_case2 = np.zeros(len(ndays_month))
    dextent_months_anom_ul_case2 = np.zeros(len(ndays_month))
    dextent_months_anom_ll_case2 = np.zeros(len(ndays_month))
    ul = 0
    ll = 100
    for tt in range(1,13):
        [inds3] = np.where(months_plot_case2 == tt)
        dextent_months_case2[tt-1] = np.nanmean(dextent_case2[inds3])
        dextent_months_nofilt_case2[tt-1] = np.nanmean(dextent_nofilt_case2[inds3])
        try:
            dextent_months_ll_case2[tt-1] = np.percentile(dextent_case2[inds3], ll)
            dextent_months_ul_case2[tt-1] = np.percentile(dextent_case2[inds3], ul)    
            dextent_months_nofilt_ll_case2[tt-1] = np.percentile(dextent_nofilt_case2[inds3], ll)
            dextent_months_nofilt_ul_case2[tt-1] = np.percentile(dextent_nofilt_case2[inds3], ul)           
        except:
            dextent_months_ll_case2[tt-1] = float('NaN')
            dextent_months_ul_case2[tt-1] = float('NaN')
            dextent_months_nofilt_ll_case2[tt-1] = float('NaN')
            dextent_months_nofilt_ul_case2[tt-1] = float('NaN')        
        dextent_months_anom_case2[tt-1] = np.nanmean(dextent_anom_case2[inds3])
        try:
            dextent_months_anom_ll_case2[tt-1] = np.percentile(dextent_anom_case2[inds3], ll)
            dextent_months_anom_ul_case2[tt-1] = np.percentile(dextent_anom_case2[inds3], ul)
        except:
            dextent_months_anom_ll_case2[tt-1] = float('NaN')
            dextent_months_anom_ul_case2[tt-1] = float('NaN')
 


# In[9]:


[minds] = np.where( (months_plot==6) | (months_plot==7)| (months_plot==8))
years_jja = years_plot[minds]
month_list =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

if plot_option == 1:
   alphaval = 0.75
   normval = 0
   leg_loc = 'upper right'
elif plot_option == 2:
   alphaval = 0.0
   normval = 1
   leg_loc = 'lower left'

yearbins = np.arange(1979,2016,1)
monthbins = np.arange(1,13.5,1)


# In[10]:


golden = (pylab.sqrt(5)+1.)/2.
figprops = dict(figsize=(8., 8./ golden ), dpi=128)    
adjustprops = dict(left=0.15, bottom=0.1, right=0.90, top=0.93, wspace=0.2, hspace=0.2) 
#############################################


# In[11]:


binvals = np.arange(1,13)
#bincenters = (binvals[0:-1]+binvals[1:])/2.0
bincenters = np.zeros(len(binvals))
bincenters[0:-1] = 0.5*(binvals[1:]+binvals[:-1])
bincenters[-1] = bincenters[-2]+1.0

yticks1 = [-0.5,-0.4,-0.3, -0.2,-0.1,   0, 0.1]
#yticks1 = [-0.4,-0.3, -0.2,-0.1,   0, 0.1,0.2,0.3,0.4]
yticks2 = [-0.03,-0.02,-0.01,   0,0.01,0.02,0.03]
#yticks2 = [   0, 0.01,0.02,0.03,0.04]

#testerr = np.zeros(len(binvals))
#testerr[:] = 0.1
upper_err = dextent_months_ul - dextent_months
lower_err = dextent_months - dextent_months_ll
upper_err_anom = dextent_months_anom_ul - dextent_months_anom
lower_err_anom = dextent_months_anom - dextent_months_anom_ll

upper_err_nofilt = dextent_months_nofilt_ul - dextent_months_nofilt
lower_err_nofilt = dextent_months_nofilt - dextent_months_nofilt_ll

if num_cases == 2:
    upper_err_nofilt_case2 = dextent_months_nofilt_ul_case2 - dextent_months_nofilt_case2
    lower_err_nofilt_case2 = dextent_months_nofilt_case2 - dextent_months_nofilt_ll_case2

fig = plt.figure(**figprops)   # New figure
ax1 = fig.add_subplot(1, 1, 1)
#ax2 = ax1.twinx()

binshift = 0.1
rotang = 90
z0 = np.zeros_like(binvals).astype('f')
p1, = ax1.plot(binvals, dextent_months,'b',linewidth=3.0,label=r'$\Delta$Extent from events')
ax1.errorbar(binvals, dextent_months,yerr=[lower_err,upper_err], fmt='bo',ecolor='b', elinewidth=8)
p2, = ax1.plot(binvals+binshift, dextent_months_anom,'r',linewidth=3.0,label=r'$\Delta$Extent anomaly from events')
ax1.errorbar(binvals+binshift, dextent_months_anom,yerr=[lower_err_anom,upper_err_anom], fmt='ro',ecolor='r', elinewidth=8)
p3, = ax1.plot(binvals,z0,'k',linewidth=2.0)
#p4, = ax2.plot(binvals,perc_area,'r',linewidth=3.0,label='Fractional area loss')    
    
ax1.grid(True, linestyle='-')
legend = ax1.legend(loc='lower left', shadow=True, fontsize=label_fontsize)
#legend = ax2.legend(loc='center right', shadow=True, fontsize=label_fontsize)
#plt.title(titletext1,fontsize=label_fontsize)


ax1.set_xticks(binvals)
ax1.set_xticklabels(month_list,rotation=rotang,fontsize=label_fontsize)

ax1.set_yticks(yticks1)
ax1.set_yticklabels(yticks1,fontsize=label_fontsize)
#ax2.set_yticks(yticks2)
#ax2.set_yticklabels(yticks2)

plt.xlim([binvals[0]-(2*binshift),binvals[-1]+(2*binshift)])
plt.ylim([yticks1[0],yticks1[-1]])

ax1.set_ylabel(r'$\Delta$Extent ($\times 10^6$ km$^2$)',fontsize=label_fontsize)
#ax2.set_ylabel('Fraction',fontsize=label_fontsize)
figname_suffix = 'values'
ax1.set_xlabel('Month',fontsize=label_fontsize)
save_name = 'seaiceloss_' + figdescript + '_dextents_errorbars_' + figname_suffix + '.png'
plt.savefig(imagedir + save_name, bbox_inches='tight')
#plt.show()


# In[12]:


yticks1 = [-0.5,-0.4,-0.3, -0.2,-0.1,   0, 0.1, 0.2]
yticks2 = yticks1
#yticks1 = [-0.4,-0.3, -0.2,-0.1,   0, 0.1,0.2,0.3,0.4]
#yticks2 = [-0.03,-0.02,-0.01,   0,0.01,0.02,0.03]
#yticks2 = [   0, 0.01,0.02,0.03,0.04]

#testerr = np.zeros(len(binvals))
#testerr[:] = 0.1
upper_err = dextent_months_ul - dextent_months
lower_err = dextent_months - dextent_months_ll
upper_err_anom = dextent_months_climo_ul - dextent_months_climo
lower_err_anom = dextent_months_climo - dextent_months_climo_ll

fig = plt.figure(**figprops)   # New figure
ax1 = fig.add_subplot(1, 1, 1)
#ax2 = ax1.twinx()

binshift = 0.1
rotang = 90
z0 = np.zeros_like(binvals).astype('f')
p1, = ax1.plot(binvals, dextent_months,'b',linewidth=3.0,label=r'$\Delta$Extent from events')
ax1.errorbar(binvals, dextent_months,yerr=[lower_err,upper_err], fmt='bo',ecolor='b', elinewidth=8)
p2, = ax1.plot(binvals+binshift, dextent_months_climo,'r',linewidth=3.0,label=r'$\Delta$Extent climatology')
ax1.errorbar(binvals+binshift, dextent_months_climo,yerr=[lower_err_anom,upper_err_anom], fmt='ro',ecolor='r', elinewidth=8)
p3, = ax1.plot(binvals,z0,'k',linewidth=2.0)
#p4, = ax2.plot(binvals,perc_area,'r',linewidth=3.0,label='Fractional area loss')    
    
ax1.grid(True, linestyle='-')
legend = ax1.legend(loc='lower left', shadow=True, fontsize=label_fontsize)
#legend = ax2.legend(loc='center right', shadow=True, fontsize=label_fontsize)
#plt.title(titletext1,fontsize=label_fontsize)



ax1.set_xticks(binvals)
ax1.set_xticklabels(month_list,rotation=rotang,fontsize=label_fontsize)

ax1.set_yticks(yticks1)
ax1.set_yticklabels(yticks1,fontsize=label_fontsize)
#ax2.set_yticks(yticks2)
#ax2.set_yticklabels(yticks2)

plt.xlim([binvals[0]-(2*binshift),binvals[-1]+(2*binshift)])
plt.ylim([yticks1[0],yticks1[-1]])

ax1.set_ylabel(r'$\Delta$Extent ($\times 10^6$ km$^2$)',fontsize=label_fontsize)
#ax2.set_ylabel('Fraction',fontsize=label_fontsize)
figname_suffix = 'values'
ax1.set_xlabel('Month',fontsize=label_fontsize)
save_name = 'seaiceloss_' + figdescript + '_dextents_withclimo_errorbars1_' + figname_suffix + '.png'
plt.savefig(imagedir + save_name, bbox_inches='tight')
if (read_and_plot_errorbars == 'False'):
    plt.show()


# In[13]:


if (read_and_plot_errorbars == 'True'):
    #yticks1 = [-0.5,-0.4,-0.3, -0.2,-0.1,   0, 0.1, 0.2]
    #yticks1 = [-0.6,-0.5,-0.4,-0.3, -0.2,-0.1,   0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    yticks1 = np.arange(-0.9,1.0,0.1)
    print(yticks1)
    [ytind] = np.where(np.abs(yticks1)<0.001)
    yticks1[ytind] = 0.0
    yticks2 = yticks1


    upper_err = dextent_months_ul - dextent_months
    lower_err = dextent_months - dextent_months_ll
    upper_err_anom = dextent_climo_monthly_ul_100   - dextent_climo_monthly # SMC
    lower_err_anom = dextent_climo_monthly - dextent_climo_monthly_ll_0 
    #upper_err_anom = dextent_months_climo_ul - dextent_climo_monthly
    #lower_err_anom = dextent_climo_monthly - dextent_months_climo_ll 
    
    fig = plt.figure(**figprops)   # New figure
    ax1 = fig.add_subplot(1, 1, 1)
    #ax2 = ax1.twinx()

    binshift = 0.2
    rotang = 90
    elinew = 8
    z0 = np.zeros_like(binvals).astype('f')
    #p1, = ax1.plot(binvals, dextent_months,'b',linewidth=3.0,label=r'$\Delta$Extent from events')
    #ax1.errorbar(binvals, dextent_months,yerr=[lower_err,upper_err], fmt='bo',ecolor='b', elinewidth=8)

    p2, = ax1.plot(binvals+binshift, dextent_climo_monthly,'0.33',linewidth=4.0,label=labeltext_climo)
    ax1.errorbar(binvals+binshift, dextent_climo_monthly,yerr=[lower_err_anom,upper_err_anom], fmt='ko',ecolor='0.33', elinewidth=elinew,marker='o',markerfacecolor='0.5',markeredgewidth=2,markeredgecolor='k')
    #p3, = ax1.plot(binvals,z0,'k',linewidth=2.0)
    plt.axhline(linewidth=3, color='k')

    if 1 == 0:
    #if num_cases == 2:
        p1b, = ax1.plot(binvals-binshift, dextent_months_nofilt_case2,'r-',linewidth=4.0,label=labeltext_meanplusbw)
        ax1.errorbar(binvals-binshift, dextent_months_nofilt_case2,yerr=[lower_err_nofilt_case2,upper_err_nofilt_case2], fmt='ko',ecolor='r', elinewidth=elinew,marker='o',markerfacecolor='r',markeredgewidth=2,markeredgecolor='k')    

    # SMC now
    p1a, = ax1.plot(binvals, dextent_months_nofilt,'b-',linewidth=4.0,label=labeltext_bw)
    #p1a, = ax1.plot(binvals, dextent_months_nofilt,'b-',linewidth=4.0,label=labeltext_friendly)
    ax1.errorbar(binvals, dextent_months_nofilt,yerr=[lower_err_nofilt,upper_err_nofilt], fmt='ko',ecolor='b', elinewidth=elinew,marker='o',markerfacecolor='b',markeredgewidth=2,markeredgecolor='k')
       
    

    
    ax1.grid(True, linestyle='-')
    #legend = ax1.legend(loc='lower left', shadow=True, fontsize=label_fontsize)
    legend = ax1.legend(loc='upper center', shadow=True, fontsize=label_fontsize-1)
    #plt.title(titletext1,fontsize=label_fontsize)

    #um.label_options(ax1,fontsize=label_fontsize,xaxis_opt=False,yaxis_opt=True,bold_opt=False)

    ax1.set_xticks(binvals)
    ax1.set_xticklabels(month_list,rotation=rotang,fontsize=label_fontsize)

    ax1.set_yticks(yticks1[::2])
    ax1.set_yticklabels((yticks1[::2]),fontsize=label_fontsize)
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    #ax2.set_yticks(yticks2)
    #ax2.set_yticklabels(yticks2)

    plt.xlim([binvals[0]-(2*binshift),binvals[-1]+(2*binshift)])
    plt.ylim([yticks1[0],yticks1[-1]])

    ax1.set_ylabel(r'$\Delta$SIE ($\times 10^6$ km$^2$)',fontsize=label_fontsize)
    #ax2.set_ylabel('Fraction',fontsize=label_fontsize)
    figname_suffix = 'values'
    ax1.set_xlabel('Month',fontsize=label_fontsize)
    save_name = 'seaiceloss_' + figdescript + '_dextents_withclimo_errorbars2_' + figname_suffix + '.png'
    plt.savefig(imagedir + save_name, bbox_inches='tight')
    #plt.show()


# In[14]:


upper_err_record_anom = dextent_record_monthly_ul_100   - dextent_record_monthly # SMC
lower_err_record_anom = dextent_record_monthly - dextent_record_monthly_ll_0 

upper_err_recent_anom = dextent_recent_monthly_ul_100   - dextent_recent_monthly # SMC
lower_err_recent_anom = dextent_recent_monthly - dextent_recent_monthly_ll_0 

fig = plt.figure(**figprops)   # New figure
ax1 = fig.add_subplot(1, 1, 1)
#ax2 = ax1.twinx()

binshift = 0.0
rotang = 90
elinew = 8
z0 = np.zeros_like(binvals).astype('f')

p2, = ax1.plot(binvals+binshift, dextent_record_monthly,'0.67',linewidth=4.0,label=labeltext_record)
ax1.errorbar(binvals+binshift, dextent_record_monthly,yerr=[lower_err_record_anom,upper_err_record_anom], fmt='ko',ecolor='0.67', elinewidth=elinew,marker='o',markerfacecolor='0.5',markeredgewidth=2,markeredgecolor='k')
#ax1.errorbar(binvals+binshift, dextent_recent_monthly,yerr=[lower_err_recent_anom,upper_err_recent_anom], fmt='ko',ecolor='r', elinewidth=elinew,marker='o',markerfacecolor='r',markeredgewidth=2,markeredgecolor='k')

#p3, = ax1.plot(binvals,z0,'k',linewidth=2.0)
plt.axhline(linewidth=3, color='k')   
ax1.grid(True, linestyle='-')

legend = ax1.legend(loc='upper center', shadow=True, fontsize=label_fontsize-1)
#plt.title(titletext1,fontsize=label_fontsize)

#um.label_options(ax1,fontsize=label_fontsize,xaxis_opt=False,yaxis_opt=True,bold_opt=False)

ax1.set_xticks(binvals)
ax1.set_xticklabels(month_list,rotation=rotang,fontsize=label_fontsize)

ax1.set_yticks(yticks1[::2])
ax1.set_yticklabels(yticks1[::2],fontsize=label_fontsize)

plt.xlim([binvals[0]-(2*binshift),binvals[-1]+(2*binshift)])
plt.ylim([yticks1[0],yticks1[-1]])

ax1.set_ylabel(r'$\Delta$SIE ($\times 10^6$ km$^2$)',fontsize=label_fontsize)
#ax2.set_ylabel('Fraction',fontsize=label_fontsize)
figname_suffix = 'values'
ax1.set_xlabel('Month',fontsize=label_fontsize)
save_name = 'seaiceloss_3day_dextents_climo_monthly_' + figname_suffix + '.png'
plt.savefig(imagedir + save_name, bbox_inches='tight')
plt.show()


# In[ ]:




