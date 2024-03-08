from Phidget22.Phidget import *
from Phidget22.Devices.LCD import *
import time
from Phidget22.Net import *

#Declare any event handlers here. These will be called every time the associated event occurs.

def main():
	lcd0 = LCD()

	#Enable automatic server discovery to list remote phidgets
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Enable server discovery to list remote phidgets
	# Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)	
	#Add a specific remote server to communicate with Phidget remotely
	# Net.addServer("raspberrypi.local", "192.168.25.188", 5661, "passwd", 0)

	lcd0.setDeviceSerialNumber(39826)
	lcd0.setChannel(0)
	# lcd0.setHubPort(0)
	lcd0.setIsRemote(1)

	lcd0.openWaitForAttachment(5000)

	lcd0.setBacklight(1)
	lcd0.writeText(LCDFont.FONT_5x8, 0, 0, "Hello")
	lcd0.writeText(LCDFont.FONT_5x8, 0, 1, "World!")
	lcd0.flush()

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	lcd0.close()

main()
