# -*- coding: utf-8 -*-
"""
Simple example of loading UI template created with Qt Designer.
This example uses uic.loadUiType to parse and load the ui at runtime. It is also
possible to pre-compile the .ui file using pyuic (see VideoSpeedTest and 
ScatterPlotSpeedTest examples; these .ui files have been compiled with the
tools/rebuildUi.py script).
"""
# import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import os

# Modules for taking screen shot of screen
from PIL import Image
import pyscreenshot as ImageGrab
import time

# Modules for getting input from mouse
import sys
from pymouse import PyMouse
from pymouse import PyMouseEvent


pg.mkQApp()

## Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
# uiFile = os.path.join(path, 'designerExample.ui')
uiFile = os.path.join(path, 'BrentDesignerExample/mainwindow.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

class MouseActions(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)
        self.MousePositions = []
        self.NumPositions = 0

        # Instantiate an mouse object
        self.mouse = PyMouse()

    def GetMousePositions(self):
        return self.MousePositions

    def click(self, x, y, button, press):
        '''Print Fibonacci numbers when the left click is pressed.'''
        if self.NumPositions <= 1:
            if press:               
                print(self.mouse.position())

                if self.NumPositions == 0:
                    print('Click on bottom right of box')

                self.MousePositions.append(self.mouse.position())
                self.NumPositions = self.NumPositions + 1

                if self.NumPositions == 2:
                    self.stop()
                              
        else:  # Exit if any other mouse button used
            self.stop()

class MainWindow(TemplateBaseClass):  
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.setWindowTitle('pyqtgraph example: Qt Designer')
        
        # Create the main window
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        
        
        self.chunkSize = 20
        # Remove chunks after we have 10
        self.maxChunks = 100
        self.startTime = pg.ptime.time()
        self.data = np.empty((self.chunkSize+1,2))
        self.ptr5 = 0

        self.p = self.ui.plot 
        self.p.setXRange(-10, 0)
        self.p.setLabel('bottom', 'Time', 's')

        self.curves = []

        self.curve = self.p.plot() #pg.ScatterPlotItem()
        self.p.setAutoPan(x=True)
        self.p.enableAutoRange('x', 0.95)


        # Attach the Auto Scroll Button to the function
        self.ui.plotBtn.clicked.connect(self.SetAutoScroll)

        self.ui.horizontalSlider.valueChanged.connect(self.GetSliderValue)

        self.Y_Offset = 0

        # Get the box coordinates from the user
        self.BoxCoordinates = self.GetBoxCoordinates()

        self.show()

    def GetBoxCoordinates(self):
        # Have the user click twice to specify the box on the screen

        print('Click twice to determine box boundaries')

        print(' ')
        print('Click on top left of box')

        C = MouseActions()
        C.run()

        Coordinates = C.GetMousePositions()
        Coordinates = np.rint(np.asarray(Coordinates))


        print('Box Coordinates are:')
        print(Coordinates)

        return Coordinates

    def GetSliderValue(self):
        # Get the current value of the horizontal slider

        position = self.ui.horizontalSlider.value()
        position = position/10


        self.Y_Offset = position

        self.ui.lcdNumber.display(self.Y_Offset)

    def SetAutoScroll(self):
        # self.update()
        self.p.setAutoPan(x=True, y=True)
        self.p.enableAutoRange('x', 1)
        self.p.enableAutoRange('y', 1)

    def update(self):
        ' Update the plots with the new data '
        now = pg.ptime.time()

        i = self.ptr5 % self.chunkSize
        # print(i)
        # Initilize the plot and the numpy array to hold data
        # only during first time point (when i = 0)
        if i == 0:
            self.curve = self.p.plot()
            # print(curve)
            # asd
            self.curves.append(self.curve)
            last = self.data[-1]
            self.data = np.empty((self.chunkSize+1,2))        
            self.data[0] = last
            while len(self.curves) > self.maxChunks:
                c = self.curves.pop(0)
                self.p.removeItem(c)
        else:
            self.curve = self.curves[-1]

        self.data[i+1,0] = now - self.startTime
        # self.data[i+1,1] = np.sin(now - self.startTime)
        self.data[i+1,1] = self.GetMeanIntensity()
    
        # Add the data to the plot
        self.curve.setData(x=self.data[:i+2, 0], y=self.Y_Offset + self.data[:i+2, 1])

        # curve.setData(x=self.data[:, 0], y=self.data[:, 1])

        # Add the scaatter plot to the UI plot!
        self.p.addItem(self.curve)

        self.ptr5 += 1

    def GetMeanIntensity(self,ShowImage=False):
        # Get a new screen shot of the computer screen

        start_time = time.time()

        BoxCoordinates = self.BoxCoordinates

        # scale = 2

        # width  = scale*abs(BoxCoordinates[0,0] - BoxCoordinates[1,0])
        # height = scale*abs(BoxCoordinates[0,1] - BoxCoordinates[1,1])

        # x = BoxCoordinates[0,1]*scale
        # y = BoxCoordinates[1,1]*scale

        # part of the screen
        img=ImageGrab.grab(bbox=(
                                BoxCoordinates[0,0],
                                BoxCoordinates[0,1],
                                BoxCoordinates[1,0],
                                BoxCoordinates[1,1])) # X1,Y1,X2,Y2
        # img.show()

        elapsed_time = round(time.time() - start_time, 2)
        print('ImageGrab time: ' + str(elapsed_time))
        
        # Convert from RGBA to grayscale
        start_time = time.time()
        gray = self.rgb2gray(img) 
        elapsed_time = round(time.time() - start_time, 2)
        print('rgb2gray time: ' + str(elapsed_time))

        mean_intensity = np.mean(gray)

    
        return mean_intensity

    def rgb2gray(self, image):
        RGB_Image = np.asarray(image, dtype=np.uint8)
        
        return RGB_Image

        
win = MainWindow()

timer = pg.QtCore.QTimer()
timer.timeout.connect(win.update)
timer.start(50)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()