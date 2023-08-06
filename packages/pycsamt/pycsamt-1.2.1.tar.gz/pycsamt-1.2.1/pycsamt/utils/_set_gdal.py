#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 15:02:44 2022

@author: daniel
"""
import os
import re
import sys
import numpy as np

from pycsamt.utils.decorator import gdal_data_check

def set_GDAL () : 
    # Check for gdal availability at module level so we don't have to
    # do this every time a function in gis_tools is being called.        
    HAS_GDAL = gdal_data_check(None)._gdal_data_found
    
    is_pyproj = False 
    if (not HAS_GDAL):
        try:
            import pyproj
        except ImportError:
            raise RuntimeError("Either GDAL or PyProj must be installed")
        else: 
            is_pyproj =True 
        
    EPSG_DICT = {}
   
    try:
        if is_pyproj: 
            epsgfn = os.path.join(pyproj.pyproj_datadir, 'epsg')
        
            f = open(epsgfn, 'r')
            lines = f.readlines()
        
            for line in lines:
                if ('#' in line): continue
                epsg_code_val = re.compile('<(\d+)>').findall(line)
        
                # print( "epsg_code_val", epsg_code_val)
        
                if epsg_code_val is not None and len(epsg_code_val) > 0 and epsg_code_val[0].isdigit():
                    epsg_code = int(epsg_code_val[0])
                    epsg_string = re.compile('>(.*)<').findall(line)[0].strip()
        
                    EPSG_DICT[epsg_code] = epsg_string
                else:
                    pass  
                #print("epsg_code_val NOT found for this line ", line, epsg_code_val)
            #end for
        else :
            # force set espsg.locally 
            raise 
        
    except:
        # Failed to load EPSG codes and corresponding proj4 projections strings from pyproj.
        # Since version 1.9.5 the epsg file stored in pyproj_datadir has been removed and
        # replaced by 'proj.db', which is stored in a different folder.
        # Since the underlying proj4 projection strings haven't changed, we simply load a
        # local copy of these mappings to ensure backward compatibility.
    
        path = os.path.dirname(os.path.abspath(__file__))
        try:
            epsg_dict_fn = os.path.join(path, 'epsg.npy')
            EPSG_DICT = np.load(epsg_dict_fn, allow_pickle=True).item()
        except: 
            sys.stdout.write(f'Do not find `epsg.npy` in {epsg_dict_fn}')


    return HAS_GDAL , EPSG_DICT 

