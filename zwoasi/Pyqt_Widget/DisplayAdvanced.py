from .DisplaySave import DisplaySave_base
from PyQt5.QtWidgets import QLineEdit,QHBoxLayout, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
# from time import sleep

class DisplayAdvanced_base(DisplaySave_base):
    def __init__(self, VideoThread, w, h, title):
        super().__init__(VideoThread,  w, h, title)
        
        # Add tabs
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Camera settings")
        self.tab2.layout = QVBoxLayout()
        #self.tab2.layout.addStretch(1)
        
        # exposure
        self.exposure =None
        self.exposure_input = QLineEdit()
        self.exposure_input.setValidator(QIntValidator())
        self.exposure_input.setMaxLength(8)
        self.exposure_input.setAlignment(Qt.AlignRight)
        self.exposure_button = QPushButton('Set exposure (µs)',self)
        self.exposure_button.clicked.connect(self.ClickSetExposure)
        self.auto_exposure_button = QPushButton('Set Autoexposure On',self)
        self.auto_exposure_button.clicked.connect(self.ClickAutoExposureOn)
        hbox_exp = QHBoxLayout()
        hbox_exp.addStretch(1)
        hbox_exp.addWidget(self.exposure_input)
        hbox_exp.addWidget(self.exposure_button)
        hbox_exp.addWidget(self.auto_exposure_button)
        
        # gain
        self.gain =None
        self.gain_input = QLineEdit()
        self.gain_input.setValidator(QIntValidator())
        self.gain_input.setMaxLength(4)
        self.gain_input.setAlignment(Qt.AlignRight)
        self.gain_button = QPushButton('Set gain',self)
        self.gain_button.clicked.connect(self.ClickSetGain)
        hbox_gain = QHBoxLayout()
        hbox_gain.addStretch(1)
        hbox_gain.addWidget(self.gain_input)
        hbox_gain.addWidget(self.gain_button)
        
        # Add the new function to the layout     
        # Add the new function to the layout  
        
        self.tab2.layout.addLayout(hbox_exp)
        self.tab2.layout.addLayout(hbox_gain)
        self.tab2.setLayout(self.tab2.layout)
        
        # self.settings_box.addLayout(hbox_exp)
        # self.settings_box.addLayout(hbox_gain)
        
        # refresh the widget layout
        self.setLayout(self.vbox)
            
   
        
    def ClickSetExposure(self):
        self.display_thread.camera.exposure = int(self.exposure_input.text())
        self.display_thread.camera.set_exp()
        
    
    def ClickSetGain(self):
        self.display_thread.camera.gain = int(self.gain_input.text())
        self.display_thread.camera.set_gain()
        

    def ClickAutoExposureOn(self):
        if not self.display_thread.camera.closed: 
            self.auto_exposure_button.clicked.disconnect(self.ClickAutoExposureOn)
            self.display_thread.auto_exp = True
            self.display_thread.camera.auto_exposure(on = True)
            
            self.auto_exposure_button.setText('Set AutoExposure Off')
            self.auto_exposure_button.clicked.connect(self.ClickAutoExposureOff)
        
    def ClickAutoExposureOff(self):
        if not self.display_thread.camera.closed:     
            self.auto_exposure_button.clicked.disconnect(self.ClickAutoExposureOff)
            # save exposure settings 
            print('autoexp off')
            self.display_thread.camera.auto_exposure(on = False)
            #self.display_thread.camera.get_gain()
            self.gain_input.setText(str(self.display_thread.camera.gain))
            #self.display_thread.camera.get_exp()
            self.exposure_input.setText(str(self.display_thread.camera.exposure))
            self.display_thread.auto_exp = False
         
            self.auto_exposure_button.setText('Set AutoExposure On')
            self.auto_exposure_button.clicked.connect(self.ClickAutoExposureOn)

class DisplayAdvanced(DisplayAdvanced_base):
    def __init__(self, VideoThread, w, h):
        super().__init__(VideoThread,  w, h, "Zwo camera display")
    def closeEvent(self, event):
        if self.display_thread.camera.ready: 
            self.display_thread.stop()
            self.display_thread.camera.close()
        if self.display_thread.camera.closed:
            print('camera closed')
            self.closed = True
            event.accept()        