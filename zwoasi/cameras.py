# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 10:38:31 2021

@author: ebel
"""
import pyzwoasi as asi

class Camera:
    display = False
    
    def __init__(self, id , width = None, height = None, fps = 10, bins = 1): 
        self.camera_id = id
        self.width = width
        self.height = height
        self.fps = fps
        self.n_bins = bins 
        self.camera = None

class ZwoCamera(Camera):
        
    def set_camera(self):
        
        # initialization of the camera
        if not self.camera:
            self.camera = asi.Camera(self.camera_id)
        self.exposure = self.camera.get_control_value(asi.ASI_EXPOSURE)[0]
        self.gain = self.camera.get_control_value(asi.ASI_GAIN)[0]
        print(self.exposure, self.gain)
       
        self.camera.set_image_type(asi.ASI_IMG_RAW8)
        self.camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD,
                                      self.camera.get_controls()['BandWidth']['MinValue'])
        self.camera.set_roi(width=self.width,
                            height=self.height,
                            bins=self.n_bins)
        self.camera.start_video_capture()
        self.display = True
        
    def set_exp(self): 
        self.camera.set_control_value(asi.ASI_EXPOSURE, self.exposure, auto=False)
    def get_exp(self): 
        self.exposure = self.camera.get_control_value(asi.ASI_EXPOSURE)[0]
        #print('exp =', self.exposure)
        #return self.exposure
    def set_gain(self): 
        self.camera.set_control_value(asi.ASI_GAIN, self.gain, auto=False)
    def get_gain(self): 
        self.gain = self.camera.get_control_value(asi.ASI_GAIN)[0]
        #print('gain =', self.gain)
        #return self.gain
        
    def set_autoexp_on(self):
        auto = ('Exposure', 'Gain')
        for ctrl in auto:
            print(ctrl)
            controls = self.camera.get_controls()
            control_type = controls[ctrl]['ControlType']
            print(control_type)
            value = controls[ctrl]['DefaultValue']
            print(value)
            print(control_type, value)
            self.camera.set_control_value(control_type, value,auto=True)
            
    def set_autoexp_off(self):
        self.get_gain()
        self.set_gain()
        self.get_exp()
        self.set_exp()
    
    def get_frame(self):
        if self.display:
            self.get_exp()
            cv_img = self.camera.capture_video_frame(timeout = self.exposure + 500000)
            return cv_img
    
    def close(self):
        self.display = False
        self.camera.stop_video_capture()
        self.camera.close()
        del self.camera
        self.camera = None
    
