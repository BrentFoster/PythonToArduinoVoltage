from pymouse import PyMouse
from pymouse import PyMouseEvent

class MouseActions(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)
        self.MousePositions = []
        self.NumPositions = 0

    def GetMousePositions(self):
    	return self.MousePositions

    def click(self, x, y, button, press):
        '''Print Fibonacci numbers when the left click is pressed.'''
        if self.NumPositions <= 1:
            if press:
                print(m.position())
                self.MousePositions.append(m.position())
                self.NumPositions = self.NumPositions + 1

                if self.NumPositions == 2:
                	self.stop()
                              
        else:  # Exit if any other mouse button used
            self.stop()



# Instantiate an mouse object
m = PyMouse()

C = MouseActions()

C.run()
print('Box Coordinates are:')
print(C.GetMousePositions())



# while True:
# 	print(m.position())
# (500, 300)