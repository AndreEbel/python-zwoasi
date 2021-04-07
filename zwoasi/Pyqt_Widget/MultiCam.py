# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:58:44 2021

@author: ebel
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout
import zwoasi as asi

from .DisplayAdvanced import DisplayAdvanced_base
from zwoasi.videothread import VideoThread

class TwoCam(QWidget):
    def __init__(self, w = 2000, h =2000, b=1):
        super().__init__()
        
        self.cam1 = asi.Camera(0)
        self.cam2 = asi.Camera(1)
        self.cam1.set_roi(width= w,
                          height = h,
                          bins = b)
        self.cam2.set_roi(width= w,
                          height = h,
                          bins = b)
        self.vt1 = VideoThread(self.cam1)
        self.vt2 = VideoThread(self.cam2)
        self.w1 = DisplayAdvanced_base(self.vt1, 500, 500, 'Camera 1')
        self.w2 = DisplayAdvanced_base(self.vt2, 500, 500, 'Camera 2')
        hbox = QHBoxLayout()
        hbox.addWidget(self.w1)
        hbox.addWidget(self.w2)
        self.setLayout(hbox)
        
    def closeEvent(self, event):
        
        print('trying to close properly')
        if self.vt1.camera.ready: 
            self.vt1.stop()
            print('stopping camera 1')
            #self.vt1.camera.close()
        if self.vt2.camera.ready: 
            self.vt2.stop()
            print('stopping camera 2')
            #self.vt2.camera.close()

        event.accept()   
   