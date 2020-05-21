#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import os, datetime, pylab
import pylab as P
from scipy.signal import butter, lfilter, filtfilt

from mstats import *
import utilities_modules as um

print(mpl.__version__)


# In[2]:


fpath_list1 = '/Users/scavallo/Documents/data/seaice_loss/paper_data_1979_2019/rapid_seaice_loss_events_int_withboth_jja_bwfilter_3d_10percentile.dat'
#fpath_cases_vrile = '/Users/scavallo/Documents/data/seaice_loss/paper_data/rapid_seaice_loss_events_int_withboth_annual_meanremoved_3d_5percentile_dtUnique01.dat'
fpath_list2 = '/Users/scavallo/Documents/data/seaice_loss/paper_data_1979_2019/rapid_seaice_loss_events_int_withboth_jja_meanremoved_3d_10percentile.dat'

newfile_path = '/Users/scavallo/Documents/data/seaice_loss/paper_data_1979_2019/rapid_seaice_loss_events_int_withboth_jja_allvriles_3d_10percentile.dat'


# In[ ]:





# In[3]:


# read cases
print(fpath_list1)
aa = np.loadtxt(fpath_list1, skiprows=0)       
datelist_list1 = aa[:,0].astype(int)
dextent_in_list1 = aa[:,1]
dextent_in_nofilt_list1 = aa[:,2]

print(fpath_list2)
bb = np.loadtxt(fpath_list2, skiprows=0)       
datelist_list2 = bb[:,0].astype(int)
dextent_in_list2 = bb[:,1]
dextent_in_nofilt_list2 = bb[:,2]

test = list(set(datelist_list1).intersection(datelist_list2))


# These are the indices in datelist_list1 that also occur somewhere in datelist_list2
commondates = datelist_list1[np.nonzero(np.in1d(datelist_list1, datelist_list2))]
[inds] = np.nonzero(np.in1d(datelist_list1, datelist_list2))
#print(commondates)
#print(inds)
#print(datelist_list1[inds])

dumval = -9999
if 1 == 0:
    outfile = open(newfile_path,'w+')
    nvalues_file1 = len(datelist_list1)
    nvalues_file2 = len(datelist_list2)
    nvalues_total = nvalues_file1 + nvalues_file2
    nvalues_merged = nvalues_total - len(inds)
    datelist_merged = []
    values_nofilt_merged = []
    counter = 0
    indcounter = 0
    for ii in range(0,nvalues_total):
        #print(ii,nvalues_total)
        if ii < nvalues_file2:
            #print(datelist_list2[counter])
            outfile.write('%-10s %7.4f %7.4f\n' % (datelist_list2[counter], dumval, dextent_in_nofilt_list2[counter]))
            if ii == nvalues_file2-1:
                counter = -1
        else:  
            if indcounter < len(inds): 
                if counter != inds[indcounter]:
                    #print(datelist_list1[counter])
                    outfile.write('%-10s %7.4f %7.4f\n' % (datelist_list1[counter], dumval, dextent_in_nofilt_list1[counter]))
                else:
                    #print(counter,indcounter)
                    indcounter += 1
            else:
                outfile.write('%-10s %7.4f %7.4f\n' % (datelist_list1[counter], dumval, dextent_in_nofilt_list1[counter]))
        counter += 1


# In[4]:


# No filter
if 1 == 0:
    outfile = open(newfile_path,'w+')
    nvalues_file1 = len(datelist_list1)
    nvalues_file2 = len(datelist_list2)
    nvalues_total = nvalues_file1 + nvalues_file2
    nvalues_merged = nvalues_total - len(inds)
    datelist_merged = []
    values_nofilt_merged = []
    counter = 0
    indcounter = 0
    for ii in range(0,nvalues_file1):
        #print(ii,indcounter)
        #if ( (ii <= len(inds)) & (ii == inds[indcounter])):
        #    indcounter+=1
        #else:
        outfile.write('%-10s %7.4f %7.4f\n' % (datelist_list1[counter], dumval, dextent_in_nofilt_list1[counter]))
        counter+=1
    counter = 0
    for ii in range(0,nvalues_file2):
        outfile.write('%-10s %7.4f %7.4f\n' % (datelist_list2[counter], dumval, dextent_in_nofilt_list2[counter]))
        counter+=1


# In[5]:


# No repeated dates
if 1 == 1:
    outfile = open(newfile_path,'w+')
    nvalues_file1 = len(datelist_list1)
    nvalues_file2 = len(datelist_list2)
    nvalues_total = nvalues_file1 + nvalues_file2
    nvalues_merged = nvalues_total - len(inds)
    datelist_merged = []
    values_nofilt_merged = []
    counter = 0
    indcounter = 0

    datelist_list1_arr = np.array(datelist_list1).astype('i')
    datelist_list2_arr = np.array(datelist_list2).astype('i')
    
    
    datelist_combined = np.concatenate([datelist_list1_arr,datelist_list2_arr])
    datelist_out, indices = np.unique(datelist_combined , return_index=True)
    
    dextent_combined = np.concatenate([dextent_in_nofilt_list1,dextent_in_nofilt_list2])
    dextent_nofilt_combined = dextent_combined[indices]
    
    #datelist_union = np.union1d( datelist_list1_arr,datelist_list2_arr)
    
    counter = 0
    for ii in range(0,len(datelist_out)):
        outfile.write('%-10s %7.4f %7.4f\n' % (str(datelist_out[counter]), dumval, dextent_nofilt_combined[counter]))
        counter+=1


# In[ ]:




