

class userClass:
#Gets called upon the creation of a new object/user. 
# The user is created with a username, password, and device ID, all other protected parameters are set to 0 until changed
    def __init__(self, username, password,DeviceId = None,lowerRateLimit = None,upperRateLimit = None, ventricularAmplitude = None, ventricularPulseWidth = None, 
                 VRP = None, atrialAmplitude = None, atrialPulseWidth = None, ARP = None, maximumSensorRate = None, reactionTime = None, responseFactor = None, recoveryTime = None): #initializes user attributes to NULL
        self.username = username 
        self._password = password
        self.DeviceId = DeviceId
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._ARP = ARP
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._VRP = VRP
        self._maximumSensorRate = maximumSensorRate
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
    def ARP(self): #gets ARP from database
        return self._ARP

    @ARP.setter
    def ARP(self, value): #sets ARP to database
        self._ARP = value

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
        self._ARP = 0
        self._VRP = 0
        self._maximumSensorRate = 0
        self._reactionTime = 0
        self._responseFactor = 0
        self._recoveryTime = 0

    def VOO(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth): #initializes all VOO parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._atrialAmplitude = 0
        self._atrialPulseWidth = 0
        self._ARP = 0
        self._VRP = 0
        self._maximumSensorRate = 0
        self._reactionTime = 0
        self._responseFactor = 0
        self._recoveryTime = 0

    def AAI(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth, ARP): #initializes all AAI parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._ARP = ARP
        self._ventricularAmplitude = 0
        self._ventricularPulseWidth = 0
        self._VRP = 0
        self._maximumSensorRate = 0
        self._reactionTime = 0
        self._responseFactor = 0
        self._recoveryTime = 0


    
    def VVI(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth, VRP): #initializes all VVI parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._VRP = VRP
        self._ARP = 0
        self._atrialAmplitude = 0
        self._atrialPulseWidth = 0
        self._maximumSensorRate = 0
        self._reactionTime = 0
        self._responseFactor = 0
        self._recoveryTime = 0
    
    def AOOR(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth, maximumSensorRate, reactionTime, responseFactor, recoveryTime): #initializes all AOO parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._maximumSensorRate = maximumSensorRate
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime
        self._ventricularAmplitude = 0
        self._ventricularPulseWidth = 0
        self._ARP = 0
        self._VRP = 0
    
    def VOOR(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth, maximumSensorRate, reactionTime, responseFactor, recoveryTime): #initializes all VOO parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._maximumSensorRate = maximumSensorRate
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime
        self._atrialAmplitude = 0
        self._atrialPulseWidth = 0
        self._ARP = 0
        self._VRP = 0

    def AAIR(self,lowerRateLimit, upperRateLimit, atrialAmplitude, atrialPulseWidth,  ARP, maximumSensorRate, reactionTime, responseFactor, recoveryTime): #initializes all AAI parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._atrialAmplitude = atrialAmplitude
        self._atrialPulseWidth = atrialPulseWidth
        self._ARP = ARP
        self._maximumSensorRate = maximumSensorRate
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime
        self._ventricularAmplitude = 0
        self._ventricularPulseWidth = 0
        self._VRP = 0

    def VVIR(self,lowerRateLimit, upperRateLimit, ventricularAmplitude, ventricularPulseWidth, VRP, maximumSensorRate, reactionTime, responseFactor, recoveryTime): #initializes all VVI parameters to zero
        self._lowerRateLimit = lowerRateLimit
        self._upperRateLimit = upperRateLimit
        self._ventricularAmplitude = ventricularAmplitude
        self._ventricularPulseWidth = ventricularPulseWidth
        self._VRP = VRP
        self._maximumSensorRate = maximumSensorRate
        self._reactionTime = reactionTime
        self._responseFactor = responseFactor
        self._recoveryTime = recoveryTime
        self._ARP = 0
        self._atrialAmplitude = 0
        self._atrialPulseWidth = 0


    def delete(self): #destructor
        del self._username
        del self._password 
        del self._lowerRateLimit 
        del self._upperRateLimit 
        del self._atrialAmplitude 
        del self._atrialPulseWidth 
        del self._ARP  
        del self._ventricularAmplitude 
        del self._ventricularPulseWidth 
        del self._VRP 
        del self._maximumSensorRate
        del self._reactionTime
        del self._responseFactor
        del self._recoveryTime


    

