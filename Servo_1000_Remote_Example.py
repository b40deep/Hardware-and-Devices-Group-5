from Phidget22.Phidget import *
from Phidget22.Devices.RCServo import *
import time
from Phidget22.Net import *

def main():
	rcServo0 = RCServo()

	#Enable automatic server discovery to list remote phidgets
	# Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Enable server discovery to list remote phidgets
	# Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)	
	#Add a specific remote server to communicate with Phidget remotely
	# Net.addServer("raspberrypi.local", "192.168.25.188", 5661, "passwd", 0)

	rcServo0.setDeviceSerialNumber(19835)
	rcServo0.setIsRemote(1)

	rcServo0.openWaitForAttachment(5000)

	rcServo0.setTargetPosition(10)
	rcServo0.setEngaged(True)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	rcServo0.close()

main()