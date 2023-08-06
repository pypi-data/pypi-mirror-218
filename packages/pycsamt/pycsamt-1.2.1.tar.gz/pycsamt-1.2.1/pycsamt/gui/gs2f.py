# -*- coding: utf-8 -*-
"""
.Console scripts. 

    $ python pycsamt write_occam2golden
    
    write model occam2d file to golden software file from input resistivities 
    and input layers. 
    
    `**` before the default keys means to convrt input values into float
    `*` before the default keys means to convrt into interger 
    Should compolsory to specify , if not will let inbput values as str 

    Jokers `**` and `*` can be anywhere else in the string default_kwargs key.
Created on Tue Apr  6 19:39:57 2021

"""
import os 
from pycsamt.geodrill.geocore import Geodrill 
from pycsamt.gui.wrap_console_scripts import wrap_cscripts as wrs


default_kwargs = {'Path to occam2d files - str - ' : None , 
                  'Occam2d mesh file name - str - ' : None , 
                  'Occam2d model file - str - ': None , 
                  'Occam2d data file - str - ' : None, 
                  'Occam2d iteration file - str - ' : None, 
                  'Occam2d save oudir - str - ' : None,
                  'Path to station profile (.stn) - str -':None,
                  'Station id to plot - str|int -': 1,
                  'Input resistivities  - list - '  : None, 
                  'Input layers  - list - ': None,
                  'Step descent in meter** - float - ' :200., 
                  'Depth of investigation in meter** - float - '  : 1000., 
                  'Scale  in [m|km] - str - ': 'm',
                  'Plot style  - str - ': 'pcolormesh',
                  'Path to iter2dat files - str -':None,
                  'Iter2dat `x,y,z` model filename - str -': None , 
                  'Iter2dat `.bln` filename - str - ': None,
                  'Output negative depth - bool -' :True,
                  }

def main(): 
    
    wrs_obj = wrs(default_kwargs =default_kwargs)
    for kwey, kwvalues in wrs_obj.sanitize_kwargs.items():
        if kwey.find('Path to') >=0 : path = kwvalues
        if kwey.find('mesh')>=0 : path_to_occam_mesh = kwvalues
        if kwey.find('data') >= 0 : path_to_occam_data = kwvalues 
        if kwey.find('iteration') >= 0 : path_to_occam_iter = kwvalues 
        if kwey.find('model') >=0: path_to_occam_model = kwvalues
        if kwey.find('save outdir')>=0 : savepath = kwvalues
        if kwey.find('investigation') >=0 :DOI = kwvalues
        if kwey.find('Location filename') >= 0 : filename= kwvalues 
        if kwey.find('negative depth') >= 0 : to_negative= kwvalues 
        if kwey.find('Scale') >= 0 : scale= kwvalues 
        if kwey.find('Input resistivities') >=0: INPUT_RESISTIVITIES= kwvalues
        if kwey.find('Input layers')>=0 : INPUT_LAYERS= kwvalues
        if kwey.find('descent') >=0: STEP_DESCENT= kwvalues
        if kwey.find('to iter2dat files')>=0 : path2 = kwvalues
        if kwey.find('Iter2dat `x,y,z`') >=0: iter2dat_fn= kwvalues
        if kwey.find('Iter2dat `.bln`')>=0 : bln_file = kwvalues

    geo_obj = Geodrill(   mesh_fn = os.path.join(path , path_to_occam_mesh),
                                iter_fn = os.path.join(path , path_to_occam_iter), 
                                model_fn =os.path.join(path, path_to_occam_model) , 
                                data_fn =os.path.join(path, path_to_occam_data ),
                                iter2dat_fn = os.path.join(path2 , iter2dat_fn),
                                bln_fn = os.path.join(path2 , bln_file),
                                input_resistivities=INPUT_RESISTIVITIES, 
                                input_layers =INPUT_LAYERS ,
                                step_descent = STEP_DESCENT,
                                doi =DOI, 
                                )    
                                   
    geo_obj.to_golden_software(filename =filename , 
                                   savepath = savepath, 
                                   scale =scale, 
                                   to_negative_depth=to_negative)  
