
import zwoasi as asi
from zwoasi.Pyqt_Widget import Display, DisplaySave, DisplayAdvanced, DisplayAdvancedHist, MultiCam, TwoCam
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
    
def ZwoDisplayAdvanced(cam_id = 0):
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
    Cam.set_roi(width=1000,
                height=1000,
                bins=2)
    Video = VideoThread(Cam)
    a = DisplayAdvanced(Video,500, 500)
    a.show()
    app.exec_()
    
def ZwoDisplayAdvancedHist(cam_id = 0):
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
    Cam.set_roi(width=1000,
                height=1000,
                bins=2)
    Video = VideoThread(Cam)
    a = DisplayAdvancedHist(Video, 500, 500)
    a.show()
    app.exec_()  

def MultiWidget(widgets): 
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    a = MultiCam(widgets)
    a.show()
    app.exec_()
    
    
def ZwoMultiCam(cam_ids = None, verbose = False):
    """
    Display multiple camera with save options and exposure/gain settings for each camera
    
    Parameters
    ----------
    cam_ids : list of integer, optional
        Identification numbers of the cameras to be displayed. 
        if None, all camera will be displayed
    """
    if verbose:
        print('hello, cam_ids = ', cam_ids)
    cams = []
    vids = []
    if cam_ids: 
        if verbose:
            print('get selcted cameras')
        for cam_id in cam_ids:
            cam = asi.Camera(cam_id)
            cams.append(cam)
    else: 
        if verbose:
            print('get all connected cameras', asi.get_num_cameras())
        cam = asi.Camera(cam_id = 0)
        cams.append(cam)
        #cams.append(asi.Camera(cam_id = 1))
            
        # for cam_id in range(asi.get_num_cameras()):
        #     if verbose:
        #         print(cam_id)   
        #     cams.append(asi.Camera(cam_id = cam_id))
        #     if verbose:
        #         print('ok', cam_id)
    if verbose:
        print(f'we have {len(cams)} cameras')
    for cam in cams:
        cam.set_roi(width=1000,
                    height=1000,
                    bins=2)
        vids.append(VideoThread(cam))
    if verbose:
        print(f'we have {len(vids)} videothreads')    
    widgets = []
    for vid in vids: 
        widgets.append(
             Display(vid, 500, 500)
            )
    if verbose:
        print(f'we have {len(widgets)} widgets')  
    
    MultiWidget(widgets)

def ZwoTwoCam():
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    a = TwoCam()
    a.show()
    #app.aboutToQuit.connect(a.closeCameras)
    app.exec_()
   