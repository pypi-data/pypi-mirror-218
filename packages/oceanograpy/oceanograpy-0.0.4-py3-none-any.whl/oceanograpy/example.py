# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 17:09:09 2023

@author: anba
"""

from workhorse_adcp import workhorse_adcp as wh_adcp 
from seabird_ctd import seabird_ctd as sb_ctd 
import processing_tools as ptools 
from matplotlib_dhi import subplots 
import adcp_plot_tools

import matplotlib.pyplot as plt
import matplotlib as mpl

pt3_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Config\ROV_ADCP_20161_PT3.txt'
adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Raw\ADCP_24142_600kHz\ROV_ADCP_12102022\_RDI_005.000'



pt3_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\Fixed Stations\02_Fixed_Bottom_Current_Turbidity\02_FBCT2\01_ADCP_600kHz-24144\Config_File\FBCT02_P3_TEST_17112022.txt'
adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\Fixed Stations\02_Fixed_Bottom_Current_Turbidity\02_FBCT2\01_ADCP_600kHz-24144\Raw\FBCT2_Full_Download_17112022\FBCT2000.000'


adcp_data = wh_adcp(filepath = adcp_filepath, PT3_filepath = pt3_filepath, verbose = 1)



#%%

import adcp_plot_tools
import processing_tools as ptools
from matplotlib_dhi import subplots

import os


adcp_plot_tools.progressive_vector_plot(adcp_data)#, color_by , start_bin, end_bin, start_ensemble, end_ensemble, title)
fig,ax = adcp_plot_tools.error_velocity_plot(adcp_data)

fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'ECHO INTENSITY')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'CORRELATION MAGNITUDE')
fig,ax = adcp_plot_tools.four_beam_flood_plot(adcp_data,field = 'PERCENT GOOD')

fig,ax = adcp_plot_tools.single_beam_flood_plot(adcp_data,field = 'ECHO INTENSITY')
fig,ax = adcp_plot_tools.single_beam_flood_plot(adcp_data,field = 'CORRELATION MAGNITUDE')
fig,ax = adcp_plot_tools.single_beam_flood_plot(adcp_data,field = 'PERCENT GOOD')
#fig,ax = adcp_plot_tools.metadata_table(adcp_data)







#%% correlation magnitude plots 



#%% Auto QAQC








#%% Add position data 




