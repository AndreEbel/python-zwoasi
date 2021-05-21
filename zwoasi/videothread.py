from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
from time import sleep, time_ns


class VideoThread(QThread):
    auto_exp = False
    save = False
    record = False
    display_frame = pyqtSignal(np.ndarray)
    save_frame = pyqtSignal(np.ndarray)
    
    def __init__(self, camera, verbose = False):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.start_video_capture()
        # camera should be initialized before starting the thread
        t_save = -1e30
        while self.camera.ready and not self.camera.closed:
           
            # recording
            if self.record:
                t_i = time_ns()
                if (t_i-t_save)*1e-9 > self.record_period:
                    self.save = True
            
            # autoexposure off
            if not self.auto_exp:
                #print('not auto exp', self.camera.exposure, self.camera.gain)
                if self.camera.exposure:
                    self.camera.set_exp()
                if self.camera.gain:
                    self.camera.set_gain()
            
            cv_img = self.camera.capture_video_frame() #capture()
            self.display_frame.emit(cv_img)
            if self.save:
                self.save_frame.emit(cv_img)
                if self.record:
                    t_save = t_i
                self.save = False
            sleep(self.camera.exposure*1e-6)
            
        self.camera.stop_video_capture()
        
    def stop(self):
        """
        Sets ready flag to False and waits for thread to finish
        """
        self.camera.ready = False
        
        self.wait()