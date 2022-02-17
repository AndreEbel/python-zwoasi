__version__ = '2'

import sys

from .pyzwoasi import ZWO_Error, get_num_cameras, list_cameras, Camera, init, zwolib
from .pyefw import EFW_Error, EFW, init, efwlib

try:
    init() # Initialize library on import, will only run once.
except ZWO_Error as e:
    print("Warning: " + str(e), file=sys.stderr)
    
from . import Pyqt_Widget
from . import Pyqt_App 