# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:58:44 2021

@author: ebel
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout
import zwoasi as asi

class MultiCam(QWidget):
    def __init__(self, widget_list):
        super().__init__()
      
        hbox = QHBoxLayout()
        for w in widget_list:
            hbox.addWidget(w)
        self.setLayout(hbox)

from .DisplayAdvanced import DisplayAdvanced_base
#from zwoasi.Pyqt_Widget import DisplayAdvanced
from zwoasi.videothread import VideoThread

class TwoCam(QWidget):
    def __init__(self):
        super().__init__()
        
        self.cam1 = asi.Camera(0)
        self.cam2 = asi.Camera(1)
        self.cam1.set_roi(width=1000,
                            height=1000,
                            bins=2)
        self.cam2.set_roi(width=1000,
                            height=1000,
                            bins=2)
        self.vt1 = VideoThread(self.cam1)
        self.vt2 = VideoThread(self.cam2)
        self.w1 = DisplayAdvanced_base(self.vt1, 500, 500)
        self.w2 = DisplayAdvanced_base(self.vt2, 500, 500)
        hbox = QHBoxLayout()
        hbox.addWidget(self.w1)
        hbox.addWidget(self.w2)
        self.setLayout(hbox)
        
    def closeCameras(self): 
        print(self.cam1.get_camera_property())
        print(self.cam2.get_camera_property())
        del self.cam1, self.cam2
        # print('trying to close camera 1')
        # self.cam1.close()
        # print('trying to close camera 2')
        # self.cam2.close()
        # print('all cameras are closed')
        
    def closeEvent(self, event):
        print('trying to close properly')
        if self.vt1.camera.ready: 
            self.vt1.stop()
            print('stopping camera 1')
        if self.vt2.camera.ready: 
            self.vt2.stop()
            print('stopping camera 2')
        
        # if not self.vt1.camera.ready:
        #     print('trying to close camera 1')
        #     self.vt1.camera.close()
        # if not self.vt2.camera.ready:
        #     print('trying to close camera 2')
        #     self.vt2.camera.close()
        
        #print('ok')
        # if self.vt1.camera.closed and self.vt2.camera.closed:
        #     print('closing window')
        event.accept()   
   