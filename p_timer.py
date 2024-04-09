from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageRatioInput import *
import time
import math
from Phidget22.Devices.LCD import *
from Phidget22.Devices.DigitalOutput import *

#Time-period limits
p_work_limit = 60
p_sbreak_limit = 30
p_lbreak_limit = 90
#curerently chosen Time-periods 
p_work_curr = 0
p_sbreak_curr = 0
p_lbreak_curr = 0

def writeLCD(self):
	self.linkedLCD.clear()
	self.linkedLCD.writeText(LCDFont.FONT_5x8, 0, 0, "WORK  SHORTB  LONGB")
	self.linkedLCD.writeText(LCDFont.FONT_5x8, 0, 1, f' {p_work_curr:02d}     {p_sbreak_curr:02d}     {p_lbreak_curr:02d}')
	self.linkedLCD.flush()

#Declare any event handlers here. These will be called every time the associated event occurs.

def ontimer_button_SensorChange(self, sensorValue, sensorUnit):
	#global sensorState
	# if sensorState != sensorValue:
	#print("SensorValue: " + str(sensorValue), (sensorState == sensorValue))
	# print("SensorUnit: " + str(sensorUnit.symbol))
	#print("----------")
	None

def ontimer_button_Attach(self):
	print("Attach!")

def ontimer_button_Detach(self):
	print("Detach!")

def ontimer_p_work_SensorChange(self, sensorValue, sensorUnit):
	global p_work_limit 
	global p_work_curr 
	p_work_curr = math.ceil(p_work_limit * sensorValue)

	print('p_work time: ' + str(p_work_curr))
	writeLCD(self)
	# print("SensorValue [2]: " + str(sensorValue))
	# print("SensorUnit [2]: " + str(sensorUnit.symbol))
	print("----------")
	


def ontimer_p_work_Attach(self):
	print("Attach [2]!")

def ontimer_p_work_Detach(self):
	print("Detach [2]!")

def ontimer_sbreak_SensorChange(self, sensorValue, sensorUnit):
	global p_sbreak_limit 
	global p_sbreak_curr 
	p_sbreak_curr = math.ceil(p_sbreak_limit * sensorValue)

	print('p_sbreak time: ' + str(p_sbreak_curr))
	writeLCD(self)
	# print("SensorValue [3]: " + str(sensorValue))
	print('p_sbreak time: ' + str(math.ceil(p_sbreak_limit * sensorValue)))
	# print("SensorUnit [3]: " + str(sensorUnit.symbol))
	print("----------")

def ontimer_sbreak_Attach(self):
	print("Attach [3]!")

def ontimer_sbreak_Detach(self):
	print("Detach [3]!")

def ontimer_lbreak_SensorChange(self, sensorValue, sensorUnit):
	global p_lbreak_limit 
	global p_lbreak_curr 
	p_lbreak_curr = math.ceil(p_lbreak_limit * sensorValue)

	print('p_lbreak time: ' + str(p_lbreak_curr))
	writeLCD(self)
	# print("SensorValue [7]: " + str(sensorValue))
	print('p_lbreak time: ' + str(math.ceil(p_lbreak_limit * sensorValue)))
	# print("SensorUnit [7]: " + str(sensorUnit.symbol))
	print("----------")

def ontimer_lbreak_Attach(self):
	print("Attach [7]!")

def ontimer_lbreak_Detach(self):
	print("Detach [7]!")


def main():
	#Enable server discovery to allow your program to find other Phidgets on the local network.
	Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

	#Create your Phidget channels
	timer_p_work = VoltageRatioInput()
	timer_sbreak = VoltageRatioInput()
	timer_lbreak = VoltageRatioInput()
	timer_button = VoltageRatioInput()
	digitalOutput0 = DigitalOutput() #Red
	digitalOutput1 = DigitalOutput() #Green
	digitalOutput2 = DigitalOutput() #Blue

	lcd = LCD()

	#Set addressing parameters to specify which channel to open (if any)
	timer_p_work.setIsRemote(True)
	timer_p_work.setChannel(2)
	timer_sbreak.setIsRemote(True)
	timer_sbreak.setChannel(3)
	timer_lbreak.setIsRemote(True)
	timer_lbreak.setChannel(7)
	timer_button.setIsRemote(True)
	timer_button.setChannel(5)
	lcd.setIsRemote(True)
	lcd.setChannel(0)

	digitalOutput0.setIsRemote(True)
	# digitalOutput0.setDeviceSerialNumber(39834)
	digitalOutput0.setChannel(0)

	digitalOutput1.setIsRemote(True)
	# digitalOutput1.setDeviceSerialNumber(39834)
	digitalOutput1.setChannel(1)

	digitalOutput2.setIsRemote(True)
	# digitalOutput2.setDeviceSerialNumber(39834)
	digitalOutput2.setChannel(2)

	

	#Assign any event handlers you need before calling open so that no events are missed.
	timer_p_work.setOnSensorChangeHandler(ontimer_p_work_SensorChange)
	timer_p_work.setOnAttachHandler(ontimer_p_work_Attach)
	timer_p_work.setOnDetachHandler(ontimer_p_work_Detach)
	timer_sbreak.setOnSensorChangeHandler(ontimer_sbreak_SensorChange)
	timer_sbreak.setOnAttachHandler(ontimer_sbreak_Attach)
	timer_sbreak.setOnDetachHandler(ontimer_sbreak_Detach)
	timer_lbreak.setOnSensorChangeHandler(ontimer_lbreak_SensorChange)
	timer_lbreak.setOnAttachHandler(ontimer_lbreak_Attach)
	timer_lbreak.setOnDetachHandler(ontimer_lbreak_Detach)
	timer_button.setOnSensorChangeHandler(ontimer_button_SensorChange)
	timer_button.setOnAttachHandler(ontimer_button_Attach)
	timer_button.setOnDetachHandler(ontimer_button_Detach)

	timer_p_work.linkedLCD = lcd
	timer_sbreak.linkedLCD = lcd
	timer_lbreak.linkedLCD = lcd

	#Open your Phidgets and wait for attachment
	digitalOutput0.openWaitForAttachment(20000)
	digitalOutput1.openWaitForAttachment(20000)
	digitalOutput2.openWaitForAttachment(20000)
	lcd.openWaitForAttachment(20000)
	lcd.setBacklight(1)
	timer_p_work.openWaitForAttachment(20000)
	timer_sbreak.openWaitForAttachment(20000)
	timer_lbreak.openWaitForAttachment(20000)
	timer_button.openWaitForAttachment(20000)

	#Set value triggers
	timer_p_work.setSensorValueChangeTrigger(0.1)
	timer_sbreak.setSensorValueChangeTrigger(0.1)
	timer_lbreak.setSensorValueChangeTrigger(0.1)


	#Do stuff with your Phidgets here or in your event handlers.
	#Set the sensor type to match the analog sensor you are using after opening the Phidget
	timer_p_work.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1109)
	timer_sbreak.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1109)
	timer_lbreak.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1109)
	timer_button.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1129)

	print('Digital Output0 Attached')
	digitalOutput0.setDutyCycle(1)
	time.sleep(2) # slows down the event handler
	digitalOutput0.setDutyCycle(0)

	print('Digital Output1 Attached')
	digitalOutput1.setDutyCycle(1)
	time.sleep(2) # slows down the event handler
	digitalOutput1.setDutyCycle(0)

	print('Digital Output2 Attached')
	digitalOutput2.setDutyCycle(1)
	time.sleep(2) # slows down the event handler
	digitalOutput2.setDutyCycle(0)
	print('end LED')



	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	timer_p_work.close()
	timer_sbreak.close()
	timer_lbreak.close()
	timer_button.close()
	digitalOutput0.close()
	digitalOutput1.close()
	digitalOutput2.close()

main()