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

import serial 
import struct

from pymouse import PyMouse
from pymouse import PyMouseEvent

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
                self.MousePositions.append(self.mouse.position())
                self.NumPositions = self.NumPositions + 1

                if self.NumPositions == 2:
                	self.stop()
                              
        else:  # Exit if any other mouse button used
            self.stop()

def GetBoxCoordinates():
	# Have the user click twice to specify the box on the screen
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

	print('Sending New Voltage to Arduino:' + str(NewVoltage))

	ser.write(str(NewVoltage))

	# ser.write(struct.pack('>B', NewVoltage))

	time.sleep(0.1)

def rgb2gray(image):
	RGB_Image = np.asarray(image)

	RGB_Image.view(dtype=np.uint32).reshape(RGB_Image.shape[:-1])

	return RGB_Image

def CalculateNewVoltage(mean_intensity, SetPointIntensity, CurrentVoltage):
    # Calculate Percent Difference using current screen intensity and set point intenstity
    percentdifference = (mean_intensity - SetPointIntensity)/SetPointIntensity;
    NewVoltage = (1 - percentdifference/10)*CurrentVoltage;

    return NewVoltage

def GetMeanIntensity(ShowImage=False):
	# Get a new screen shot of the computer screen
	img=ImageGrab.grab()

	if ShowImage == True:		
		img.show()
	
	# Convert from RGBA to grayscale
	gray = rgb2gray(img) 

	# Ignore the alpha channel for the mean intensity
	gray = gray[:,:,0:3]

	print(gray.shape)

	mean_intensity = np.mean(gray)

	return mean_intensity


if __name__ == "__main__":

	# ser = serial.Serial('/dev/tty.usbmodem1421', 115200)

	SetPointIntensity = 50
	CurrentVoltage = 2.5

	Coordinates = GetBoxCoordinates()


	# for i in range(0,50):
	# 	start_time = time.time()

	# 	mean_intensity = GetMeanIntensity()

	# 	newVoltage = CalculateNewVoltage(mean_intensity, SetPointIntensity, CurrentVoltage)

	# 	SendValueToArduino(newVoltage)

	# 	print(mean_intensity)

	# 	elapsed_time = time.time() - start_time
	# 	print('Elapsed Time: ' + str(elapsed_time))



	# img = Image.fromarray(gray, 'RGB')
	# img.show()





    # array = numpy.array(img.getdata(),numpy.uint8).reshape(img.size[1], img.size[0])
    # print(array)




# import serial
# arduino = serial.Serial('/dev/tty.usbmodem1421', 115200, timeout=.1)
# while True:
# 	data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
# 	if data:
# 		print data