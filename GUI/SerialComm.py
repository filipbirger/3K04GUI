import serial
import struct
import DataBase as db
import numpy as np

class SerialComm:
    
    def __init__(self):
        self.comm = serial.Serial()
        self.isConnected = False
    
    def connect(self):
        try:
            self.comm.baudrate = 115200
            self.comm.port = "Com6"
            self.isConnected = True
            self.comm.open()
        except serial.SerialException as error:
            print("Error",error)
            self.isConnected = False

    '''
    array =[]
    Data = np.genfromtxt("data.txt",encoding=None)
    for each in Data:
        array.append(each)

    MODE = array[0]
    LRL = array[1]
    URL =array[2]
    VA = array[3]
    VPW = array[4]
    VRP = array[5]
    AA = array[6]
    APW = array[7]
    ARP = array[8]
    maximumSensorRate = array[9]
    reactionTime = array[10]
    responseFactor = array[11]
    recoveryTime = array[12]
    '''

    def receive(pMODE,pLRL,pUrl,pVA,pVPW,pVRP,pAA,pAPW,pARP,pMaximumSensorRate,pReactionTime,pResponseFactor,pRecoveryTime):
        #Set up
        frdm_port = "COM7"
        Start = b'\x16'
        SYNC = b'\x22'
        Fn_set = b'\x55'

        #Packing the data into Bytes
        MODE = struct.pack("B", pMODE)
        lowerRateLimit = struct.pack("B", pLRL)
        upperRateLimit = struct.pack("B", pUrl)
        ventricularAmplitude = struct.pack("d", pVA)
        ventricularPulseWidth = struct.pack("d", pVPW)
        VRP = struct.pack("H", pVRP)
        atrialAmplitude = struct.pack("d", pAA)
        atrialPulseWidth = struct.pack("d", pAPW)
        ARP = struct.pack("H", pARP)
        maximumSensorRate  = struct.pack("B", pMaximumSensorRate)
        reactionTime = struct.pack("H", pReactionTime)
        responseFactor = struct.pack("B", pResponseFactor)
        recoveryTime = struct.pack("H", pRecoveryTime)
        
        Signal_set_order = Start+Fn_set+MODE+lowerRateLimit+upperRateLimit+ventricularAmplitude+ventricularPulseWidth+VRP+atrialAmplitude+atrialPulseWidth+ARP+maximumSensorRate+reactionTime+responseFactor+recoveryTime

        Signal_echo_order = Start+SYNC+MODE+lowerRateLimit+upperRateLimit+ventricularAmplitude+ventricularPulseWidth+VRP+atrialAmplitude+atrialPulseWidth+ARP+maximumSensorRate+reactionTime+responseFactor+recoveryTime

        with serial.Serial(frdm_port, 115200) as pacemaker:
            pacemaker.write(Signal_set_order)

        #Unpacking the data from Bytes to str/int
        with serial.Serial(frdm_port, 115200) as pacemaker:
            pacemaker.write(Signal_echo_order)
            data = pacemaker.read(61)
            MODE_echo = struct.unpack('B',data[0:1])[0]
            lowerRateLimit_echo = struct.unpack('B',data[1:2])[0]
            upperRateLimit_echo = struct.unpack('B',data[2:3])[0]
            ventricularAmplitude_echo = struct.unpack("d", data[3:11])[0]
            ventricularPulseWidth_echo = struct.unpack("d", data[11:19])[0]
            VRP_echo = struct.unpack("H", data[19:21])[0]
            atrialAmplitude_echo = struct.unpack("d", data[21:29])[0]
            atrialPulseWidth_echo = struct.unpack("d", data[29:37])[0]
            ARP_echo = struct.unpack("H", data[37:39])[0]
            maximumSensorRate_echo = struct.unpack("B", data[39:40])[0]
            reactionTime_echo = struct.unpack("H", data[40:42])[0]
            responseFactor_echo = struct.unpack("B", data[42:43])[0]
            recoveryTime_echo = struct.unpack("H", data[43:45])[0]
            ATR_signal = struct.unpack("d", data[45:53])[0] #For egram(NOT SURE)
            VENT_signal = struct.unpack("d", data[53:61])[0]

            if MODE_echo == pMODE and lowerRateLimit_echo == pLRL and upperRateLimit_echo == pUrl and ventricularAmplitude_echo == pVA and ventricularPulseWidth_echo == pVPW and VRP_echo == pVRP and atrialAmplitude_echo == pAA and atrialPulseWidth_echo == pAPW and ARP_echo == pARP and maximumSensorRate_echo == pMaximumSensorRate and reactionTime_echo == pReactionTime and responseFactor_echo == pResponseFactor and recoveryTime_echo == pRecoveryTime:
                return True
            else:
                return False

    def read(self):
        #Set up
        frdm_port = "COM7"
        Start = b'\x16'
        SYNC = b'\x22'
        Fn_set = b'\x55'
        Signal_echo = Start + SYNC
        i=0
        while(i<45):
            Signal_echo = Signal_echo + struct.pack("B", 0)
            i = i+1
        with serial.Serial(frdm_port, 115200) as pacemaker:
            pacemaker.write(Signal_echo)
            data = pacemaker.read(61)
            ATR_signal = struct.unpack("d", data[45:53])[0]
            VENT_signal = struct.unpack("d", data[53:61])[0]
            return [ATR_signal,VENT_signal] #For egram
    
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
        

