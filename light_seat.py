from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time

# def onVoltageInput0_SensorChange(self, sensorValue, sensorUnit):
#     # print("SensorValue: " + str(sensorValue))
#     # print("SensorUnit: " + str(sensorUnit.symbol))
#     if sensorValue < light_trigger:
#         print("Seated")
#     else:
#         print('.')

def onLightSensorChange(self, sensorValue, sensorUnit, state):
    # print("SensorValue: " + str(sensorValue))
    # print("SensorUnit: " + str(sensorUnit.symbol))
    if sensorValue < state['light_trigger']:
        print("Seated")
    else:
        print('.')

def setup_light_sensor(state):
    light_seat = VoltageInput()
    light_seat.setIsHubPortDevice(True)
    light_seat.setHubPort(0)
    light_seat.setOnSensorChangeHandler(lambda self, sensorValue, sensorUnit:onLightSensorChange(self, sensorValue, sensorUnit, state))
    light_seat.openWaitForAttachment(5000)
    light_seat.setSensorType(VoltageSensorType.SENSOR_TYPE_1142)
    
def main():
    state = {
        'light_trigger' : 100
    }

    setup_light_sensor(state)
    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

main()