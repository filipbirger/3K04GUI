

class userClass:
#Gets called upon the creation of a new object/user. 
# The user is created with a username, password, and device ID, all other protected parameters are set to 0 until changed
    def __init__(self, username, password,DeviceId = None,lowerRateLimit = None,upperRateLimit = None, ventricularAmplitude = None, ventricularPulseWidth = None, ventricularSensitivity = None, 
                 VRP = None, Hysteresis = None, rateSmoothing = None, atrialAmplitude = None, atrialPulseWidth = None, atrialSensitivity = None, ARP = None, PVARP = None, maximumSensorRate = None, activityThreshold = None, reactionTime = None, responseFactor = None, recoveryTime = None): #initializes user attributes to NULL
        self.username = username 
        self._password = password
        self.DeviceId = DeviceId
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
        self._maximumSensorRate = maximumSensorRate
        self._activityThreshold = activityThreshold
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime

    @property
    def username(self): #get username from database
        return self._username

    @username.setter
    def username(self, value): #sets username to database
        self._username = value

    @property
    def password(self): #gets password from database
        return self._password

    @password.setter
    def password(self, value): #sets password to database
        self._password = value

    @property
    def lowerRateLimit(self): #gets lower rate limit from database
        return self._lowerRateLimit

    @lowerRateLimit.setter
    def lowerRateLimit(self, value): #sets lower rate limit to database
        self._lowerRateLimit = value

    @property
    def upperRateLimit(self): #gets upper rate limit from database
        return self._upperRateLimit

    @upperRateLimit.setter
    def upperRateLimit(self, value): #sets upper rate limit to database
        self._upperRateLimit = value

    @property
    def atrialAmplitude(self): #gets atrial amplitude from database
        return self._atrialAmplitude

    @atrialAmplitude.setter
    def atrialAmplitude(self, value): #sets atrial amplitude to database
        self._atrialAmplitude = value

    @property
    def atrialPulseWidth(self): #gets atrial pulse width from database
        return self._atrialPulseWidth

    @atrialPulseWidth.setter
    def atrialPulseWidth(self, value): #sets atrial pulse width to database
        self._atrialPulseWidth = value

    @property
    def atrialSensitivity(self): #gets atrial sensitivity from database
        return self._atrialSensitivity

    @atrialSensitivity.setter
    def atrialSensitivity(self, value): #sets atrial sensitivity to database
        self._atrialSensitivity = value

    @property
    def ARP(self): #gets ARP from database
        return self._ARP

    @ARP.setter
    def ARP(self, value): #sets ARP to database
        self._ARP = value

    @property
    def PVARP(self): #gets PVARP from database
        return self._PVARP

    @PVARP.setter
    def PVARP(self, value): #sets PVARP to database
        self._PVARP = value

    @property
    def Hysteresis(self): #gets Hysteresis from database
        return self._Hysteresis

    @Hysteresis.setter
    def Hysteresis(self, value): #sets Hysteresis to database
        self._Hysteresis = value

    @property
    def rateSmoothing(self): #gets Rate Smoothing from database
        return self._rateSmoothing

    @rateSmoothing.setter
    def rateSmoothing(self, value): #sets Rate Smoothing to database
        self._rateSmoothing = value

    @property
    def ventricularAmplitude(self): #gets Ventricular amplitude from database
        return self._ventricularAmplitude

    @ventricularAmplitude.setter
    def ventricularAmplitude(self, value): #sets ventricular amplitude to database
        self._ventricularAmplitude = value

    @property
    def ventricularPulseWidth(self): #gets ventricular pulse width from database
        return self._ventricularPulseWidth

    @ventricularPulseWidth.setter
    def ventricularPulseWidth(self, value): #sets ventricular pulse width to database
        self._ventricularPulseWidth = value

    @property
    def ventricularSensitivity(self): #gets ventricular sensitivity from database
        return self._ventricularSensitivity

    @ventricularSensitivity.setter
    def ventricularSensitivity(self, value): #sets ventricular sensitivity to database
        self._ventricularSensitivity = value

    @property
    def VRP(self): #gets VRP from database
        return self._VRP

    @VRP.setter
    def VRP(self, value): #sets VRP to database
        self._VRP = value

    @property
    def maximumSensorRate(self): #gets max sensor rate from database
        return self._maximumSensorRate

    @maximumSensorRate.setter
    def maximumSensorRate(self, value): #sets max sensor rate to database
        self._maximumSensorRate = value

    @property
    def activityThreshold(self): #gets activity threshold from database
        return self._activityThreshold

    @activityThreshold.setter
    def activityThreshold(self, value): #sets activity threshold to database
        self._activityThreshold = value

    @property
    def reactionTime(self): #gets reaction time from database
        return self._reactionTime

    @reactionTime.setter
    def reactionTime(self, value): #sets reaction time to database
        self._reactionTime = value

    @property
    def responseFactor(self): #gets response factor from database
        return self._reactionTime

    @responseFactor.setter
    def responseFactor(self, value): #sets response factor to database
        self._responseFactor = value
    
    @property
    def recoveryTime(self): #gets recoveryTime from database
        return self._recoveryTime

    @recoveryTime.setter
    def recoveryTime(self, value): #sets recovery time to database
        self._recoveryTime = value


    def AOO(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth): #initializes all AOO parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._ventricularAmplitude = 0
        self._ventricularPulseWidth = 0
        self._ventricularSensitivity = 0
        self._atrialSensitivity = 0
        self._ARP = 0
        self._VRP = 0
        self._PVARP = 0
        self._Hysteresis = 0
        self._rateSmoothing = 0

    def VOO(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth): #initializes all VOO parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._atrialAmplitude = 0
        self._atrialPulseWidth = 0
        self._ventricularSensitivity = 0
        self._atrialSensitivity = 0
        self._ARP = 0
        self._VRP = 0
        self._PVARP = 0
        self._Hysteresis = 0
        self._rateSmoothing = 0

    def AAI(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth, atrialSensitivity, ARP, PVARP, Hysteresis, rateSmoothing ): #initializes all AAI parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._atrialSensitivity = atrialSensitivity
        self._ARP = ARP
        self._PVARP = PVARP
        self._Hysteresis = Hysteresis
        self._rateSmoothing = rateSmoothing
        self._ventricularAmplitude = 0
        self._ventricularPulseWidth = 0
        self._ventricularSensitivity = 0
        self._VRP = 0


    
    def VVI(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth, ventricularSensitivity, VRP, Hysteresis, rateSmoothing): #initializes all VVI parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._ventricularSensitivity = ventricularSensitivity
        self._VRP = VRP
        self._Hysteresis = Hysteresis
        self._rateSmoothing = rateSmoothing
        self._atrialSensitivity = 0
        self._ARP = 0
        self._atrialAmplitude = 0
        self._atrialPulseWidth = 0
        self._PVARP = 0
    
    def AOOR(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth, maximumSensorRate, activityThreshold, reactionTime, responseFactor, recoveryTime): #initializes all AOO parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._maximumSensorRate = maximumSensorRate
        self._activityThreshold = activityThreshold
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime
        self._ventricularAmplitude = 0
        self._ventricularPulseWidth = 0
        self._ventricularSensitivity = 0
        self._atrialSensitivity = 0
        self._ARP = 0
        self._VRP = 0
        self._PVARP = 0
        self._Hysteresis = 0
        self._rateSmoothing = 0
    
    def VOOR(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth, maximumSensorRate, activityThreshold, reactionTime, responseFactor, recoveryTime): #initializes all VOO parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._maximumSensorRate = maximumSensorRate
        self._activityThreshold = activityThreshold
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime
        self._atrialAmplitude = 0
        self._atrialPulseWidth = 0
        self._ventricularSensitivity = 0
        self._atrialSensitivity = 0
        self._ARP = 0
        self._VRP = 0
        self._PVARP = 0
        self._Hysteresis = 0
        self._rateSmoothing = 0

    def AAIR(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth, atrialSensitivity, ARP, PVARP, Hysteresis, rateSmoothing, maximumSensorRate, activityThreshold, reactionTime, responseFactor, recoveryTime): #initializes all AAI parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._atrialSensitivity = atrialSensitivity
        self._ARP = ARP
        self._PVARP = PVARP
        self._Hysteresis = Hysteresis
        self._rateSmoothing = rateSmoothing
        self._maximumSensorRate = maximumSensorRate
        self._activityThreshold = activityThreshold
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime
        self._ventricularAmplitude = 0
        self._ventricularPulseWidth = 0
        self._ventricularSensitivity = 0
        self._VRP = 0

    def VVIR(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth, ventricularSensitivity, VRP, Hysteresis, rateSmoothing, maximumSensorRate, activityThreshold, reactionTime, responseFactor, recoveryTime): #initializes all VVI parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._ventricularSensitivity = ventricularSensitivity
        self._VRP = VRP
        self._Hysteresis = Hysteresis
        self._rateSmoothing = rateSmoothing
        self._maximumSensorRate = maximumSensorRate
        self._activityThreshold = activityThreshold
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime
        self._atrialSensitivity = 0
        self._ARP = 0
        self._atrialAmplitude = 0
        self._atrialPulseWidth = 0
        self._PVARP = 0


    def delete(self): #destructor
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
        del self._maximumSensorRate
        del self._activityThreshold
        del self._reactionTime
        del self._responseFactor
        del self._recoveryTime


    

