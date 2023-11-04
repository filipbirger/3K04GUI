import serial

class SerialComm:
    def __init__(self):
        self.comm = serial.Serial('COM7',9600)