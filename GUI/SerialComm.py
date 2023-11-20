import serial
import struct
import DataBase as db


class SerialComm:
    
    def __init__(self):
        self.comm = serial.Serial()
        self.isConnected = False
    
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
                value = getattr(user, attr)
                temp += struct.pack("f", value)
        
            pmode = struct.pack("f", mode)

            write = b"\x16\x55" + pmode + temp
            print(write)
        
        except serial.SerialTimeoutException as error:
            print("Error", error)
        

