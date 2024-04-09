from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageRatioInput import *
import time

#Declare any event handlers here. These will be called every time the associated event occurs.

def onVoltageRatioInput3_SensorChange(self, sensorValue, sensorUnit):
	print("SensorValue: " + str(sensorValue))
	print("SensorUnit: " + str(sensorUnit.symbol))
	print("----------")

def onVoltageRatioInput3_Attach(self):
	print("Attach!")

def onVoltageRatioInput3_Detach(self):
	print("Detach!")

def main():
	#Enable server discovery to allow your program to find other Phidgets on the local network.
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Create your Phidget channels
	voltageRatioInput3 = VoltageRatioInput()

	#Set addressing parameters to specify which channel to open (if any)
	voltageRatioInput3.setIsRemote(True)
	voltageRatioInput3.setChannel(3)

	#Assign any event handlers you need before calling open so that no events are missed.
	voltageRatioInput3.setOnSensorChangeHandler(onVoltageRatioInput3_SensorChange)
	voltageRatioInput3.setOnAttachHandler(onVoltageRatioInput3_Attach)
	voltageRatioInput3.setOnDetachHandler(onVoltageRatioInput3_Detach)

	#Open your Phidgets and wait for attachment
	voltageRatioInput3.openWaitForAttachment(20000)

	#Do stuff with your Phidgets here or in your event handlers.
	#Set the sensor type to match the analog sensor you are using after opening the Phidget
	voltageRatioInput3.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1106)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	voltageRatioInput3.close()

main()