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

class Display_base(QWidget):
    closed = False
    def __init__(self, VideoThread, w, h, title):
        super().__init__()
        self.display_thread = VideoThread
        self.setWindowTitle(title)
        
        # 1st row: Display
        self.display_width = w
        self.display_height = h
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(self.display_width, self.display_height)
        self.image_label.adjustSize()
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.display_box =  QVBoxLayout()
        self.display_box.addWidget(self.image_label)
        #self.display_box.addStretch(1)
        
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
        #self.settings_box.addStretch()
        # create a vertical box layout
        self.vbox = QVBoxLayout()
       
        self.vbox.addLayout(self.display_box)
        #self.vbox.addStretch(1)
        self.vbox.addLayout(self.settings_box)

        # set the vbox layout as the widgets layout
        self.setLayout(self.vbox)
        
        # initialize the camera
        self.display_thread.camera.set_camera()
        # start the thread
        self.display_thread.start()
    

        # create a grey pixmap
        self.pixmap = QPixmap(100, 100)
        self.pixmap.fill(QColor('darkGray'))
        # set the image image to the grey pixmap
        self.image_label.setPixmap(self.pixmap.scaled(
                                                        self.image_label.width(),self.image_label.height(),
                                                        Qt.KeepAspectRatio, 
                                                        Qt.FastTransformation
                                                        )
            )
                                                    
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        #print(h, w, self.image_label.size())
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = QPixmap.fromImage(convert_to_Qt_format)
        return p
    
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """
        Updates the image_label with a new opencv image
        """
        self.frame = cv_img
        self.pixmap = self.convert_cv_qt(cv_img)
        #print(self.image_label.width(),self.image_label.height())
        self.image_label.setPixmap(self.pixmap.scaled(
            self.image_label.width(),self.image_label.height(),
            Qt.KeepAspectRatio, 
            Qt.FastTransformation))
    
    # Activates when Start/Stop video button is clicked to Start (ss_video
    def ClickStartVideo(self):
        self.ss_video.clicked.disconnect(self.ClickStartVideo)
        
        # update labels
        self.textLabel1.setText('Video running')

        # Change button to stop
        self.ss_video.setText('Stop video')
        
        self.display_thread.display_frame.connect(self.update_image)
        # Stop the video if button clicked  
        self.ss_video.clicked.connect(self.ClickStopVideo)
    
    # Activates when Start/Stop video button is clicked to Stop (ss_video)
    def ClickStopVideo(self):
        self.display_thread.display_frame.disconnect()
        self.ss_video.clicked.disconnect(self.ClickStopVideo)
        
        self.ss_video.setText('Start video')
        self.textLabel1.setText('Ready to start')
        # Start the video if button clicked
        self.ss_video.clicked.connect(self.ClickStartVideo)
    
    @pyqtSlot()
    def closing(self):
        self.display_thread.camera.close()
        if self.display_thread.camera.closed:
            print('camera has been closed')
            
class Display(Display_base):
    
    def __init__(self, VideoThread, w, h):
        super().__init__(VideoThread, w, h, "Zwo camera display")
    def closeEvent(self, event):
        if self.display_thread.camera.ready: 
            self.display_thread.stop()
        if self.display_thread.camera.closed:
            print('camera closed')
            self.closed = True
            event.accept()        