from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time
from Phidget22.Devices.RFID import *
from Phidget22.Devices.Spatial import *


######################  RFID   #####################
####################################################


def onRFIDTag(self, tag, protocol, state):
    if tag == '01069345ef': #phone rfid
        state['rfid_phone'] = True
    if tag == '0102388876': #friend rfid
        state['rfid_friend'] = True
    printr(state)
    
def onRFIDTagLost(self, tag, protocol, state):
    if tag == '01069345ef': #phone rfid
        state['rfid_phone'] = False
        printr(state)

def setup_rfid_sensor(state):
    rfid_phone = RFID()
    rfid_phone.setDeviceSerialNumber(63558)
    rfid_phone.setOnTagHandler(lambda self, tag, protocol:onRFIDTag(self, tag, protocol, state))
    rfid_phone.setOnTagLostHandler(lambda self, tag, protocol:onRFIDTagLost(self, tag, protocol, state))
    rfid_phone.openWaitForAttachment(5000)
    return rfid_phone


######################  LIGHT   #####################
#####################################################


def onLightSensorChange(self, sensorValue, sensorUnit, state):
    if sensorValue < state['light_trigger']:
        state['light_seated'] = True
        printr(state)
    else:
        state['light_seated'] = False
        printr(state)

def setup_light_sensor(state):
    light_seat = VoltageInput()
    light_seat.setIsHubPortDevice(True)
    light_seat.setHubPort(0)
    light_seat.setOnSensorChangeHandler(lambda self, sensorValue, sensorUnit:onLightSensorChange(self, sensorValue, sensorUnit, state))
    light_seat.openWaitForAttachment(5000)
    light_seat.setSensorType(VoltageSensorType.SENSOR_TYPE_1142)


######################  GYRO   #####################
####################################################


def onGyroSensorChange(self, acceleration, angularRate, magneticField, timestamp, state):
    if str(self) == 'Spatial Ch:0 -> MOT1101 -> HUB0000 Port:3 S/N:626713':
        state['gyro_prev_l'] = abs(round(acceleration[1],2)) if state['gyro_prev_l'] == 0 else state['gyro_prev_l']
        state['gyro_curr_l'] = abs(round(acceleration[1],2)) 
        state['gyro_delta_l'] = abs(state['gyro_curr_l'] - state['gyro_prev_l'])
        if state['gyro_delta_l']>state['gyro_trigger']:
            state['posture_l'] = False
        else:
            state['posture_l'] = True
        printr(state)

    elif str(self) == 'Spatial Ch:0 -> MOT1101 -> HUB0000 Port:2 S/N:626713':
        state['gyro_prev_r'] = abs(round(acceleration[1],2)) if state['gyro_prev_r'] == 0 else state['gyro_prev_r']
        state['gyro_curr_r'] = abs(round(acceleration[1],2)) 
        state['gyro_delta_r'] = abs(state['gyro_curr_r'] - state['gyro_prev_r'])
        if state['gyro_delta_r']>state['gyro_trigger']:
            state['posture_r'] = False
        else:
            state['posture_r'] = True
        printr(state)
    
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


######################  PRINT  #####################
####################################################


def printr(state):
    print(f'PHON{'🟢' if state['rfid_phone'] else '🔴'} FRND{'🟢' if state['rfid_friend'] else '🔴'} SEAT{'🟢' if state['light_seated'] else '🔴'} SHDR{'🟢' if state['posture_r'] else '🔴'} SHDL{'🟢' if state['posture_l'] else '🔴'} ')


######################         #####################
####################################################


def main():
    state = {
        'rfid_phone' : False,
        'rfid_friend' : False,
        'light_seated' : False,
        'light_trigger' : 100,
        'posture_l' : False,
        'posture_r' : False,
        'gyro_prev_l' : 0,
        'gyro_curr_l' : 0,
        'gyro_delta_l' : 0,
        'gyro_prev_r' : 0,
        'gyro_curr_r' : 0,
        'gyro_delta_r' : 0,
        'gyro_trigger' : 0.05
    }

    setup_light_sensor(state)
    setup_rfid_sensor(state)
    setup_gyroscopes(state)

    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

main()