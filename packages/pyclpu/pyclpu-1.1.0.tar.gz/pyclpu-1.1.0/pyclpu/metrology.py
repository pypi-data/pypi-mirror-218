# -*- coding: utf-8 -*-
""" This is the CLPU module to work with data from metrology.

Please do only add or modify but not delete content.

requires explicitely {
 - os
 - tkinter
 - numpy
 - cv2
 - typing
}

import after installation of pyclpu via {
  from pyclpu import metrology
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/metrology.py))
  sys.path.append(os.path.abspath(root))
  import metrology
  from importlib import reload 
  reload(metrology)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNALimport cv2
import os
import sys
from inspect import getsourcefile
from importlib import reload

import math
import numpy as np

from scipy import signal

import matplotlib.pyplot as plt
from tkinter import filedialog #not for the function
from typing import List, Tuple

# INTERNAL
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) # get environment
sys.path.append(os.path.abspath(root))                           # add environment
sys.path.append(os.path.abspath(root)+os.path.sep+"LIB")         # add library

if "constants" not in globals() or globals()['constants'] == False:
    import constants                        # import all global constants from                   constants.py
    import formats                          # import all global formats from                     formats.py
    from manager  import error               # import error() from management                    manager.py
    from manager  import message             # import message() from management                  manager.py
    from manager  import warning             # import warning() from management                  manager.py
    from waveform import wfmread             # import wfmread() from waveform                    waveform.py
    from waveform import Waveform            # import Waveform from waveform                     waveform.py
    reload(constants)
    reload(formats)

# =============================================================================
# CLASSES
# =============================================================================
class ThomsonParabola:
    def __init__(self):
        pass
    # seleccionar_carpeta_destino(): This function open a folder dialog and allow select a destination folder
    # inputs: none
    # outputs; string with the folder path
    @staticmethod
    def Seleccionar_carpeta_destino() -> str:
        carpeta_destino = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        return carpeta_destino

    # seleccionar_archivos(): This function open a multiple filedialog and allow select a destination folder
    # inputs: none
    # outputs: List of string with the files path
    @staticmethod
    def Seleccionar_archivos() -> List[str]:
        archivos = filedialog.askopenfilenames(title="Seleccionar archivos", filetypes=(
        ("Archivos TIFF", "*.tiff;*.tif"), ("Todos los archivos", "*.*")))
        lista = []
        lista.extend(archivos)
        return lista

    # _searchpoint(img, a, sea, k): auxiliar function in cas that the trace is lost allow to search forward one pixel more selecting the best value
    # in the next five pixels adjacent
    # input img: image that is anlizing
    #       pointlist  : list of selected point for this trace
    #       previousvalue: previous value for the Y coordinate
    #       actualX: actual x value in the scan
    # output: the previous value of y
    @staticmethod
    def _searchpoint(img, pointlist, previousvalue, actualX):
        try:
            # create a dictionary
            asa = {}
            # load the adjacent values
            for l in range(3):
                asa[l] = img[actualX, int(previousvalue) + l]

            # select the maximum values
            max_value = max(asa.values())

            # append the best value
            for key, value in asa.items():
                if value == max_value:
                    pointlist.append((int(key + previousvalue), actualX))
                    previousvalue = key + previousvalue
                    break

            return previousvalue

        except Exception as ex:
            raise Exception("searchpoint fail")

    # _rows(img, a, sea, k): auxiliar function search the local maximum in one row
    # input img: image that is anlizing
    #       clone  : copy of image where the local maximum are highligthed
    #       previousvalue: previous value for the Y coordinate
    #       actualX: actual row
    #       threshold: the difference between two point in order to be considered a local maximum
    @staticmethod
    def _rows(img, clone, actualX, threshold):
        # initialize variables
        # set to save the maximum
        localmax = set()

        # row of the image proccesed
        row = img[actualX:actualX + 1, :]

        localMaxima = []
        oldstatus = 0
        newstatus = 0
        maxvalue = 0
        maxvalex = 0

        # scan the row.  Works as a states machine searching for flanks
        for x in range(row.shape[1] - 1):
            centerValue = int(row[0, x])
            rightValue = int(row[0, x + 1])

            if rightValue - centerValue > threshold:
                if newstatus == 0 and oldstatus == 0:
                    minx = x
                    oldstatus = 0
                    newstatus = 1
            elif centerValue - rightValue > threshold:
                if newstatus == 1 and oldstatus == 1:
                    oldstatus = 1
                    newstatus = 0
            else:
                if newstatus == 1 and oldstatus == 0:
                    oldstatus = 1
                    newstatus = 1
                    if maxvalue < centerValue:
                        maxvalue = centerValue
                        maxvalex = x
                elif newstatus == 0 and oldstatus == 1:
                    maxx = x
                    oldstatus = 0
                    newstatus = 0
                    p = (maxvalex, actualX)
                    localMaxima.append(p)
                    localmax.add(maxvalex)

                    maxvalue = 0
                    maxvalex = 0
                elif newstatus == 1 and oldstatus == 1:
                    if maxvalue < centerValue:
                        maxvalue = centerValue
                        maxvalex = x

        # highlight the local maximum
        for maxima in localMaxima:
            cv2.circle(clone, maxima, 1, (255, 255, 0))

        # return the local maximum ordered
        return sorted(localmax)

    # ThompsomParabolaImageprocessingV2: This function search for the different traces in a Thomson parabola image. produces five folder:
    # folder input save the original image
    # folder output save the original image where the traces are painted with different colours
    # folder mask save the traces with different colours
    # folfer ouput gray save the traces without discrimination
    # folder text save the sum of the 5 adjacent values in a csv
    # input: pathDestinationSelected: output folder
    #       picturesSelected: List of path for the different pictures
    #       coluours: List of colours to be used in the different outputs like mask. should be a tuple RGB
    #       threshold: the difference between two point in order to be considered a local maximum
    #       wake: The maximum number of points tha can be founded with searchpoint function
    #       quality: the minimum number of real point admmited in a trace
    @staticmethod
    def ThompsomParabolaImageprocessingV2(pathDestinationSelected: str, picturesSelected: List[str],
                                          colours: List[Tuple[int, int, int]], threshold: int, wake: int, qualit: int):
        # intialize variables
        pictures = picturesSelected
        removepictures = []
        filename = ""

        # output paths
        pathinputs = os.path.join(pathDestinationSelected, "input")
        pathoutputsgray = os.path.join(pathDestinationSelected, "output_gray")
        pathoutputs = os.path.join(pathDestinationSelected, "output")
        pathoutputsmask = os.path.join(pathDestinationSelected, "mask")
        pathoutputtext = os.path.join(pathDestinationSelected, "text")

        # create the folder
        if not os.path.exists(pathinputs):
            os.makedirs(pathinputs)

        if not os.path.exists(pathoutputs):
            os.makedirs(pathoutputs)

        if not os.path.exists(pathoutputsgray):
            os.makedirs(pathoutputsgray)

        if not os.path.exists(pathoutputsmask):
            os.makedirs(pathoutputsmask)

        if not os.path.exists(pathoutputtext):
            os.makedirs(pathoutputtext)

        # start the proccess
        try:
            # scan each file in the List
            for file in picturesSelected:

                # inicialize variables
                memory = {}
                quality = {}
                trazas = {}

                # get the name of the file
                filename = os.path.basename(file)

                # read the file
                img = cv2.imread(file, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_GRAYSCALE)

                # filter the X ray in the image
                cv2.medianBlur(img, 5, img)

                # prepare the different output images
                clone = img.copy()
                clone = cv2.convertScaleAbs(clone, alpha=(255.0 / 65535.0))
                clone3 = img.copy()
                clone3 = cv2.convertScaleAbs(clone3, alpha=(255.0 / 65535.0))
                original = img.copy()
                clone2 = np.zeros_like(img, dtype=np.uint8)
                clone4 = np.zeros_like(img, dtype=np.uint8)
                clone = cv2.cvtColor(clone, cv2.COLOR_GRAY2RGB)
                clone3 = cv2.cvtColor(clone3, cv2.COLOR_GRAY2RGB)

                # range of row scans
                range_iter = range(1020, -1, -1)

                # search the local maximum
                for i in range_iter:
                    sort = ThomsonParabola._rows(img, clone2, i, threshold)
                    if len(sort) != 0:
                        memory[i] = sort
                memory = {k: memory[k] for k in sorted(memory.keys())}

                # combinin the different maximum to find the nearest if doesnt exist search with sarchpoint function a point
                init2 = list(memory.keys())
                counter = 1

                if memory:
                    for j in range(init2[0], init2[-1]):
                        a = []
                        rem = {}

                        # check the actual y in memory
                        if j in memory:
                            qul = 0
                            flse = 0
                            # select all the local maximum in a row
                            for prev in memory[j]:
                                flse = 0
                                a = []
                                a.append((prev, j))
                                me = prev
                                meme = prev
                                qul += 1
                                if j in rem:
                                    rem[j].append(int(meme))
                                else:
                                    aux = []
                                    aux.append(int(me))
                                    rem[j] = aux
                                # compare with the next row to find the closest maximum
                                for k in range(j + 1, init2[-1]):
                                    if k in memory:
                                        if len(memory[k]) != 0:
                                            c1 = 0
                                            for sea in memory[k]:
                                                if sea + 3 >= me and sea - 3 <= me:
                                                    a.append((sea, k))
                                                    c1 = 1
                                                    meme = sea
                                                    me = sea
                                                    qul += 1
                                                    flse = 0
                                                    break
                                                elif sea + 6 >= me and sea <= me:
                                                    meme = sea
                                                    qul += 1
                                                    c1 = 1
                                                    me = ThomsonParabola._searchpoint(img, a, sea, k)
                                                    break
                                                else:
                                                    c1 = 2
                                            if c1 == 1:
                                                if k in rem:
                                                    rem[k].append(int(meme))
                                                else:
                                                    aux = []
                                                    aux.append(int(meme))
                                                    rem[k] = aux
                                                c1 = 0
                                            elif c1 == 2:
                                                me = ThomsonParabola._searchpoint(img, a, me, k)
                                                flse += 1
                                                if flse > wake:
                                                    break
                                        else:
                                            me = ThomsonParabola._searchpoint(img, a, me, k)
                                            flse += 1
                                            if flse > wake:
                                                break
                                    else:
                                        me = ThomsonParabola._searchpoint(img, a, me, k)
                                        flse += 1
                                        if flse > wake:
                                            break
                                    if me > 1200:
                                        break
                                    if flse > wake and len(a) == wake:
                                        for l in range(wake):
                                            a.pop()

                                        break
                                # save the trace and the quality of the trace
                                trazas[counter] = a
                                quality[counter] = qul
                                if counter == 162:
                                    counter = counter
                                qul = 0
                                counter += 1
                                # remove the local maximum already used in this trace
                                for kk in rem.keys():
                                    for kkk in rem[kk]:
                                        if kkk in memory[kk]:
                                            memory[kk].remove(kkk)

                                # remove the traces with not enough quality
                                for a in quality.items():
                                    if a[1] < qualit:
                                        trazas.pop(a[0], None)
                # save proccess
                c3 = 0
                for trazalist in trazas.keys():
                    trazasarray = trazas[trazalist]

                    # save one file for each trace
                    pathoutputtext2 = os.path.join(pathoutputtext, filename)

                    # create path
                    if not os.path.exists(pathoutputtext2):
                        os.makedirs(pathoutputtext2)
                    nam = "Traza" + str(c3) + ".csv"

                    # write csv and prepare the other outputs
                    with open(os.path.join(pathoutputtext2, nam), 'w') as writer:
                        for l in range(len(trazasarray) - 1):
                            clone3 = cv2.line(clone3, trazasarray[l], trazasarray[l + 1], colours[c3], 4)
                            clone4 = cv2.line(clone4, trazasarray[l], trazasarray[l + 1], 255, 3)
                            X = trazasarray[l][0]
                            Y = trazasarray[l][1]

                            Summa = int(original[Y, X - 2]) + int(original[Y, X - 1]) + int(original[Y, X]) + int(
                                original[Y, X + 1]) + int(original[Y, X + 2])
                            towrite = f"{X},{Y},{Summa}"
                            writer.write(towrite + "\n")

                    c3 += 1
                # save the other files
                cv2.imwrite(os.path.join(pathinputs, filename), clone)
                cv2.imwrite(os.path.join(pathoutputs, filename + "out.tiff"), clone3)
                cv2.imwrite(os.path.join(pathoutputsgray, filename + "out2.tiff"), clone2)
                cv2.imwrite(os.path.join(pathoutputsmask, filename + "mask.tiff"), clone4)
                print(filename + "  processed\n")

        # in case of fail the processed picturs are removed and the proccess is restarted
        except Exception as ex:
            print(ex)
            print(filename + "  fail\n")

            for f in removepictures:
                pictures.pop(f)
            # ThompsomParabolaImageprocessingV2(pathDestinationSelected,pictures,colours,threshold,wake,qualit)
            
class ToF():
    """ Interactive Time-of-Flight diagnostics.
    The class allows interactive work with data from a 1D Time-of-Flight detector. The interpretation of input waveforms is done relativistically. 
    
    Args:
        distance  (float,optional) : Source to detector distance in units of [m].
        waveform  (str,optional) : Absolute path to measurement in a waveform file.
        channel   (int,optional) : If more than one channel is contained in the waveform file,
            channel number `channel` is chosen for analyisis. Defaults to `1`.
        polarity  (int,optional) : Polarity is `+1` for positive amplitudes of peaks and `-1` else. 
            Defaults to `+1`.
    
    Attributes:
        signaltonoise (int) : Assumed signal to noise ratio, initializes to 3.
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
    
    Returns:
        Xrise (float) : Arrival time of X-rays with respect to the time base of the waveform, evaluated when the noise-filtered signal surpases signal to noise ratio, likely in units of [s].
        Xfall (float) : Time, with respect to the time base of the waveform, when signal of X-rays decayed under the signal to noise ratio, evaluated on the noise filtered trace, likely in units of [s].
        Prise (float) : Arrival time of Projectiles with respect to the time base of the waveform, evaluated when the noise-filtered signal surpases signal to noise ratio, likely in units of [s].
        Pfall (float) : Time, with respect to the time base of the waveform, when signal of Projectiles decayed under the signal to noise ratio, evaluated on the noise filtered trace, likely in units of [s].
        tof (:obj: ``numpy.array``) : Time of flight from source position to detector for all data-bins between Prise and Pfall.
        Gminus1 (:obj: ``numpy.array``) : Ratio of relativistic kinethic energy and rest mass energy (equals gamma-factor minus 1) for all data-bins between Prise and Pfall. For conversion to kinethic energy, multiply rest mass of species under regard.
        dN_dGminus1 (:obj: ``numpy.array``) : Detector signal in practical units of `dN/d(gamma-1)`, where N is in units of the amplitude of the measurement.
        dN_dGminus1_lowpass (:obj: ``numpy.array``) : Low pass of detector signal in practical units of `dN/d(gamma-1)`, where N is in units of the amplitude of the measurement.
        
    Note:
        The original data array is not part of the object after processing.
        
    Examples:
        The class can be used in a functional way

        ```python 
        from pyclpu import metrology
        spectrum = metrology.ToF(distance = 100, waveform = "path/to/data.csv", channel = 1)
        ```

        A more object oriented use case demonstrates how a run can be started after initialization

        ```python 
        from pyclpu import metrology

        tof_detector = metrology.ToF()
        tof_detector.distance = 100
        tof_detector.channel = 1
        tof_detector.polarity = -1

        tof_detector.waveform = "path/to/data.csv"

        tof_detector.analyse()
        tof_detector.show()
        ```
        returns a non-blocking plot that can be refreshed through further calls to `show()`.
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.polarity = 1
        self.signaltonoise = 3
        self.status = False
        # INTEGRITY
        if not hasattr(self, 'distance'):
            warning(self.__class__.__name__,"No source to detector distance defined, expect key `distance` as type `float`.")
        if not hasattr(self, 'waveform'):
            warning(self.__class__.__name__,"No source file defined for data, expect key `waveform` as type `str`.")
        if not hasattr(self, 'channel'):
            warning(self.__class__.__name__,"No source channel defined for data, expect key `channel` as type `int`.")
        # IN PLACE
        if hasattr(self, 'distance') and hasattr(self, 'waveform') and hasattr(self, 'channel'):
            self.__run__()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'distance'):
            error(self.__class__.__name__,"No source to detector distance defined, expect key `distance` as type `float`. DO NOTHING.",1169)
            self.status = False
            return None
        if not hasattr(self, 'waveform'):
            error(self.__class__.__name__,"No source file defined for data, expect key `waveform` as type `str`. DO NOTHING.",1169)
            self.status = False
            return None
        if not hasattr(self, 'channel'):
            warning(self.__class__.__name__,"No source channel defined for data, expect key `channel` as type `int`. Set `channel = 1`.")
            self.channel = 1
        # VARIABLES

        # METHODS

        # MAIN
        # load data
        trace = Waveform(wfm = wfmread(self.waveform), channel = self.channel)
        if trace.status == False:
            error(self.__class__.__name__,"Can not build trace from waveform data.",1160)
            self.status = False
            return None
        trace.vertical = trace.vertical * self.polarity
        # find arrival time of X-rays
        # a) with peak detection
        #    - find peaks in bandpass-corrected signal
        # Xtime = signal.find_peaks_cwt(trace.vertical, np.arange(1,self.typicalpeakwidth), min_snr = 3)
        # b) assuming clear rising edge (fast method, least accuracy)
        #    - calculate typical length of one "noise wave"
        for n in range(1,trace.vertical.size):
            if trace.vertical[n-1] < trace.vertical[n]:
                for m in range(n,trace.vertical.size):
                    if trace.vertical[m-1] > trace.vertical[m]:
                        noise_period = max(1,4 * (m-n))
                        break
        #    - calculate average noise level within typical length
        noise = np.sum(np.abs(trace.vertical[0:noise_period])) / noise_period
        #    - calculate moving average with a bin size equal to the typical length
        ret = np.cumsum(trace.vertical, dtype=float)
        ret[noise_period:] = ret[noise_period:] - ret[:-noise_period]
        moving_average = np.zeros(np.shape(ret))
        moving_average[int(noise_period/2) - 1:-int(noise_period/2)] = ret[noise_period - 1:] / noise_period
        #    - get tips which are above the noise (i.e. noise multiplied with signal to noise ratio)
        tips = np.where(moving_average > self.signaltonoise * noise)[0]
        #    - get rising edge as first element of the first tip
        try:
            self.Xrise = trace.horizontal[tips[0]]
        except:
            error(self.__class__.__name__,"Can not find X-ray peak from waveform data.",1160)
            self.status = False
            return None
        #    - get falling edge as last element of the first tip
        for n,t in enumerate(tips):
            self.Xfall = trace.horizontal[t]
            if tips[n+1] != t + 1:
                break
        # find slower projectiles (if there is no gap between X-rays and projectiles, maybe there is a problem with leaking electrons)
        try:
            N_Prise = tips[n+1]
            N_Pfall = tips[-1]
            self.Prise = trace.horizontal[N_Prise]
            self.Pfall = trace.horizontal[N_Pfall]
        except:
            warning(self.__class__.__name__,"Detect no gap between X-ray peak and peak of massive projectiles. See plot and tune, e.g. signal to noise ratio. Exits after pop-up window is closed.")
            plt.plot(moving_average)
            plt.plot(trace.vertical)
            plt.hlines([tips[0],tips[n]])
            plt.show()
            return None
        # transform time base to base in units of kinetic-energy/rest-mass-energy for times larger than Ptime (ratio equal to gamma - 1)
        tof = trace.horizontal[N_Prise:N_Pfall] - self.Xrise + self.distance / constants.speed_of_light
        T_m = 1./np.sqrt(1. - (self.distance/constants.speed_of_light/tof)**2) - 1.
        # transform the signal amplitude in spectral counts (so far without multiplying a calibration factor)
        dT_dt = (T_m[1:]-T_m[:-1])/(tof[1:]-tof[:-1])
        dT_dt = np.append(dT_dt, [dT_dt[-1]])
        dN_dT = trace.vertical[N_Prise:N_Pfall] / ( - dT_dt)
        dN_dT_lowpass = moving_average[N_Prise:N_Pfall] / ( - dT_dt)
        # publication
        self.tof = tof
        self.Gminus1 = T_m
        self.dN_dGminus1 = dN_dT
        self.dN_dGminus1_lowpass = dN_dT_lowpass
        # integrity of results
        if isinstance(dN_dT,np.ndarray):
            self.status = True
        else:
            message(self.__class__.__name__,"Output stream invalid.")
            self.status = False
        # housekeeping
        del noise, trace, moving_average, tof, T_m, dT_dt, dN_dT, dN_dT_lowpass
        return None
    def analyse(self):
        # START
        self.__run__()
    def show(self):
        if self.status:
            # use open frame or create new
            new_plt_id = True
            try:
                if hasattr(self, 'plot'):
                    if "num" in self.plot.keys():
                        if plt.fignum_exists(self.plot['num']):
                            fig = self.plot['fig']
                            ax0 = self.plot['axs']
                            ax0.clear()
                            new_plt_id = False
                            plt.figure(fig.number)
            except:
                pass
            if new_plt_id:    
                plt.ion()
                fig = plt.figure(figsize=(15,10), dpi=100)
                ax0 = fig.add_subplot()
                self.plot = {}
                self.plot['num'] = fig.number
                self.plot['fig'] = fig
                self.plot['axs'] = ax0
            # plotting
            ax0.plot(self.Gminus1,self.dN_dGminus1,label="data spectrum")
            ax0.plot(self.Gminus1,self.dN_dGminus1_lowpass,label="lowpass spectrum")
            ax0.legend()
            plt.tight_layout()
            # display
            if new_plt_id:
                plt.show()
                plt.pause(1.001)
            else:
                plt.draw()
                plt.pause(0.201)