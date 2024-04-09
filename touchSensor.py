from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageRatioInput import *
import time

# value to store the state
sensorState = 0e0
number = 0

#Declare any event handlers here. These will be called every time the associated event occurs.

def onVoltageRatioInput5_SensorChange(self, sensorValue, sensorUnit):
	global sensorState
	global number
	# if sensorState != sensorValue:

	# sensorState = sensorValue
	number += 1
	print("SensorValue: " + str(sensorValue), (sensorState == sensorValue))
	print("SensorUnit: " + str(sensorUnit.symbol))
	print("----------")

def onVoltageRatioInput5_Attach(self):
	print("Attach!")

def onVoltageRatioInput5_Detach(self):
	print("Detach!")

def main():
	#Enable server discovery to allow your program to find other Phidgets on the local network.
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Create your Phidget channels
	voltageRatioInput5 = VoltageRatioInput()

	#Set addressing parameters to specify which channel to open (if any)
	voltageRatioInput5.setIsRemote(True)
	voltageRatioInput5.setChannel(5)

	#Assign any event handlers you need before calling open so that no events are missed.
	voltageRatioInput5.setOnSensorChangeHandler(onVoltageRatioInput5_SensorChange)
	voltageRatioInput5.setOnAttachHandler(onVoltageRatioInput5_Attach)
	voltageRatioInput5.setOnDetachHandler(onVoltageRatioInput5_Detach)

	#Open your Phidgets and wait for attachment
	voltageRatioInput5.openWaitForAttachment(20000)

	#Do stuff with your Phidgets here or in your event handlers.
	#Set the sensor type to match the analog sensor you are using after opening the Phidget
	voltageRatioInput5.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1129)
	# voltageRatioInput5.setVoltageRatioChangeTrigger(0.005)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	voltageRatioInput5.close()

main()