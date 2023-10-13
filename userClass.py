

class userClass:
    def __init__(self, username, password,lowerRateLimit = None,upperRateLimit = None, ventricularAmplitude = None, ventricularPulseWidth = None, ventricularSensitivity = None, 
                 VRP = None, Hysteresis = None, rateSmoothing = None, atrialAmplitude = None, atrialPulseWidth = None, atrialSensitivity = None, ARP = None, PVARP = None):
        self.username = username
        self._password = password
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

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def lowerRateLimit(self):
        return self._lowerRateLimit

    @lowerRateLimit.setter
    def lowerRateLimit(self, value):
        self._lowerRateLimit = value

    @property
    def upperRateLimit(self):
        return self._upperRateLimit

    @upperRateLimit.setter
    def upperRateLimit(self, value):
        self._upperRateLimit = value

    @property
    def atrialAmplitude(self):
        return self._atrialAmplitude

    @atrialAmplitude.setter
    def atrialAmplitude(self, value):
        self._atrialAmplitude = value

    @property
    def atrialPulseWidth(self):
        return self._atrialPulseWidth

    @atrialPulseWidth.setter
    def atrialPulseWidth(self, value):
        self._atrialPulseWidth = value

    @property
    def atrialSensitivity(self):
        return self._atrialSensitivity

    @atrialSensitivity.setter
    def atrialSensitivity(self, value):
        self._atrialSensitivity = value

    @property
    def ARP(self):
        return self._ARP

    @ARP.setter
    def ARP(self, value):
        self._ARP = value

    @property
    def PVARP(self):
        return self._PVARP

    @PVARP.setter
    def PVARP(self, value):
        self._PVARP = value

    @property
    def Hysteresis(self):
        return self._Hysteresis

    @Hysteresis.setter
    def Hysteresis(self, value):
        self._Hysteresis = value

    @property
    def rateSmoothing(self):
        return self._rateSmoothing

    @rateSmoothing.setter
    def rateSmoothing(self, value):
        self._rateSmoothing = value

    @property
    def ventricularAmplitude(self):
        return self._ventricularAmplitude

    @ventricularAmplitude.setter
    def ventricularAmplitude(self, value):
        self._ventricularAmplitude = value

    @property
    def ventricularPulseWidth(self):
        return self._ventricularPulseWidth

    @ventricularPulseWidth.setter
    def ventricularPulseWidth(self, value):
        self._ventricularPulseWidth = value

    @property
    def ventricularSensitivity(self):
        return self._ventricularSensitivity

    @ventricularSensitivity.setter
    def ventricularSensitivity(self, value):
        self._ventricularSensitivity = value

    @property
    def VRP(self):
        return self._VRP

    @VRP.setter
    def VRP(self, value):
        self._VRP = value



    def AOO(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth):
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth

    def VOO(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth):
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth

    def AAI(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth, atrialSensitivity, ARP, PVARP, Hysteresis, rateSmoothing ):
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._atrialSensitivity = atrialSensitivity
        self._ARP = ARP
        self._PVARP = PVARP
        self._Hysteresis = Hysteresis
        self._rateSmoothing = rateSmoothing
    
    def VVI(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth, ventricularSensitivity, VRP, Hysteresis, rateSmoothing):
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._ventricularSensitivity = ventricularSensitivity
        self._VRP = VRP
        self._Hysteresis = Hysteresis
        self._rateSmoothing = rateSmoothing

    def delete(self):
        del self._username
        del self._password 
        del self._lowerRateLimit 
        del self._upperRateLimit 
        del self._atrialAmplitude 
        del self._atrialPulseWidth 
        del self._atrialSensitivity 
        del self._ARP 
        del self._PVARP 
        del self._Hysteresis 
        del self._rateSmoothing 
        del self._ventricularAmplitude 
        del self._ventricularPulseWidth
        del self._ventricularSensitivity 
        del self._VRP 
