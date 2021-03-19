# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:58:44 2021

@author: ebel
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout

class MultiCam(QWidget):
    def __init__(self, widget_list):
        super().__init__()
      
        hbox = QHBoxLayout()
        for w in widget_list:
            hbox.addWidget(w)
        self.setLayout(hbox)