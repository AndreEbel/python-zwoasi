# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 06:21:29 2021

@author: ebel
"""

from .Pyqt_Widget import Display, DisplayAdvanced, DisplayAdvancedHist, MultiCam
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import sys

from .camera import ZwoCamera
from .videothread import VideoThread

import zwoasi as asi

def ZwoDisplay():

    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    Cam = ZwoCamera(id = 0 , width = 2000, height = 2000, fps = 10)
    Video = VideoThread(Cam)
    a = Display(Video, 500, 500)
    a.show()
    app.exec_()
    
def ZwoDisplaySave():

    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    Cam = ZwoCamera(id = 0 , width = 2000, height = 2000, fps = 10)
    Video = VideoThread(Cam)
    a = DisplaySave(Video, 500, 500)
    a.show()
    app.exec_()
    
def ZwoDisplayAdvanced():

    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    Cam = ZwoCamera(id = 0 , width = 2000, height = 2000, fps = 10)
    Video = VideoThread(Cam)
    a = DisplayAdvanced(Video,500, 500)
    a.show()
    app.exec_()
    
def ZwoDisplayAdvancedHist():
    
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    Cam = ZwoCamera(id = 0 , width = 2000, height = 2000, fps = 10)
    Video = VideoThread(Cam)
    a = DisplayAdvancedHist(Video, 500, 500)
    a.show()
    app.exec_()  

def ZwoMultiCam():
    cams = []
    vids = []
    for i in range(asi.get_num_cameras()):
        cams.append(
            ZwoCamera(id = i , width = 2000, height = 2000, fps = 10)
            )
    for cam in cams:
        vids.append(
            VideoThread(cam)
            )
        
    apps = []
    for vid in vids: 
        apps.append(
            DisplayAdvanced(vid, 500, 500)
            )
        
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    a = MultiCam(apps)
    a.show()
    app.exec_()