

class userClass:
    def __init__(self, username, password,lowerRateLimit = 0,upperRateLimit = 0, ventricularAmplitude = 0, ventricularPulseWidth = 0, ventricularSensitivity = 0, 
                 VRP = 0, Hysteresis = 0, rateSmoothing = 0, atrialAmplitude = 0, atrialPulseWidth = 0, atrialSensitivity = 0, ARP = 0, PVARP = 0):
        self.username = username
        self.password = password
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._atrialSensitivity = atrialSensitivity
        self._ARP = ARP
        self._PVARP = PVARP
        self._Hysteresis = Hysteresis
        self._rateSmoothing = rateSmoothing
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._ventricularSensitivity = ventricularSensitivity
        self._VRP = VRP
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def setUsername(self, name):
        self.username = name

    def setPassword(self, p):
        self.password = p

    def AOO(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth):
        self.lowerRateLimit = lowerRateLimit
        self.upperRateLimit = upperRateLimit
        self.atrialAmplitude = atrialAmplitude
        self.atrialPulseWidth = atrialPulseWidth

    def VOO(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth):
        self.lowerRateLimit = lowerRateLimit
        self.upperRateLimit = upperRateLimit
        self.ventricularAmplitude = ventricularAmplitude
        self.atrialPulseWidth = ventricularPulseWidth

    def AAI(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth, atrialSensitivity, ARP, PVARP, Hysteresis, rateSmoothing ):
        self.lowerRateLimit = lowerRateLimit
        self.upperRateLimit = upperRateLimit
        self.atrialAmplitude = atrialAmplitude
        self.atrialPulseWidth = atrialPulseWidth
        self.atrialSensitivity = atrialSensitivity
        self.ARP = ARP
        self.PVARP = PVARP
        self.Hysteresis = Hysteresis
        self.rateSmoothing = rateSmoothing
    
    def VVI(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth, ventricularSensitivity, VRP, Hysteresis, rateSmoothing):
        self.lowerRateLimit = lowerRateLimit
        self.upperRateLimit = upperRateLimit
        self.ventricularAmplitude = ventricularAmplitude
        self.ventricularPulseWidth = ventricularPulseWidth
        self.ventricularSensitivity = ventricularSensitivity
        self.VRP = VRP
        self.Hysteresis = Hysteresis
        self.rateSmoothing = rateSmoothing