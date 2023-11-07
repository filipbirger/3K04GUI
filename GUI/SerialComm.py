import serial
import struct

class SerialComm:
    
    def __init__(self):
        self.comm = serial.Serial()
        self.isConnected = False
    
    def connect(self):
        try:
            self.comm.baudrate = 115200
            self.comm.port = "Com7"
            self.isConnected = True
        except serial.SerialException as error:
            print("Error",error)
            self.isConnected = False


    
    def serWriteAOO(self, lowerRateLimit, upperRateLimit,atrialAmplitude,atrialPulseWidth):
        try:
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pAtrialAmplitude = struct.pack("F",atrialAmplitude )
            pAtrialPulseWidth = struct.pack("F",atrialPulseWidth)

            write = b"\x16\x55"+pLowerRateLimit+pUpperRateLimit+pAtrialAmplitude+pAtrialPulseWidth
            self.comm.write(write)
        
        except serial.SerialTimeoutException as error:
            print("Error",error)
            
    def serVerify(self):
        return






