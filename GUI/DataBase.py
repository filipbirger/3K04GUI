import sqlite3

class DataBase():
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
                ventricularSensitivity REAL, 
                VRP REAL, 
                Hysteresis REAL,
                rateSmoothing REAL,
                atrialAmplitude REAL, 
                atrialPulseWidth REAL,
                atrialSensitivity REAL,
                ARP REAL,
                PVARP REAL
            )
        """)
        self.conn.commit()

    def insertUser(self, user):
        with self.conn:
            user_data = {
                "username": user.username,
                "password": user.password,
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
                "PVARP": user.PVARP
            }
            self.c.execute("""
                INSERT INTO Users VALUES (
                    :username, :password, :DeviceId, :lowerRateLimit, :upperRateLimit, :ventricularAmplitude, 
                    :ventricularPulseWidth, :ventricularSensitivity, :VRP, :Hysteresis, :rateSmoothing,
                    :atrialAmplitude, :atrialPulseWidth, :atrialSensitivity, :ARP, :PVARP
                )
            """, user_data)

    def updateUser(self, user):
        with self.conn:
            user_data = {
                "username": user.username,
                "password": user.password,
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
            }
            self.c.execute("""
                UPDATE Users SET
                    password = :password,
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
                    PVARP = :PVARP
                WHERE username = :username
            """, user_data)



    
    def delete_user(self, username):
        with self.conn:
            self.c.execute("DELETE FROM Users WHERE username = ?", (username,))

    
    # Additional method for the DataBase class to get all users

    def getAllUsers(self):
        self.c.execute("SELECT * FROM Users")
        return self.c.fetchall()

    def getUserByUsername(self, username):
        self.c.execute("SELECT * FROM Users WHERE username = ?", (username,))
        data = self.c.fetchone()
        
        # Fetching column names from the cursor description
        columns = [column[0] for column in self.c.description]
        
        # Creating a dictionary with column names as keys
        user_data_dict = dict(zip(columns, data))
        
        return user_data_dict
   
   
    def close(self):
        self.conn.close()

# This will return the user data as a dictionary, making it easier to display in the getPrevMode function.

