import sqlite3
import base64
 
#from Crypto.Cipher import AES
#from Crypto.Util.Padding import pad, unpad

class DataBase():#Gets called upon the creation of a new object/user
    def __init__(self):
        self.conn = sqlite3.connect('User_Database.db')
        self.c = self.conn.cursor()
        
        # Corrected the CREATE TABLE statement
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS Users(
                username TEXT PRIMARY KEY,
                password TEXT,
                DeviceId INTEGER,
                lowerRateLimit REAL,
                upperRateLimit REAL,
                ventricularAmplitude REAL, 
                ventricularPulseWidth REAL, 
                VRP REAL, 
                atrialAmplitude REAL, 
                atrialPulseWidth REAL,
                ARP REAL,
                maximumSensorRate REAL,
                reactionTime REAL,
                responseFactor REAL,
                recoveryTime REAL,
                fixedAVDelay REAL,
                dynamicAVDelay REAL,
                sensedAVDelay REAL,
                ATRDuration REAL,
                ATRFallbackMode REAL,
                ATRFallbackTime REAL
            )
        """)
        self.conn.commit()

    def insertUser(self, user):
        #pushes the newly created user to the table while mapping the parameters to the appropriate column
        shift = 3  # Shift value for encryption
        encrypted_username = self.caesar_cipher_encrypt(user.username, shift)
        encrypted_password = self.caesar_cipher_encrypt(user.password, shift)
        with self.conn:
            user_data = {
                "username": encrypted_username,
                "password": encrypted_password,
                "DeviceId": user.DeviceId,
                "lowerRateLimit": user.lowerRateLimit,
                "upperRateLimit": user.upperRateLimit,
                "ventricularAmplitude": user.ventricularAmplitude,
                "ventricularPulseWidth": user.ventricularPulseWidth,
                "VRP": user.VRP,
                "atrialAmplitude": user.atrialAmplitude,
                "atrialPulseWidth": user.atrialPulseWidth,
                "ARP": user.ARP,
                "maximumSensorRate" : user.maximumSensorRate,
                "reactionTime" : user.reactionTime,
                "responseFactor" : user.responseFactor,
                "recoveryTime" : user.recoveryTime,
                "fixedAVDelay" : user.fixedAVDelay,
                "dynamicAVDelay" : user.dynamicAVDelay,
                "sensedAVDelay" : user.sensedAVDelay,
                "ATRDuration" : user.ATRDuration,
                "ATRFallbackMode" : user.ATRFallbackMode,
                "ATRFallbackTime" : user.ATRFallbackTime
             }
            self.c.execute("""
                INSERT INTO Users VALUES (
                    :username, :password, :DeviceId, :lowerRateLimit, :upperRateLimit, :ventricularAmplitude, 
                    :ventricularPulseWidth, :VRP,
                    :atrialAmplitude, :atrialPulseWidth, :ARP,:maximumSensorRate,:reactionTime,
                    :responseFactor,:recoveryTime,:fixedAVDelay, :dynamicAVDelay, :sensedAVDelay,
                    :ATRDuration, :ATRFallbackMode, :ATRFallbackTime
                )
            """, user_data)


  
    def updateUser(self, user):
        #updates users already found in the table given username is the input 
        shift = 3  # Shift value for encryption
        encrypted_username = self.caesar_cipher_encrypt(user.username, shift) if user.username else None
        encrypted_password = self.caesar_cipher_encrypt(user.password, shift) if user.password else None
        with self.conn:
            user_data = {
                "username": encrypted_username,
                "password": encrypted_password,
                "DeviceId": user.DeviceId,
                "lowerRateLimit": float(user.lowerRateLimit) if user.lowerRateLimit else None,
                "upperRateLimit": float(user.upperRateLimit) if user.upperRateLimit else None,
                "ventricularAmplitude": float(user.ventricularAmplitude) if user.ventricularAmplitude else None,
                "ventricularPulseWidth": float(user.ventricularPulseWidth) if user.ventricularPulseWidth else None,
                "VRP": float(user.VRP) if user.VRP else None,
                "atrialAmplitude": float(user.atrialAmplitude) if user.atrialAmplitude else None,
                "atrialPulseWidth": float(user.atrialPulseWidth) if user.atrialPulseWidth else None,
                "ARP":float(user.ARP) if user.ARP else None,
                "maximumSensorRate": float(user.maximumSensorRate) if user.maximumSensorRate else None,
                "reactionTime": float(user.reactionTime) if user.reactionTime else None,
                "responseFactor": float(user.responseFactor) if user.responseFactor else None,
                "recoveryTime": float(user.recoveryTime) if user.recoveryTime else None,
                "fixedAVDelay": float(user.fixedAVDelay) if user.fixedAVDelay else None,
                "dynamicAVDelay": float (user.dynamicAVDelay) if user.dynamicAVDelay else None,
                "sensedAVDelay": float (user.sensedAVDelay) if user.sensedAVDelay else None,
                "ATRDuration": float (user.ATRDuration) if user.ATRDuration else None,
                "ATRFallbackMode": float (user.ATRFallbackMode) if user.ATRFallbackMode else None,
                "ATRFallbackTime": float (user.ATRFallbackTime) if user.ATRFallbackTime else None
            }
            self.c.execute("""
                UPDATE Users SET
                    password = :password,
                    DeviceId = :DeviceId,
                    lowerRateLimit = :lowerRateLimit,
                    upperRateLimit = :upperRateLimit,
                    ventricularAmplitude = :ventricularAmplitude,
                    ventricularPulseWidth = :ventricularPulseWidth,
                    VRP = :VRP,
                    atrialAmplitude = :atrialAmplitude,
                    atrialPulseWidth = :atrialPulseWidth,
                    ARP = :ARP,
                    maximumSensorRate = :maximumSensorRate,
                    reactionTime = :reactionTime,
                    responseFactor = :responseFactor,
                    recoveryTime = :recoveryTime,
                    fixedAVDelay = :fixedAVDelay,
                    dynamicAVDelay = :dynamicAVDelay,
                    sensedAVDelay = :sensedAVDelay,
                    ATRDuration = :ATRDuration,
                    ATRFallbackMode = :ATRFallbackMode,
                    ATRFallbackTime = :ATRFallbackTime
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
        shift = 3  # Shift value for decryption

        # Query to fetch the user data
        self.c.execute("SELECT * FROM Users WHERE username = ?", (username,))
        data = self.c.fetchone()

        if data:
            # Fetching column names from the cursor description
            columns = [column[0] for column in self.c.description]

            # Decrypting username and password
            decrypted_username = self.caesar_cipher_decrypt(data[0], shift)  # Assuming username is the first column
            decrypted_password = self.caesar_cipher_decrypt(data[1], shift)  # Assuming password is the second column

            # Creating a dictionary with column names as keys and decrypted data for username and password
            user_data_dict = dict(zip(columns, data))
            user_data_dict['username'] = decrypted_username
            user_data_dict['password'] = decrypted_password

            return user_data_dict
        else:
            return None  # Or handle the case when the user is not found

     # Caesar Cipher encryption function
    def caesar_cipher_encrypt(self, text, shift):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                shift_amount = shift % 26
                if char.islower():
                    encrypted_text += chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
                else:
                    encrypted_text += chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A'))
            elif char.isdigit():
                encrypted_text += str((int(char) + shift) % 10)
            else:
                encrypted_text += char
        return encrypted_text

    # Caesar Cipher decryption function
    def caesar_cipher_decrypt(self, encrypted_text, shift):
        return self.caesar_cipher_encrypt(encrypted_text, -shift)
    
    def close(self):
        #closes the connection to the database
        self.conn.close()