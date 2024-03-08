from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.DigitalOutput import *
import time

#Declare any event handlers here. These will be called every time the associated event occurs.

def onVoltageChange(self, voltage):
	print("Voltage: " + str(voltage))
	if(self.linkedDigitalOutput7.getAttached()):
		self.linkedDigitalOutput7.setDutyCycle(1)
		time.sleep(0.01) # slows down the event handler
		self.linkedDigitalOutput7.setDutyCycle(0)

def main():
	#Enable server discovery to allow your program to find other Phidgets on the local network.
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Add a specific remote server to communicate with Phidget remotely
	Net.addServer("", "192.168.42.188", 5661, "", 0)

	#Create your Phidget channels
	voltageInput7 = VoltageInput()
	digitalOutput6 = DigitalOutput()
	digitalOutput7 = DigitalOutput()

	#Set addressing parameters to specify which channel to open (if any)
	voltageInput7.setIsRemote(True)
	voltageInput7.setDeviceSerialNumber(39826)
	voltageInput7.setChannel(7)
	digitalOutput7.setIsRemote(True)
	digitalOutput7.setDeviceSerialNumber(39826)
	digitalOutput7.setChannel(7)

	#Here we create an attribute of input called "linkedOutput", and assign it the handle for output
	voltageInput7.linkedDigitalOutput7 = digitalOutput7

	#Assign any event handlers you need before calling open so that no events are missed.
	voltageInput7.setOnVoltageChangeHandler(onVoltageChange)

	#Open your Phidgets and wait for attachment
	digitalOutput6.openWaitForAttachment(5000)
	digitalOutput7.openWaitForAttachment(5000)
	voltageInput7.openWaitForAttachment(5000)

	#Do stuff with your Phidgets here or in your event handlers.
	voltageInput7.setVoltageChangeTrigger(0.1)
	# digitalOutput7.setDutyCycle(1)
	digitalOutput7.setDutyCycle(0)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	voltageInput7.close()
	digitalOutput7.close()

main()