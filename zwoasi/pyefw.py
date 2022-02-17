import ctypes as c
import sys
from ctypes.util import find_library

# Returned error code
# _EFW_ERROR_CODE = {EFW_SUCCESS = 0,
#                     EFW_ERROR_INVALID_INDEX,
#                     EFW_ERROR_INVALID_ID,
#                     EFW_ERROR_INVALID_VALUE,
#                     EFW_ERROR_CLOSED, #not opened
#                     EFW_ERROR_REMOVED, #failed to find the filter wheel, maybe the filter wheel has been removed
#                     EFW_ERROR_MOVING,#filter wheel is moving
#                     EFW_ERROR_GENERAL_ERROR,#other error
#                     EFW_ERROR_CLOSED,
#                     EFW_ERROR_END = -1
#                     }

class EFW_Error(Exception):
    """
    Exception class for errors returned from the :mod:`zwoasi` module.
    """
    def __init__(self, message):
        Exception.__init__(self, message)


class EFW_IOError(EFW_Error):
    """
    Exception class for all errors returned from the ASI SDK library.
    """
    def __init__(self, message, error_code=None):
        EFW_Error.__init__(self, message)
        self.error_code = error_code
# Mapping of error numbers to exceptions. Zero is used for success.

class EFW_CaptureError(EFW_Error):
    """
    Exception class for when :func:`Camera.capture()` fails.
    """
    def __init__(self, message, exposure_status=None):
        EFW_Error.__init__(self, message)
        self.exposure_status = exposure_status

efw_errors = [None,
              EFW_IOError('Invalid index', 1),
              EFW_IOError('Invalid ID', 2),
              EFW_IOError('Invalid value', 3),
              EFW_IOError('EFW closed', 4),
              EFW_IOError('EFW removed', 5),
              EFW_IOError('Moving', 6),
              EFW_IOError('General error', 7),
              EFW_IOError('End', 8)
              ]


# Filter wheel information
class _EFW_INFO(c.Structure):
    _fields_ = [
        ('ID', c.c_int),
        ('Name', c.c_char * 64),
        ('slotNum', c.c_int)
        ]
    
    def get_dict(self):
        r = {}
        for k, _ in self._fields_:
            v = getattr(self, k)
            if sys.version_info[0] >= 3 and isinstance(v, bytes):
                v = v.decode()
            r[k] = v
        return r

def init(library_file): 

    if library_file is None:
        library_file = find_library('EFW_filter')
    if library_file is None:
        raise EFW_Error('EFW SDK library not found')

    efwlib = c.cdll.LoadLibrary(library_file)

    efwlib.EFWGetNum.argtypes = []
    efwlib.EFWGetNum.restype = c.c_int

    efwlib.EFWGetID.argtypes = [c.c_int, c.POINTER(c.c_int)]
    efwlib.EFWGetID.restype = c.c_int

    efwlib.EFWGetProperty.argtypes = [c.c_int, c.POINTER(_EFW_INFO)]
    efwlib.EFWGetProperty.restype = c.c_int

    efwlib.EFWOpen.argtypes = [c.c_int]
    efwlib.EFWOpen.restype = c.c_int

    efwlib.EFWGetPosition.argtypes = [c.c_int, c.POINTER(c.c_int)]
    efwlib.EFWGetPosition.restype = c.c_int

    efwlib.EFWSetPosition.argtypes = [c.c_int, c.c_int]
    efwlib.EFWSetPosition.restype = c.c_int

    efwlib.EFWSetDirection.argtypes = [c.c_int, c.c_bool]
    efwlib.EFWSetDirection.restype = c.c_int

    efwlib.EFWGetDirection.argtypes = [c.c_int, c.c_bool]
    efwlib.EFWGetDirection.restype = c.c_int

    efwlib.EFWClose.argtypes = [c.c_int]
    efwlib.EFWClose.restype = c.c_int

    efwlib.EFWGetProductIDs.argtypes = [c.POINTER(c.c_int)]
    efwlib.EFWGetProductIDs.restype = c.c_int

    efwlib.EFWCalibrate.argtypes = [c.c_int]
    efwlib.EFWCalibrate.restype = c.c_int

    return efwlib

class EFW(object): 
    
    def __init__(self, library_file = None): 
        self.dll = init(library_file)

    def GetNum(self): 
        return self.dll.EFWGetNum()


    def GetID(self, num): 
        ID = c.c_int
        r = self.dll.EFWGetID(num, ID)
        if r:
            raise efw_errors[r]
        return ID

    def GetProperty(self, ID): 
        props = _EFW_INFO
        r = self.dll.EFWGetProperty(ID, props)
        if r:
            raise efw_errors[r]
        return props.get_dict()

    def Open(self, ID): 
        r = self.dll.EFWOpen(ID)
        if r:
            raise efw_errors[r]
    
    def Close(self, ID): 
        r = self.dll.EFWClose(ID)
        if r:
            raise efw_errors[r]

    def GetPosition(self, ID): 
        slot = c.c_int
        r = self.dll.EFWGetPosition(ID, slot)
        if r:
            raise efw_errors[r]
        return slot

    def SetPosition(self, ID, slot): 
        r = self.dll.EFWSetPosition(ID, slot)
        if r:
            raise efw_errors[r]
    
    def GetDirection(self, ID): 
        direction = c.c_bool
        r = self.dll.EFWGetDirection(ID, direction)
        if r:
            raise efw_errors[r]
        return direction
    
    def SetDirection(self, ID, direction): 
        r = self.dll.EFWSetDirection(ID, direction)
        if r:
            raise efw_errors[r]
    
    def GetProductIDs(self): 
        self.dll.EFWGetProductIDs()
    

