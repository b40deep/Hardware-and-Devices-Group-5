from Phidget22.Phidget import *
from Phidget22.Devices.Spatial import *
import time

gyro_prev_l = 0
gyro_curr_l = 0
gyro_delta_l = 0
gyro_prev_r = 0
gyro_curr_r = 0
gyro_delta_r = 0
gyro_trigger = 0.05

def onGyro_SpatialData(self, acceleration, angularRate, magneticField, timestamp):
    if str(self) == 'Spatial Ch:0 -> MOT1101 -> HUB0000 Port:3 S/N:626713':
        # print("Acceleration: \t"+ str(acceleration[0])+ "  |  "+ str(acceleration[1])+ "  |  "+ str(acceleration[2]))
        # print("AngularRate: \t"+ str(angularRate[0])+ "  |  "+ str(angularRate[1])+ "  |  "+ str(angularRate[2]))
        # print("MagneticField: \t"+ str(magneticField[0])+ "  |  "+ str(magneticField[1])+ "  |  "+ str(magneticField[2]))
        # print("Timestamp: " + str(timestamp))
        # print(f'ACC0:{acceleration[0]:.2f}')
        # print(f'ACC0:{acceleration[1]:.2f}')
        # print(f'ACC0:{acceleration[2]:.2f}')
        global gyro_prev_l
        global gyro_curr_l
        global gyro_delta_l
        global gyro_trigger
        gyro_prev_l = abs(round(acceleration[1],2)) if gyro_prev_l == 0 else gyro_prev_l
        gyro_curr_l = abs(round(acceleration[1],2)) 
        gyro_delta_l = abs(gyro_curr_l - gyro_prev_l)
        # print(f'delta {delta} {(">") if delta>trigger else ("<")} {trigger}')
        print(f'LEFT {("👎") if gyro_delta_l>gyro_trigger else ("👍") } ')
        # print("----------")
    elif str(self) == 'Spatial Ch:0 -> MOT1101 -> HUB0000 Port:2 S/N:626713':
        global gyro_prev_r
        global gyro_curr_r
        global gyro_delta_r
        gyro_prev_r = abs(round(acceleration[1],2)) if gyro_prev_r == 0 else gyro_prev_r
        gyro_curr_r = abs(round(acceleration[1],2)) 
        gyro_delta_r = abs(gyro_curr_r - gyro_prev_r)
        # print(f'delta {delta} {(">") if delta>trigger else ("<")} {trigger}')
        print(f'RGHT {("👎") if gyro_delta_r>gyro_trigger else ("👍") } ')
    
def setup_gyroscopes():
    gyroR = Spatial()
    gyroR.setHubPort(2)
    gyroR.setDeviceSerialNumber(626713)
    gyroR.setOnSpatialDataHandler(onGyro_SpatialData)
    gyroR.openWaitForAttachment(5000)
    gyroL = Spatial()
    gyroL.setHubPort(3)
    gyroL.setDeviceSerialNumber(626713)
    gyroL.setOnSpatialDataHandler(onGyro_SpatialData)
    gyroL.openWaitForAttachment(5000)

def main():
    setup_gyroscopes()
    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    # gyro0.close()

main()

