import time
import serial # if you have not already done so
ser = serial.Serial('/dev/tty.usbmodem1421', 115200)
num = 0
while True:
	num = num + 1
	ser.write(str(num) + '\n')

	time.sleep(1)