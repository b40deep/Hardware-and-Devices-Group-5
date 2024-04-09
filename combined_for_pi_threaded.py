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

# LED Control based on the timer's state
def control_leds(state):
    # Simplify LED control by turning all off, then selectively turning one on
    state["red_LED"].setState(False)
    state["green_LED"].setState(False)
    state["blue_LED"].setState(False)

    if state["is_paused"]:
        state["blue_LED"].setState(True)
    elif state["current_phase"] == "work":
        state["red_LED"].setState(True)
    else:  # "sbreak" or "lbreak"
        state["green_LED"].setState(True)

def controlServo(state):
    # moving the servo 180 degrees to open or close
    if(state['work_timer'].linkedServo.getAttached()):
        position = state['work_timer'].linkedServo.getTargetPosition()
        # temp=position
        position = 0 if position > 0 else 180
        # print(f'################################################{temp}\t{position}')
        state['work_timer'].linkedServo.setTargetPosition(position)

def controlBuzzer(state):
    # make the buzzer go off
    if(not state['work_timer'].linkedEvent.is_set()):
            state['work_timer'].linkedEvent.set()

def userReady():
    # check if the user is seated, gyros okay, and phone present
    return bool(dict.get("light_seated")=="True") and bool(dict.get("phone_rfid")=="True") and bool(dict.get("posture_l")=="True") and bool(dict.get("posture_r")=="True")
    

def onLbreakTimerChange(self, voltage):
    # print(f'lbreak: {voltage:.2f}')
    dict.update("lbreak", str(voltage))

def onSbreakTimerChange(self, voltage):
    # print(f'sbreak: {voltage:.2f}')
    dict.update("sbreak", str(voltage))
    # if(not self.linkedEvent.is_set()):
    #     self.linkedEvent.set()

def onWorkTimerChange(self, voltage):
    # print(f'work: {voltage:.2f}')
    dict.update("work", str(voltage))
    # if(self.linkedServo.getAttached()):
    #     self.linkedServo.setTargetPosition(10 + voltage*30)

def onServoPositionChange(self, position):
    # print(f'servo_pos: {position:.2f}')
    dict.update("servo_pos", str(position))

def onTouchSensorChange(self, sensorValue, sensorUnit, state):
    printr('touch_sensor')
    # print(f'touch_sensor: {sensorValue}')
    dict.update("touch_sensor", str(sensorValue))
    if userReady():
        if sensorValue>0:
            togglePomodoro(state)

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
		for i in range(15):
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


# Handler for sensor change events, updating timer states     
def create_timer_sensor_change_handler(lcd, state, time_block_type):
    '''
	sensor: 	  The Phidget sensor object that triggered the event. While it's not used in this function, 
	              it's necessary to include it to match the signature expected by the Phidgets library.
	sensor_value: The value of the sensor that triggered the event.
	sensor_unit:  The unit of the sensor value. This might not be used in your particular implementation 
	              but is included to match the Phidgets event handler signature.
	'''
    def on_timer_sensor_change(sensor, sensor_value, sensor_unit):
        print(f"Sensor Value Changed: {sensor_value} for {time_block_type}")   # Debugging line
        # Update time based on sensor input
        new_value = math.ceil(60 * sensor_value) if time_block_type == "work" else \
                    math.ceil(30 * sensor_value) if time_block_type == "sbreak" else \
                    math.ceil(90 * sensor_value)
        print(f"New {time_block_type} value: {new_value}")  # Debugging line to see the calculated new value
        # Update state
        state['timer_states'][time_block_type] = new_value
        # Immediately update the LCD with new times
        message = "WORK  SHORTB  LONGB"
        detail = f"{state['timer_states']['work']:02d}     {state['timer_states']['sbreak']:02d}     {state['timer_states']['lbreak']:02d}"
        write_lcd(lcd, message, detail)
    return on_timer_sensor_change

# Set up the sensor for detecting changes and starting the pomodoro cycle
def setup_timer(timer, lcd, state, device_serial_number, channel, time_block_type):
    # timer = VoltageRatioInput()
    # uncomment line below if connecting to rasberry pi network instead of locally connecting
    # timer.setIsRemote(True)
    timer.setDeviceSerialNumber(device_serial_number)
    timer.setChannel(channel)
    timer.setOnSensorChangeHandler(create_timer_sensor_change_handler(lcd, state, time_block_type))
    timer.openWaitForAttachment(5000)
    timer.setSensorValueChangeTrigger(0.001)
    timer.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1109)
    return timer

def togglePomodoro(state):
    # while bool(dict.get("light_seated")=="True") and bool(dict.get("phone_rfid")=="True") and bool(dict.get("posture_l")=="True") and bool(dict.get("posture_r")=="True"):
    # if preconditions are not met, timer button has to be pressed to start / resume
    current_time = time.time()
    with state["pause_condition"]:  # Use the condition to synchronise state changes
        # If pomodoro countdown is not running, start it
        if not state["is_running"]:
            state["is_running"] = True
            state["is_paused"] = False
            # If pomodoro countdown had previously started, allow the existing countdown to proceed.
            if not state["timer_thread"].is_alive():
                state["timer_thread"] = threading.Thread(target=run_pomodoro, args=(state,))
                state["timer_thread"].start()  
        # Pause the countdown if it's running        
        elif state["is_running"] and not state["is_paused"]:
            state["is_paused"] = True
            state["pause_time"] = current_time  # Record pause time for resuming countdown
            write_lcd(state["lcd"], "PAUSED", "")
        else:
            pause_duration = current_time - state.get("pause_time", current_time)
            state["end_time"] += pause_duration  # Adjust end time by pause duration
            state["is_paused"] = False
            write_lcd(state["lcd"], "RESUMED", "")
            state["pause_condition"].notify()  # Notify the countdown thread to resume
    control_leds(state) # Control LEDs after state update

# Run through a pomodoro cycle of work and break periods
def run_pomodoro(state):
    phases = ["work", "sbreak"] * 3 + ["work", "lbreak"]
    for phase in phases:
        state["current_phase"] = phase  # Update the current phase
        if not state["is_running"] or state["is_paused"]:
            continue
        control_leds(state) # Control LEDs here for the new phase
        countdown(state, phase)
        if phase == "lbreak":  # End cycle after long break
            state["is_running"] = False
            break
    control_leds(state) # Also control LEDs when the pomodoro cycle completes
    write_lcd(state["lcd"], "Pomodoro Complete", "")

def countdown(state, phase):
    limit = state["timer_states"][phase] * 6  # Convert minutes to seconds
    state["end_time"] = time.time() + limit
    while time.time() < state["end_time"]:
        if not state["is_running"]:
            return
        if state["is_paused"]:
            with state["pause_condition"]:
                state["pause_condition"].wait()  # Wait until notified to resume
        remaining = state["end_time"] - time.time()
        mins, secs = divmod(int(remaining), 60)
        message = f"{phase.upper()}"
        detail = f"Time left: {mins:02d}:{secs:02d}"
        write_lcd(state["lcd"], message, detail)
        time.sleep(1)  # Use time.sleep(60) for real-time countdown
    print(f'timer done: {phase}')
    # These happen at the end of every countdown e.g., end of work phase, end of break phase, etc.
    if phase == "work":
        controlBuzzer(state) # Buzz when it's break time.
        controlServo(state) #   Open the phone holder for break times
    if (phase == "sbreak" or phase == "lbreak") and dict.get("phone_rfid") == "True" :
        controlServo(state) #   Close the phone holder for work times

def setup_touch(touch_sensor, LCD_SERIAL_NUM, state):
    touch_sensor.setDeviceSerialNumber(LCD_SERIAL_NUM)
    touch_sensor.setChannel(5)
    touch_sensor.setIsRemote(1)
    touch_sensor.setOnSensorChangeHandler(lambda self, sensorValue, sensorUnit:onTouchSensorChange(self, sensorValue, sensorUnit, state))
    touch_sensor.openWaitForAttachment(5000)
    touch_sensor.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1110)

def setup_servo(desk_servo, SERVO_SERIAL_NUM):
    desk_servo.setDeviceSerialNumber(SERVO_SERIAL_NUM)
    desk_servo.setIsRemote(1)
    desk_servo.setOnPositionChangeHandler(onServoPositionChange)
    desk_servo.openWaitForAttachment(5000)
    desk_servo.setTargetPosition(0)
    desk_servo.setEngaged(True) 

def setup_buzzer(buzzer, buzzerOutput, LCD_SERIAL_NUM):
    buzzer.setDeviceSerialNumber(LCD_SERIAL_NUM)
    buzzer.setChannel(7)
    buzzer.openWaitForAttachment(5000)
    buzzerOutput.start() # Start thread after opening channels
    buzzer.setDutyCycle(0)

def setup_light(light_seated):
    light_seated.setHubPort(0)
    light_seated.setOnSensorChangeHandler(onLightSensorChange)
    light_seated.openWaitForAttachment(5000)
    light_seated.setSensorType(VoltageSensorType.SENSOR_TYPE_1142)

def setup_rfid_phone(rfid_phone):
    rfid_phone.setOnTagHandler(onRFIDTag)
    rfid_phone.setOnTagLostHandler(onRFIDTagLost)
    rfid_phone.openWaitForAttachment(5000)

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
    dict.setDeviceLabel("testdict")
    lcd = LCD()
    lbreak_timer = VoltageRatioInput()
    sbreak_timer = VoltageRatioInput()
    work_timer = VoltageRatioInput()
    desk_servo = RCServo()
    touch_sensor = VoltageRatioInput()
    buzzer = DigitalOutput()
    light_seated = VoltageInput()
    light_seated.setIsHubPortDevice(True)
    rfid_phone = RFID()
    rfid_phone.setDeviceSerialNumber(RFID_SERIAL_NUM)

    #Set addressing parameters to specify which channel to open (if any)
    lcd.setDeviceSerialNumber(LCD_SERIAL_NUM) 
    lcd.setChannel(0)
    lcd.openWaitForAttachment(4000) 
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

    # dictionary to handle State management
    state= {
        "timer_thread": threading.Thread(),  # Placeholder for the countdown thread
        "pause_condition": threading.Condition(),  # Use a condition to synchronise state changes
        "is_running": False, # Placeholder for the running state of the pomodoro cycle
        "is_paused": False, # Placeholder for the paused state of the pomodoro cycle
        "pause_time": 0, # Placeholder for the time the pause button was pressed 
        "end_time": 0, # Placeholder for the end time of the current phase
        "timer_states": {"work": 1, "sbreak": 1, "lbreak": 1}, # Example default values
        "current_phase": None, # Placeholder for the current phase of the pomodoro cycle
        "last_toggle": 0, # Placeholder for the last time the touch sensor was toggled
        "lcd": lcd, # Placeholder for the LCD object
        "red_LED": red_LED,
        "green_LED": green_LED,
        "blue_LED": blue_LED,

        "work_timer": work_timer,
    }


    dict.setIsRemote(1)
    dict.openWaitForAttachment(4000)
    dict.set("servo_pos", "0")
    dict.set("lbreak", "0")
    dict.set("sbreak", "0")
    dict.set("work", "0")
    dict.set("touch_sensor", "0")
    dict.set("light_seated", "False")
    dict.set("light_trigger", "100")    # don't think needed in live dictionary
    dict.set("phone_rfid", "False")
    dict.set("friend_rfid", "False")
    dict.set("gyro_prev_l", "0")    # don't think needed in live dictionary
    dict.set("gyro_curr_l", "0")    # don't think needed in live dictionary
    dict.set("gyro_delta_l", "0")   # don't think needed in live dictionary
    dict.set("posture_l", "False")
    dict.set("gyro_prev_r", "0")    # don't think needed in live dictionary
    dict.set("gyro_curr_r", "0")    # don't think needed in live dictionary
    dict.set("gyro_delta_r", "0")   # don't think needed in live dictionary
    dict.set("posture_r", "False")
    dict.set("gyro_trigger", "0")   # don't think needed in live dictionary


    	# Setup timers for work, short break, and long break with initial times
    lbreak_timer.setIsRemote(1)
    sbreak_timer.setIsRemote(1)
    work_timer.setIsRemote(1)
    setup_timer(work_timer, lcd, state, LCD_SERIAL_NUM, 2, "work")
    setup_timer(sbreak_timer, lcd, state, LCD_SERIAL_NUM, 3, "sbreak")
    setup_timer(lbreak_timer, lcd, state, LCD_SERIAL_NUM, 7, "lbreak")
    #Here we create an attribute of input called "linkedOutput", and assign it the handle for output
    work_timer.linkedServo = desk_servo

    setup_touch(touch_sensor, LCD_SERIAL_NUM, state)
    setup_servo(desk_servo, SERVO_SERIAL_NUM)

    # Create a Thread and Event for buzzer and pass the Event to a Phidget 
    buzzerEvent = Event()
    buzzerOutput = Thread(target=buzzer_Output, args=(buzzerEvent, buzzer),daemon=True)
    work_timer.linkedEvent = buzzerEvent # link buzzer to something for it to work
    setup_buzzer(buzzer, buzzerOutput, LCD_SERIAL_NUM)
    setup_light(light_seated)
    setup_rfid_phone(rfid_phone)
    setup_gyroscopes(state)

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