from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageRatioInput import *
import time
import math
from Phidget22.Devices.LCD import *
from Phidget22.Devices.DigitalOutput import *
import threading

# Event handlers for Phidget device attachment and detachment      
def on_attach(channel):
	    print("Attached Channel: " + str(channel.getChannel()))
		
def on_detach(channel):
	    print("Detached Channel: " + str(channel.getChannel()))
            
# Update the LCD with a new message (reflects user's time settings or countdown of current time block)
def write_lcd(lcd, message, detail):
	lcd.clear()
	lcd.writeText(LCDFont.FONT_5x8, 0, 0, message)
	lcd.writeText(LCDFont.FONT_5x8, 0, 1, detail)
	lcd.flush()
     
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
def setup_timer(lcd, state, device_serial_number, channel, time_block_type):
    timer = VoltageRatioInput()
    # uncomment line below if connecting to rasberry pi network instead of locally connecting
    # timer.setIsRemote(True)
    timer.setDeviceSerialNumber(device_serial_number)
    timer.setChannel(channel)
    timer.setOnSensorChangeHandler(create_timer_sensor_change_handler(lcd, state, time_block_type))
    timer.setOnAttachHandler(on_attach)
    timer.setOnDetachHandler(on_detach)
    timer.openWaitForAttachment(5000)
    timer.setSensorValueChangeTrigger(0.001)
    timer.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1109)
    return timer
	        
def setup_touch_sensor(device_serial_number, channel, state):
    touch_sensor = VoltageRatioInput()
    touch_sensor.setDeviceSerialNumber(device_serial_number)
    touch_sensor.setChannel(channel)
    touch_sensor.setOnSensorChangeHandler(lambda sensor, value, unit: toggle_pomodoro(state, value))
    touch_sensor.openWaitForAttachment(5000)
    touch_sensor.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1110)
    return touch_sensor

# Toggle the pomodoro timer between running, paused, and stopped states
def toggle_pomodoro(state, sensor_value):
    current_time = time.time()
    # Debounce if the last toggle was less than 3 second ago, or if sensor value doesnt indicate a touch
    if current_time - state["last_toggle"] < 3 or sensor_value <= 0:
        return
    state["last_toggle"] = current_time

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
    # phases = ["work", "sbreak"] * 3 + ["work", "lbreak"]
    phases = ["work", "sbreak", "lbreak"]
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
    limit = state["timer_states"][phase] * 60  # Convert minutes to seconds
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


def main():
	
	#Enable server discovery to allow your program to find other Phidgets on the local network.
    Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)
    Net.addServer("raspberrypi.local", "192.168.137.254", 5661, "", 0)

    lcd_serial_number = 39834
   #Create required Phidget channels
    lcd = LCD()
	
    # uncomment below block of code if connecting to rasberry pi network instead of locally connecting
    # lcd.setIsRemote(True)
	# timer_button.setIsRemote(True)
	# red_LED.setIsRemote(True)
	# blue_LED.setIsRemote(True)
	# green_LED.setIsRemote(True)
	
	#Set addressing parameters to specify which channel to open (if any)
    lcd.setDeviceSerialNumber(lcd_serial_number) 
    lcd.setChannel(0)
    lcd.openWaitForAttachment(20000) 
    lcd.setBacklight(1)
	# Display "Pomodoro Timer" and "Ready" for 3 seconds  
    write_lcd(lcd, "Pomodoro Timer", "Ready")  
    time.sleep(1)  # Wait for 3 seconds
     
    # Initialise LEDs
    red_LED = DigitalOutput()
    green_LED = DigitalOutput()
    blue_LED = DigitalOutput() 
    # Set device serial numbers and channels for LEDs
    leds = [red_LED, green_LED, blue_LED]
    for led, channel in zip(leds, [0, 1, 2]):
        led.setDeviceSerialNumber(lcd_serial_number)  # Assuming LEDs are connected to the same interface
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
        "blue_LED": blue_LED
	}
    
	# Setup timers for work, short break, and long break with initial times
    setup_timer(state["lcd"], state, lcd_serial_number, 2, "work")
    setup_timer(state["lcd"], state, lcd_serial_number, 3, "sbreak")
    setup_timer(state["lcd"], state, lcd_serial_number, 7, "lbreak")
    # Setup touch sensor for starting and pausing the pomodoro cycle
    setup_touch_sensor(lcd_serial_number, 5, state)

    # Initial LCD display with default or prompted values
    message = "WORK  SHORTB  LONGB"  
    detail = f'{state["timer_states"]["work"]:02d}     {state["timer_states"]["sbreak"]:02d}     {state["timer_states"]["lbreak"]:02d}'
    write_lcd(state["lcd"], message, detail)
      
    try:
        input("Press Enter to close...\n")
    finally:
        state["lcd"].close()
        for led in leds:
            led.close()

if __name__ == "__main__":
    main()
