from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.RCServo import *
from Phidget22.Devices.LCD import *
import time

def onVoltageChange(self, voltage):
	print("Voltage: " + str(voltage))
	if(self.linkedLCD.getAttached() and self.linkedServo.getAttached()):
		self.linkedServo.setTargetPosition(10 + voltage*30)
		self.linkedLCD.writeText(LCDFont.FONT_5x8, 0, 0, "Position:")
		self.linkedLCD.writeText(LCDFont.FONT_5x8, 0, 1, str(self.linkedServo.getPosition()))
		self.linkedLCD.flush()

def main():
	voltageInput7 = VoltageInput()
	rcServo0 = RCServo()
	lcd0 = LCD()

	voltageInput7.setDeviceSerialNumber(39834)
	voltageInput7.setChannel(7)
	rcServo0.setDeviceSerialNumber(14559)
	rcServo0.setChannel(0)
	lcd0.setDeviceSerialNumber(39834)
	lcd0.setChannel(0)

	#Here we create an attribute of input called "linkedOutput", and assign it the handle for output
	voltageInput7.linkedServo = rcServo0
	voltageInput7.linkedLCD = lcd0


	voltageInput7.setOnVoltageChangeHandler(onVoltageChange)

	voltageInput7.openWaitForAttachment(5000)
	rcServo0.openWaitForAttachment(5000)
	lcd0.openWaitForAttachment(5000)
	lcd0.setBacklight(1)

	voltageInput7.setVoltageChangeTrigger(0.1)

	rcServo0.setTargetPosition(0)
	rcServo0.setEngaged(True)
	# time.sleep(2)
	# rcServo0.setEngaged(False)
	

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	voltageInput7.close()

main()