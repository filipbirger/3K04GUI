import random
import struct


class SerialTesting:
    
    def write(self, data):
        print(f"Writing to serial: {data}")

    def read(self, numByte):
        ATR_signal = random.gammavariate(0.1,100)
        VENT_signal = random.uniform(0.1,100)
        return struct.pack("dd", ATR_signal, VENT_signal)
 