# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:30:09 2021

@author: ebel
"""
from .DisplayAdvanced import DisplayAdvanced
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from skimage.exposure import histogram
import numpy as np
from PyQt5.QtCore import pyqtSlot

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)#, tight_layout=True)
        self.ax = fig.add_subplot(111)
        self.ax.set_xlim(0,255)
        self.ax.tick_params(axis='both', which='major', labelsize=7)
        self.ax.set_yticks([])
        self.ax.set_xticks([])
        #for tick in self.ax.get_yticklabels():
        #    tick.set_rotation(90)
        super(MplCanvas, self).__init__(fig)
        
class DisplayAdvancedHist(DisplayAdvanced):
    def __init__(self, VideoThread, w,h):
        super().__init__(VideoThread,  w, h)
        
        screen_dpi = 96
        self.canvas = MplCanvas(
            self, 
            width=self.display_width/screen_dpi, 
            height=200/screen_dpi, 
            dpi=screen_dpi)
        
        self._plot_ref = None
        self.display_box.addWidget(self.canvas)
       

        # set the vbox layout as the widgets layout
        #self.setLayout(self.setLayout(self.vbox))        
    
    @pyqtSlot(np.ndarray)
    def update_plot(self, cv_img):
        """
        Updates the image_label with a new opencv image
        """
        self.hist = []
        
        #for i in range(cv_img.shape[-1]):
        hist, self.bins = histogram(cv_img, #cv_img[:, :, i]
                                    source_range='dtype',
                                    normalize=False)
        self.hist.append(hist)
        step = int(40/self.display_thread.camera.n_bins)
        reduced = np.ravel(cv_img)[0:-1:step]
        self.mean_img = np.mean(reduced)
        
        self.std_img = np.std(reduced)
        
        if self._plot_ref is None:
            
            self._plot_ref = []
            for hist in self.hist:
                plot = self.canvas.ax.plot(self.bins, hist)
                self._plot_ref.append(plot[0])
                
            self.m = self.canvas.ax.axvline(self.mean_img, color='red')
            self.std = self.canvas.ax.axvspan(self.mean_img-self.std_img, self.mean_img+self.std_img, color='red', alpha=0.5)
            #print('ok')
        else:
            #print(m)
            # We have a reference, we can use it to update the data for that line.
            for plot, hist in zip(self._plot_ref, self.hist):
                plot.set_ydata(hist)
            self.m.set_xdata(self.mean_img)
            self.std.set_xy(np.array([[ self.mean_img-self.std_img, 0.        ],
                             [ self.mean_img-self.std_img,  1.        ],
                             [self.mean_img+self.std_img ,  1.        ],
                             [self.mean_img+self.std_img ,  0.        ],
                             [self.mean_img-self.std_img , 0.        ]]))
        self.canvas.ax.relim()
        self.canvas.ax.autoscale_view(scalex = False)
        self.canvas.draw()
    
   
    
    # Activates when Start/Stop video button is clicked to Start (ss_video)
    def ClickStartVideo(self):
        super().ClickStartVideo()
        self.display_thread.display_frame.connect(self.update_plot)

        