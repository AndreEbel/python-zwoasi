# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:04:32 2021

@author: ebel
"""

from .Display2 import Display2_base

from PyQt5.QtWidgets import QLineEdit, QWidget,QLabel,QHBoxLayout,QVBoxLayout, QPushButton
from PyQt5.QtGui import QIntValidator
#import cv2
import tifffile
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
from time import time_ns, sleep
import os

class DisplaySave_base(Display2_base):
    metadata = {}
    def __init__(self, VideoThread, w, h, title, verbose):
        super().__init__(VideoThread,  w, h, title, verbose)
        
        self.save_status = QLabel('No frame')
        self.info_box.addWidget(self.save_status)
        #self.tabs.adjustSize()
        # Add tabs
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Save options")
        self.tab1.layout = QVBoxLayout()
        #self.tab1.layout.addStretch(1)
        
        # 3rd row: Set filename and save button
        self.filename = None
        self.filename_input = QLineEdit()
        self.filename_input.setAlignment(Qt.AlignRight)
        self.name_button = QPushButton('Set filename',self)
        self.name_button.clicked.connect(self.ClickSetName)
        self.textLabel2 = QLabel('No video')
        self.save_button = QPushButton('Save frame',self)
        self.save_button.clicked.connect(self.ClickSaveFrame)
        
        hbox2 = QHBoxLayout()
        #hbox2.addStretch(1)
        hbox2.addWidget(self.filename_input)
        hbox2.addWidget(self.name_button)
        hbox2.addWidget(self.textLabel2)
        hbox2.addWidget(self.save_button)
        
        # 4th row: Set period and record button
        self.period =None
        self.period_input = QLineEdit()
        self.period_input.setValidator(QIntValidator())
        self.period_input.setMaxLength(4)
        self.period_input.setAlignment(Qt.AlignRight)
        self.period_button = QPushButton('Set period',self)
        self.period_button.clicked.connect(self.ClickSetPeriod)
        self.textLabel3 = QLabel('No video')
        self.record_button = QPushButton('Start recording',self)
        self.record_button.clicked.connect(self.ClickStartRecording)
              
        hbox3 = QHBoxLayout()
        #hbox3.addStretch(1)
        hbox3.addWidget(self.period_input)
        hbox3.addWidget(self.period_button)
        hbox3.addWidget(self.textLabel3)
        hbox3.addWidget(self.record_button)
        
        # Add the new function to the layout  
        
        self.tab1.layout.addLayout(hbox2)
        self.tab1.layout.addLayout(hbox3)
        self.tab1.setLayout(self.tab1.layout)
        
        #self.settings_box.addWidget(self.tabs)
        # refresh the widget layout
        self.setLayout(self.vbox)
        
        # add flags
        self.saving = False
        self.recording = False
   
    @pyqtSlot(np.ndarray)
    def save_image(self, img):
        """
        save image as a tiff file with metadata

        Parameters
        ----------
        img : 2D numpy array
            image data 
        extra_metadata : dict, optional
            dictionnary where the extra metadata to be stored in the tiff file is passed. 
            The default is None.

        Returns
        -------
        None.

        """
        name = self.dir + self.filename + f'_{time_ns()}.png'
        metadata = {'time': str(time_ns())}
        if self.metadata != None: 
            metadata.update(self.metadata)
        if self.verbose: 
            print(f'saving {name}')
        tifffile.imwrite(name, img, metadata= metadata)
        #cv2.imwrite(name, img)
        if self.verbose:     
            print('image saved')
        self.display_thread.save = False  
        if not self.display_thread.record:
            self.textLabel2.setText('Ready to save frame')  
            
    # Activates when Start/Stop video button is clicked to Start (ss_video
    def ClickStartVideo(self):
        super().ClickStartVideo()
       
        # update labels
        self.save_status.setText('No save parameters')
        self.textLabel2.setText('Filename required')
        self.textLabel3.setText('Period (s) required')
        self.display_thread.save_frame.connect(self.save_image)
        
    
    # Activates when Start/Stop video button is clicked to Stop (ss_video)
    def ClickStopVideo(self):
        super().ClickStopVideo()
        self.display_thread.save_frame.disconnect()
        
        # update labels
        self.save_status.setText('No frame')
        self.textLabel2.setText('No video')
        self.textLabel3.setText('No video')
        
    def ClickSetName(self):
        if self.filename_input.text(): 
            self.filename = self.filename_input.text()
            self.save_status.setText('Ready to record')
            self.textLabel2.setText('Ready to save frame')
            if self.verbose: 
                print(self.filename)
        else: 
            if self.verbose: 
                print('no input')
        
    def ClickSetPeriod(self):
        if self.period_input.text(): 
            self.period = int(self.period_input.text())
            self.save_status.setText('Ready to record continuously')
            self.textLabel3.setText('Ready to record multiple frames')
            if self.verbose: 
                print(self.period)
        else: 
            if self.verbose: 
                print('no input')
        
    def ClickSaveFrame(self):         
        print('saved pressed')
        if self.display_thread.camera.ready:
            if self.filename: 
                #self.saving = True
                # update labels
                self.save_status.setText('Saving frame')
                self.textLabel2.setText('Saving frame')
                self.dir = os.getcwd()+'\\'
                self.display_thread.save = True    

            else: 
                self.textLabel2.setText('No valid filename')
        else: 
            self.textLabel2.setText('No video')
            
    def ClickStartRecording(self): 
        if self.verbose: 
            print('recording pressed')
        if self.display_thread.camera.ready:
            if self.filename: 
                if self.period:
                    if self.verbose: 
                        print('recording ok')
                    self.record_button.clicked.disconnect(self.ClickStartRecording)
                    self.display_thread.record_period = self.period
                    
                    # check if folder exist or create it 
                    self.dir = os.getcwd()+'\\'+self.filename + '\\'
                    try: 
                        os.mkdir(self.dir)
                    except: 
                        pass 
                    if self.verbose: 
                        print('folder ok')
                    self.display_thread.record = True
                    # update labels
                    #self.textLabel1.setText('Saving frames')
                    self.save_status.setText('Saving frames')
                    self.textLabel3.setText('Saving frames')
                    # Change button to stop
                    self.record_button.setText('Stop recording')
                    # Stop the video if button clicked
                    self.record_button.clicked.connect(self.ClickStopRecording)
                else: 
                    self.save_status.setText('No valid period')
                    self.textLabel3.setText('No valid period')
            else: 
                self.save_status.setText('No valid filename')
                self.textLabel3.setText('No valid filename') 
        else: 
            self.save_status.setText('No video')
            self.textLabel3.setText('No video')
        
    def ClickStopRecording(self): 
        self.record_button.clicked.disconnect(self.ClickStopRecording)
        self.display_thread.save = False
        self.display_thread.record = False
        self.video_status.setText('Video running')
        self.save_status.setText('Recording stopped')
        self.textLabel3.setText('Recording thread stopped')
        sleep(0.1)
        if self.display_thread.camera.ready:
            if self.filename: 
                if self.period:
                    self.save_status.setText('Ready to record')
                    self.textLabel3.setText('Ready to record')
                else: 
                    self.save_status.setText('No valid period')
                    self.textLabel3.setText('No valid period')
            else: 
                self.save_status.setText('No valid filename')
                self.textLabel3.setText('No valid filename') 
        else: 
            self.save_status.setText('No video')
            self.textLabel3.setText('No video')
        # Change button to start
        self.record_button.setText('Start recording')
        # Start the video if button clicked
        self.record_button.clicked.connect(self.ClickStartRecording)
        
class DisplaySave(DisplaySave_base):
    def __init__(self, VideoThread, w, h, verbose = False):
        super().__init__(VideoThread,  w, h, "Zwo camera display", verbose)
    def closeEvent(self, event):
        if self.display_thread.camera.ready: 
            self.display_thread.stop()
            try: 
                self.display_thread.camera.close()
            except: 
                print('camera already closed')
        if self.display_thread.camera.closed:
            print('closing')
            self.closed = True
            event.accept()        