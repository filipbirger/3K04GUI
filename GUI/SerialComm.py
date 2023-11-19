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
            self.comm.open()
        except serial.SerialException as error:
            print("Error",error)
            self.isConnected = False


    
    def serWriteAOO(self,mode,lowerRateLimit, upperRateLimit,atrialAmplitude,atrialPulseWidth):
        try:
            pmode = struct.pack("F",mode)
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pAtrialAmplitude = struct.pack("F",atrialAmplitude )
            pAtrialPulseWidth = struct.pack("F",atrialPulseWidth)

            write = b"\x16\x55"+pmode+pLowerRateLimit+pUpperRateLimit+pAtrialAmplitude+pAtrialPulseWidth
            self.comm.write(write)
        
        except serial.SerialTimeoutException as error:
            print("Error",error)

    def serWriteVOO(self, lowerRateLimit,upperRateLimit,ventricularAmplitude,ventricularPulseWidth):
        try:
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pVentricularAmplitude = struct.pack("F",ventricularAmplitude )
            pVentricularPulseWidth = struct.pack("F",ventricularPulseWidth)

            write = b"\x16\x55"+pLowerRateLimit+pUpperRateLimit+pVentricularAmplitude+pVentricularPulseWidth
            self.comm.write(write)
        
        except serial.SerialTimeoutException as error:
            print("Error",error)

    def serWriteAAI(self, lowerRateLimit,upperRateLimit,atrialAmplitude,atrialPulseWidth,ARP):
        try:
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pAtrialAmplitude = struct.pack("F",atrialAmplitude )
            pAtrialPulseWidth = struct.pack("F",atrialPulseWidth)
            pARP = struct.pack("F",ARP)

            write = b"\x16\x55"+pLowerRateLimit+pUpperRateLimit+pAtrialAmplitude+pAtrialPulseWidth+pARP
            self.comm.write(write)
        
        except serial.SerialTimeoutException as error:
            print("Error",error)

    def serWriteVVI(self, lowerRateLimit,upperRateLimit,ventricularAmplitude,ventricularPulseWidth,VRP):
        try:
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pVentricularAmplitude = struct.pack("F",ventricularAmplitude )
            pVentricularPulseWidth = struct.pack("F",ventricularPulseWidth)
            pVRP = struct.pack("F",VRP)

            write = b"\x16\x55"+pLowerRateLimit+pUpperRateLimit+pVentricularAmplitude+pVentricularPulseWidth+pVRP
            self.comm.write(write)
        
        except serial.SerialTimeoutException as error:
            print("Error",error)

    def serWriteAOOR(self, lowerRateLimit,upperRateLimit,atrialAmplitude,atrialPulseWidth,maximumSensorRate,activityThreshold,reactionTime,responseFactor,recoveryTime):
        try:
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pAtrialAmplitude = struct.pack("F",atrialAmplitude )
            pAtrialPulseWidth = struct.pack("F",atrialPulseWidth)
            pMaximumSensorRate = struct.pack("F",maximumSensorRate)
            pActivityThreshold = struct.pack("F",activityThreshold)
            pReactionTime = struct.pack("F",reactionTime)
            pResponseFactor = struct.pack("F",responseFactor)
            pRecoveryTime = struct.pack("F",recoveryTime)

            write = b"\x16\x55"+pLowerRateLimit+pUpperRateLimit+pAtrialAmplitude+pAtrialPulseWidth+pMaximumSensorRate+pActivityThreshold+pReactionTime+pResponseFactor+pRecoveryTime
            self.comm.write(write)
        
        except serial.SerialTimeoutException as error:
            print("Error",error)

    def serWriteVOOR(self, lowerRateLimit,upperRateLimit,ventricularAmplitude,ventricularPulseWidth,maximumSensorRate,activityThreshold,reactionTime,responseFactor,recoveryTime):
        try:
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pVentricularAmplitude = struct.pack("F",ventricularAmplitude )
            pVentricularPulseWidth = struct.pack("F",ventricularPulseWidth)
            pMaximumSensorRate = struct.pack("F",maximumSensorRate)
            pActivityThreshold = struct.pack("F",activityThreshold)
            pReactionTime = struct.pack("F",reactionTime)
            pResponseFactor = struct.pack("F",responseFactor)
            pRecoveryTime = struct.pack("F",recoveryTime)

            write = b"\x16\x55"+pLowerRateLimit+pUpperRateLimit+pVentricularAmplitude+pVentricularPulseWidth+pMaximumSensorRate+pActivityThreshold+pReactionTime+pResponseFactor+pRecoveryTime
            self.comm.write(write)
    
    
        except serial.SerialTimeoutException as error:
            print("Error",error)
    
    def serWriteAAIR(self, lowerRateLimit,upperRateLimit,atrialAmplitude,atrialPulseWidth,maximumSensorRate,ARP,activityThreshold,reactionTime,responseFactor,recoveryTime):
        try:
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pAtrialAmplitude = struct.pack("F",atrialAmplitude )
            pAtrialPulseWidth = struct.pack("F",atrialPulseWidth)
            pMaximumSensorRate = struct.pack("F",maximumSensorRate)
            pARP = struct.pack("F",ARP)
            pActivityThreshold = struct.pack("F",activityThreshold)
            pReactionTime = struct.pack("F",reactionTime)
            pResponseFactor = struct.pack("F",responseFactor)
            pRecoveryTime = struct.pack("F",recoveryTime)

            write = b"\x16\x55"+pLowerRateLimit+pUpperRateLimit+pAtrialAmplitude+pAtrialPulseWidth+pMaximumSensorRate+pARP+pActivityThreshold+pReactionTime+pResponseFactor+pRecoveryTime
            self.comm.write(write)
        
        except serial.SerialTimeoutException as error:
            print("Error",error)

    def serWriteVVIR(self, lowerRateLimit,upperRateLimit,ventricularAmplitude,ventricularPulseWidth,maximumSensorRate,VRP,activityThreshold,reactionTime,responseFactor,recoveryTime):
        try:
            pLowerRateLimit = struct.pack("F",lowerRateLimit)
            pUpperRateLimit = struct.pack("F",upperRateLimit)
            pVentricularAmplitude = struct.pack("F",ventricularAmplitude )
            pVentricularPulseWidth = struct.pack("F",ventricularPulseWidth)
            pMaximumSensorRate = struct.pack("F",maximumSensorRate)
            pVRP = struct.pack("F",VRP)
            pActivityThreshold = struct.pack("F",activityThreshold)
            pReactionTime = struct.pack("F",reactionTime)
            pResponseFactor = struct.pack("F",responseFactor)
            pRecoveryTime = struct.pack("F",recoveryTime)

            write = b"\x16\x55"+pLowerRateLimit+pUpperRateLimit+pVentricularAmplitude+pVentricularPulseWidth+pMaximumSensorRate+pVRP+pActivityThreshold+pReactionTime+pResponseFactor+pRecoveryTime
            
            self.comm.write(write)

        except serial.SerialTimeoutException as error:
            print("Error",error)
    '''
    def get_echo(self):
        #Signal_echo = b"\x22\x55"+pLowerRateLimit+pUpperRateLimit+pVentricularAmplitude+pVentricularPulseWidth+pVentricularSensitivity+pMaximumSensorRate+pVRP+pHysteresis+pRateSmoothing+pActivityThreshold+pReactionTime+pResponseFactor+pRecoveryTime

        with serial.Serial(self.comm.port, 115200) as pacemaker:
            pacemaker.write(Signal_echo)
            data = pacemaker.read(49)
    '''
    def serVerify(self):
        return






