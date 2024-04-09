from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.RCServo import *
import time
from Phidget22.Net import *
from Phidget22.Devices.Dictionary import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageRatioInput import *
import math
from Phidget22.Devices.LCD import *
from Phidget22.Devices.DigitalOutput import *
import threading
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.RFID import *
from Phidget22.Devices.Spatial import *
from threading import Thread, Event


#   dictionary must be global
dict = Dictionary()

def onLbreakTimerChange(self, voltage):
    # print(f'lbreak: {voltage:.2f}')
    dict.update("lbreak", str(voltage))
    if(self.linkedServo.getAttached()):
        self.linkedServo.setTargetPosition(10 + voltage*30)

def onSbreakTimerChange(self, voltage):
    # print(f'sbreak: {voltage:.2f}')
    dict.update("sbreak", str(voltage))
    if(not self.linkedEvent.is_set()):
        self.linkedEvent.set()

def onWorkTimerChange(self, voltage):
    # print(f'work: {voltage:.2f}')
    dict.update("work", str(voltage))

def onServoPositionChange(self, position):
    # print(f'servo_pos: {position:.2f}')
    dict.update("servo_pos", str(position))

def onTouchSensorChange(self, sensorValue, sensorUnit):
    printr('touch_sensor')
    # print(f'touch_sensor: {sensorValue}')
    dict.update("touch_sensor", str(sensorValue))

def onLightSensorChange(self, sensorValue, sensorUnit):
    # if sensorValue < 100: # state['light_trigger']
    if sensorValue < int(dict.get('light_trigger')): # state['light_trigger']
        # print(f'light_seated: {sensorValue}')
        dict.update("light_seated", str(True))
    else:
        # print(f'light_seated: {sensorValue}')
        dict.update("light_seated", str(False))

def onRFIDTag(self, tag, protocol):
    if tag == '01069345ef': #phone rfid
        # print(f'phone_rfid: {True}')
        dict.update("phone_rfid", str(True))
    if tag == '0102388876': #friend rfid
        # print(f'friend_rfid: {True}')
        dict.update("friend_rfid", str(True))
    
def onRFIDTagLost(self, tag, protocol):
    if tag == '01069345ef': #phone rfid
        # print(f'phone_rfid: {False}')
        dict.update("phone_rfid", str(False))

def onGyroSensorChange(self, acceleration, angularRate, magneticField, timestamp, state):
    if str(self) == 'Spatial Ch:0 -> MOT1101 -> HUB0000 Port:3 S/N:626713':
        prev = float(dict.get('gyro_prev_l'))
        curr = abs(round(acceleration[1],2))
        delta = curr - prev
        trigger = float(dict.get('gyro_trigger'))
        posture = None
        if prev == 0: dict.update('gyro_prev_l', str(curr)) 
        dict.update('gyro_curr_l', str(curr))
        dict.update('gyro_delta_l', str(curr - prev))
        posture = False if delta > trigger else True
        dict.update("posture_l", str(posture))
        # print(f'posture_l: {posture}')

    elif str(self) == 'Spatial Ch:0 -> MOT1101 -> HUB0000 Port:2 S/N:626713':
        prev = float(dict.get('gyro_prev_r'))
        curr = abs(round(acceleration[1],2))
        delta = curr - prev
        trigger = float(dict.get('gyro_trigger'))
        posture = None
        if prev == 0: dict.update('gyro_prev_r', str(curr)) 
        dict.update('gyro_curr_r', str(curr))
        dict.update('gyro_delta_r', str(curr - prev))
        posture = False if delta > trigger else True
        dict.update("posture_r", str(posture))
        # print(f'posture_r: {posture}')
        

def buzzer_Output(buzzerEvent, buzzer):
	while buzzerEvent.wait():
		for i in range(10):
			buzzer.setDutyCycle(0)
			time.sleep(1/3000)
			buzzer.setDutyCycle(1)
			time.sleep(1/3000)
		buzzerEvent.clear()

def printr(key):
    # print('dict update')
    # if key == "touch_sensor"or "light_seated"or "phone_rfid"or "friend_rfid"or "posture_l"or "posture_r":
    if True:
        touch_sensor = dict.get("touch_sensor")
        light_seated = dict.get("light_seated")
        phone_rfid = dict.get("phone_rfid")
        friend_rfid = dict.get("friend_rfid")
        posture_l = dict.get("posture_l")
        posture_r = dict.get("posture_r")
        print(f'"touch_sensor"{touch_sensor}\t"light_seated"{light_seated}\t"phone_rfid"{phone_rfid}\t"friend_rfid"{friend_rfid}\t"posture_l"{posture_l} \t"posture_r"{posture_r}')

# Update the LCD with a new message (reflects user's time settings or countdown of current time block)
def write_lcd(lcd, message, detail):
    lcd.clear()
    lcd.writeText(LCDFont.FONT_5x8, 0, 0, message)
    lcd.writeText(LCDFont.FONT_5x8, 0, 1, detail)
    lcd.flush()

def setup_gyroscopes(state):
    gyroR = Spatial()
    gyroR.setHubPort(2)
    gyroR.setDeviceSerialNumber(626713)
    gyroR.setOnSpatialDataHandler(lambda self, acceleration, angularRate, magneticField, timestamp: onGyroSensorChange(self, acceleration, angularRate, magneticField, timestamp, state))
    gyroR.openWaitForAttachment(5000)
    gyroL = Spatial()
    gyroL.setHubPort(3)
    gyroL.setDeviceSerialNumber(626713)
    gyroL.setOnSpatialDataHandler(lambda self, acceleration, angularRate, magneticField, timestamp: onGyroSensorChange(self, acceleration, angularRate, magneticField, timestamp, state))
    gyroL.openWaitForAttachment(5000)

def main():

    #Enable server discovery to list remote phidgets
    Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE) 
    #Add a specific remote server to communicate with Phidget remotely
    # Net.addServer("raspberrypi.local", "137.44.181.148", 5661, "", 0)
    Net.addServer("raspberrypi.local", "192.168.137.254", 5661, "", 0)

    #   setup some variables
    LCD_SERIAL_NUM = 39834
    SERVO_SERIAL_NUM = 14559
    RFID_SERIAL_NUM = 63558
        
    #   setup the phidgets
    lbreak_timer = VoltageInput()
    sbreak_timer = VoltageInput()
    work_timer = VoltageInput()
    desk_servo = RCServo()
    dict.setDeviceLabel("testdict")
    lcd = LCD()
    touch_sensor = VoltageRatioInput()
    buzzer = DigitalOutput()
    light_seated = VoltageInput()
    light_seated.setIsHubPortDevice(True)
    rfid_phone = RFID()
    rfid_phone.setDeviceSerialNumber(RFID_SERIAL_NUM)

    #Set addressing parameters to specify which channel to open (if any)
    lcd.setDeviceSerialNumber(LCD_SERIAL_NUM) 
    lcd.setChannel(0)
    lcd.openWaitForAttachment(6000) 
    lcd.setBacklight(1)
    # Display "Pomodoro Timer" and "Ready" for 3 seconds  
    write_lcd(lcd, "Pomodoro Timer", "Ready")

    #   Initialise LEDs
    red_LED = DigitalOutput()
    green_LED = DigitalOutput()
    blue_LED = DigitalOutput()
    #   Set device serial numbers and channels for LEDs
    leds = [red_LED, green_LED, blue_LED]
    for led, channel in zip(leds, [0, 1, 2]):
        led.setDeviceSerialNumber(LCD_SERIAL_NUM)  # Assuming LEDs are connected to the same interface
        led.setChannel(channel)
        led.openWaitForAttachment(5000)
    
    time.sleep(0.5)  # Wait for 1 second
    red_LED.setState(True)
    time.sleep(0.5)  # Wait for 1 second
    red_LED.setState(False)
    green_LED.setState(True)
    time.sleep(0.5)  # Wait for 1 second
    green_LED.setState(False)
    blue_LED.setState(True)
    time.sleep(0.5)  # Wait for 1 second
    blue_LED.setState(False)

    lbreak_timer.setDeviceSerialNumber(LCD_SERIAL_NUM)
    lbreak_timer.setChannel(7)
    sbreak_timer.setDeviceSerialNumber(LCD_SERIAL_NUM)
    sbreak_timer.setChannel(3)
    work_timer.setDeviceSerialNumber(LCD_SERIAL_NUM)
    work_timer.setChannel(2)
    touch_sensor.setDeviceSerialNumber(LCD_SERIAL_NUM)
    touch_sensor.setChannel(5)
    desk_servo.setDeviceSerialNumber(SERVO_SERIAL_NUM)
    buzzer.setDeviceSerialNumber(LCD_SERIAL_NUM)
    buzzer.setChannel(7)

    dict.setIsRemote(1)
    lbreak_timer.setIsRemote(1)
    sbreak_timer.setIsRemote(1)
    work_timer.setIsRemote(1)
    desk_servo.setIsRemote(1)
    touch_sensor.setIsRemote(1)
    # light_seated.setIsRemote(1)

    #Here we create an attribute of input called "linkedOutput", and assign it the handle for output
    lbreak_timer.linkedServo = desk_servo
    # Create a Thread and Event for buzzer and pass the Event to a Phidget 
    buzzerEvent = Event()
    buzzerOutput = Thread(target=buzzer_Output, args=(buzzerEvent, buzzer),daemon=True)
    sbreak_timer.linkedEvent = buzzerEvent # link buzzer to something for it to work


    light_seated.setHubPort(0)
    light_seated.setOnSensorChangeHandler(onLightSensorChange)
    rfid_phone.setOnTagHandler(onRFIDTag)
    rfid_phone.setOnTagLostHandler(onRFIDTagLost)
    buzzer.openWaitForAttachment(5000)
    sbreak_timer.openWaitForAttachment(5000)
    lbreak_timer.setOnVoltageChangeHandler(onLbreakTimerChange)
    sbreak_timer.setOnVoltageChangeHandler(onSbreakTimerChange)
    work_timer.setOnVoltageChangeHandler(onWorkTimerChange)
    desk_servo.setOnPositionChangeHandler(onServoPositionChange)
    touch_sensor.setOnSensorChangeHandler(onTouchSensorChange)


    dict.openWaitForAttachment(4000)
    dict.set("servo_pos", "0")
    dict.set("lbreak", "0")
    dict.set("sbreak", "0")
    dict.set("work", "0")
    dict.set("touch_sensor", "0")
    dict.set("light_seated", "False")
    dict.set("light_trigger", "100")
    dict.set("phone_rfid", "False")
    dict.set("friend_rfid", "False")
    dict.set("gyro_prev_l", "0")
    dict.set("gyro_curr_l", "0")
    dict.set("gyro_delta_l", "0")
    dict.set("posture_l", "0")
    dict.set("gyro_prev_r", "0")
    dict.set("gyro_curr_r", "0")
    dict.set("gyro_delta_r", "0")
    dict.set("posture_r", "0")
    dict.set("gyro_trigger", "0")

    setup_gyroscopes(state=None)

    lbreak_timer.openWaitForAttachment(5000)
    work_timer.openWaitForAttachment(5000)
    desk_servo.openWaitForAttachment(5000)
    touch_sensor.openWaitForAttachment(5000)
    touch_sensor.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1110)
    light_seated.openWaitForAttachment(5000)
    light_seated.setSensorType(VoltageSensorType.SENSOR_TYPE_1142)
    rfid_phone.openWaitForAttachment(5000)

    buzzerOutput.start() # Start thread after opening channels
    buzzer.setDutyCycle(0)


    lbreak_timer.setVoltageChangeTrigger(0.1)
    sbreak_timer.setVoltageChangeTrigger(0.1)
    work_timer.setVoltageChangeTrigger(0.1)

    desk_servo.setTargetPosition(0)
    desk_servo.setEngaged(True) 




    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    desk_servo.close()
    lbreak_timer.close()
    sbreak_timer.close()
    work_timer.close()
    buzzer.close()
    dict.close()

main()