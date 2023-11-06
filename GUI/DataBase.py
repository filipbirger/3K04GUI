import sqlite3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


class DataBase():#Gets called upon the creation of a new object/user
    def __init__(self):
        self.conn = sqlite3.connect('User_Database.db')
        self.c = self.conn.cursor()
        
        # Corrected the CREATE TABLE statement
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS Users(
                username TEXT PRIMARY KEY,
                password TEXT,
                iv TEXT,
                DeviceId INTEGER,
                lowerRateLimit REAL,
                upperRateLimit REAL,
                ventricularAmplitude REAL, 
                ventricularPulseWidth REAL,
                ventricularSensitivity REAL, 
                VRP REAL, 
                Hysteresis REAL,
                rateSmoothing REAL,
                atrialAmplitude REAL, 
                atrialPulseWidth REAL,
                atrialSensitivity REAL,
                ARP REAL,
                PVARP REAL,
                maximumSensorRate REAL,
                activityThreshold REAL,
                reactionTime REAL,
                responseFactor REAL,
                recoveryTime REAL
            )
        """)
        self.conn.commit()

        self.key = get_random_bytes(16)

    def insertUser(self, user):
        #pushes the newly created user to the table while mapping the parameters to the appropriate column
        with self.conn:
            iv, encrypted_password = self.encrypt(user.password)
            user_data = {
                "username": user.username,
                "password": encrypted_password,
                "iv": iv,
                "DeviceId": user.DeviceId,
                "lowerRateLimit": user.lowerRateLimit,
                "upperRateLimit": user.upperRateLimit,
                "ventricularAmplitude": user.ventricularAmplitude,
                "ventricularPulseWidth": user.ventricularPulseWidth,
                "ventricularSensitivity": user.ventricularSensitivity,
                "VRP": user.VRP,
                "Hysteresis": user.Hysteresis,
                "rateSmoothing": user.rateSmoothing,
                "atrialAmplitude": user.atrialAmplitude,
                "atrialPulseWidth": user.atrialPulseWidth,
                "atrialSensitivity": user.atrialSensitivity,
                "ARP": user.ARP,
                "PVARP": user.PVARP,
                "maximumSensorRate" : user.maximumSensorRate,
                "activityThreshold" : user.activityThreshold,
                "reactionTime" : user.reactionTime,
                "responseFactor" : user.responseFactor,
                "recoveryTime" : user.recoveryTime
            }
            self.c.execute("""
                INSERT INTO Users VALUES (
                    :username, :password,:iv, :DeviceId, :lowerRateLimit, :upperRateLimit, :ventricularAmplitude, 
                    :ventricularPulseWidth, :ventricularSensitivity, :VRP, :Hysteresis, :rateSmoothing,
                    :atrialAmplitude, :atrialPulseWidth, :atrialSensitivity, :ARP, :PVARP, :maximumSensorRate,
                    :activityThreshold,:reactionTime,:responseFactor,:recoveryTime
                )
            """, user_data)

    def updateUser(self, user):
        #updates users already found in the table given username is the input 
        with self.conn:
            user_data = {
                "username": user.username,
                "DeviceId": user.DeviceId,
                "lowerRateLimit": float(user.lowerRateLimit) if user.lowerRateLimit else None,
                "upperRateLimit": float(user.upperRateLimit) if user.upperRateLimit else None,
                "ventricularAmplitude": float(user.ventricularAmplitude) if user.ventricularAmplitude else None,
                "ventricularPulseWidth": float(user.ventricularPulseWidth) if user.ventricularPulseWidth else None,
                "ventricularSensitivity": float(user.ventricularSensitivity) if user.ventricularSensitivity else None,
                "VRP": float(user.VRP) if user.VRP else None,
                "Hysteresis": float(user.Hysteresis) if user.Hysteresis else None,
                "rateSmoothing": float(user.rateSmoothing) if user.rateSmoothing else None,
                "atrialAmplitude": float(user.atrialAmplitude) if user.atrialAmplitude else None,
                "atrialPulseWidth": float(user.atrialPulseWidth) if user.atrialPulseWidth else None,
                "atrialSensitivity": float(user.atrialSensitivity) if user.atrialSensitivity else None,
                "ARP":float(user.ARP) if user.ARP else None,
                "PVARP": float(user.PVARP) if user.PVARP else None,
                "maximumSensorRate": float(user.maximumSensorRate) if user.maximumSensorRate else None,
                "activityThreshold": float(user.activityThreshold) if user.activityThreshold else None,
                "reactionTime": float(user.reactionTime) if user.reactionTime else None,
                "responseFactor": float(user.responseFactor) if user.responseFactor else None,
                "recoveryTime": float(user.recoveryTime) if user.recoveryTime else None
            }
            self.c.execute("""
                UPDATE Users SET
                    DeviceId = :DeviceId,
                    lowerRateLimit = :lowerRateLimit,
                    upperRateLimit = :upperRateLimit,
                    ventricularAmplitude = :ventricularAmplitude,
                    ventricularPulseWidth = :ventricularPulseWidth,
                    ventricularSensitivity = :ventricularSensitivity,
                    VRP = :VRP,
                    Hysteresis = :Hysteresis,
                    rateSmoothing = :rateSmoothing,
                    atrialAmplitude = :atrialAmplitude,
                    atrialPulseWidth = :atrialPulseWidth,
                    atrialSensitivity = :atrialSensitivity,
                    ARP = :ARP,
                    PVARP = :PVARP,
                    maximumSensorRate = :maximumSensorRate,
                    activityThreshold = :activityThreshold,
                    reactionTime = :reactionTime,
                    responseFactor = :responseFactor,
                    recoveryTime = :recoveryTime
                WHERE username = :username
            """, user_data)



    
    def delete_user(self, username):
        #responsible for deleting a user from the database 
        with self.conn:
            self.c.execute("DELETE FROM Users WHERE username = ?", (username,))

    
    # Additional method for the DataBase class to get all users

    def getAllUsers(self):
        #returns all users and is utilized by my Gui class to determine if there are fewer than 10 users present when creating a new user 
        self.c.execute("SELECT * FROM Users")
        return self.c.fetchall()

    def getUserByUsername(self, username):
        self.c.execute("SELECT * FROM Users WHERE username = ?", (username,))
        data = self.c.fetchone()
        
        if data:
            columns = [column[0] for column in self.c.description]
            user_data_dict = dict(zip(columns, data))
            
            # Decrypt the password before returning
            iv = user_data_dict['iv']
            user_data_dict['password'] = self.decrypt(iv, user_data_dict['password'])
            
            return user_data_dict
        else:
            return None

    
    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    def decrypt(self, iv, ciphertext):
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ciphertext)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        return pt
   
   
    def close(self):
        #closes the connection to the database
        self.conn.close()



