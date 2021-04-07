
import zwoasi as asi
from zwoasi.Pyqt_Widget import Display, DisplaySave, DisplayAdvanced, DisplayAdvancedHist, TwoCam
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import sys

from zwoasi.videothread import VideoThread


def ZwoDisplay(cam_id=0):
    """
    Simple display with no settings 

    Parameters
    ----------
    cam_id : integer, optional
        Identification number of the camera. 
        The default is 0 if only one camera is connected
    """
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    cam = asi.Camera(cam_id)
    cam.set_roi(width=2000,
                height=2000,
                bins=1)
    Video = VideoThread(cam)
    a = Display(Video, 500, 500)
    a.show()
    app.exec_()
    
def ZwoDisplaySave(cam_id = 0):
    """
    Simple display with a save options 

    Parameters
    ----------
    cam_id : integer, optional
        Identification number of the camera. 
        The default is 0 if only one camera is connected
    """
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    Cam = asi.Camera(cam_id)
    Cam.set_roi(width=1000,
                height=1000,
                bins=2)
    Video = VideoThread(Cam)
    a = DisplaySave(Video, 500, 500)
    a.show()
    app.exec_()
    
def ZwoDisplayAdvanced(cam_id = 0, w = 2000, h =2000, b=1):
    """
    Camera display with save options and exposure/gain settings 

    Parameters
    ----------
    cam_id : integer, optional
        Identification number of the camera. 
        The default is 0 if only one camera is connected
    """
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    Cam = asi.Camera(cam_id)
    if cam_id != None:
        
        Cam.set_roi(width =w,
                    height = h,
                    bins= b)
    Video = VideoThread(Cam)
    a = DisplayAdvanced(Video,200, 200)
    a.show()
    app.exec_()
    
def ZwoDisplayAdvancedHist(cam_id = 0, w = 2000, h =2000, b=1):
    """
    Camera display with: 
        - save options
        - exposure/gain settings 
        - live histogram
    
    Parameters
    ----------
    cam_id : integer, optional
        Identification number of the camera. 
        The default is 0 if only one camera is connected
    """
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    Cam = asi.Camera(cam_id)
    if cam_id != None:
        
        Cam.set_roi(width = w,
                    height = h,
                    bins = b)
    Video = VideoThread(Cam)
    a = DisplayAdvancedHist(Video, 100, 100)
    a.show()
    app.exec_()  

def ZwoTwoCam(w = 2000, h =2000, b=1):
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    a = TwoCam(w , h , b)
    a.show()
    app.exec_()
   