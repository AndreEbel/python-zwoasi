# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:04:32 2021

@author: ebel
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget,QTabWidget, QLabel,QVBoxLayout, QHBoxLayout, QPushButton,QLineEdit, QFrame
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
import pyqtgraph as pg

class Display2_base(QWidget):
    closed = False
    def __init__(self, VideoThread, w, h, title, verbose):
        super().__init__()
        self.display_thread = VideoThread
        self.setWindowTitle(title)
        
        self.verbose = verbose
        
         # create a vertical box layout
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(0)
        self.vbox.setAlignment(Qt.AlignTop)
        # 1st row: Display
        self.display_width = w
        self.display_height = h
        self.image_label = pg.ImageView()#QLabel(self)
        self.image_label.setImage(np.zeros((self.display_height, self.display_width )))
        self.image_label.autoRange()
        self.vbox.addWidget(self.image_label) 
        
        # 2nd row: settings / info bar 
        self.settings_box =  QVBoxLayout()
        
        self.controlpanel = QFrame()
        self.controlpanel.setMaximumHeight(50)
        self.controlpanel.setFrameShape(QFrame.StyledPanel)
        self.controlpanel.setFrameShadow(QFrame.Raised)
        self.info_box = QHBoxLayout(self.controlpanel)
        self.info_box.setAlignment(Qt.AlignTop)
        self.video_status = QLabel('Ready to start')
        self.info_box.addWidget(self.video_status)
        self.settings_box.addWidget(self.controlpanel)
        
        # Initialize tab screen
        self.parampanel = QFrame()
        self.parampanel.setMaximumHeight(150)
        self.parampanel.setFrameShape(QFrame.StyledPanel)
        self.parampanel.setFrameShadow(QFrame.Raised)
        self.paramlayout = QHBoxLayout(self.parampanel)
        self.paramlayout.setAlignment(Qt.AlignTop)
        self.settings_box.addWidget(self.parampanel)
        
        self.ss_video = QPushButton('Start video',self)
        self.ss_video.clicked.connect(self.ClickStartVideo)
        self.paramlayout.addWidget(self.ss_video)

        self.tabs = QTabWidget()
        # self.tabs.setMaximumHeight(150)
        self.paramlayout.addWidget(self.tabs)
        # first tab
        self.tab = QWidget()
        self.tab.layout = QVBoxLayout()
        self.tabs.addTab(self.tab, "Image size")
        
        
        #width, height, and bins 
        self.widthlabel = QLabel('Width')
        self.width_input = QLineEdit()
        self.width_input.setValidator(QIntValidator())
        self.width_input.setMaxLength(4)
        self.width_input.setAlignment(Qt.AlignLeft)
        vbox_width= QVBoxLayout()
        vbox_width.addWidget(self.widthlabel)
        vbox_width.addWidget(self.width_input)
        
        self.heightlabel = QLabel('Height')
        self.height_input = QLineEdit()
        self.height_input.setValidator(QIntValidator())
        self.height_input.setMaxLength(4)
        self.height_input.setAlignment(Qt.AlignLeft)
        vbox_height= QVBoxLayout()
        vbox_height.addWidget(self.heightlabel)
        vbox_height.addWidget(self.height_input)
        
        self.binslabel = QLabel('Bins')
        self.bins_input = QLineEdit()
        self.bins_input.setValidator(QIntValidator())
        self.bins_input.setMaxLength(1)
        self.bins_input.setAlignment(Qt.AlignLeft)
        vbox_bins= QVBoxLayout()
        vbox_bins.addWidget(self.binslabel)
        vbox_bins.addWidget(self.bins_input)
        
        # initialize the input
        if self.display_thread.camera.id != None: # because 0 is ok
            self.width_input.setText(str(self.display_thread.camera.width))
            self.height_input.setText(str(self.display_thread.camera.height))
            self.bins_input.setText(str(self.display_thread.camera.bins))
        
        self.size_button = QPushButton('Set image size',self)
        self.size_button.clicked.connect(self.ClickSetImageSize)
        
        hbox_size= QHBoxLayout()       
        # hbox_size.addWidget(self.ss_video)
        hbox_size.addLayout(vbox_width)
        hbox_size.addLayout(vbox_height)
        hbox_size.addLayout(vbox_bins)
        hbox_size.addWidget(self.size_button)
        self.tab.layout.addLayout(hbox_size)
        self.tab.setLayout(self.tab.layout)
        
        self.vbox.addLayout(self.settings_box)

        # set the vbox layout as the widgets layout
        self.setLayout(self.vbox)
        
        # initialize the camera
        self.display_thread.camera.set_camera()
   
    
    @pyqtSlot(np.ndarray)
    def update_image(self, img):
        """
        Updates the image_label with a new opencv image
        """
        self.frame = img
        # self.pixmap = self.convert_cv_qt(img)
        self.image_label.setImage(self.frame.T)
        #print(self.image_label.width(),self.image_label.height())
        # self.image_label.setPixmap(self.pixmap.scaled(
        #     self.image_label.width(),self.image_label.height(),
        #     Qt.KeepAspectRatio, 
        #     Qt.FastTransformation))
    
    # Activates when Start/Stop video button is clicked to Start (ss_video
    def ClickStartVideo(self):
        self.ss_video.clicked.disconnect(self.ClickStartVideo)
        
        # update labels
        self.video_status.setText('Video running')

        # Change button to stop
        self.ss_video.setText('Stop video')
        # start the thread
        #self.display_thread.camera.set_camera()
        self.display_thread.camera.ready= True
        self.display_thread.start()
        self.display_thread.display_frame.connect(self.update_image)
        # Stop the video if button clicked  
        self.ss_video.clicked.connect(self.ClickStopVideo)
    
    # Activates when Start/Stop video button is clicked to Stop (ss_video)
    def ClickStopVideo(self):
        self.display_thread.display_frame.disconnect()
        self.ss_video.clicked.disconnect(self.ClickStopVideo)
        # start the thread
        self.display_thread.stop()
        self.ss_video.setText('Start video')
        self.video_status.setText('Ready to start')
        # Start the video if button clicked
        self.ss_video.clicked.connect(self.ClickStartVideo)
    
    @pyqtSlot()
    def closing(self):
        self.display_thread.camera.close()
        if self.display_thread.camera.closed:
            print('camera has been closed')
            
    def ClickSetImageSize(self):
        if (self.width_input.text()!=None)&(self.height_input.text()!=None)&(self.bins_input.text()!=None):
            w = int(self.width_input.text())
            h = int(self.height_input.text())
            b = int(self.bins_input.text())
            #print("stop the camera")
            self.display_thread.stop()
            self.display_thread.camera.set_roi(width=w, 
                                               height=h,
                                               bins=b)
            #print("restart the camera")
            self.display_thread.camera.ready= True
            self.display_thread.start()
            self.width_input.setText(str(self.display_thread.camera.width))
            self.height_input.setText(str(self.display_thread.camera.height))
            self.bins_input.setText(str(self.display_thread.camera.bins))
        else: 
            if self.verbose: 
                print('all inputs are not filled')
        
class Display2(Display2_base):
    
    def __init__(self, VideoThread, w, h, verbose):
        super().__init__(VideoThread, w, h, "Zwo camera display", verbose)
    def closeEvent(self, event):
        if self.display_thread.camera.ready: 
            self.display_thread.stop()
        if self.display_thread.camera.closed:
            print('camera closed')
            self.closed = True
            event.accept()        