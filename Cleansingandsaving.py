# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:01:43 2020

@author: laura Gallardo & Camilo Menares

Reads, cleans and samples TOLOLO data 
Data --ozone only--for the period 2013-2020 were downloaded from http://ebas.nilu.no/
This set corresponds to hourly averaged values

Data (ozone, water vapor, radiation, wind, etc)for the period 1995-2013 
were obtained from the Chilean Meteorological Office
thanks to Dr. Carmen Vega (carmen.vega@dgac.gob.cl) and colleagues
"""



#Importing libraries

import pandas as pd              # Data structures
import matplotlib.pyplot as plt  # Plotting 
import os as os                  # Directory management    
import numpy as np               # Numerics   
import datetime
import info_Plotting  #Import key settings for the following graphs and data
# Libreria creada para definir las rutas y los string de los Modelos
from info_Plotting import FHIST
from info_Plotting import FSERIES




#Exploring EBAS data
# The following file was read using Readingandsaving.py
# It consists of a dataframe containg hourly values of ozone and the corresponding 
# standard deviation

# The ozone sensor is a refur-bished ozone photometer (Thermo Scientific, TE49c) since 2013
# see Anet et al, 2017 doi:10.5194/acp-17-6477-2017 for details, including
# https://acp.copernicus.org/articles/17/6477/2017/acp-17-6477-2017-supplement.pdf
# See https://assets.thermofisher.com/TFS-Assets/EPM/manuals/EPM-manual-Model%2049i.pdf
# 
#Thus 
# Response time: 20s with 10s lag
# Precision: 1ppbv
# Selectable Full Scale Range: 0.05--200 ppm or 0.1--400 mg/m^3
# Lower limit of detection: 1.0ppb (zero noise 0.5 ppb RMS)


# orig = os.getcwd() #Says where the file is
# fn=orig+'\\DATA\\'+'EBAS-O3H-2013-2019'
# df = pd.read_csv(fn) 
# df.rename(columns = {'Unnamed: 0':'Date'}, inplace = True)

# df_orig_ebas=df #Original EBAS data set

# # Plotting time series
# FSERIES('O3','EBAS',df,1) #PENDING TIME AXES

# #Creating histograms of data
# #FHIST(spec,dbname,df,Nbins, ext=None)
# FHIST('O3','EBAS',df,50) #PENDING Anchored text

# #These data ave been subject to evaluation we do not "clean"

# dfH_ebas=df

############################
#Exploring DMC data
# The following file was read using Readingandsaving.py
# It consists of a dataframe containg hourly values of ozone and the corresponding 
# standard deviation
orig = os.getcwd() #Says where the file is
#fn=orig+'/Data/'+'DMC-O3_RH_15m_dmc-1995-2012'  # cambiar fn linea inferior
fn=orig+'\\DATA\\'+'DMC-O3_RH_15m_dmc-1995-2012'  

df = pd.read_csv(fn,index_col=0,parse_dates=True) 
#df.rename(columns = {'Unnamed: 0':'Date'}, inplace = True)
df_orig_dmc=df  #Original time series, before cleansing


#Plotting time series

FSERIES('O3','DMC',df,1) #PENDING TIME AXES
# The ozone sensor was a TECO  49-003  analyzer, between 1995-2013
# see Anet et al, 2017 doi:10.5194/acp-17-6477-2017 for details
# https://www.eol.ucar.edu/instruments/thermo-environmental-instruments-model-49-ozone-analyzer
#Thus 
# Response time: 20s with 10s lag
# Precision: 1ppbv
# Selectable Full Scale Range: 0.05--200 ppm or 0.1--400 mg/m^3
# Lower limit of detection: 1.0ppb (zero noise 0.5 ppb RMS)
# Other measurement characteristics (comments on signal/noise, bias limits, etc)

#Removing values below detection limit or the assumed range of calibration, i.e. 5 ppbv

df.O3_ppbv[df.O3_ppbv <5] = np.nan

# # WARNING
# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#   df.O3_ppbv[df.O3_ppbv <5] = np.nan
# C:\Users\laura\Desktop\DataVis\TOLOLO\Cleansingandsaving.py:100: SettingWithCopyWarning: 
# A value is trying to be set on a copy of a slice from a DataFrame

#The time series evidences calibration spikes. In lack of the record of dates of calibration, 
# we remove values above 65 ppbv, considering the data distribution of EBAS hourly values

df.O3_ppbv[df.O3_ppbv > 200] = np.nan

FSERIES('O3','DMC',df,1) #PENDING TIME AXES


orig = os.getcwd() 

fn=orig+'\\DATA\\'+'DMC-O3_RH_15m_dmc-1995-2012_clear'
#fn=orig+'/Data/DMC-O3_RH_15m_dmc-1995-2012_clear'
df.to_csv(fn)


#Creating histograms of data
#FHIST(spec,dbname,df,Nbins, ext=None)
#FHIST('O3','DMC',df,50) #PENDING Anchored text




#Resamplig to hourly values and calculating the corresponding standard deviation

# dfH=df.resample('H').mean()
# dfstd=df.resample('H').std()
#ERROR: COMPLAINS
# C:\Users\laura\Desktop\DataVis\TOLOLO\Cleansingandsaving.py:100: SettingWithCopyWarning: 
# A value is trying to be set on a copy of a slice from a DataFrame

# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#   df.O3_ppbv[df.O3_ppbv > 68] = np.nan
# C:\Users\laura\anaconda3\lib\site-packages\numpy\lib\histograms.py:839: RuntimeWarning: invalid value encountered in greater_equal
#   keep = (tmp_a >= first_edge)
# C:\Users\laura\anaconda3\lib\site-packages\numpy\lib\histograms.py:840: RuntimeWarning: invalid value encountered in less_equal
#   keep &= (tmp_a <= last_edge)
# Traceback (most recent call last):

#   File "C:\Users\laura\Desktop\DataVis\TOLOLO\Cleansingandsaving.py", line 112, in <module>
#     dfH=df.resample('H').mean()

#   File "C:\Users\laura\anaconda3\lib\site-packages\pandas\core\generic.py", line 8115, in resample
#     level=level,

#   File "C:\Users\laura\anaconda3\lib\site-packages\pandas\core\resample.py", line 1270, in resample
#     return tg._get_resampler(obj, kind=kind)

#   File "C:\Users\laura\anaconda3\lib\site-packages\pandas\core\resample.py", line 1404, in _get_resampler
#     "Only valid with DatetimeIndex, "

# TypeError: Only valid with DatetimeIndex, TimedeltaIndex or PeriodIndex, but got an instance of 'RangeIndex'

#Creating data series of hourly ozone and corresponding standard deviation
