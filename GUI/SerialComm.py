import serial as ser
import struct
import DataBase as db
import numpy as np
import time
from SerialTesting import SerialTesting
import serial.tools.list_ports

class SerialComm:
    
    def __init__(self):
        self.comm = ser.Serial()
        self.isConnected = False
        self.egramList = []
        self.verifySum = 0.0

 
    
    def connect(self):
        self.ports  = serial.tools.list_ports.comports()
        #for port,desc,hwid in sorted(self.ports):
            #print("{}: {} [{}]".format(port,desc,hwid))

        self.comm = ser.Serial(port="com4", baudrate=115200)
        #self.isConnected = True
       


    def serWriteAOO(self, mode, user):
        try:
            temp = b''

            # Iterate over the attributes of the user object
            for attr in list(vars(user))[3:]:
                if attr == '_atrialAmplitude' or attr == '_ventricularAmplitude' :
                    value = getattr(user, attr)
                    #self.verifySum +=value
                    temp += struct.pack("d", value)

                else:
                    value = getattr(user, attr)
                    intValue = int(value)
                    #self.verifySum +=value
                    temp += struct.pack("h", intValue)
            
            pmode = struct.pack("h", mode)
            #sVerifySum = struct.pack("f", self.verifySum)


            sendBoard = b"\x16\x55" + pmode + temp
            self.comm.write(sendBoard)
        
        except ser.SerialTimeoutException as error:
            print("Error", error)

    """
    def verifySum(self):
        data = self.comm.read(2)
        if data == b"\x16\x18":
            print("Error")
        else: 
            pass
    """    

    def readIn(self):
   
    
        self.serialWrite = b"\x16\x19"
        self.comm.write(self.serialWrite)    

        data = self.comm.read(100)
        print(data)

        for i in range(0,len(data),2):
            ATR_signal = struct.unpack("b", data[i:i+1])[0]*3.3
            VENT_signal = struct.unpack("b", data[i+1:i+2])[0]*3.3
            self.egramList.append([ATR_signal,VENT_signal])
            if len(self.egramList)>100:
                self.egramList.pop(0)
        time.sleep(0.1)
    
        print(self.egramList)

        return self.egramList
            


       
    def testSerial(self):
        i = 0
        for i in range(30):  # Read 100 times for testing
            self.readIn()
            print(self.egramList[-1])
        print("Test completed.")

    

    

    

