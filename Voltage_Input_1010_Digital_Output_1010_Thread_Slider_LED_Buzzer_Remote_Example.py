from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.DigitalOutput import *
import time
from threading import Thread, Event
from Phidget22.Devices.RCServo import *
from Phidget22.Devices.LCD import *

#Declare any event handlers here. These will be called every time the associated event occurs.

def onVoltageChange(self, voltage):
	print("Voltage: " + str(voltage))
	if(self.linkedDigitalOutput7.getAttached()):
		self.linkedDigitalOutput7.setDutyCycle(1)
		time.sleep(0.01) # slows down the event handler
		self.linkedDigitalOutput7.setDutyCycle(0) 
	if(not self.linkedEvent.is_set()):
		self.linkedEvent.set()

def buzzer_Output(buzzerEvent, digitalOutput):
	while buzzerEvent.wait():
		for i in range(10):
			digitalOutput.setDutyCycle(0)
			time.sleep(1/3000)
			digitalOutput.setDutyCycle(1)
			time.sleep(1/3000)
		buzzerEvent.clear()

def main():
	#Enable server discovery to allow your program to find other Phidgets on the local network.
	# Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Add a specific remote server to communicate with Phidget remotely
	# Net.addServer("", "192.168.42.188", 5661, "", 0)

	#Create your Phidget channels
	voltageInput7 = VoltageInput()
	digitalOutput0 = DigitalOutput()
	digitalOutput7 = DigitalOutput()
	rcServo0 = RCServo()
	lcd0 = LCD()

	#Set addressing parameters to specify which channel to open (if any)
	#voltageInput7.setIsRemote(True)
	voltageInput7.setDeviceSerialNumber(39834)
	voltageInput7.setChannel(7)
	#digitalOutput0.setIsRemote(True)
	digitalOutput0.setDeviceSerialNumber(39834)
	digitalOutput0.setChannel(0)
	#digitalOutput7.setIsRemote(True)
	digitalOutput7.setDeviceSerialNumber(39834)
	digitalOutput7.setChannel(7)

	#Here we create an attribute of input called "linkedOutput", and assign it the handle for output
	voltageInput7.linkedDigitalOutput7 = digitalOutput7

	# Create a Thread and Event for buzzer and pass the Event to a Phidget 
	buzzerEvent = Event()
	buzzerOutput = Thread(target=buzzer_Output, args=(buzzerEvent, digitalOutput0),daemon=True)
	voltageInput7.linkedEvent = buzzerEvent

	#Assign any event handlers you need before calling open so that no events are missed.
	voltageInput7.setOnVoltageChangeHandler(onVoltageChange)

	#Open your Phidgets and wait for attachment
	digitalOutput0.openWaitForAttachment(5000)
	digitalOutput7.openWaitForAttachment(5000)
	voltageInput7.openWaitForAttachment(5000)
	buzzerOutput.start() # Start thread after opening channels

	#Do stuff with your Phidgets here or in your event handlers.
	voltageInput7.setVoltageChangeTrigger(0.1)
	digitalOutput0.setDutyCycle(0)
	digitalOutput7.setDutyCycle(0)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	voltageInput7.close()
	digitalOutput0.close()
	digitalOutput7.close()

main()