from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.RCServo import *
import time
from Phidget22.Net import *
from Phidget22.Devices.Dictionary import *

dict = Dictionary()

def onVoltageChange(self, voltage):
	print("Voltage: " + str(voltage))
	print("Position: " + dict.get("position"))

def onDictionaryUpdate(self, key, value):
    print(key + f': {float(value):.2f}')

def main():

	#Enable server discovery to list remote phidgets
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)	
	#Add a specific remote server to communicate with Phidget remotely
	Net.addServer("raspberrypi.local", "192.168.137.254", 5661, "", 0)

	voltageInput7 = VoltageInput()
	dict.setDeviceLabel("testdict")

	voltageInput7.setDeviceSerialNumber(39834)
	voltageInput7.setChannel(7)

	voltageInput7.setIsRemote(1)

	voltageInput7.setOnVoltageChangeHandler(onVoltageChange)
	dict.setOnUpdateHandler(onDictionaryUpdate)

	dict.openWaitForAttachment(20000)
	voltageInput7.openWaitForAttachment(5000)	

	print("Position: " + dict.get("position"))

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	voltageInput7.close()
	dict.close()

main()