# -*- coding: utf-8 -*-
#       Created on Sat Dec 12 13:55:47 2020
#       Author: Kouadio K.Laurent<etanoyau@gmail.com>
#       Licence: GPL

import os 
import copy 
import warnings
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import scipy.interpolate  as spi 

try : 
    from mtpy.core.mt import MT
except :
    pass 

from pycsamt.__init__ import is_installing 
from pycsamt.core.edi import Edi 
from pycsamt.core.cs import CSAMT
from pycsamt.core  import z as CSAMTz
from pycsamt.utils import zcalculator as Zcc
from pycsamt.utils.decorator import deprecated
from pycsamt.utils import func_utils as func 
from pycsamt._csamtpylog import csamtpylog
from pycsamt.utils.exceptions import ( 
    ProcessingError , 
    FrequencyError, 
    ResistivityError, 
    PhaseError, 
    FileHandlingError
    
    )
try : 
    from pycsamt.__init__ import itqdm 
    if itqdm : 
        import tqdm
except: itqdm = False 

try: 
    from sklearn.decomposition import PCA 
except : 
    is_success = is_installing ('sklearn')
    if not is_success : 
        raise ImportError( 'Could not import module `sklearn`. Please '
                          'install scikit-learn manually.')


TAGS =dict(
    ama= 'Adaptative moving-average', 
    tma = 'Trimming moving-average',
    flma = 'Fixed-length dipole moving-average', 
    ss = 'MT remove static-shift',
    dist = 'MT remove distorsion',
    ) 
class Processing(object):
    """ 
    processing class : Processing workflow correction  class
     deal with  AVG Zonge station file "*.stn" or SEG-EDI file. 
     
     
    Arguments
    ----------
        **data_fn** : str 
                    path to Zonge *AVG file or SEG-EDI files or jfiles
            
        **res_array** : array_like (ndarray,1) 
                    apparent resistivities uncorrected data 
            
        **freq_array** : array_like (ndarray,1)
                   frequency array during survey 
           
        **phase_array** : array_like(ndarray,1)
                   phase array during survey 
            
    More attribute will populate : 
        
    =================  ==========  ============================================
    Attributes         Type        Explanation
    =================  ==========  ============================================
    _rj                array_like   static shift factor  
    rho_static         array_like   corrected data from files
    _reference_freq    float        reference value to start corrected data . 
                                    If provided , function will use for data  
                                    correction.if notprovided, program will 
                                    search the reference frequency automatically
                                    and set it for computation. 
    verbose            int          control the level of verbosity. Higher more
                                    messages.
    =================  ==========  ============================================
    
    ========================  =================================================
    Methods                    Description
    ========================  =================================================
    TMA                         Trimming Moving Average computation. 
    FLMA                        Fixed Length Dipole Moving average computation. 
    AMA                         Adaptative Moving average . see Biblio. 
    ========================  =================================================
    
    More attributes can be added by inputing a key word dictionary
    
     .. note:: Reference frequency doesnt need to  be on frequency range
               If value is not in frequency array, program will 
               interpolate value
    
   :Example:
       
       >>> from pycsamt.processing.corr import Processing
       >>> path =  os.path.join(os.environ["pyCSAMT"], 
       ...                       'pycsamt','data', LCS01.AVG)
       ... static_cor =Processing().TMA (data_fn=path,
       ...                                 reference_freq=1024.,
       ...                                 number_of_TMA_points =5 )
       ... print(static_cor)   
    """
    
    def __init__(self, data_fn=None , freq_array=None, 
                 res_array=None, phase_array =None , verbose =0,
                 **kwargs): 
        
        self._logging =csamtpylog.get_csamtpy_logger(self.__class__.__name__)
        
        self.data_fn =data_fn 
        self._freq_array =freq_array 
        self._res_array =res_array
        self.verbose = verbose 
        self.component = kwargs.pop('component', 'xy')
        self.profile_fn = kwargs.pop('profile_fn', None)
        self.savepath = kwargs.pop('savepath', None)
        
        self._reference_frequency =None 
        self._phase_array =None
        self._norm_freq=None 
        self._rj =None 
        self.rho_static=None 
        self.csamt_obj =None 
        
        for keys in list(kwargs.keys()): 
            setattr(self, keys, kwargs[keys])
        
        if self.data_fn is not None : 
            self.read_processing_file()
        
    @property 
    def frequency (self): 
        return self._freq_array
    @frequency.setter 
    def frequency(self, freq): 
        if freq.dtype not in ['float', 'int']:
            try : freq = np.array([float(ff) for ff in freq])
            except : raise FrequencyError(
                    'Frequency must be float number!')
        else : self._freq_array=freq
        
 
    @property 
    def app_rho (self): 
        return self._res_array 
    @app_rho.setter 
    def app_rho (self, app_res): 
        if app_res.dtype not in ['float', 'int']: 
            try : app_res =np.array([float(res) for res in app_res])
            except : raise ResistivityError(
                    'Apparent resistivities values must be float number.!')
        self._res_array=app_res
            
    @property 
    def referencefreq(self):
        return self._reference_frequency 
    @referencefreq.setter
    def referencefreq(self, reffreq):
        
        if isinstance(reffreq, tuple) : # the case where value are preforced 
            reffreq = reffreq[0]
        try :reffreq =float(reffreq)
        except:raise FrequencyError(
            'Reference frequency must be a float or int number.')

        if reffreq not in self.frequency:
            print('---> Reference frequency is not in frequeny range'
                  ' frequency should be will be interpolated')
            if reffreq < self._freq_array.min() or reffreq >\
                self._freq_array.max():
                warnings.warn(
                    'Frequency out off the range, Please provide frequency'
                    'inside the range <{0}  to {1}>'.format(
                        self._freq_array.min(),self._freq_array.max()))
                                                          
                raise FrequencyError(
                    'Frequency out of the range !')
                
            self._reference_frequency =Zcc.find_reference_frequency(
                freq_array=self.frequency, reffreq_value=reffreq ,
                                            sharp=True, etching=True)
                                                                    
        else : self._reference_frequency= reffreq

    @property 
    def phase (self): 
        return self._phase_array 
    @phase.setter 
    def phase(self, phz): 
        try : 
            if isinstance(phz, tuple):
                phz = phz[0]

            phz=np.array([float(pzz) for pzz in phz])
        except:
            
            raise PhaseError(
            'Phase input must be a float number and radians.')

        self._phase_array=phz
        

    def read_processing_file(self, data_fn=None , 
                             profile_fn=None,
                              reference_freq=None,
                              component =None, 
                              **kwargs ):
        """
        Mehod read processing files and load attributes for use.
        
        :param data_fn: full path to data file ,  coulb be `avg` of 
            Zonge International Engineering  or `edi`  of Society of 
            Exploration Geophysics or `j|dat` format of AG.Jones MT.
        :type data_fn: str 
        
        :param profile_fn: full path to station profile file. It's compulsory
            to provide this file when read avgfile.
        :type profile_fn: str 
        
        """
        freq_array =kwargs.pop('freq_array', None)
        res_array = kwargs.pop('res_dict_arrays', None)
        phase_array =kwargs.pop('phase_dict_arrays', None)
 
        self._logging.info('Load attributes for data processing.')
        
        if data_fn is not None : 
            self.data_fn =data_fn 
        if profile_fn is not None : 
            self.profile_fn = profile_fn 
        if freq_array  is not None : 
            self.frequency = freq_array
        
        if res_array is not None : 
            self.res_app_obj = res_array 
        if phase_array is not None:
            self.phase_obj = phase_array
        if component is not None: 
            self.component = component 
            
        flag = 0            # flag to figure out edifiles to to use avg  file
                            # without it profile stn could be possible 
        if self.data_fn is None :
            if self.frequency is None or self.res_app_obj is None or \
                self.phase_obj is None :
                mess= ''.join([
                    'NoneType data can not be computed. Please provide your',
                    ' data path or station dictionnaries of resistivities',
                    ' and phases values or ndarray(len(frequency),len(sites))',
                    ' of resistivities and phases values in degree.'])
                    
                self._logging.info(mess)
                warnings.warn(mess)
                
                raise ProcessingError(
                    'Could not process data with Nonetype obj!'
                    'Please provide your right data files or '
                    ' ndarray|dict of resistivies and phases values in degree.')
                
            else: # enter in this loop assumes that res and  phase value are  
            #provided manually , phase values are in degree.
                # check the len of dictionnaries
                for pobj, pname in zip([self.res_app_obj,self.phase_obj ],
                                       ['res_obj', 'phs_obj']):
                    if isinstance(pobj, np.ndarray) :
                        if pobj.ndim==1: self.site_id='S00' # only one site
                        else :
                            # ndarray( len(frequency) x len(number of stations)) 
                            self.site_id =[ 'S{0:02}'.format(ii) 
                                       for ii in range(pobj.shape[1])]
                        if pname =='res_obj':
                            # create a dict obj of ndarray 
                            self.res_app_obj ={self.site_id[ii]: pobj[:, ii] 
                                          for ii in range(pobj.shape[1])}
                        if pname =='phs_obj':
                            self.phase_obj ={self.site_id[ii]:pobj[:, ii] 
                                          for ii in range(pobj.shape[1])}
                            
                if len(self.res_app_obj) != len(self.phase_obj ) : 
                    mess='Resistivity and phase length must be the same.'+\
                        'The resistivity size is ={0} and phase is= {1}'
                    warnings.warn(mess.format(len(self.res_app_obj,
                                                  len(self.phase_obj))))
                    self._logging.error(mess.format(len(self.res_app_obj,
                                                        len(self.phase_obj))))              
                    raise ProcessingError(
                        'Resistivity and phase must be the same length!')
                    
                # convert values in rad 
                self.phase_obj = {stn: np.deg2rad(phs_values %90)
                             for stn,phs_values in self.phase_obj.items()}
                              
        if self.data_fn is not None :
    
            if self.data_fn.lower().endswith('avg') is True :
                flag=1
                
            try : 
                csamt_obj = CSAMT(data_fn = self.data_fn, 
                                    profile_fn =self.profile_fn,
                                    component=self.component)
                self.frequency = csamt_obj.freq 
                self.res_app_obj = csamt_obj.resistivity
                self.phase_obj ={ key:np.deg2rad(values) 
                            for key, values in csamt_obj.phase.items()
                            }
                self.site_id= sorted(self.res_app_obj.keys())
                self.station_distance = csamt_obj.station_distance 
            
                # try to get dipole length attribute 
                mess ='Default dipole length is set to 50.m'
                try :
    
                    self.dipolelength =csamt_obj.dipolelength 
                except:
                    self._logging.debug(mess)
                    warnings.warn(mess)
                    self.dipolelength = 50.
                else :
                    if self.dipolelength is None:
                        warnings.warn(mess)
                        self.dipolelength =50.
                        
            except FileHandlingError: 
                raise FileHandlingError(
                    f" It seems {self.data_fn!r} does not exist."
                    "  Please provide the right filename or path.")            

            except PermissionError: 
                l1=''.join([' https://stackoverflow.com/questions/13215716/', 
                              'ioerror-errno-13-permission-denied-when-trying-to', 
                              '-open-hidden-file-in-w-mod'])
                l2 = ''.join([
                    'https://docs.microsoft.com/en-us/windows/win32/api/',
                    'fileapi/nf-fileapi-createfilea?redirectedfrom=MSDN'])
                raise TypeError(
                    f"[Errno 13] Permission denied: {self.data_fn!r}. "
                      f"Please consult the following links: {l1!r} and {l2!r} .")

            except: 
                if flag ==1 and self.profile_fn is None: 
                    # force to read only avg data from avg object
                    # without station profile file
                    ######################################################
                    from pycsamt.core  import avg as CSAMTavg
                    ######################################################
                    
                    csamt_obj =CSAMTavg.Avg(data_fn =self.data_fn)
                    self.res_app_obj= csamt_obj.Data_section.Resistivity.loc
                    # Zonge phase are in mrad then converted to rad 
                    # for consistency converted to degree and read again 
                    self.phase_obj =csamt_obj.Data_section.Phase.loc
                    self.phase_obj ={stn:  np.deg2rad(
                        np.rad2deg(phase_values/ 1e3)%90)
                        for stn, phase_values in self.phase_obj.items()}
                    #self.site_id=sorted(avg_obj.Data_section.Station.names)
                    self.site_id=sorted(self.res_app_obj.keys()) 
                    # get avg data and seek the reference frequency at safety data 
                    # avg_data_section = csamt_obj.Data_section._data_array
                    self.frequency= csamt_obj.Data_section.Frequency.value 
                    self.station_distance = csamt_obj.Data_section.Station.value
                    
        # set the matrix of rho data 
        # ignore the dimensionality of the data at each station and masked the 
        # nan values 
        self.phase_obj = func.resize_resphase_values(
            self.phase_obj, return_array =False)
        self.phase_=buildBlock_freqRhoOrPhase(self.phase_obj)
        self.phase_ = np.rad2deg(self.phase_)%90 
        
        self.res_app_obj= func.resize_resphase_values(
            self.res_app_obj, return_array =False)
        self.app_res_= buildBlock_freqRhoOrPhase(self.res_app_obj)
        #-----------------------------------------------------------        
        #---> set reference frequency . if not will detect automatically  
        # as higher frequency with clean data 
        if reference_freq is not None :
            self.referencefreq=reference_freq
        
        if  self.referencefreq is None : 
            if flag ==1 :
                try : 
                    self.referencefreq, *_= Zcc.perforce_reference_freq(
                        dataset=csamt_obj._data_section,
                        frequency_array=self.frequency)
                except : 

                    self.referencefreq= self.frequency.max()                                        
            else : 

                self.referencefreq= self.frequency.max() 
                
        setattr(self, 'csamt_obj', csamt_obj)

    def TMA (self, data_fn=None ,  reference_freq=None,
             number_of_TMA_points =5., **kwargs ):
        """
        Corrected apparent resistivities with Trimmed-moving-average 
        filter(TMA) .TMA estimates average apparent resistivities at a
        single static-correction-reference frequency. 
        if reference frequency is not provided , will find automatically.
        
        Parameters
        -----------
            * data_fn : str 
                    path to avg file or edi file .
                
            * freq_array : array_like (ndarray,1) 
                    frequency array of at normalization frequency 
                    (reference value)of all stations.
                     station j to n .( units =  Hz )
                
            * res_array :     dict of array_like (ndarra,1) 
                    dict of array of app.resistivity at reffreq.
                    from station j to n.
                    
            * phase_array : dict of array_lie(ndarray,1), dict of array 
                            of phase at reffreq.from station j to n.
                             (unit=rad)value of frequency with clean data .
                             (unit=Hz)
                 
            * stnVSrho_loc : dict 
                    set of dictionnary of all app.resistivity 
                    data from station j to n . (optional)
                
            * num_of_TMA_point  :int 
                    window to apply filter .
            
        Returns
        -------
            dict 
               rho_corrected , value corrected with TMA filter  from 
               station j to n. 
        
  
        1.  corrected data from [AVG]
        
        :Example:
            
            >>> from pycsamt.processing.corr import Shifting
            >>> path =  os.path.join(os.environ["pyCSAMT"], 
            ...         'pycsamt','data', LCS01.AVG)
            ... static_cor =shifting().TMA (data_fn=path, 
            ...                            reference_freq=1024.,
                                        number_of_TMA_points =5 )
                  
        2. corrected from edifiles [EDI] 
        
        :Example:
            
            >>> from pycsamt.core.cs import CSAMT
            >>> from pycsamt.processing.corr import Processing
            >>> edipath = r'C:/Users\Administrator\Desktop\test\edirewrite'
            >>> csamt_obj =CSAMT(edipath =edipath)
            >>> static_cor =Processing().TMA( reference_freq =256. ,
            ...                               freq_array = csamt_obj.freq ,
            ...                               res_array = csamt_obj.resistivity , 
            ...                            phase_array =csamt_obj.phase ,
            ...                            number_of_TMA_points=5)
            ... print(static_cor)
            
        """
        profile_fn= kwargs.pop('profile_fn', None)
        phase_array = kwargs.pop('phase_dict_arrays', None)
        res_array = kwargs.pop('res_dict_arrays', None)
        freq_array =kwargs.pop('freq_array', None)
        if self.verbose > 0: 
            print('** {0:<27} {1} {2}'.format("Filter's name",
                                              '=', 
                                              "Trimming moving-average(TMA)"))
        
        self._logging.info (
            'Computing Trimming Moving Average  filter to correct'
            ' apparent resistivities.!')
        
        if data_fn is not None :
            self.data_fn  = data_fn 
        if profile_fn is not None :
            self.profile_fn = profile_fn
        
        # print(reference_freq)
        # if reference_freq is not None : self.referencefreq = reference_freq 
        
        if res_array is not None :
            self.res_app_obj = res_array 
        if phase_array is not None : 
            self.phase_obj = phase_array
        if freq_array is not None : 
            self.frequency = freq_array
  
        if self.csamt_obj  is None :
            self.read_processing_file(reference_freq = reference_freq)
        if self.verbose >0:
            print('** {0:<27} {1} {2} Hz.'.format("Reference frequency",
                                          '=', self.referencefreq))
                                          
        # ---> use the TMA filter to correct apparent resistivities 
        
        self.app_rho =Zcc.get_data_from_reference_frequency(
            array_loc=self.res_app_obj, freq_array=self.frequency,
                                         reffreq_value=self.referencefreq)
                                                        
        self.phase=Zcc.get_data_from_reference_frequency(
            array_loc=self.phase_obj, freq_array=self.frequency,
                                     reffreq_value=self.referencefreq),
                                                          
        # make a copy of dict_loc of apparent resistivity 
        self.stnVSrho_loc=self.res_app_obj     
        # compute the slope     
        slopej =np.arctan((self.phase/(np.pi/4)-1))*(np.pi/2)**-1     
        #extrapolate up in frequency
        rho_app_jplus =np.log10(self.app_rho)+ np.log10(np.sqrt(2))*slopej  
        
        # collect a group of five log(rj+), i.e. for station index j, i = j-2 to j+2.
        # Discard the lowest and highest valued log(rj+) from the group
        # of five and average the remaining
        # three => avg_log
        log_app_rj_tma = Zcc.compute_TMA (data_array=rho_app_jplus,
                                 number_of_TMApoints=number_of_TMA_points)
        # The target static-correction apparent resistivity for station j
        if len(rho_app_jplus) ==1 : # compute only one site 
        
             log_app_rj_tma = rho_app_jplus 
            
        rho_static_targetj =self.app_rho * (np.power(
            10,log_app_rj_tma))/np.power(10,rho_app_jplus)

                                # compute the rstatic factor rj : 
        self._rj =self.app_rho*(rho_static_targetj)**-1
        # shiffting all value to corrected data : we make a copy.
        # we assume that user can use the argument values 
        # already defined. no need to compute again

        if isinstance(self._rj, float): # for one edifile , for consistency 
            self._rj= np.array(self._rj) #try to convert value into array  
        #---------------------------------------------------------------------
        # because dictionnaries could be  little messies sometimes, let create
        # for each values of apparent resistivities its own correction factor rj 
        # then used each correction factor to compute the corrected resistivities 
        # can be change and use matrix like ` FLMA` method. The advantage of using 
        #dict is that , we dont need to  check frequency range and flipped it 
        # at every time.
        #-----------------------------------------------------------------------
        self.tma ={}
        stnNames = sorted(self.site_id)#sorted(self.stnVSrho_loc.keys())
        rj_fd={key:value for key, value in zip (stnNames,self._rj.tolist())}
        for stn , rho_values in self.stnVSrho_loc.items():
            self.tma[stn]= np.apply_along_axis(
                        lambda rhoS: rhoS /rj_fd[stn],0, rho_values)
        
        # compte corrected phase  in degree 
        self.phase_corrected ={}  # reconverted phase in radians to degree values 
        for stn , phase_values in self.phase_obj.items():
            self.phase_corrected[stn]= np.apply_along_axis(
                lambda phaseS: ((phaseS /rj_fd[stn])* 180/ np.pi)%90, 0,
                phase_values)
            
        
         # set the matrix of rho data 
        # self.phase_=buildBlock_freqRhoOrPhase(self.phase_obj)
        # self.phase_ = np.rad2deg(self.phase_)%90 
        
         # set the matrix of rho data  corrected 
        # self.weigth_factor = buildBlock_freqRhoOrPhase(self._rj)
        self.phase_cor = buildBlock_freqRhoOrPhase( self.phase_corrected)
        self.app_res_cor= buildBlock_freqRhoOrPhase(self.tma)
        # self.app_res_= buildBlock_freqRhoOrPhase(self.res_app_obj)

        return self.tma
        
        
   
    
    def FLMA(self, data_fn=None ,dipole_length = 50., number_of_dipole=5.,
               reference_freq=None, **kwargs ):
        """
        Fixed length-dipole moving average `FLMA` to correct apparent
        resistivities.The FLMA filter estimates static-corrected apparent 
        resistivities at a single reference frequency by calculating a profile
        of average impedances along the length of the line. Sounding curves
        are then shifted so that they intersect the averaged profile.
        The highest frequency with clean data should be selected as the
        static-correction reference frequency.

        :param data_fn: full path to data file , could be[AVG|EDI|J]
        :type data_fn: str 
        
        :param dipole_length: value of dipole length in meters 
        :type dipole_length: float, default is 50.
        
        :param number_of_dipole: number of dipole to cover hanning window width 
        :type number_of_dipole : int, float, default is 5.
        
        :param reference_freq: reference frequency at clean data , if not provided
                    reference will be compute automaticcally 
        :type reference_freq: int, float 
        
        :param freq_array: array of survey frequency of the field  
        :type freq_array: array_like 
        
        :param res_dict_arrays: resistivity array of data collected on the field, 
            could be a ndarray of resistivites at each frequency of each sites
            or a dictionnary of array 
        :type res_dict_arrays: ndarray_array, dict , optional
        
        :param phase_dict_arrays: phase values of data at each stations 
                    could be an ndarray of phase with ndarray(len(freq),
                    len(nstaions)) or dictionnary of phase values at each stations.
        :type phase_dict_arrays: ndarray, optional 
        
        :return:  rho corrected at each survey sites
        :type: dict 
        
         .. note:: skin depth param is not to used for `FLMA` filter application.
                  It is not necessary to provide when apply for `FLMA` filter.
                  
        1. read from edipath or jpath 
        
        :Example:
            
            >>> from pycsamt.processing.corr import shifting 
            >>> edipath =os.path.join(os.environ['pyCSAMT'], 'data', 'edi')
            >>> corr_obj= shifting(data_fn =edipath)
            >>> corrapp  = corr_obj.FLMA(number_of_dipole=7,
            ...                             reference_freq=1024.)
            >>> corr_obj._rj
            >>> corrapp
           
        2. read Zonge avg file 
         
        :Example:
            
            >>> from pycsamt.processing.corr import Processing
            >>> avg_path = os.path.join(os.environ['pyCSAMT'], 'data', 'avg')
            >>>  csamt_obj =CSAMT(data_fn =os.path.join(avg_path, 'K2.AVG'),
            ...                  profile_fn=os.path.join(avg_path, 'K2.stn'))
            >>> corr_obj= Processing(data_fn =os.path.join(avg_path, 'K2.AVG'),
            ...                     profile_fn=os.path.join(avg_path, 'K2.stn'))
            >>> corrapp  = corr_obj.FLMA(number_of_dipole=7, reference_freq=8000.)
            >>> print(corr_obj._rj)
            >>> print(corrapp)
        
        """
        profile_fn= kwargs.pop('profile_fn', None)
        
        phase_array = kwargs.pop('phase_dict_arrays', None)
        res_array = kwargs.pop('res_dict_arrays', None)
        freq_array=kwargs.pop('freq_array', None)
        
        _filter_name =kwargs.pop('fname', 'flma')
        
        number_of_skin_depth =kwargs.pop('number_of_skin_depth', 3.)

        self.flip_freq =False 
        
        # use this tip to also compute AMA with this method
        if _filter_name =='flma':
            lfname = 'Fixed length-dipole moving-average(FLMA)'
            __filter_func =Zcc.compute_FLMA
        elif _filter_name =='ama' :
            lfname = 'Adaptative moving-average(AMA)'
            __filter_func = Zcc.compute_AMA
        if self.verbose > 0:
            print('** {0:<27} {1} {2}'.format(
                "Filter's name",'=',lfname))
        
        self._logging.info ('Computing {} to correct apparent resistivities.!'.
                            format(lfname.lower()))

        if data_fn is not None : 
            self.data_fn  = data_fn 
        if profile_fn is not None : 
            self.profile_fn = profile_fn
       
        # load other optional params 
        
        if res_array is not None : 
            self.res_app_obj = res_array 
        if phase_array is not None : 
            self.phase_obj = phase_array
        if freq_array is not None : 
            self.frequency = freq_array
        
        if self.csamt_obj is None :
            self.read_processing_file(reference_freq = reference_freq )
        
        if self.verbose > 0: 
            print('** {0:<27} {1} {2} Hz.'.format("Reference frequency",
                                  '=', self.referencefreq))
        #---> Applied FLMA to correctedapparent resistivities 
        # check flip frequency 
        
        if self.frequency[0] < self.frequency [-1]:
            self.frequency =self.frequency [::-1]
            print('--> Frequencies are flipped'
                  ' to default order ( Highest to lowest)! ' )
            warnings.warn('Frequencies flipped from Highest to lowest !')
            self.flip_freq =True 
        
        #build matrix  if values constitutes adict of stations names and array 
        
        self.stnVSrho_loc= copy.deepcopy(self.res_app_obj)   
        # then compute matrix and flip matrix arrays 
        res_app_obj, _= Zcc.get_matrix_from_dict(
            dict_array= self.res_app_obj, flip_freq=self.flip_freq )
                                                    
        phase_obj,_ = Zcc.get_matrix_from_dict(
            dict_array= self.phase_obj, freq_array= self.frequency) 
    
        # get apparent resistivity and phase  at reference frequency 
        self.app_rho =res_app_obj[ int(np.where(
            self.frequency==self.referencefreq)[0]),:]
        self.phase= phase_obj[int(np.where(
            self.frequency==self.referencefreq)[0]),:]
    
        # Apparent resistivity and impedance phase are converted 
        #to impedance values, Zj, for each station # compute Z_absolute an average Z
        # compute omega 
        mu0 = 4* np.pi * 1e-7 
        omega_reffreq  = 2* np.pi *  self.referencefreq  
        
        zj = np.sqrt(self.app_rho * omega_reffreq * mu0 ) * (
            np.cos(self.phase)+  1j * np.sin(self.phase) ) 
        # compute FLMA 
        #Filter weights are adjusted for finite-length dipoles by integrating a segment
        #of the Hanning window over one dipole length at each station.
        z_target_j =  __filter_func(z_array= zj, 
                                      dipole_length= dipole_length, 
                                      number_of_points=number_of_dipole,
                                      number_of_skin_depth=number_of_skin_depth, 
                                      reference_freq= self.referencefreq)

        #Recover static-corrected apparent resistivity at reference frequency from Zj.
        # recover_Zj  = np.abs(zj)**2/ (omega_reffreq * mu0)
        rho_static_targetj  = np.abs(z_target_j)**2 / (omega_reffreq * mu0)
         
        #Shift sounding curves at all frequencies by multiplying by factor rstaticj/rj.
        # and  compute the rstatic factor rj : 
    
        self._rj =  rho_static_targetj/self.app_rho  
        
        # build rj static matrix  to  shift all sounding curves 
        rj_matrix= np.repeat(
            self._rj.reshape(1,self._rj.shape[0]),
                                res_app_obj.shape[0],axis =0)
        
        mm_rho = res_app_obj * rj_matrix 
        mm_phase = phase_obj * rj_matrix 
        
        if self.flip_freq is True : #flip static correction 
           mm_rho =mm_rho [::-1]
           mm_phase =  mm_phase[::-1]
           if self.verbose > 0: 
               print('--> Data are  flipped recomputed from '
                     ' Lowest to Highest as raw frequencies order !')
           
        # resetting  data on dict 
        self.flma ={stn: mm_rho[:,ii] 
                    for ii , stn in enumerate(self.site_id)}
        # compte corrected phase  in degree 
        self.phase_corrected = {stn: np.rad2deg(mm_phase[:,ii]) %90 
                                for ii , stn in enumerate(self.site_id)}

                 # set the matrix of rho data  corrected 
        self.phase_cor = buildBlock_freqRhoOrPhase( self.phase_corrected)
        self.app_res_cor= buildBlock_freqRhoOrPhase(self.flma)
        
        return self.flma

    def AMA (self, data_fn=None , dipole_length = 50., number_of_skin_depth=3.,
              freq_array=None, reference_freq=None, **kwargs ):
              
        """
        Adapative moving average `AMA` to correct apparent resistivities.
        AMA filter estimates static-corrected apparent resistivities
        at a single reference frequency by calculating a profile of average
         impedances along the length of the line. Sounding curves are then
        shifted so that they intersect the averaged profile. The highest 
        frequency with clean data should be selected as the static-correction
        reference frequency.
        
        :param number_of_skin_depths: skin depth for filter length 
        :type number_of_skin_depths : int, float, default is 3.
        
        :return: resistivities corrected with ama filter 
        :rtype:dict , 
        
        .. seealso:: for other parameters explanations 
                 see  the docstring of `FlMA`
                 
         
        1. read from edipath or jpath 
        
        :Example:
            
            >>> from pycsamt.processing.corr import shifting 
            >>> edipath =os.path.join(os.environ['pyCSAMT'], 'data', 'edi')
            >>> corr_obj= shifting(data_fn =edipath)
            >>> corrapp  = corr_obj.AMA(number_of_points=7,
            ...                             reference_freq=1024.)
            >>> corr_obj._rj
            >>> corrapp
           
        2. read Zonge avg file 
         
        :Example:
            
            >>> from pycsamt.processing.corr import shifting 
            >>> avg_path = os.path.join(os.environ['pyCSAMT'], 'data', 'avg')
            >>>  csamt_obj =CSAMT(data_fn =os.path.join(avg_path, 'K2.AVG'),
            ...                  profile_fn=os.path.join(avg_path, 'K2.stn'))
            >>> corr_obj= shifting(data_fn =os.path.join(avg_path, 'K2.AVG'),
            ...                     profile_fn=os.path.join(avg_path, 'K2.stn'))
            >>> corrapp  = corr_obj.AMA(number_of_points=5, reference_freq=8000.)
            >>> print(corr_obj._rj)
            >>> print(corrapp)
            
        """
        profile_fn= kwargs.pop('profile_fn', None)
        phase_array = kwargs.pop('phase_dict_arrays', None)
        res_array = kwargs.pop('res_dict_arrays', None)
        freq_array = kwargs.pop('freq_array', None)
        
        self.ama = self.FLMA(data_fn =data_fn , 
                              number_of_skin_depth =number_of_skin_depth ,
                              dipole_length= dipole_length ,
                              reference_freq=reference_freq,
                              profile_fn =profile_fn , 
                              phase_dict_arrays=phase_array, 
                              res_dict_arrays=res_array,
                              fname='ama', 
                              freq_array=freq_array)

        return self.ama
    
    @deprecated('Deprecated method! use `pycsamt.processing.Processing.AMA` '
                ' or `pycsamt.processing.Processing.FLMA` instead.')
    def compute_fixed_and_adaptative_moving_average(self, filterfunc, 
                         data_fn =None, profile_fn =None ,
                         dipole_length =50., reference_freq=None, 
                         **kwargs):
        """
        Can use this fonction  to compute at the same time FLMA and AMA by 
        setting only the `filter func` argument . If the function is used 
        set the param `filterfunc` to the filter we need. Avoid repetition 
        in the code Later.
        
        * :meth:`pycsamt.core.processing.zcalculator.compute_AMA`
        * :meth:`pycsamt.core.processing.zcalculator.compute_FLMA`
        
        :param filterfunc: filter fonction , can be :ref:`filter-AMA` or 
                            :ref:`filter-FLMA`
        :type filterfunc: obj
        
        :param data_fn: full path to data file , could be[AVG|EDI|J]
        :type data_fn: str 
        
        :param dipole_length: value of dipole length in meters 
        :type dipole_length: float, default is 50.
        
        :param number_of_skin_depths: skin depth for filter length 
        :type number_of_skin_depths : int, float, default is 5.
        
        :param reference_freq: reference frequency at clean data , 
                    if not provided reference will be compute automaticcally 
        :type reference_freq: int, float 
        
        1. compute fixed length dipole moving average FLMA 
        
        :Example:
            
            >>> from pycsamt.processing.corr import shifting 
            >>> edipath =os.path.join(os.environ['pyCSAMT'], 'data', 'edi')
            >>> corr_obj= shifting(data_fn =edipath)
            >>> res_flma_obj  = corr_obj.compute_fixed_and_adaptative_moving_average(
                filterfunc=Zcc.compute_FLMA,  number_of_points=7,
            ...                             reference_freq=8192.)
            >>> corr_obj._rj
            >>> res_flma_obj 
            
        2. compute adaptative moving-average AMA
        
        :Example:
            
            >>> from pycsamt.processing.corr import shifting 
            >>> edipath =os.path.join(os.environ['pyCSAMT'], 'data', 'edi')
            >>> corr_obj= shifting(data_fn =edipath)
            >>> res_ama_obj   = corr_obj.compute_fixed_and_adaptative_moving_average(
                filterfunc=Zcc.compute_FLMA,  number_of_skin_depth=7,
            ...                             reference_freq=8192.)
            >>> corr_obj._rj
            >>> res_ama_obj 
 
        """
        self._logging.info('Computing AMA Filtering')
        
        res_array =kwargs.pop('res_array', None)
        phase_array =kwargs.pop('phase_array', None)
        freq_array =kwargs.pop('freq_array', None)
        number_of_skin_depth=kwargs.pop('number_of_skin_depth',3.)

        #------------ check the reading file ------------------------------
        # set flag to controle the path values provided  and flip to control the 
        # check the frequency range : Default is Highest to lowest  
        # set attribute to keep copy of res-array dict
        flag =0        
        self.flip_freq =False
        self.__setattr__('stnVSrho_loc', None) 
        # statements parameters 
        if data_fn is not None : 
            self.data_fn =data_fn 
        if profile_fn is not None : self.profile_fn = profile_fn
        #check statemt if provided 
        
        if self.data_fn is None : 
            if res_array is not None: res_app_obj =res_array 
            if phase_array is not None :  phase_obj =phase_array 
            if freq_array is not None : 
                self.frequency =freq_array 
            if res_array is None or phase_array is None or freq_array is None :
                raise ProcessingError('NoneType can be computed.'
                    ' Please provide either path to data file ' 
                    ' or provided resistivity , phase and frequeny arrays!')
        
        # be sure that if data_fn is provided , data should be read  
        # as priority 
        if self.data_fn is not None : 
            csamt_obj= CSAMT(data_fn =self.data_fn, 
                             profile_fn= self.profile_fn)
            res_app_obj = csamt_obj.resistivity 
            phase_obj = csamt_obj.phase 
            self.frequency =csamt_obj.freq
            self.dipolelength = csamt_obj.dipolelength
            
            flag=1
            
            if (self.data_fn.endswith('avg') is True  or \
                self.data_fn.endswith('avg'.upper())) is True  :
                avg_data_section = csamt_obj._data_section
                               
                try : 
                    self.referencefreq= Zcc.perforce_reference_freq(
                        dataset=avg_data_section, 
                        frequency_array=self.frequency)
                except : self.referencefreq= self.frequency.max() 
   
        # check flip frequency 
        if self.frequency[0] < self.frequency [-1]:
            self.frequency =self.frequency [::-1]
            print('--> Frequencies are flipped'
                  ' to default order ( Highest to lowest)! ' )
            warnings.warn('Frequencies flipped from Highest to lowest !')
            self.flip_freq =True 
        
        #build matrix  if values constitutes adict of stations names and array 
        
        if isinstance(res_app_obj, dict): 
            stnNames =sorted(list(res_app_obj.keys()))
             # make a copy of dict_loc of apparent resistivity 
            import copy 
            self.stnVSrho_loc= copy.deepcopy(res_app_obj)   
            # then compute matrix and flip matrix arrays 
            res_app_obj, _= Zcc.get_matrix_from_dict(
                dict_array= res_app_obj, flip_freq=self.flip_freq )
                                                    
        if isinstance(phase_obj, dict): 
            phase_obj,_ = Zcc.get_matrix_from_dict(
                dict_array= phase_obj, freq_array= self.frequency) 
                                                       
            if flag ==1 : # recomputed phase degree to rad 
                phase_obj = np.deg2rad(phase_obj)
                
                
        if reference_freq is not None :
            self.referencefreq =reference_freq 
            
        elif reference_freq is None : 
            self.referencefreq= Zcc.perforce_reference_freq(
                dataset=res_app_obj, frequency_array=self.frequency)
                                                            
        if self.stnVSrho_loc is None :
            # create station id 
            stnNames = ['S{0:02}'.format(ii) 
                        for ii in range(res_app_obj.shape[1])]
            #create dictapp rho
            # for xx in range(res_app_obj.shape[1]):
            #     self.stnVSrho_loc [stnNames[xx]]= res_app_obj[:, xx]
            self.stnVSrho_loc ={stnNames[xx]:res_app_obj[:, xx] 
                                for xx in range(res_app_obj.shape[1]) }
            
        # get apparent resistivity and phase  at reference frequency 
        self.app_rho =res_app_obj[ int(np.where(
            self.frequency==self.referencefreq)[0]),:]
        self.phase= phase_obj[int(np.where(
            self.frequency==self.referencefreq)[0]),:]
        # Apparent resistivity and impedance phase are converted 
        #to impedance values, Zj, for each station 
        # compute Z_absolute an average Z
        
        #------------computation filter part -----------------------
         # compute omega n
        mu0 = 4* np.pi * 1e-7 
        omega_reffreq  = 2* np.pi *  self.referencefreq  
        
        zj = np.sqrt(self.app_rho * omega_reffreq * mu0 ) * (
            np.cos(self.phase)+  1j * np.sin(self.phase) ) 
        # compute FLMA 
        #Filter weights are adjusted for finite-length dipoles by integrating 
        #a segmentof the Hanning window over one dipole length at each station.
        
        z_target_j = filterfunc(reference_freq = self.referencefreq, 
                                     phase =self.phase,
                                     app_rho = self.app_rho,
                                      dipole_length= dipole_length, 
                                      number_of_skin_depth =number_of_skin_depth, 
                                      z_array=zj)
        #Recover static-corrected apparent resistivity at reference frequency
        #  from Zj.recover_Zj  = np.abs(zj)**2/ (omega_reffreq * mu0)
        
        #----computation of rj static factor ---
        
        rho_static_targetj  = np.abs(z_target_j)**2 / (omega_reffreq * mu0)
        #Shift sounding curves at all frequencies 
        #by multiplying by factor rstaticj/rj.
        # and  compute the rstatic factor rj : 
        self._rj =  rho_static_targetj/self.app_rho  
        # build rj static matrix  to  shift all sounding curves 
        rj_matrix= np.repeat(
            self._rj.reshape(1,self._rj.shape[0]),
                                res_app_obj.shape[0],axis =0)
        
        mm_rho = res_app_obj * rj_matrix 
        mm_phase = phase_obj * rj_matrix 
        if self.flip_freq is True : #flip static correction 
           mm_rho =mm_rho [::-1]
           mm_phase =  mm_phase[::-1]
           print('--> Data are  flipped recomputed from '
                 ' Lowest to Highest as raw frequencies order !')
           
        # resetting  data on dict 
        self.flma_or_ama ={stn: mm_rho[:,ii] 
                    for ii , stn in enumerate(stnNames)}
        # compte corrected phase  in degree 
        self.phase_corrected = {stn: np.rad2deg(mm_phase[:,ii]) %90 
                                for ii , stn in enumerate(stnNames)}
        return self.flma_or_ama    
    
    @deprecated ("Use 'pycsamt.processing.Processing.correct_edi' instead."
                 " Faster and avoid circular reading.")
    def write_corrected_edi (self, 
                     data_fn =None,
                     reference_frequency=None, 
                     FILTER ='tma' , 
                     **kwargs):
        """
        Method to correct  edifiles applying filters. 
        
        Availbale filters are *tma* (triming moving average),
        *flma* fixed-length dipole moving average and  `ama` adaptative moving
        average for Electromagnetic Array Profilin(EMAP).
        To apply filter for MT data, set `FILTER` arguments to `ss`  for 
        static shift removal and  `dist` for  distortion removal. It's possible
        to apply EMPA filters to MT data by setting `datatype` argument to "mt". 

        :param data_fn: full path to edifiles 
        :type data_fn: str 
        
        :reference_frequency: refrequency at clean data, optional when apply for 
                        filter `ss` and `dist`.
        :type reference_frequency: float 
        
        :param FILTER: type of filter to write, can be `tma` or `flma`  for EMAP
                    data or `ss` (remove static schift) or `dist` 
                    (remove distortion)for MT data . *Default* is `tma` assume 
                    data provided are EMAP data.
        :type FILTER: str, default is`tma`
        
        Holds others parameters:
            
        =====================  ==========  ====================================
        Params                  Type            Description 
        =====================  ==========  ====================================
        filename                str         name of output edifiles
        number_of_points        int         weighted window. *Default* is 7. 
                                            if one edifile is provided , change 
                                            weigthed point to 1.
        dipole_length           float       length of dipole. *Default* is 50.m
        reduce_res_factor_x     float       static shift factor to be applied to x
                                            components (ie z[:, 0, :]).This is
                                            assumed to be in resistivity scale
        reduce_res_factor_y     float       static shift factor to be applied to y
                                            components (ie z[:, 1, :]).  This is
                                            assumed to be in resistivity scale
        distortion_tensor       ndarray     real distortion tensor as a 2x2, 
                                            np.ndarray(2, 2, dtype=real)
        distortion_err_tensor   ndarray     real distortion tensor error as a 2x2
                                            np.ndarray(2, 2, dtype=real) 
        datatype                str         type of data provided . Could be `mt`
                                            or  `emap`. Detect automatically 
                                            if `None`.
        savepath                str         full path to save outputfile.
        =====================  ==========  ====================================
        
        1. corrected single edifile 
        
        :Example: 
            
            >>> from pycsamt.processing import shifting
            >>>  edifile =os.path.join(os.environ['pyCSAMT'], 'data', 
            ...                           'edi', 'new_csa000.edi' )
            >>> corr_obj= shifting()
            >>> corr_obj.write_corrected_edi(data_fn = edifile,
            ...                                 number_of_points =1., 
            ...                             dipole_length =50., FILTER='ss')
            
        
        2. corrected multi edifiles EMAP
        
        :Example: 
            
            >>> from pycsamt.processing import shifting
            >>>  edipath =os.path.join(os.environ['pyCSAMT'], 'data', 'edi')
            >>> corr_obj= shifting()
            >>> corr_obj.write_corrected_edi(data_fn = edipath,
            ...                             number_of_points =7., 
            ...                             dipole_length =50.,
            ...                                FILTER='flma')
            
        """
        #######################################################################
        from pycsamt.core  import edi as CSAMTedi
        #######################################################################
        new_edifilename =kwargs.pop('filename', None)
        number_of_points= kwargs.pop('number_of_points', 1)
        dipole_length = kwargs.pop('dipole_length', 50.)
        number_of_skin_depth= kwargs.pop('number_of_skin_depth', 3.)
        
        reduce_res_factor_x=kwargs.pop('reduce_res_factor_x', 1.)
        reduce_res_factor_y =kwargs.pop('reduce_res_factor_y', 1.)
        
        distortion_tensor =kwargs.pop('distortion_tensor', None)
        distortion_err_tensor =kwargs.pop('distortion_err_tensor', None)
        
        distortion_tensor, distortion_err_tensor
   
        datatype =kwargs.pop('datatype', None)
        savepath = kwargs.pop('savepath', None)
        if savepath is not None: 
            self.savepath =savepath 
        
        self.savepath =func.cpath(self.savepath , '_coutputEDI_')
        
        if FILTER is None :FILTER ='tma' # block None to default 'tma'
        
        try: _filter =FILTER.lower()
        except : 
            raise ProcessingError(
                'name of filters is `str` not  `{0}`'.format(type(_filter)))
        
        
        if _filter not in ['tma', 'ama' , 'flma', 'ss', 'dist']: 
           
           warnings.warn('Filter provided is UNrecognized'
                         'we will set filter to `tma`')
           print('--> Filter is resetting to TMA')
           
           raise ProcessingError(
               'Filter provided is Unrecognizable!')
           
        self._logging.info('Rewrite edifiles by applying filters')
 
        # controle the range of frequencies :
            # Default range is Highest frequency to lowest 
        flip_freq =False 
        
        if data_fn is not None : 
            self.data_fn = data_fn # call data path  
 
        #--> call multi edi # create multi ediobj
        edi_objs = CSAMTedi.Edi_collection(edipath =self.data_fn ) 
        
        # collect all edi_objects  and get 
        #the pertinents attributes like sites names 
        ediObjs= edi_objs.edi_obj_list
        edi_objs_id = edi_objs.id 
        
        # get datatype from the first edifiles among edi Objs list
        
        if datatype is None : 
            if 'ndipole' in ''.join(['{0}'. format(ii) 
                              for ii in ediObjs[0].MTEMAP.mtemapsectinfo]):
                datatype ='emap'
            else :
                datatype = 'mt' # data contain  MT section  infos 

        # force EMAP filter to apply to MT data 

        if _filter in ['tma', 'ama', 'flma'] and datatype =='mt':
            
            mess = ''.join(['---> EDI file provided is MT data. Filter {0} ',
                ' should be applied and Impedance tensor should be ',
                 'computed and corrected along the default components',
                ' `xy` as EMAP data with unknown strike direction.'])
        
            warnings.warn('!'+ mess.format(_filter, datatype) )
                        
            print('! ' + mess.format(_filter, datatype))
            
            datatype= 'emap' # resetting datatype as CSAMT data 
            
    
        if datatype =='emap':           # read EMAP edifiles and apply filters 
            if _filter not in ['flma', 'tma', 'ama']:
                print('--> Filter no found! Reseeting filter'
                      ' to  default filter :`tma`')
                _filter ='tma'
                
        #call now corrected obbjects
        corr_obj =Processing(data_fn =self.data_fn , 
                            profile_fn =self.profile_fn )
        
        if _filter =='tma': # apply filter tma 
            res_corrected =  corr_obj.TMA( 
                number_of_TMA_points= number_of_points,
                        reference_freq = reference_frequency)
            
            phase_corrected = corr_obj.phase_corrected # get phase corrected 
            # flip frequency if not sorted Highest to lowest 
            if corr_obj.frequency [0] < corr_obj.frequency[-1]:
                frequency_array =corr_obj.frequency[::-1]
                flip_freq =True  
                
            else : frequency_array =corr_obj.frequency
        
        elif _filter =='flma':
            res_corrected =  corr_obj.FLMA(number_of_dipole= number_of_points, 
                                    reference_freq = reference_frequency,
                                    dipole_length = dipole_length
                                    )
       
            phase_corrected = corr_obj.phase_corrected
            
            flip_freq =corr_obj.flip_freq 
            
            # for consistency 
            if corr_obj.frequency [0] < corr_obj.frequency[-1]:
               frequency_array =corr_obj.frequency[::-1]
            else :frequency_array =corr_obj.frequency
            
        elif _filter =='ama':
            res_corrected =  corr_obj.AMA(
                number_of_skin_depth= number_of_skin_depth, 
                reference_freq = reference_frequency,
                dipole_length = dipole_length
                                    )
       
            phase_corrected = corr_obj.phase_corrected
            
            flip_freq =corr_obj.flip_freq 
            
            # for consistency 
            if corr_obj.frequency [0] < corr_obj.frequency[-1]:
               frequency_array =corr_obj.frequency[::-1]
            else :frequency_array =corr_obj.frequency
        
         # collect the value of reference frequency to display
        if reference_frequency is None :   
            reference_frequency = corr_obj.referencefreq 

        #-----> loop all edi objects from collections edifiles 
        # print(res_corrected)
        for k , (stn, edi_obj)  in enumerate(zip (edi_objs_id , ediObjs), 1): 
            
            # create for each edi obj  temporary corrector
            #object for resetting z impedance Tensor 
            csamt_z_obj = CSAMTz.Z()
            # Initialize  resistivity arrays and phase
            #arrays to hold corrected values 
            #  not include errors propagations 
            # seek the frequency array for each edi 
            if _filter in ['ss', 'dist']: 
                frequency_array = edi_obj.Z.freq    
                
            res_array = np.zeros((frequency_array.size, 2,2 ),
                                 dtype = np.float)
            phs_array = np.zeros((frequency_array.size, 2,2 ), 
                                 dtype = np.float)
            
            if _filter in [ 'tma', 'flma', 'ama']:
                if flip_freq is True :     
                    # flip array if frequency is sorted lowest to Highest
                    res_corrected[stn] = res_corrected[stn][::-1]
                    phase_corrected[stn] =phase_corrected[stn] [::-1]
                    
                res_array [:, 0 , 1 ] =  res_corrected[stn]
                phs_array[: , 0, 1] = phase_corrected[stn]
                    
                # now recompute  all component with corrected values
                csamt_z_obj.set_res_phase(res_array = res_array,
                            phase_array=phs_array,
                            freq=  frequency_array) 
               
             # use filters `ss` and `dist` for MT data     
            if  datatype =='mt' or _filter in ['ss', 'dist']:       
                if _filter =='ss':
                    static_shift, z_corrected = \
                        edi_obj.Z.remove_ss(
                            reduce_res_factor_x=reduce_res_factor_x, 
                            reduce_res_factor_y=reduce_res_factor_y)
    
                    csamt_z_obj.compute_resistivity_phase(
                        z_array=z_corrected,
                        z_err_array= edi_obj.Z.z_err, 
                        freq=edi_obj.Z.freq)
                # set z_erray error 
                    z_err_array = edi_obj.Z.z_err 
                    if self.verbose >0:
                        print('--> Remove  static shift is done !')
                
                if _filter =='dist': # remove only distorsion 
                    if distortion_tensor is None : 
                        warnings.warn(
                            'Could not remove distorsion .Provided real '
                            'distortion tensor as a 2x2 matrices.')
                        print('---> Remove distorsion Error ! Please provide '
                              'the distortion Tensor as 2x2 matrices. ')
                        raise ProcessingError(
                            'Could not remove distorsion.Please provided real '
                            ' distortion 2x2 matrixes')
                    _, z_corrected, z_corrected_err = \
                        edi_obj.Z.remove_distortion(
                            distortion_tensor =distortion_tensor,
                            distortion_err_tensor=distortion_err_tensor)
                        
                    if self.verbose > 0:
                        print('--> ! Remove  distortion is done !')
                    
                    z_err_array = z_corrected_err
                    
                csamt_z_obj.compute_resistivity_phase(z_array=z_corrected,
                                                  z_err_array= z_err_array,
                                                  freq=edi_obj.Z.freq)
            # Resset all components  to let edi 
            #containers to hold news corrected values 
            edi_obj.Z._z = csamt_z_obj.z
            edi_obj.Z._z_err = csamt_z_obj.z_err
            edi_obj.Z._resistivity = csamt_z_obj.resistivity 
            edi_obj.Z._resistivity_err = csamt_z_obj.resistivity_err 
            edi_obj.Z._phase = csamt_z_obj.phase
            edi_obj.Z._phase_err = csamt_z_obj.phase_err
            
            #now write corrected edifiles for each edi object 
            edi_obj.write_edifile(new_edifilename=new_edifilename,
                                  datatype =datatype , 
                                  savepath =self.savepath) 

        print('{0:*^77}'.format('EDI {0} FILE'.format(datatype.upper())))    
   
        for ff, name in list(TAGS.items()):
            
            if  ff == _filter :
                print('** {0:<27} {1} {2}'.format(
                    'Filter ','=', _filter.upper()))
                print('** {0:<27} {1} {2}'.format(
                    'Type of correction ','=',name.capitalize()))
                
                if _filter =='tma' : 
                    print('** {0:<27} {1} {2}'.format('Number of points ',
                                              '=', int(number_of_points)))
                if _filter=='flma':
                    print('** {0:<27} {1} {2}'.format('Number of dipole ',
                                               '=', int(number_of_points)))
                    print('** {0:<27} {1} {2} m.'.format('Dipole length ', 
                                                '=', dipole_length ))
                if _filter=='ama':
                    print('** {0:<27} {1} {2}'.format(
                        'Number of skin depth ','=', int(number_of_skin_depth)))
                    print('** {0:<27} {1} {2} m.'.format('Dipole length ', 
                                                          '=', dipole_length ))
                if self.verbose > 0: 
                    print('** {0:<27} {1} {2} Hz.'.format(
                        'Reference frequency ','=', reference_frequency))

        print('** {0:<27} {1} {2}'.format('Frequency numbers',
                                          '=', len(frequency_array)))
        print('** {0:<27} {1} {2}'.format('Number of sites processed',
                                          '=', len(ediObjs)))
        
        print('** {0:<27} {1} {2}'.format('Save directory',
                                          '=', self.savepath))
        print('*'*77)
        
    def correct_edi (self, 
                     data_fn =None,
                     reference_frequency=None, 
                     FILTER ='tma' , 
                     **kwargs):
        """
        Method to correct  edifiles applying filters. 
        
        Availbale filters are *tma* (triming moving average),
        *flma* fixed-length dipole moving average and  `ama` adaptative moving
        average for Electromagnetic Array Profilin(EMAP).
        To apply filter for MT data, set `FILTER` arguments to `ss`  for 
        static shift removal and  `dist` for  distortion removal. It's possible
        to apply EMPA filters to MT data by setting `datatype` argument to "mt". 

        :param data_fn: full path to edifiles 
        :type data_fn: str 
        
        :reference_frequency: refrequency at clean data, optional when apply for 
                        filter `ss` and `dist`.
        :type reference_frequency: float 
        
        :param FILTER: type of filter to write, can be `tma` or `flma`  for EMAP
                    data or `ss` (remove static schift) or `dist` 
                    (remove distortion)for MT data . *Default* is `tma` assume 
                    data provided are EMAP data.
        :type FILTER: str, default is`tma`
        
        Holds others parameters:
            
        =====================  ==========  ====================================
        Params                  Type            Description 
        =====================  ==========  ====================================
        filename                str         name of output edifiles
        number_of_points        int         weighted window. *Default* is 7. 
                                            if one edifile is provided , change 
                                            weigthed point to 1.
        dipole_length           float       length of dipole. *Default* is 50.m
        reduce_res_factor_x     float       static shift factor to be applied to x
                                            components (ie z[:, 0, :]).This is
                                            assumed to be in resistivity scale
        reduce_res_factor_y     float       static shift factor to be applied to y
                                            components (ie z[:, 1, :]).  This is
                                            assumed to be in resistivity scale
        distortion_tensor       ndarray     real distortion tensor as a 2x2, 
                                            np.ndarray(2, 2, dtype=real)
        distortion_err_tensor   ndarray     real distortion tensor error as a 2x2
                                            np.ndarray(2, 2, dtype=real) 
        datatype                str         type of data provided . Could be `mt`
                                            or  `emap`. Detect automatically 
                                            if `None`.
        savepath                str         full path to save outputfile.
        =====================  ==========  ====================================
        
        1. corrected single edifile 
        
        :Example: 
            
            >>> from pycsamt.processing import shifting
            >>>  edifile =os.path.join(os.environ['pyCSAMT'], 'data', 
            ...                           'edi', 'new_csa000.edi' )
            >>> corr_obj= shifting()
            >>> corr_obj.write_corrected_edi(data_fn = edifile,
            ...                                 number_of_points =1., 
            ...                             dipole_length =50., FILTER='ss')
            
        
        2. corrected multi edifiles EMAP
        
        :Example: 
            
            >>> from pycsamt.processing import shifting
            >>>  edipath =os.path.join(os.environ['pyCSAMT'], 'data', 'edi')
            >>> corr_obj= shifting()
            >>> corr_obj.write_corrected_edi(data_fn = edipath,
            ...                             number_of_points =7., 
            ...                             dipole_length =50.,
            ...                                FILTER='flma')
            
        """
        new_edifilename =kwargs.pop('filename', None)
        number_of_points= kwargs.pop('number_of_points', 1)
        dipole_length = kwargs.pop('dipole_length', 50.)
        number_of_skin_depth= kwargs.pop('number_of_skin_depth', 3.)
        datatype =kwargs.pop('datatype', None)
        savepath = kwargs.pop('savepath', None)
        
        if savepath is not None: 
            self.savepath =savepath 
        
        self.savepath =func.cpath(self.savepath , '_coutputEDI_')
        
        if FILTER is None :FILTER ='tma' # block None to default 'tma'
        
        try: _filter =FILTER.lower()
        except : 
            raise ProcessingError(
                'name of filters is `str` not  `{0}`'.format(type(_filter)))

        if _filter not in TAGS.keys(): 
           msg =''.join([
               f"UNknown filter {_filter!r}. Recognized filters are: ",
               f"{func.smart_format(TAGS.keys())}."])
           
           warnings.warn(msg )
           raise ProcessingError(msg)
    
        self._logging.info(f'Apply filters {_filter!r} to edifiles')
 
        # controle the range of frequencies :
            # Default range is Highest frequency to lowest 
        flip_freq =False 
        
        if data_fn is not None : 
            self.data_fn = data_fn # call data path  
            
        if self.csamt_obj is None : 
            self.read_processing_file(data_fn =self.data_fn , 
                                profile_fn =self.profile_fn )
        
        # collect all edi_objects  and get 
        #the pertinents attributes like sites names 
        ediObjs= self.csamt_obj.edi_obj_list
        edi_objs_id =  self.csamt_obj.id 
    
        # get datatype from the first edifiles among edi Objs list
        if datatype is None : 
            if 'ndipole' in ''.join(['{0}'. format(ii) 
                              for ii in ediObjs[0].MTEMAP.mtemapsectinfo]):
                datatype ='emap'
            else :
                datatype = 'mt' # data contain  MT section  infos 

        # force EMAP filter to apply to MT data 

        if _filter in ['tma', 'ama', 'flma'] and datatype =='mt':
            
            mess = ''.join([
                ' Data type seems to be MT data. Impedance tensor should',
                ' be computed and corrected along the default components',
                ' with unknown strike direction.',
                ])
        
            warnings.warn(mess)
            if self.verbose >0:
                print(mess)
            
            datatype= 'emap' # resetting datatype as CSAMT data 
            
        if datatype =='emap':           # read EMAP edifiles and apply filters 
            if _filter not in ['flma', 'tma', 'ama']:
                print(f"--=> Filter {_filter!r} no found. Use  the default"
                      " filter = `ama` instead ")
                      
                _filter ='tma'
                
        if _filter =='tma': # apply filter tma 
            res_corrected =  self.TMA( 
                number_of_TMA_points= number_of_points,
                        reference_freq = reference_frequency)
            
            phase_corrected = self.phase_corrected # get phase corrected 
            # flip frequency if not sorted Highest to lowest 
            if self.frequency [0] < self.frequency[-1]:
                frequency_array =self.frequency[::-1]
                flip_freq =True  
                
            else : frequency_array =self.frequency
        
        elif _filter =='flma':
            res_corrected =  self.FLMA(number_of_dipole= number_of_points, 
                                    reference_freq = reference_frequency,
                                    dipole_length = dipole_length
                                    )
            
            phase_corrected = self.phase_corrected
            
            flip_freq =self.flip_freq 
            
            # for consistency 
            if self.frequency [0] < self.frequency[-1]:
               frequency_array =self.frequency[::-1]
            else :frequency_array =self.frequency
            
        elif _filter =='ama':
            res_corrected =  self.AMA(
                number_of_skin_depth= number_of_skin_depth, 
                reference_freq = reference_frequency,
                dipole_length = dipole_length
                                    )
       
            phase_corrected = self.phase_corrected
            
            flip_freq =self.flip_freq 
            
            # for consistency 
            if self.frequency [0] < self.frequency[-1]:
               frequency_array =self.frequency[::-1]
            else :frequency_array =self.frequency
        
         # collect the value of reference frequency to display
        if reference_frequency is None :   
            reference_frequency = self.referencefreq 

        if itqdm : 
            pbar =tqdm.tqdm(total= len(edi_objs_id),
                             ascii=True,unit='B',
                             desc ='WEgeophysics-pycsamt[---> EDICorrected]', 
                             ncols =77)
            
        #-----> loop all edi objects from collections edifiles 
        # print(res_corrected)
        for k , (stn, edi_obj)  in enumerate(zip (edi_objs_id , ediObjs), 1): 
            
            # create for each edi obj  temporary corrector
            #object for resetting z impedance Tensor 
            csamt_z_obj = CSAMTz.Z()
            # Initialize  resistivity arrays and phase
            #arrays to hold corrected values 
            #  not include errors propagations 
            # seek the frequency array for each edi 
            if _filter in ['ss', 'dist']: 
                frequency_array = edi_obj.Z.freq    
                
            res_array = np.zeros((frequency_array.size, 2,2 ),
                                 dtype = np.float)
            phs_array = np.zeros((frequency_array.size, 2,2 ), 
                                 dtype = np.float)
            
            if _filter in [ 'tma', 'flma', 'ama']:
                if flip_freq is True :     
                    # flip array if frequency is sorted lowest to Highest
                    res_corrected[stn] = res_corrected[stn][::-1]
                    phase_corrected[stn] =phase_corrected[stn] [::-1]
                    
                res_array [:, 0 , 1 ] =  res_corrected[stn]
                phs_array[: , 0, 1] = phase_corrected[stn]
                    
                # now recompute  all component with corrected values
                csamt_z_obj.set_res_phase(res_array = res_array,
                            phase_array=phs_array,
                            freq=  frequency_array)                
            # Resset all components  to let edi 
            #containers to hold news corrected values 
            edi_obj.Z._z = csamt_z_obj.z
            edi_obj.Z._z_err = csamt_z_obj.z_err
            edi_obj.Z._resistivity = csamt_z_obj.resistivity 
            edi_obj.Z._resistivity_err = csamt_z_obj.resistivity_err 
            edi_obj.Z._phase = csamt_z_obj.phase
            edi_obj.Z._phase_err = csamt_z_obj.phase_err
            
            #now write corrected edifiles for each edi object 
            edi_obj.write_edifile(new_edifilename=new_edifilename,
                                  datatype =datatype , 
                                  savepath =self.savepath) 
            # show the progress bar if itqdm installed
            if itqdm :
                pbar.update(k)
        # close the progress bar
        if itqdm :
            pbar.close()
        print(' completed' if itqdm else '--- correction completed ----')
        print('{0:*^77}'.format('EDI {0} FILE'.format(datatype.upper())))    
   
        for ff, name in list(TAGS.items()):
            if  ff == _filter :
                print('** {0:<27} {1} {2}'.format(
                    'Filter ','=', _filter.upper()))
                print('** {0:<27} {1} {2}'.format(
                    'Type of correction ','=',name.capitalize()))
                
                if _filter =='tma' : 
                    print('** {0:<27} {1} {2}'.format('Number of points ',
                                              '=', int(number_of_points)))
                if _filter=='flma':
                    print('** {0:<27} {1} {2}'.format('Number of dipole ',
                                               '=', int(number_of_points)))
                    print('** {0:<27} {1} {2} m.'.format('Dipole length ', 
                                                '=', dipole_length ))
                if _filter=='ama':
                    print('** {0:<27} {1} {2}'.format(
                        'Number of skin depth ','=', int(number_of_skin_depth)))
                    print('** {0:<27} {1} {2} m.'.format('Dipole length ', 
                                                          '=', dipole_length ))
                if self.verbose > 0: 
                    print('** {0:<27} {1} {2} Hz.'.format(
                        'Reference frequency ','=', reference_frequency))

        print('** {0:<27} {1} {2}'.format('Frequency numbers',
                                          '=', len(frequency_array)))
        print('** {0:<27} {1} {2}'.format('Number of sites processed',
                                          '=', len(ediObjs)))
        
        print('** {0:<27} {1} {2}'.format('Save directory',
                                          '=', self.savepath))
        print('*'*77)
        
        
    @staticmethod 
    def remove_static_shift( edi_fn, ss_x=1., ss_y=1., **kws):
        """
        Remove static shift from the apparent resistivity

        Assume the original observed tensor Z is built by a static shift S
        and an unperturbated "correct" Z0 :

             * Z = S * Z0

        therefore the correct Z will be :
            * Z0 = S^(-1) * Z
            
        :param ss_x: correction factor for x component
        :type ss_x: float
    
        :param ss_y: correction factor for y component
        :type ss_y: float
    
        :returns: new Z object with static shift removed
        :rtype: pycsamt.core.z.Z
    
        .. note:: The factors are in resistivity scale, so the
                  entries of  the matrix "S" need to be given by their
                  square-roots!

        :Remove Static Shift: ::

            >>> import pycsamt.processing as Processing 
            >>> import pycsamt.processing as Processing 
            >>> edifile = '/Users/Daniel/Desktop/Data/AMT/E1/di_test/new_csa00.edi'
            >>> outputedi = 'rmss_csa00.edi'
            >>> Processing.remove_static_shift(
                edi_fn = edifile, ss_x= .5, ss_y=1.2,new_edi_fn = outputedi
                                               )
        """
        
        cedi_obj = MT(fn =edi_fn)
        new_z_obj = cedi_obj.remove_static_shift(ss_x=ss_x , ss_y=ss_y)
        ediobj = Edi(edi_filename=edi_fn)
        ediobj.write_new_edifile( new_Z=new_z_obj, **kws)
        return new_z_obj  
        
        
    @staticmethod 
    def remove_distortion( edi_fn , num_freq=None, **kws):
        """
        remove distortion following Bibby et al. [2005].

        :param num_freq: number of frequencies to look for distortion from the
                         highest frequency
        :type num_freq: int

        :returns: Distortion matrix
        :rtype: np.ndarray(2, 2, dtype=real)

        :returns: Z with distortion removed
        :rtype: pycsamt.core.z.Z

        :Remove distortion and write new .edi file: ::

            >>> import pycsamt.processing as Processing 
            >>> import pycsamt.ff.processing as Processing 
            >>> edifile = '/Users/Daniel/Desktop/Data/AMT/E1/di_test/new_csa00.edi'
            >>> outputedi = 'rmss_csa00.edi'
            >>> Processing.remove_distortion(edi_fn = edifile, new_edi_fn= outputedi
                )

        """
        dedi_obj = MT(fn =edi_fn)
        D, new_z = dedi_obj.remove_distortion()
        ediobj = Edi(edi_filename=edi_fn)
        ediobj.write_new_edifile( new_Z=new_z, **kws)
        return D, new_z   
        
    @staticmethod 
    def noiseRemoval(edi_fn = None, kind='sim', **kws): 
        """ Remove multiple noises in EDIs and save to new files. Noise can be 
        either a `staticshift` , `distorsion` noises or other interferences. 
        
        For Electromagnetic Array Profiling (EMAP) data correction, may refer to 
        :meth:`pycsamt.processing.Processing.correct_edi`. The Remove 
        distortion following Bibby et al. [2005]. Remove static shift from the 
        apparent resistivity assume the original observed tensor Z is built by
        a static shift S and an unperturbated 
        
             * Z = S * Z0
     
        therefore the correct Z will be :
            
            * Z0 = S^(-1) * Z
                
        :param edi_fn: Path-Like object. Full path to EDI-files. 
        :type edi_fn: str 
        
        :param kind: Type of noise to remove. Can be a static shift effect for 
            ``ss``, distorsion for ``dist``. The human activites can be removed 
            using the `pca`` and the other interferences can be removed using 
            the simplier filters ``sim``. Default is ``sim``. 
        :type kind: str 
        
        :param ss_x: correction factor for x component
        :type ss_x: float
    
        :param ss_y: correction factor for y component
        :type ss_y: float
        
        :param num_freq: number of frequencies to look for distortion from the
                         highest frequency
        :type num_freq: int

        :returns: Distortion matrix
        :rtype: np.ndarray(2, 2, dtype=real)
    
        :returns: 
            - new Z object with static shift removed
            - Distortion matrix
            
        :rtype: pycsamt.core.z.Z
        
        .. note:: The factors are in resistivity scale, so the
                  entries of  the matrix "S" need to be given by their
                  square-roots!
                  
        :Example:
            >>> from pycsamt.processing import Processing 
            >>> edipath = '/Users/Desktop/ediout/'
            >>> Processing.noiseRemoval(edi_fn =edipath)
            
        :See also: 
            
            - MTpy of Alison.Kirkby@ga.gov.au via https://github.com/MTgeophysics/mtpy
            
        """
        kind =str(kind).lower() 
        if kind in ('ss', 'staticshift'): kind =='ss'
        elif kind in ('dt', 'dist', 'distortion'): kind =='dt'
        elif kind in  ('principal component analysis', 'pca', 'sklearn'): 
            kind ='pca'
        elif kind in ('simple', 's0', 'simplier', 'light', 'base'): 
            kind ='sim' 
        else : 
            raise ValueError(f"Wrong Param `kind`: {kind}. "
                             "Should be `ss` or `dist`"
                             )
        if os.path.isfile(edi_fn): 
            edi_fn = os.path.dirname (edi_fn) # keep only the path 
        if not os.path.dirname(edi_fn): 
            raise ValueError(f'Wrong given EDI path: {edi_fn}')
            
        D= None 
        # show progress bar 
        if itqdm : 
            pbar =tqdm.tqdm(total= len(os.listdir(edi_fn)),ascii=True,unit='B',
                             desc ='WEgeophysics-pycsamt[---> NoiseRemoval]', 
                             ncols =77)
        for k, edi in enumerate (os.listdir(edi_fn)): 
            edifile = os.path.join(edi_fn, edi)
            with warnings.catch_warnings(): # ignore multiple warnings 
                warnings.simplefilter('ignore')
                if kind =='ss': 
                    new_z = Processing.remove_static_shift(edifile, **kws)
                elif kind =='dt': 
                    D, new_z = Processing.remove_distortion (edifile, **kws)
                elif kind =='pca': 
                    new_z = Processing.pca_filter(edifile, **kws)
                elif kind =='sim': 
                    new_z = Processing.simpler_filter(edifile, **kws)
            # show the progress bar ;
            if itqdm :
                pbar.update(k)
        # close the progress bar
        if itqdm :
            pbar.close()
    
        print(' completed' if itqdm else '--- process completed ----')
        
        return new_z, D 
     
    @staticmethod 
    def pca_filter (edi_fn, var=.95 , **kws): 
        """ Sanitize EDIs data and remove the outliers using the principal 
        component analysis (PCA).
        
        In considering the human activity noises removal using the PCA
        
        :param edi_fn: Path-Like object. Full path to EDI-file. 
        :type edi_fn: str 
        
        :param var: component or ratio of moise to remove.  Default value is 
            ``.95``. 
        :type var: float
        
        :param kws: Additional keywords arguments from
            :mod:`sklearn.decomposition.PCA` 
        :type kws: dict 
        
        :returns: New Z impedance object with remove outliers. 

        :rtype: pycsamt.core.z.Z
        
        :Example: 
        >>> from pycsamt.processing import Processing 
        >>> from pycsamt.core.edi import Edi 
        >>> edifile = '/home/edi/m20.E000.edi'
        >>> newZ =Processing.pca_filter ( edifile, var =.80 ) 
        >>> #write a new corrected edifile 
        >>> _= Edi(edifile).write_new_edifile(new_Z= newZ, 
        ...               new_edi_fn ='m20.removeO.E000.edi')
            
        """
 
        def reshape_and_fit_z (z , back =False , fit= 'transform') :
            """ Reshape z for to np.ndarray(nfreq, 1) for scikit-learn API  
            back for filling the z ndarray (nfreq, 2, 2)"""
            z = z.reshape ((1, z.shape [0])) if back else z.reshape (
                (z.shape [1], 1)) 
             
            z = (pca.fit_transform(z) if fit =='transform' else 
                 pca.inverse_transform(z) ) if fit is not None else z 
            return z 

                              
        edi_fn = func._assert_all_types(edi_fn, str)
        if not os.path.isfile(edi_fn): 
            raise ValueError(f'Wrong given EDI file: {edi_fn}')
    
        if isinstance (var, str):
            try : var =float(var) 
            except: 
                if '%' in var: 
                    var = float(var.replace('%', ''))*1e-2
                else: 
                    raise ValueError('Variance could be a float '
                                     f'value not: {type(var).__name__!r}')
        if var > 1.: 
            raise ValueError('Variance ratio should be '
                             f'less than 1 :{str(var)!r}')
    
        #create an EDI OBJECT 
        ediObj = Edi(edi_fn )
        # make a new object 
        new_Z = CSAMTz.Z(z_array=np.zeros((ediObj.Z.freq.shape[0], 2, 2),
                                       dtype='complex'),
                      z_err_array=np.zeros((ediObj.Z.freq.shape[0], 2, 2)),
                      freq=ediObj.Z.freq)
       
        # construct the pca object from sklearn 
        pca = PCA(n_components= var, **kws) 
        # loop to remove outliers on the Z impedance object 
        for ii in range(2):
            for jj in range(2):
                # need to look out for zeros in the impedance
                # get the indicies of non-zero components
                nz_index = np.nonzero(ediObj.Z.z[:, ii, jj])
                 
                if len(nz_index[0]) == 0:
                    continue
                # get the non_zeros components 
                with np.errstate(all='ignore'):
                    z_real = ediObj.Z.z[nz_index, ii, jj].real
                    z_imag = ediObj.Z.z[nz_index, ii, jj].imag
                    z_err = ediObj.Z.z_err[nz_index, ii, jj]
    
                    z_real_t =reshape_and_fit_z(z_real) 
                    z_imag_t = reshape_and_fit_z(z_imag) 
                    z_err_t = reshape_and_fit_z(z_err)               
                    z_real_b =reshape_and_fit_z(z_real_t,back=True,fit =None) 
                    z_imag_b = reshape_and_fit_z(z_imag_t,back=True,fit =None) 
                    z_err_b = reshape_and_fit_z(z_err_t,back=True,fit =None 

                                                ) 
               # set the new Z object 
                new_Z.z[nz_index, ii, jj] = z_real_b  + 1j * z_imag_b 
                new_Z.z_err[nz_index, ii, jj] = z_err_b
                
        # compute resistivity and phase for new Z object
        new_Z.compute_resistivity_phase()
     
        return new_Z
    
    @staticmethod 
    def simpler_filter (edi_fn, **kws): 
        """ Sanitize EDIs data and remove the outliers using simple 
        fitting function. 
        
        In considering the other interferences noises removal using the base 
        or simpler filter via fitting impedances values. 
        
        
        :param edi_fn: Path-Like object. Full path to EDI-file. 
        :type edi_fn: str 
        
        :param kws: additional keyword arguments for correct values 
        
        :Example: 
        >>> from pycsamt.processing import Processing 
        >>> from pycsamt.core.edi import Edi 
        >>> edifile = '/home/edi/m20.E000.edi'
        >>> newZ =Processing.simple_removal( edifile ) 
        >>> #write a new corrected edifile 
        >>> _= Edi(edifile).write_new_edifile(new_Z= newZ, 
        ...               new_edi_fn ='m20.removeSR.E000.edi')
        
        """
        
        edi_fn = func._assert_all_types(edi_fn, str)
        if not os.path.isfile(edi_fn): 
            raise ValueError(f'Wrong given EDI file: {edi_fn}')
    
        #create an EDI OBJECT 
        ediObj = Edi(edi_fn )
        
        # make a new object 
        new_Z = CSAMTz.Z(z_array=np.zeros((ediObj.Z.freq.shape[0], 2, 2),
                                       dtype='complex'),
                      z_err_array=np.zeros((ediObj.Z.freq.shape[0], 2, 2)),
                      freq=ediObj.Z.freq)
    
        # loop to correct the Z impedance object values 
        for ii in range(2):
            for jj in range(2):
                # need to look out for zeros in the impedance
                # get the indicies of non-zero components
                nz_index = np.nonzero(ediObj.Z.z[:, ii, jj])
        
                if len(nz_index[0]) == 0:
                    continue
                # get the non_zeros components 
                with np.errstate(all='ignore'):
                    z_real = func.reshape(
                        ediObj.Z.z[nz_index, ii, jj].real)
                    z_imag = func.reshape(
                        ediObj.Z.z[nz_index, ii, jj].imag)
                    z_err = func.reshape(
                        ediObj.Z.z_err[nz_index, ii, jj]) 
                    # correct the values 
                    z_real_c, *_ =func.scale_values (z_real,**kws) 
                    z_imag_c, *_ = func.scale_values(z_imag, **kws) 
                    z_err_c, *_ = func.scale_values(z_err, **kws) 
                    
               # set the new Z object 
                new_Z.z[nz_index, ii, jj] = func.reshape(
                    z_real_c, 1)   + 1j * func.reshape(z_imag_c, 1) 
                new_Z.z_err[nz_index, ii, jj] = func.reshape(z_err_c, 1)
                
        # compute resistivity and phase for new Z object
        new_Z.compute_resistivity_phase()
     
        return new_Z

def interp_to_reference_freq(freq_array, rho_array, 
                             reference_freq, plot=False): 
    """
    Interpolate frequencies to the reference frequencies.
    
    :param freq_array:  frequency array
    :type freq_array: array_like
    
    :param reference_freq: frequency at clean data 
    :type reference_freq: float 
    """
    #find number of frequency
    freqObj , _reffreq =freq_array , reference_freq 
    rhoObj=rho_array
    if freqObj.dtype not in ['float', 'int'] :  
        raise TypeError('Frequency values must be float number.')
    if rhoObj.dtype not in ['float', 'int'] :
       raise TypeError(
           'Apparent Resistivities values must be on float number')
    # do it in the case dtype value are integer.  
    freqObj=np.array([float(kk) for kk in freqObj]) 
    rhoObj=np.array([float(kk) for kk in rhoObj])
    
    if reference_freq not in freqObj : 
        raise FrequencyError(
            'Reference frequency selected as input '
        'argument is not Found on the frequency array.'
            ' Please select the right frequency ')
    
    def cut_off_array_to_interp(freq_array, reference_freq,
                                kind_interp='linear'):

        """
        Seek the array for interpolation with reference frequency.
        Return size of array to interpolate and the array 
        
        :param freq_array:  frequency array
        :type freq_array: array_like
        
        :param reference_freq: frequency at clean data 
        :type reference_freq: float 
        
        :param kind_interp: kind of interpolation 
                            Default is `linear`
        :type kind_interp: str 
        """
        for ss , value in enumerate(freq_array): 
            if reference_freq == freq_array[-1]:
                array_to_interp  = freq_array
                break
            if value == reference_freq:
                array_to_interp  =freq_array[:ss+1]
                break 
        return array_to_interp.size,array_to_interp  
    
    x_num_of_freq , interparray= cut_off_array_to_interp(
        freq_array=freqObj, reference_freq=_reffreq)
    
    func_interp =spi.interp1d(interparray, rhoObj[:x_num_of_freq], 
                              kind='linear')

    new_rhoObj= func_interp(freqObj[:x_num_of_freq] )
    if plot: 
        fig, ax =plt.subplots()
        ax.loglog(freqObj[:x_num_of_freq], new_rhoObj, c='r', lw=5)
        ax.loglog(freq_array,rhoObj )
        plt.show()
        
    return new_rhoObj

def buildBlock_freqRhoOrPhase (dictRhoOrPhase): 
    """ From a dictionnary, build matrix like ndarray (nfreq, Rho|Phase)
    
    :param dictRhoOrPhase: dictionnary of station and values. 
                        We assume stations is sorted to first station 
                        to the last
    :return: 
        Block matrix of rho or phase 
    """

    df_= pd.DataFrame(dictRhoOrPhase)
    data_block = df_.to_numpy()
    return data_block 



    
    
    
    
    
    
    
    
    
