from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.RFID import *
import time

#Declare any event handlers here. These will be called every time the associated event occurs.

def onRFID0_Tag(self, tag, protocol):
	print("Found Tag: " + str(tag))
	print("Protocol: " + RFIDProtocol.getName(protocol))
	print("----------")

def onRFID0_TagLost(self, tag, protocol):
	print("Lost Tag: " + str(tag))
	print("Protocol: " + RFIDProtocol.getName(protocol))
	print("----------")

def onRFID0_Attach(self):
	print("Attach!")

def onRFID0_Detach(self):
	print("Detach!")

def main():
	#Enable server discovery to allow your program to find other Phidgets on the local network.
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Create your Phidget channels
	rfid0 = RFID()

	#Set addressing parameters to specify which channel to open (if any)
	rfid0.setIsRemote(True)

	#Assign any event handlers you need before calling open so that no events are missed.
	rfid0.setOnTagHandler(onRFID0_Tag)
	rfid0.setOnTagLostHandler(onRFID0_TagLost)
	rfid0.setOnAttachHandler(onRFID0_Attach)
	rfid0.setOnDetachHandler(onRFID0_Detach)

	#Open your Phidgets and wait for attachment
	rfid0.openWaitForAttachment(20000)

	#Do stuff with your Phidgets here or in your event handlers.

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	rfid0.close()

main()