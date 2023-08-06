# -*- coding: utf-8 -*-
""" This is the CLPU module for waveform manipulation.

Please do only add or modify but not delete content.

requires explicitely {
 - os
 - sys
 - numpy
}

import after installation of pyclpu via {
  from pyclpu import waveform
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/waveform.py))
  sys.path.append(os.path.abspath(root))
  import waveform
  from importlib import reload 
  reload(waveform)
}

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNAL
import os
import sys
from inspect import getsourcefile
from importlib import reload

import math
import numpy as np

import matplotlib.pyplot as plt

# INTERNAL
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) # get environment
sys.path.append(os.path.abspath(root))                           # add environment
sys.path.append(os.path.abspath(root)+os.path.sep+"LIB")         # add library

if "constants" not in globals() or globals()['constants'] == False:
    import constants                        # import all global constants from                   constants.py
    import formats                          # import all global formats from                     formats.py
    from manager import error               # import error() from management                     manager.py
    from manager import message             # import message() from management                   manager.py
    from manager import warning             # import warning() from management                   manager.py
    from manager import give_extension      # import give_extension() from management            manager.py
    from manager import give_dirlst         # import give_dirlst() from management               manager.py
    reload(constants)
    reload(formats)

# STYLE

# =============================================================================
# CONSTANTS
# =============================================================================
# INTEGRATION AND TESTING
test = True

# PARAMETERS

# CONSTANTS

# =============================================================================
# METHODS
# =============================================================================
# INTEGRATION AND TESTING
def test_pingpong(*args, **kwargs):
    """ Tests functionality of functions. 
 
    Function prints any input.
 
    Args:
        `*args`   : Any number of positional arguments.
        `**kwargs`: Any number of named keyval arguments.
    
    Returns:
        exit_stat (bool) : True in case of success and False else.
    
    Examples:
        ```python
        test_pingpong(True,kwa=True)
        ```
        returns
        ```
        True
        kwa : True
        ```
    """
    try:
        for arg in args:
            print(arg)
        for key, value in kwargs.items():
            print(str(key) + " : "+ str(value))
    except:
        return False
    return True

# WAVEFORM T/I/O
def iswfm(path: str) -> bool:
    """ Checks for waveform file. 
 
    The function looks up if the argument of type string describes the path to a waveform file.
 
    Args:
        path (str) : The path which is to be checked.
    
    Returns:
        exit_stat (bool) : True in case there is an waveform file and False else.
    
    Examples:
        ```python
        iswfm("")
        ```
        returns
        ```
        False
        ```
        
    Todo:
        * accept waveform object as input as well
    """
    try:
        extension = give_extension(path)
        if extension in formats.acceptedinput["waveform"]:
            return True
        else:
            return False
    except:
        error(iswfm.__name__,"",code=1287)

def wfmread(path):
    """ Reads waveform file. 
 
    The function tries to read a waveform file to a numpy array as `[channel,amplitude,timebase]`.
 
    Args:
        path (str) : The path to a waveform file.
    
    Returns:
        wfm (:obj: `numpy.array`) : Matrix of values as ``[channel,amplitude,timebase]``
    """
    # METHODS
    def loader(from_file):
        if give_extension(from_file) == ".bin":
            try:
                from RSRTxReadBin import RTxReadBin
            except:
                path_to_module = os.path.join(*give_dirlst(root)[:-1],"lib","RTxReadBin-1.0-py3-none-any.whl")
                error(wfmread.__name__,"RTxReadBin not installed. Run pip install "+path_to_module,1169)
                return None
            # load all
            y, x, S = RTxReadBin(from_file)
            vertical = np.transpose(y[:,0,:]) # assume the zeroth acquisition to be the only one and build [channel,amplitude]
            #print(S['MultiChannelVerticalOffset'])
            horizontal = x
        else:
            # find data
            skiplines = 0
            with open(from_file, 'r') as file:
                lines = file.readlines()
            for number,line in enumerate(lines):
                try:
                    first_character = line.strip()[0]
                    if (first_character.isnumeric() or first_character == "-"):
                        skiplines = number
                        break
                except:
                    continue
            # load data
            try:
                contents = np.loadtxt(from_file,skiprows=skiplines)
            except:
                contents = np.genfromtxt(from_file,skip_header=skiplines,delimiter=",",filling_values=np.NaN)
                contents = contents[:, ~np.isnan(contents).any(axis=0)]
            # try to find timebase in first column or as constant
            if all(np.isclose(np.diff(contents[:,0]),np.diff(contents[:,0])[0])):
                horizontal = contents[:,0]
                vertical = np.transpose(contents[:,1:]) # build [channel,amplitude]
            else:
                vertical = np.transpose(contents) # build [channel,amplitude]
                # known exception: R&S
                timebase_known = False
                if ".wfm." in from_file.lower():
                    meta_file = from_file.lower().replace(".wfm.",".")
                    # known keywords
                    with open(meta_file, 'r') as file:
                        lines = file.readlines()
                    for line in lines:
                        if "resolution" in line.lower():
                            try:
                                find_increment = line.lower().replace("resolution","").strip().strip(":;,")
                                horizontal = np.arange(vertical.shape[1]) * np.float(find_increment)
                                timebase_known = True
                                break
                            except:
                                continue
                # unknown exception: manual input
                if not timebase_known:
                    ask_increment = input("Please enter the increment of timesteps in units of [s]:\n")
                    horizontal = np.arange(vertical.shape[1]) * np.float(ask_increment)
                # housekeeping
                del timebase_known
        return {"horizontal" : horizontal, "vertical" : vertical}
    # EXECUTE
    if iswfm(path):
        wfm = loader(path)
    else:
        return None
    if wfm["vertical"].ndim == 1:
        wfm["vertical"] =np.array([wfm["vertical"]])
    # RETURN
    if wfm is None: # happens if there is trouble with the waveform format or the path
        error(wfmread.__name__,"",code=667)
        return None
    else:
        return wfm
        
def wfmshow(wfm, *args, **kwargs):
    """ Displays waveform. 
 
    The function shows the content of a waveform.
 
    Args:
        wfm (:obj: `numpy.array`) : Wafeform array.
    
    Returns:
        exit_stat (bool) : True in case of a completed run and False else.
    
    Examples:
        ```python
        wfmshow("")
        ```
        returns
        ```
        False
        ```
    """
    name = kwargs.get('name', "ANONYMOUS")
    # Routine
    #try:
    for ai,active_channel in enumerate(wfm["vertical"]):
        plt.plot(wfm["horizontal"],active_channel,label=str(ai))
    plt.legend()
    plt.show()
    plt.close('all')
    return True
    #except:
    #    error(wfmshow.__name__,"",13)
    #    return False
 
def wfmwrite(full_name, wfm):
    """ Writes waveform array to disk.
    The function writes the content of a waveform array to a disk loaction.
    It also generates a plot that is saved next to the data.
    
    Args:
        full_name (str) : Absolute path and filename in one string.
        wfm (:obj: `numpy.array`) : Wafeform array.
    
    Returns:
        exit_stat (bool) : True in case of a completed run and False else.
    """
    try:
        # data
        output = [wfm["horizontal"]]
        for active_channel in enumerate(wfm["vertical"]):
            output.append(active_channel)
        np.savetxt(full_name, np.array(output).T, delimiter=",")
        # visual feedback
        for active_channel in enumerate(wfm["vertical"]):
            plt.plot(wfm["horizontal"],active_channel)
        plt.savefig(full_name+".png")
        plt.close('all')
        return True
    except:
        error(wfmwrite.__name__,"",13)
        return False
        
# WAVEFORM MANIPULATION

    
# =============================================================================
# CLASSES
# =============================================================================
# INTEGRATION AND TESTING
class Main:
    # https://realpython.com/python-class-constructor/
    def __new__(cls, *args, **kwargs):
        #1) Create from this class as cls a new instance of an object Main
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        #2) Initialize from the instance of an object Main as self the initial state of the object Main
        for arg in args:
            warning(self.__class__.__name__,"Object does not accept unnamed arguments! Ignore: "+str(arg))
        for key, value in kwargs.items():
            self.key = value
        return None
            
    def __setattr__(self, name, value):
        #3) Set attributes of the instance during runtime, e.g. to change the initial state
        #if name in self.__dict__:
        #    print("!!! Warning...........Call to __setattr__ overwrites value of "+str(name)+ " with "+str(value))
        super().__setattr__(name, value)
        return None

    def __repr__(self) -> str:
        #anytime) representation as string, e.g. for print()
        string = "(\n"
        for att in self.__dict__:
            string = string + str(att) + " -> " + str( getattr(self,att) ) + "\n"
        return str(type(self).__name__) + string + ")"

# MAIN OBJECT  
class Waveform():
    """ Waveform object.
    The class allows interaction with a waveform object.
    
    Args:
        wfm    (dict,optional) : Waveform source as dictionary ``{"horizontal": numpy.array, "vertical": numpy.array(*channels)}`` .
        channel (int,optional) : Channel of interest.
    
    Attributes:
        status (bool) : True if processing was successfull, else False.
            Initializes to False.
    
    Returns:
        horizontal (float) : Array with horizontal axis.
        vertical (float) : Array with vertical axis.
        
    Note:
        The source of the waveform is not part of the object after processing.
        
    Examples:
        The class holds the main object of the `waveform` module.

        ```python 
        from pyclpu import waveform
        wfm_1 = waveform.Waveform()
        ```
    """
    # INI
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.status = False
        # INTEGRITY
        if not hasattr(self, 'wfm'):
            warning(self.__class__.__name__,"No waveform source defined, expect key `waveform` as `waveform={'horizontal': numpy.array, 'vertical': numpy.array(*channels)}`.")
        if not hasattr(self, 'channel'):
            warning(self.__class__.__name__,"No source channel defined for data, expect key `channel` as type `int`.")
        # IN PLACE
        if hasattr(self, 'wfm') and hasattr(self, 'channel'):
            self.__run__()
        return None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if hasattr(self, 'wfm') and hasattr(self, 'channel'):
            if name in ["wfm","channel"]:
                self.__run__()
        return None
    def __run__(self):
        # INTEGRITY
        if not hasattr(self, 'wfm'):
            error(self.__class__.__name__,"No waveform source defined, expect key `waveform` as `waveform={'horizontal': numpy.array, 'vertical': numpy.array(*channels)}`. DO NOTHING.",1169)
            return None
        if not hasattr(self, 'channel'):
            warning(self.__class__.__name__,"No source channel defined for data, expect key `channel` as type `int`. Set `channel = 1`.")
            self.channel = 1
        # VARIABLES
        if self.wfm is None:
            error(self.__class__.__name__,"No valid waveform source defined, expect key `waveform` as `waveform={'horizontal': numpy.array, 'vertical': numpy.array(*channels)}`. DO NOTHING.",1169)
            return None
        self.horizontal = self.wfm["horizontal"]
        self.vertical = self.wfm["vertical"][self.channel-1]
        # MAIN
        # fourier transform etc.
        
        # integrity of results
        self.status = True
        # housekeeping
        del self.wfm
        return None


# =============================================================================
# PYTHON MAIN
# =============================================================================
# SELF AND TEST
if globals()["__name__"] == '__main__':
    # STARTUP
    print("START TEST OF CLPU IMAGE MODULE")
    print("!!! -> expect True ")
    # parse command line
    args = sys.argv
    # TESTS
    # (001) CONSTANTS
    print("\n(001) CONSTANTS")
    print(test)
    # (002) FUNCTION CALL
    print("\n(002) FUNCTION CALL")
    print(test_pingpong(True,kwa=True))
    # (003) CLASS INIT
    print("\n(003) CLASS INIT")
    test_class = Main(kwa=True)
    test_class.add = True
    print(test_class)
    del test_class
    