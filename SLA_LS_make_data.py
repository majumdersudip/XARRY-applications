#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 14:03:19 2019

@author: sudip
"""

import xarray as xr
import os
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

path0='/Volumes/CastelaoLAB/data/satellite/CMEMS/msla/twosat/'
datasets=[]

for ii in range(8):    
    path=path0+"{:02d}".format(ii+2010)
    os.chdir(path)
    ds = xr.open_mfdataset('dt_global_twosat_phy_l4*.nc',autoclose=True)
    lon_name = 'longitude'  # whatever name is in the data
        # Adjust lon values to make sure they are within (-180, 180)
    ds['_longitude_adjusted'] = xr.where(ds[lon_name] > 180, ds[lon_name] - 360, ds[lon_name])
        # reassign the new coords to as the main lon coords
        # and sort DataArray using new coordinate values
    ds = (ds.swap_dims({lon_name: '_longitude_adjusted'}).sel(**{'_longitude_adjusted': sorted(ds._longitude_adjusted)}).drop(lon_name))
    ds = ds.rename({'_longitude_adjusted': lon_name})
    df=ds.sel(latitude=slice(55,70),longitude=slice(-65,-35))
    outfi='/Users/sudip/Desktop/Research/UGA_research/data/'+'SLA_LS_'+"{:02d}".format(ii+2010)+'.nc'
    df.to_netcdf(path=outfi)
