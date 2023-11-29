import serial
import struct
import DataBase as db
import numpy as np
import time
from SerialTesting import SerialTesting

class SerialComm:
    
    def __init__(self):
        self.comm = serial.Serial()
        self.isConnected = False
        self.egramList = []
        self.verifySum = 0.0
    
    def connect(self):
        try:
            self.comm.baudrate = 115200
            self.comm.port = "Com7"
            self.isConnected = True
            self.comm.open()
        except serial.SerialException as error:
            print("Error",error)
            self.isConnected = False


    def serWriteAOO(self, mode, user):
        try:
            temp = b''

            # Iterate over the attributes of the user object
            for attr in list(vars(user))[3:]:
                if attr == '_atrialAmplitude' or attr == '_atrialPulseWidth' or attr == '_ventricularAmplitude' or attr == '_ventricularPulseWidth' :
                    value = getattr(user, attr)
                    self.verifySum +=value
                    temp += struct.pack("f", value)

                else:
                    value = getattr(user, attr)
                    intValue = int(value)
                    self.verifySum +=value
                    temp += struct.pack("h", intValue)
            
            pmode = struct.pack("h", mode)
            sVerifySum = struct.pack("f", self.verifySum)


            write = b"\x16\x17" + pmode + temp + sVerifySum
            print(write)
        
        except serial.SerialTimeoutException as error:
            print("Error", error)

    
    def verifySum(self):
        data = self.comm.read(2)
        if data == b"\x16\x18":
            print("Error")
        else: 
            pass
        

    def readIn(self):
        while True:
            try:
                self.serialWrite = b"\x16\x19"
                self.comm.write(self.serialWrite)    

                data = self.comm.read(16)
                ATR_signal = struct.unpack("d", data[0:8])[0]
                VENT_signal = struct.unpack("d", data[8:16])[0]
                self.egramList.append([ATR_signal,VENT_signal])
                if len(self.egramList)>20:
                    self.egramList.pop(0)
                time.sleep(0.2)
            except KeyboardInterrupt:
                print("Stopping continuous reading.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

       
    def testSerial(self):
        i = 0
        for i in range(30):  # Read 100 times for testing
            self.readIn()
            print(self.egramList[-1])
        print("Test completed.")

    

    

    

