# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:03:02 2021

@author: ebel
"""

from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
from time import sleep, time_ns


class VideoThread(QThread):
    exposure = None
    gain = None
    auto_exp = False
    save = False
    record = False
    display = False
    display_frame = pyqtSignal(np.ndarray)
    save_frame = pyqtSignal(np.ndarray)
    
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        # capture from web cam
        self.camera.set_camera()
        t_save = -1e30
        while self.camera.display:
            # recording
            if self.record:
                t_i = time_ns()
                if (t_i-t_save)*1e-9 > self.record_period:
                    self.save = True
            
            # autoexposure off
            if not self.auto_exp:
                if self.exposure:
                    self.camera.set_exp()
                if self.gain:
                    self.camera.set_gain()
            
            cv_img = self.camera.get_frame()
            self.display_frame.emit(cv_img)
            if self.save:
                self.save_frame.emit(cv_img)
                if self.record:
                    t_save = t_i
                self.save = False
            sleep_time = np.max([self.camera.exposure*1e-6, 1/self.camera.fps])
            sleep(sleep_time)
        # shut down capture system
        self.camera.close()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.camera.display = False
        self.wait()