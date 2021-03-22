# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:04:32 2021

@author: ebel
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel,QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap,  QColor
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np

class Display(QWidget):
    def __init__(self, VideoThread, w, h):
        super().__init__()
        self.display_thread = VideoThread
        self.setWindowTitle("Qt live label demo")
        
        # 1st row: Display
        self.display_width = w
        self.display_height = h
        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.display_box =  QVBoxLayout()
        self.display_box.addWidget(self.image_label)
        
        # 2nd row: Start / stop button
        self.textLabel1 = QLabel('Ready to start')
        self.ss_video = QPushButton('Start video',self)
        self.ss_video.clicked.connect(self.ClickStartVideo)
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.textLabel1)
        hbox1.addWidget(self.ss_video)

        self.settings_box =  QVBoxLayout()
        self.settings_box.addLayout(hbox1)
        # create a vertical box layout
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.display_box)
        self.vbox.addLayout(self.settings_box)

        # set the vbox layout as the widgets layout
        self.setLayout(self.vbox)
        
        # flags
        self.started = False
        
        if self.started == False:
            # create a grey pixmap
            grey = QPixmap(self.display_width, self.display_height)
            grey.fill(QColor('darkGray'))
            # set the image image to the grey pixmap
            self.image_label.setPixmap(grey)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """
        Updates the image_label with a new opencv image
        """
        self.frame = cv_img
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    # Activates when Start/Stop video button is clicked to Start (ss_video
    def ClickStartVideo(self):
        self.ss_video.clicked.disconnect(self.ClickStartVideo)
        self.started = True
        
        # update labels
        self.textLabel1.setText('Video running')
        #self.textLabel2.setText('Filename required')
        #self.textLabel3.setText('Period (s) required')

        # Change button to stop
        self.ss_video.setText('Stop video')
        
        # start the thread
        self.display_thread.start()
        
        self.display_thread.display_frame.connect(self.update_image)
        #self.display_thread.save_frame.connect(self.save_image)
        # Stop the video if button clicked
        self.ss_video.clicked.connect(self.display_thread.stop)  
        self.ss_video.clicked.connect(self.ClickStopVideo)
    
    # Activates when Start/Stop video button is clicked to Stop (ss_video)
    def ClickStopVideo(self):
        self.display_thread.display_frame.disconnect()
        #self.display_thread.save_frame.disconnect()
        self.ss_video.clicked.disconnect(self.display_thread.stop)
        self.ss_video.clicked.disconnect(self.ClickStopVideo)
        
        self.ss_video.setText('Start video')
        self.textLabel1.setText('Ready to start')
        #self.textLabel2.setText('No video')
        #self.textLabel3.setText('No video')
        # Start the video if button clicked
        self.ss_video.clicked.connect(self.ClickStartVideo)
    
    def closeEvent(self, event):
        if self.display_thread.display: 
            self.display_thread.stop()
        self.display_thread.camera.close()
        event.accept()        