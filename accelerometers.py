
from Phidget22.Phidget import *
from Phidget22.Devices.Accelerometer import *
import time


def onAccelerometer0_AccelerationChange(self, acceleration, timestamp):
    print(f'Acceleration:  {acceleration[0]:.2f}   |   {acceleration[1]:.2f}   |   {acceleration[2]:.2f}')
    # print("Timestamp: " + str(timestamp))
    print("----------")
def change(acc, val):
    print(val)
    print(acc.getAcceleration())
def main():
    accelerometer0 = Accelerometer()
    accelerometer0.setHubPort(2)
    accelerometer0.setDeviceSerialNumber(626713)
    accelerometer0.setOnAccelerationChangeHandler(onAccelerometer0_AccelerationChange)
    accelerometer0.openWaitForAttachment(5000)

    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    accelerometer0.close()

main()