from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.RCServo import *
import time
from Phidget22.Net import *
from Phidget22.Devices.Dictionary import *

dict = Dictionary()

def onVoltageChange(self, voltage):
	# print("Voltage: " + str(voltage))
	print(f'Voltage: {voltage:.2f}')
	if(self.linkedServo.getAttached()):
		self.linkedServo.setTargetPosition(10 + voltage*30)

def onPositionChange(self, position):
	# print("Position: " + str(position))
	print(f'Position: {position:.2f}')
	dict.update("position", str(position))

def main():

	#Enable automatic server discovery to list remote phidgets
	# Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Enable server discovery to list remote phidgets
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)	
	#Add a specific remote server to communicate with Phidget remotely
	# Net.addServer("raspberrypi.local", "137.44.181.148", 5661, "", 0)
	Net.addServer("raspberrypi.local", "192.168.42.179", 5661, "", 0)

	voltageInput7 = VoltageInput()
	rcServo0 = RCServo()
	dict.setDeviceLabel("testdict")

	voltageInput7.setDeviceSerialNumber(39834)
	voltageInput7.setChannel(7)
	rcServo0.setDeviceSerialNumber(14559)

	voltageInput7.setIsRemote(1)
	rcServo0.setIsRemote(1)

	#Here we create an attribute of input called "linkedOutput", and assign it the handle for output
	voltageInput7.linkedServo = rcServo0

	voltageInput7.setOnVoltageChangeHandler(onVoltageChange)
	rcServo0.setOnPositionChangeHandler(onPositionChange)

	voltageInput7.openWaitForAttachment(5000)
	rcServo0.openWaitForAttachment(5000)
	dict.openWaitForAttachment(20000)

	voltageInput7.setVoltageChangeTrigger(0.1)

	rcServo0.setTargetPosition(0)
	rcServo0.setEngaged(True)	
	dict.set("position", "0")
	dict.set("voltage", "0")

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	rcServo0.close()
	voltageInput7.close()
	dict.close()

main()