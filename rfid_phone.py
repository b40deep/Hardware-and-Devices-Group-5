from Phidget22.Phidget import *
from Phidget22.Devices.RFID import *

def onAttach(self):
    print("Attach!")

def onDetach(self):
    print("Detach!")

def onRFIDTag(self, tag, protocol):
    print(f"{'Phone connected!' if tag == '01069345ef' else 'Friend recorded!' if tag == '0102388876' else None}")
    print("----------")

def onRFIDTagLost(self, tag, protocol):
    print(f"{'Phone disconnected!' if tag == '01069345ef' else ''}")
    print("----------")

def setup_rfid_sensor():
    rfid_phone = RFID()
    rfid_phone.setDeviceSerialNumber(63558)
    rfid_phone.setOnTagHandler(onRFIDTag)
    rfid_phone.setOnTagLostHandler(onRFIDTagLost)
    rfid_phone.setOnAttachHandler(onAttach)
    rfid_phone.setOnDetachHandler(onDetach)
    rfid_phone.openWaitForAttachment(5000)
    return rfid_phone

def close_sensors():
    print('available sensors closed')

def main():
    setup_rfid_sensor()

    try:
        input("Press Enter to close...\n")
    finally:
        None

if __name__ == "__main__":
    main()