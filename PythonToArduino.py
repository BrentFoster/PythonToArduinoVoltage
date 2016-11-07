# pip install Image
# pip install pyscreenshot
# pip install pySerial

# pip install pymouse
# pip install pyobjc-framework-Quartz


# http://www.instructables.com/id/Arduino-Python-Communication-via-USB/?ALLSTEPS
# http://www.toptechboy.com/arduino/lesson-8-writing-analog-voltages-in-arduino/

# import Image
import pyscreenshot as ImageGrab
import numpy as np
from PIL import Image
import time
import sys


import serial 
# import struct

from pymouse import PyMouse
from pymouse import PyMouseEvent

def saveLog(filename, logData):
	# try:
	#Save computation time in a log file
	text_file = open(filename, "r+")
	text_file.readlines()
	text_file.write("%s\n" % logData)
	text_file.close()
	# except:
	# 	print("Failed writing log data to .txt file")

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

def GetBoxCoordinates():
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

def SendValueToArduino(NewVoltage):	
	
	# Clear the output!
	# ser.flushInput()
	# ser.flushOutput() 

	# print('Sending New Voltage to Arduino:' + str(round(NewVoltage,2)))

	ser.write(str(round(NewVoltage,2)))

	# ser.write(struct.pack('>B', NewVoltage))

	time.sleep(0.5)

def rgb2gray(image):
	RGB_Image = np.asarray(image)

	RGB_Image.view(dtype=np.uint32).reshape(RGB_Image.shape[:-1])

	return RGB_Image

def CalculateNewVoltage(mean_intensity, SetPointIntensity, CurrentVoltage):
    # Calculate Percent Difference using current screen intensity and set point intenstity
    percentdifference = (mean_intensity - SetPointIntensity)/SetPointIntensity;
    NewVoltage = (1 - percentdifference/10)*CurrentVoltage;

    # Maximum voltage on the arduino is 5 volts
    if NewVoltage > 5:
    	NewVoltage = 5
    elif NewVoltage <0:
    	NewVoltage = 0

    return NewVoltage

def GetMeanIntensity(BoxCoordinates, iteration=1, ShowImage=False):
	# Get a new screen shot of the computer screen
	img=ImageGrab.grab()
	
	# Convert from RGBA to grayscale
	gray = rgb2gray(img) 

	# Index the gray scale image to include only the user defined box
	BoxCoordinates = np.asarray(BoxCoordinates, dtype=np.int16)

	width  = 2*abs(BoxCoordinates[0,0] - BoxCoordinates[1,0])
	height = 2*abs(BoxCoordinates[0,1] - BoxCoordinates[1,1])

	x = BoxCoordinates[0,1]*2
	y = BoxCoordinates[0,0]*2

	# Ignore the alpha channel for the mean intensity
	gray_image_box = gray[x:x+height, 
						  y:y+width, 0:3]

	mean_intensity = np.mean(gray_image_box)

	if ShowImage == True:	
		# Only show the screen shot for the first iteration
		if iteration == 0:	
			img = Image.fromarray(gray_image_box)
			img.show()

	if iteration ==0:
		print('Box Width: ' + str(width))
		print('Box Height: ' + str(height))

	

	return mean_intensity

if __name__ == "__main__":

	ser = serial.Serial('/dev/tty.usbmodem1421', 115200)


	# for i in range(0,200):
	# 	SendValueToArduino(1.123456)

	CurrentVoltage = raw_input("Set Initial Voltage (0-5): ")
	CurrentVoltage = float(CurrentVoltage)

	if CurrentVoltage > 5:
		raise Warning('Initial Voltage must be < 5!')

	SetPointIntensity = raw_input("Set Point Intensity: ")
	SetPointIntensity = float(SetPointIntensity)

	ShowImageFlag = raw_input("Show Image of Box? (yes/no): ")
	if ShowImageFlag == 'yes':
		ShowImageFlag = True
	else:
		ShowImageFlag = False
	
	print(' ')
	print('Initial Voltage set to ' + str(CurrentVoltage))
	print('Set Point Intensity set to ' + str(SetPointIntensity))
	print('Showing image set to ' + str(ShowImageFlag))
	print(' ')

	
	BoxCoordinates = GetBoxCoordinates()
	print(' ')
	print('Running...')

	its = 0
	start_time = time.time()

	while True:
		mean_intensity = GetMeanIntensity(BoxCoordinates, iteration=its, ShowImage=ShowImageFlag)
		newVoltage = CalculateNewVoltage(mean_intensity, SetPointIntensity, CurrentVoltage)

		SendValueToArduino(newVoltage)

		# Voltage read on arduino is 0.03 less than this number
		newVoltage = newVoltage - 0.03

		print('Mean Intensity: ' + str(round(mean_intensity,2)))
		print('Current Voltage: ' + str(round(newVoltage,2)))

		elapsed_time = round(time.time() - start_time, 2)

		logData = [round(mean_intensity,2), round(newVoltage,2), elapsed_time]


		saveLog('OutputValues.txt', logData)
		print('Elapsed Time: ' + str(elapsed_time))

		its = its + 1
		print(' ')



