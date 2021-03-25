# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:04:32 2021

@author: ebel
"""

from .Display import Display_base

from PyQt5.QtWidgets import QLineEdit, QLabel,QHBoxLayout, QPushButton
from PyQt5.QtGui import QIntValidator
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
from time import time_ns, sleep
import os

class DisplaySave_base(Display_base):
    def __init__(self, VideoThread, w, h):
        super().__init__(VideoThread,  w, h)
      
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
        hbox2.addStretch(1)
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
        hbox3.addStretch(1)
        hbox3.addWidget(self.period_input)
        hbox3.addWidget(self.period_button)
        hbox3.addWidget(self.textLabel3)
        hbox3.addWidget(self.record_button)
        
        # Add the new function to the layout       
        self.settings_box.addLayout(hbox2)
        self.settings_box.addLayout(hbox3)

        # refresh the widget layout
        self.setLayout(self.vbox)
        
        # add flags
        self.saving = False
        self.recording = False
   
    @pyqtSlot(np.ndarray)
    def save_image(self, cv_img):
        """
        """
        name = self.dir + self.filename + f'_{time_ns()}.png'
        print(f'saving {name}')
        cv2.imwrite(name, cv_img)
        print('image saved')
        self.display_thread.save = False  
        if not self.display_thread.record:
            self.textLabel2.setText('Ready to save frame')  
    
    # Activates when Start/Stop video button is clicked to Start (ss_video
    def ClickStartVideo(self):
        super().ClickStartVideo()
       
        # update labels
        self.textLabel2.setText('Filename required')
        self.textLabel3.setText('Period (s) required')
        self.display_thread.save_frame.connect(self.save_image)
        
    
    # Activates when Start/Stop video button is clicked to Stop (ss_video)
    def ClickStopVideo(self):
        super().ClickStopVideo()
        self.display_thread.save_frame.disconnect()
        
        # update labels
        self.textLabel2.setText('No video')
        self.textLabel3.setText('No video')
        
    def ClickSetName(self):
        self.filename = self.filename_input.text()
        self.textLabel2.setText('Ready to save frame')
        print(self.filename)
        
    def ClickSetPeriod(self):
        self.period = int(self.period_input.text())
        self.textLabel3.setText('Ready to record multiple frames')
        print(self.period)
        
    def ClickSaveFrame(self):         
        print('saved pressed')
        if self.display_thread.camera.ready:
            if self.filename: 
                #self.saving = True
                # update labels
                self.textLabel2.setText('Saving frame')
                self.dir = os.getcwd()+'\\'
                self.display_thread.save = True    

            else: 
                self.textLabel2.setText('No valid filename')
        else: 
            self.textLabel2.setText('No video')
            
    def ClickStartRecording(self): 
        
        print('recording pressed')
        if self.display_thread.camera.ready:
            if self.filename: 
                if self.period:
                    print('recording ok')
                    self.record_button.clicked.disconnect(self.ClickStartRecording)
                    self.display_thread.record_period = self.period
                    
                    # check if folder exist or create it 
                    self.dir = os.getcwd()+'\\'+self.filename + '\\'
                    try: 
                        os.mkdir(self.dir)
                    except: 
                        pass 
                    print('folder ok')
                    self.display_thread.record = True
                    # update labels
                    self.textLabel3.setText('Saving frames')
                    # Change button to stop
                    self.record_button.setText('Stop recording')
                    # Stop the video if button clicked
                    self.record_button.clicked.connect(self.ClickStopRecording)
                else: 
                    self.textLabel3.setText('No valid period')
            else: 
                self.textLabel3.setText('No valid filename') 
        else: 
            self.textLabel3.setText('No video')
        
    def ClickStopRecording(self): 
        self.record_button.clicked.disconnect(self.ClickStopRecording)
        self.display_thread.save = False
        self.display_thread.record = False
        self.textLabel3.setText('Recording thread stopped')
        sleep(0.1)
        self.textLabel3.setText('Ready to record')
        # Change button to start
        self.record_button.setText('Start recording')
        # Start the video if button clicked
        self.record_button.clicked.connect(self.ClickStartRecording)
        
class DisplaySave(DisplaySave_base):
    def __init__(self, VideoThread, w, h):
        super().__init__(VideoThread,  w, h)
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