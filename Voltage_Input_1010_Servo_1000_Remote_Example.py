from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.RCServo import *
import time
from Phidget22.Net import *

def onVoltageChange(self, voltage):
	print("Voltage: " + str(voltage))
	if(self.linkedServo.getAttached()):
		self.linkedServo.setTargetPosition(10 + voltage*30)

def main():

	#Enable automatic server discovery to list remote phidgets
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Enable server discovery to list remote phidgets
	# Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)	
	#Add a specific remote server to communicate with Phidget remotely
	# Net.addServer("raspberrypi.local", "192.168.25.188", 5661, "passwd", 0)

	voltageInput7 = VoltageInput()
	rcServo0 = RCServo()

	voltageInput7.setDeviceSerialNumber(39826)
	voltageInput7.setChannel(7)
	rcServo0.setDeviceSerialNumber(19835)

	voltageInput7.setIsRemote(1)
	rcServo0.setIsRemote(1)

	#Here we create an attribute of input called "linkedOutput", and assign it the handle for output
	voltageInput7.linkedServo = rcServo0

	voltageInput7.setOnVoltageChangeHandler(onVoltageChange)

	voltageInput7.openWaitForAttachment(5000)
	rcServo0.openWaitForAttachment(5000)

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