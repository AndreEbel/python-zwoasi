
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
        if b: 
            if b in Cam.get_camera_property()['SupportedBins']: 
                bins = int(b)
        else:
            bins = 1
        if w: 
            if w < int(Cam.get_camera_property()['MaxWidth']/bins): 
                width = int(w)
            else: 
                width = int(Cam.get_camera_property()['MaxWidth']/bins)
        else: 
            width = int(Cam.get_camera_property()['MaxWidth']/bins)
            
        if h: 
            if h < int(Cam.get_camera_property()['MaxHeight']/bins): 
                height = int(h)
            else: 
                height = int(Cam.get_camera_property()['MaxHeight']/bins)
        else: 
            height  = int(Cam.get_camera_property()['MaxHeight']/bins)
        width -= width % 8  # Must be a multiple of 8
        height -= height % 8  # Must be a multiple of 8
        print(width, height, bins)
        Cam.set_roi(width =width,
                    height = height,
                    bins= bins)
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
        if b: 
            if b in Cam.get_camera_property()['SupportedBins']: 
                bins = b
        else:
            bins = 1
        if w: 
            if w < (Cam.get_camera_property()['MaxWidth'])/bins: 
                width = w
            else: 
                width = (Cam.get_camera_property()['MaxWidth'])/bins
        else: 
            width = Cam.get_camera_property()['MaxWidth']/bins
        if h: 
            if h < (Cam.get_camera_property()['MaxHeight'])/bins: 
                height = h 
            else: 
                height = (Cam.get_camera_property()['MaxHeight'])/bins
        else: 
            height  = Cam.get_camera_property()['MaxHeight']/bins
        width -= width % 8  # Must be a multiple of 8
        height -= height % 8  # Must be a multiple of 8
        print(width, height, bins)
        Cam.set_roi(width,
                    height,
                    bins)
    Video = VideoThread(Cam)
    a = DisplayAdvancedHist(Video, 100, 100)
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

def ZwoTwoCam(w = 2000, h =2000, b=1):
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    a = TwoCam(w , h , b)
    a.show()
    #app.aboutToQuit.connect(a.closeCameras)
    app.exec_()
   