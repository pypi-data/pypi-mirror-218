# -*- coding: utf-8 -*-
#       Created on Sat Dec 12 16:21:10 2020
#       Author: Kouadio K.Laurent<etanoyau@gmail.com>
#       Licence: GPL
"""
Module Infos 
============== 
Module contains various parameters  of files handling and the definition of 
some technical words. It parses , asserts and controls  the  different inputs formats 
recognized  by the software.
 
"""
import os
import warnings
import numpy as np 

from pycsamt._csamtpylog import csamtpylog 
from pycsamt.utils.exceptions import pyCSAMTError_file_handling

class notion :
    """
    Definition singular class to explain CSAMT technical words. 
    Also usefull for user to have info  about any scientific context 
    the sofware introduces. Each warnings refering to any context 
    could give the details of the errors by printing the definition itself.
    It seems like a short documentation.
    """
 
    reference_frequency =''.join([
        '"Reference number " is The highest frequency with clean data.' 
        'More details in <Weik, M. H., 2001, reference frequency,',
         ' in Computer Science and Communications ',
         'Dictionary, Springer US, 1442.>  or consult the link:', 
         ' http://www.zonge.com/legacy/PDF_DatPro/Astatic.pdf'])
    
    TMA=''.join(['Trimmed-Moving-Average filter : design to remove ',
                 'single-station offsetswhile preserving broader scale ',
                 'changes.It is uded to estimate average apparent resistivities',
                 'at a single static-correction-reference frequency.'])
        
    AVG=''.join(['AVG is typical file from AMTAVG Zonge Engeneering software.',
                 ' It averages GDP CSAMT (CSAM) and Harmonic CSAMT (CSHA) raw',
                 ' data. Several files may be created, including a log file ',
                 '(.LOG-file)listing file (.AL-file), average data files ',
                 '(.AD- and .AVG-file), plot file (.Z-file), and vector',
                 ' files (.Xnn-files).'])
            
    FMLA=''.join([ 'The FLMA filter estimates static-corrected apparent',
                  ' resistivities at a single reference frequency by' ,
                  'calculating a profile of average impedances along the',
                  ' length of the line. Use a fixed-length-moving-average',
                  'filter to estimate average apparent resistivities at a',
                  ' single static-correction-reference frequency.'])
            
    Hanning_window =''.join([ 'The Hanning window is a taper formed by using', 
                             ' a weighted cosine. The Hanning was named for ',
                             ' Julius von Hann, an Austrian meteorologist.',
                             ' It is also known as the Cosine Bell. Some ',
                             'authors prefer that it be called a Hann window,',
                             ' to help avoid confusion with the very similar ',
                             'Hamming window.' ])  
    
    weighted_Beta = ''.join(['The coefficient Betaj describe the way in which ',
                             'dipole responses adjacent to the sounding site ',
                             'x = Xk are weighted to emulate the shape of a ',
                             'Hanning window. For a given window width Wand',
                             ' center point Xko these weights can be adjusted ',
                             ' so that the difference between the continuous ',
                             'Hanning window h( x - X k) and the synthesized ',
                             'version of it h(x. xd is minimized in a ',
                             'least-squares sense.'])
    
    j= ''.join(['J-format is Magnetotelluric data file  written by A.G. Jones ',
                    ' file format:The convention used is for RXY to represent ',
                    'the E-polarization (TE) mode,and for RYX to represent ',
                    ' the B-polarization mode. Please refer to',
                    ' http://mtnet.info/docs/jformat.txt  for more details.',
                    'Some example file can also be find at:',
                    ' http://mtnet.info/docs/jformat_example.txt'])
    
    occam_mesh_parameter_specs_info = ''.join([
                        'Params specs is four lines for each layer.',
                        'The four lines contain symbols which represent the',
                        ' value of four triangles in each mesh block.', 
                        ' These four lines stand for the top, left, bottom,',
                        ' and right-hand triangles of each block in a layer.',
                        'The character <?,Z,A|Y,0> indicates what resistivity ',
                        'value is to be assigned to the triangle.']) 
                                                                    
    occam_mesh_parameter_specs_meaning = {
        'ZZZZZZZZZZZZ': 'means that the triangle contains seawater', 
        '????????????': 'means that the triangle is a free parameter to be calculated',
        '000000000000': 'means that it contains air',
        'YYYAAAAAAAYYY' :'‘A’ through ‘Y’indicate fixed resistivity valuesas specified above.'
        }
    
    j_recordR ={'period': 'period in s, if negative then is frequency in Hz.',
                        'rho'   : 'apparent resistivity, if negative then rejected.',
                        'pha'   : 'phase in degrees',
                        'rhomax': 'rho + 1 standard error',
                        'rhomin': 'rho - 1 standard error',
                        'phamax': 'pha + 1 standard error',
                        'phamin': 'pha - 1 standard error',
                        'wrho'  : 'weight for rho, if <0 then rejected',
                        'wpha'  : 'weight for phase',
                        -999. : 'missing data marker'
            }
    j_recordZ ={ 'period': 'period in s, if negative then is frequency in Hz.',
                        'real'  : 'real part of the transfer function.',
                        'imag'  : 'imaginary part of the transfer function.',
                        'error' : 'standard error.',
                        'weight': 'weight (Note: some weights are in error!).',
                        -999. : 'missing data marker.',
                }
    
    utm_zone_dict_designator ={
                            'X':[72,84], 
                            'W':[64,72], 
                            'V':[56,64],
                            'U':[48,56],
                            'T':[40,48],
                            'S':[32,40], 
                            'R':[24,32], 
                            'Q':[16,24], 
                            'P':[8,16],
                            'N':[0,8], 
                            'M':[-8,0],
                            'L':[-16, 8], 
                            'K':[-24,-16],
                            'J':[-32,-24],
                            'H':[-40,-32],
                            'G':[-48,-40], 
                            'F':[-56,-48],
                            'E':[-64, -56],
                            'D':[-72,-64], 
                            'C':[-80,-72],
                            'Z':[-80,84]
                            }
        
class suit :
    """
    Singular class to easy manipulate word. used everywhere in the 
    script to avoid redondancy. 
    """
    idle=[' ',
          'nan',
          np.nan,
          '*',
          'NaN',
          'none',
          None, 
          '**' ]
    
    longitude =['lon',
                'Longitude',
                'LONGITUDE',
                'LON',
                'LONG',
                'longitude'
                ]
    
    latitude =['lat',
               'Latitude',
               'LATITUDE',
               'LAT',
               'Lat',
               'latitude'
               ]
    
    easting =['e',
              'east',
              'EASTING',
              'easting'
              ] 
    
    northing =['n',
               'north',
               'NORTHING',
               'northing'
               ] 
    
    station =['dot',
              'station',
              'sta',
              'st'
              ]
    
    elevation=['h',
               'elev',
               'elevation',
               'ELEV',
               'ELEVATION'
               ]
    
    topography=['topography']
    stn_separation=['station separation stn']
    azimuth=['azimuth']



class _sensitive:
    """
    Be aware to editing the class instances below. Editing instance 
    attributes is your own risk. 
    
    .. note :: `sensitive class` . Please keep carefully the indices as 
        it was ranged. It's a core of program to correctly run.
        Core of parser of each files except files from `pycsamt.geodrill`
        packages. Aims are:
            1. checking file. Control the given files
            2. reading and writting file. Zonge Avg_format or J-Format or
                EDI -format and else.
            3. to compute value . Indice are used for computation, 
                set and get specific value.
    """
    _logger =csamtpylog.get_csamtpy_logger(__name__)
    
    _j=['>AZIMUTH', '>LATITUDE','>LONGITUDE','>ELEVATION',
       'RXX', 'RXY', 'RYX', 'RYY', 'RTE', 'RTM', 'RAV',
       'RDE', 'RZX', 'RZY', 'SXX', 'SXY', 'SYX', 'SYY', 'STE',
       'STM', 'SAV', 'SDE', 'SZX', 'SZY', 'ZXX', 'ZXY', 'ZYX', 
                   'ZYY', 'ZTE', 'ZTM', 'ZAV', 'ZDE', 'ZZX', 'ZZY', 'QXX',
                   'QXY', 'QYX', 'QYY', 'QTE', 'QTM', 'QAV', 'QDE', 'QZX',
                   'QZY', 'CXX', 'CXY', 'CYX', 'CYY', 'CTE', 'CTM', 'CAV', 
                   'CDE', 'CZX', 'CZY', 'TXX', 'TXY', 'TYX', 'TYY', 'TTE', 
                   'TTM', 'TAV', 'TDE', 'TZX', 'TZY' ,'ZXX', 'ZXY','ZYX']
    
    _avg=['skp','Station',' Freq','Comp',' Amps','Emag',
         'Ephz','Hmag','Hphz','Resistivity','Phase',
         '%Emag','sEphz','%Hmag','sHphz','%Rho','sPhz', 
                    'Tx.Amp','E.mag','E.phz','B.mag','B.phz','Z.mag',
                    'Z.phz','ARes.mag','SRes','E.wgt', 'B.wgt','E.%err',
                    'E.perr','B.%err','B.perr','Z.%err','Z.perr',
                    'ARes.%err']
    
    _edi =['>HEAD','>INFO', #Head=Infos-Freuency-Rhorot,Zrot and end blocks
        '>=DEFINEMEAS','>=MTSECT', '>FREQ ORDER=INC', #Definitions Measurments Blocks
        '>ZROT','>RHOROT','>!Comment','>FREQ','>HMEAS','>EMEAS',
        #Apparents Resistivities  and Phase Blocks
        '>RHOXY','>PHSXY','>RHOXY.VAR','>PHSXY.VAR','>RHOXY.ERR','>PHSXY.ERR','>RHOXY.FIT','>PHSXY.FIT', 
        '>RHOYX','>PHSYX','>RHOYX.VAR','>PHSYX.VAR','>RHOYX.ERR','>PHSYX.ERR','>RHOYX.FIT','>PHSYX.FIT',
        '>RHOXX','>PHSXX','>RHOXX.VAR','>PHSXX.VAR','>RHOXX.ERR','>PHSXX.ERR','>RHOXX.FIT','>PHSXX.FIT',
        '>RHOYY','>PHSYY','>RHOYY.VAR','>PHSYY.VAR','>RHOYY.ERR','>PHSYY.ERR','>RHOYY.FIT','>PHSYY.FIT',
        '>FRHOXY','>FPHSXY','>FRHOXY.VAR','>FPHSXY.VAR','>FRHOXY.ERR','>FPHSXY.ERR','>FRHOXY.FIT','>FPHSXY.FIT', 
        '>FRHOXX','>FPHSXX','>FRHOXX.VAR','>FPHSXX.VAR','>FRHOXX.ERR','>FPHSXX.ERR','>FRHOXX.FIT','>FPHSXX.FIT',
        #Time series-Sepctra and EM/OTHERSECT
        '>TSERIESSECT', '>TSERIES', '>=SPECTRASECT', '>=EMAPSECT', '>=OTHERSECT',
         #Impedance Data Blocks
        '>ZXYR','>ZXYI','>ZXY.VAR', '>ZXYR.VAR','>ZXYI.VAR', '>ZXY.COV', 
        '>ZYXR','>ZYXI','>ZYX.VAR', '>ZYXR.VAR','>ZYXI.VAR', '>ZYX.COV',
        '>ZYYR','>ZYYI','>ZYY.VAR', '>ZYYR.VAR','>ZYYI.VAR', '>ZYY.COV',
        '>ZXXR', '>ZXXI','>ZXXR.VAR','>ZXXI.VAR','>ZXX.VAR','>ZXX.COV',
        '>FZXXR','>FZXXI','>FZXYR','>FZXYI', 
        #Continuous 1D inversion 
        '>RES1DXX', '>DEP1DXX', '>RES1DXY', '>DEP1DXY',
        '>RES1DYX', '>DEP1DYX', '>RES1DYY', '>DEP1DYY',
        '>FRES1DXX', '>FDEP1DXX', '>FRES1DXY', '>FDEP1DXY',
        # Coherency and Signal Data Blocks
        '>COH','>EPREDCOH','>HPREDCOH','>SIGAMP','>SIGNOISE', 
        #Tipper Data blocks 
        '>TIPMAG','>TIPPHS','TIPMAG.ERR', '>TIPMAG.FIT', '>TIPPHS.FIT',
        '>TXR.EXP', '>TXI.EXP', '>TXVAR.EXP','>TYR.EXP','>TYI.EXP','>TYVAR.EXP',
        #Strike, Skew, and Ellipticity Data Blocks 
        '>ZSTRIKE','>ZSKEW','>ZELLIP', '>TSTRIKE', '>TSKEW','>TELLIP', 
        #Spatial filter blocks
        '>FILWIDTH','>FILANGLE','>EQUIVLEN' , '>END'] 
    
    _occam_startup =['Format', 
                     'Description',
                     'Model File',
                    'Data File',
                    'Date/Time',
                    'Iterations to run',
                    'Target Misfit',
                    'Roughness Type',
                    'Diagonal Penalties',
                    'Stepsize Cut Count',
                    'Model Limits',
                    'Model Value Steps',
                    'Debug Level',
                    'Iteration',
                    'Lagrange Value',
                    'Roughness Value',
                    'Misfit Value',
                    'Misfit Reached',
                    'Param Count'] # end with file or startup 
    
    _occam_datafile =['FORMAT',
                      'TITLE',
                      'SITES',
                      'OFFSETS (M)',
                      'FREQUENCIES',
                      'DATA BLOCKS',
                      'DATUM',
                      'ERROR'] #data of simple file.or dat 
                     
    _occam_modelfile =['FORMAT',
                       'MODEL NAME',
                       'DESCRIPTION',
                       'MESH FILE',
                       'MESH TYPE',
                       'STATICS FILE',
                       'PREJUDICE FILE',
                       'BINDING OFFSET',
                       'NUM LAYERS'] # model of simple file 
                      
    _occam_meshfile =['?????????????',
                      'ZZZZZZZZZZZZ',
                      'YYYYYYYYYYYY',
                      '000000000000', 
                      'AAAAAAAAAAAAA'] # end by mesh or simple file 
                            #Check the firstS layer (LIST NUMBER 0 135 52 0 0 2) 
                            #SPECIFIED the catacteristik of mesh
                            #only difference between the startup is at the end ,
                            # the startup file have the same number so 
                            # the iter is not the same case , number change .
                            #response file , check if the range or the lenght == 7. 
    _occam_logfile =['STARTING R.M.S',
                     ' ** ITERATION',
                     'TOFMU: MISFIT',
                    'AND IS',
                    'USING',
                    'STEPSIZE IS',
                    'ROUGHNESS IS']#or end with Logfile.
    
    _stn=['""dot',
          '""e',
          '""h',
          '""n',
          '""sta',
          '""len',
          '""east',
         '""north',
         '""lat',
         '""long',
         '""elev',
         '""azim',
         '""stn']
    
    
    @classmethod
    def which_file(cls, filename=None, deep= True): 
        """
        Which file is the class method. List of recognized files able to parse
        by pyCSAMT software.
        Sensitive class method. 
        
        Parameters
        ----------
            **filename** :str 
                            corresponding file to read , pathLike 
            **deep** : bool , 
                    control reading : False for just control the extension file ,
                    not opening file . True  control in deeper file and
                     find which file were inputted.
                
        Returns  
        ---------
            str 
            FileType could be [`avg` | `j` | `edi` | `resp` | `mesh` | `occamdat` |
                 `stn` | `model` | `iter` | `logfile` | `startup`]
        
       
        List of files read by pyCSAMT :
        
        ==============  =======================================================
        CodeFile                        Description
        ==============  =======================================================
        *avg*           Zonge Engineering file Plainty file of ASTATIC file. 
        *j*             A.G .Jonhson J=Format file. 
        *edi*           SEG (Society of Exploration Geophysics) Electrical
                        Data Interchange file (SEG-EDI) 
        *stn*           Zonge Engineering station file 
        *occamdat*      deGroot-Hedlin, C., and S. Constable, Occam file. 
        *mesh*          Constable, S. C., R. L. Parker, and C. G. Constable 
                        mesh file 
        *model*         Occam Model file  
        *startup*       Occam startup file  
        *iter*          Occam iteration file get after Inversion  
        *resp*          Occam response file , Get after inversion 
        *logfile*       Occam Logfile, Get after inverson (Inversion file )
        ==============  ======================================================= 
        
       
        :Example:
       
            >>> files = ['K1_exp.bln','LCS01.avg' ,'LCS01_2_to_1.avg', 'K1.stn',
            ...            'csi000.dat','csa250.edi','LogFile.logfile',
            ...                 'Occam2DMesh','Occam2DModel', 'OccamDataFile.dat',
            ...            'S00_ss.edi', 'Startup','RESP13.resp', 
            ...                 'ITER02.iter']
            >>>  for ii in files : 
            >>>      path =  os.path.join(os.environ["pyCSAMT"], 
            ...                                  'csamtpy','data', ii)
            ...       try : 
            ...         print(_sensitive.which_file(path,deep=True))
            ...       except :pass 
        """
        
        _code = {'edi':cls._edi , 'j': cls._j, 'startup':cls._occam_startup, 
                 'occamdat':cls._occam_datafile,'model': cls._occam_modelfile,
                 'mesh': cls._occam_meshfile, 'iter': cls._occam_startup, 
                 'avg': cls._avg,  'stn': cls._stn,'logfile':cls._occam_logfile,
                 'resp': ['none','none'],
                  }
        
        _filename = filename
        
        if _filename is None : 
            raise pyCSAMTError_file_handling('Error file: NoneType can '
                                     'not be computed. Check your right path.') 
        if _filename is not None : 
            if os.path.basename(_filename).split(
                    '.')[-1].lower() in list(_code.keys()): #code file recognized
                _flag = os.path.basename(_filename).split('.')[-1].lower()
                if deep ==False :return _flag
            else : _flag = 0 #file not recognized 

        # Open the file now 
        try :
            with open (_filename , 'r', encoding ='utf8') as _f : 
                    _data_lines =_f.readlines()
        except PermissionError:
            msg =''.join(['https://stackoverflow.com/questions/36434764/',
                          'permissionerror-errno-13-permission-denied'])
            raise PermissionError(
                    'This Error occurs because you try to access a file '
                   'from Python without having the necessary permissions. '
                    f'Please read the following guide <{msg}> to let Python'
                   ' to have permission to read and write files.')
            
        if _flag !=0 :  
                                   # file extension has been recognized on dict code keys. 
            cls._logger.info('Reading %s file' % os.path.basename(_filename))
            
            _value_code = _code[_flag]
            
            if _flag =='edi': #avoid expensive function then controle 2thing before continue 
                if _value_code [0] not in  _data_lines[0] :
                        warnings.warn('File probably is incorrect.'
                                      ' Please consult EDI_Main file components : {0}'.\
                                      format(''.join(cls._edi)))
                        raise pyCSAMTError_file_handling(
                            "Wrong SEG-EDI file. It'seems -File provided"
                            " doesnt include '>HEAD. "
                            "Please provide the right EDI-FORMAT")
                elif _value_code[-1] not in _data_lines[-1] :
                    warnings.warn('File probably incorrect.'
                                  ' Please consult EDI_Main file composents : {0}'.\
                                  format(''.join(cls._edi)))
                    raise pyCSAMTError_file_handling(
                        "Wrong SEG-EDI file. It'seems -File provided"
                        " doesnt include '>END. Please provide the right EDI-FORMAT")
            
            elif _flag =='resp' :               # control quick response file
                                                #check if the len of resp= 7 
                if len( _data_lines[0].strip().split()) !=7 : 
                    raise pyCSAMTError_file_handling(
                        "Wrong OCCAM-RESPONSE file."
                        " Please provide the right response file.")
                else : return _flag 
                
            elif _flag =='avg': 
                _reason = cls.validate_avg(avg_data_lines=_data_lines)[0]
                if _reason not in ['yesAST', 'yes'] : 
                    warnings('File <{0}> does not match Zonge AVGfile. '
                             'Get info to {1}'.format(os.path.basename(_filename), notion.AVG))
                    raise pyCSAMTError_file_handling(
                        "Wrong <{0}>Zonge AVG-file. Please provide "
                        "the right file.".format(os.path.basename(_filename)))
                return _flag
            
            elif _flag =='mesh': 
               try :[float(ss) for ss in _data_lines[1].strip().split()] #check the first occam layer 
               except :
                   warnings.warn('Wrong OCCAM-MESH file.'
                                 'Get more info on that site :'
                                 'https://marineemlab.ucsd.edu/Projects/Occam/index.html')
                   raise pyCSAMTError_file_handling(
                       "Wrong OCCAM-MESH <%s>file ."
                       "We don't find the characteristic of thefirst layer."\
                       "Please provide the right OCCAM meshfile." % os.path.basename(_filename)) 
               for _meshcodec in _value_code: 
                   if _meshcodec in _data_lines[-1]: return _flag 
                   else :
                       warnings.warn('Trouble occurs while reading'
                                     'the "OCCAM-params specs.More details in :{0}.\n {1}'.
                                     format(notion.occam_mesh_parameter_specs_info,
                                            notion.occam_mesh_parameter_specs_meaning))
                       raise pyCSAMTError_file_handling(
                           'We do not find a "Parameter specs" in'
                           ' your <{0}>'.format(os.path.basename(_filename)))
                   
                   
            #once both thing has already been controled . then continue . avoid avg because already has deep controlled 
            # with special static method then pass 
            _ccounter =0 # threshold control is match to 7 except stn.
            for _codec in _value_code : # loop the dict value of code  #loop now all the
                if _flag not in ['avg', 'resp','mesh']: 
                    for num , _data_item in enumerate(_data_lines):
                        if _codec in _data_item :
                            _ccounter += 1
                    if _flag =='stn': 
                        if _ccounter >= 3 : return _flag 
                    elif _flag =='j':
                        if _ccounter >=5 : return _flag
                    if _ccounter>=7 :return _flag 
            if _ccounter <7 :
                raise pyCSAMTError_file_handling(
                    'ERROR occurs while reading file !<{0}>. '
                 'File doesnt not match the typical <{1}>'
                 ' Format.'.format(os.path.basename(_filename), _flag))  
        
        elif _flag == 0 : #file not recognized in _codekeys , 
                             #then try to read and to find which file mastch the best.
            _ccounter=0
            for _keycode, _value_code in _code.items(): 
                for num, valueitem in enumerate(_data_lines) :
                    for codec  in _value_code : #read value in code 
                        if codec.lower() in valueitem.lower(): 
                            _ccounter +=1
                    if _keycode =='j' :
                        if _ccounter >=4 :return _keycode
                    if _ccounter >= 7 :
                        if _keycode =='startup':
                            if all([float(val) for val 
                                    in _data_lines[
                                        len(_value_code)+1].strip().split()]) == False :
                                return 'iter'
                            else :return _keycode
                        return _keycode
                    
            #Now we assune that the file must be the 
            #response file then read according response control 
            try :
                resp0 =[float(ss) for ss in _data_lines [0]]
                resp_end =[float(ss) for ss in _data_lines[-1]]
                resp_mid = [float(ss) for ss in _data_lines [int(len(_data_lines)/2)]] # get the middele of file and try float converter 
                assert (len(resp0) == len(resp_end)) and (len(resp_end)==len(resp_mid)),\
                    pyCSAMTError_file_handling(
                        'We presume that  RESP <{0}> file doesnt not '
                        'match a OCCAM-RESPONSE file.'.format(
                            os.path.basename(_filename)))
            except :
                
                message =''.join([
                    'Error reading File. pyCSAMT can read only <{0}> Format file.', 
                    'Format file. Program can not find the type of that file : <{1}>.', 
                    'You may use script <rewriteXXX> of  pyCSAMT to try to rewrite file', 
                    'either to SEG-EDI |j|STN|AVG| or OCCAM{DAT, RESP,MODEL,ITER} files.'
                    ])
                cls._logger.error(message.format(
                    '|'.join(list(_code.keys())),
                    os.path.basename(_filename) ))
                warnings.warn(message.format(
                    '|'.join(list(_code.keys())),
                    os.path.basename(_filename) ))

                return 
            
            return 'resp'


                 
    @staticmethod 
    def validate_avg(avg_data_lines):
        """
        Core function  to validate avg file .
        
        :param avg_data_lines: list of avgfile
        :type avg_data_lines: list 
        
        :returns: 'yesAST' or 'yes' where  'yesAST' is  Astatic file 
                    and  'yes'  is plainty avg file (the main file)  
        :rtype: str 
        
        :returns: item, spliting the headAvg components strutured by file.
        :rtype: list 
        
        :Example:
            
            >>> from csamtpy.etc.infos.Infos inmport _sensistive as SB
            >>> path =  os.path.join(os.environ["pyCSAMT"], 
            ...                                  'csamtpy','data', LCS01_2_to_1.avg)
            ... with open (path, 'r', encoding ='utf8') as f : 
            ...   datalines = f.readlines()
            ... ss =SB._sensitive.validate_avg(avg_data_lines=datalines)
        """
        
        num=[0]
        for jj, code in enumerate(['ASTATIC','$Stn','$Survey', '$Tx','$Rx',
                                   'ARes.mag','SRes','Z.phz','Tx.Amp','ARes.%err']):
            for items in avg_data_lines :
                if items.find(code)> 0:num.append(1) 
                if jj >=5 and(sum(num) >=3):
                    if items.find(code)> 0: item =items.strip().split(',')
                    return ('yesAST', item)
            if jj >=5 and (sum(num)<3):break

        for jj, code in enumerate(['AMTAVG','ASPACE' ,'XMTR' ,'skp' ,'\\-',
                                    'Resistivity','Phase','Comp',' Amps','%Rho']):
            for items in avg_data_lines :
                if items.find(code)> 0:num.append(1) 
                if jj >=4 and(sum(num) >=3):
                    if items.find(code)> 0:
                        item =items.strip().split()
                        return ('yes', item) 
                    
        if sum(num) ==0 : raise pyCSAMTError_file_handling(
                'Data format provided are not typically issued from Zonge AVG format .')
           
 
    
    