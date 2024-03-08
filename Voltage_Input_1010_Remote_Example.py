from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time
from Phidget22.Net import *

def onVoltageChange(self, voltage):
	print("Voltage: " + str(voltage))

def main():
	voltageInput7 = VoltageInput()

	#Enable automatic server discovery to list remote phidgets
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Enable server discovery to list remote phidgets
	# Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)	
	#Add a specific remote server to communicate with Phidget remotely
	# Net.addServer("raspberrypi.local", "192.168.25.188", 5661, "passwd", 0)

	voltageInput7.setDeviceSerialNumber(39826)
	voltageInput7.setChannel(7)
	voltageInput7.setIsRemote(1)

	voltageInput7.setOnVoltageChangeHandler(onVoltageChange)

	voltageInput7.openWaitForAttachment(5000)

	voltageInput7.setVoltageChangeTrigger(0.5)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	voltageInput7.close()

main()