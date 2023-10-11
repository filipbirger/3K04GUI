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
                    :username, :password, :lowerRateLimit, :upperRateLimit, :ventricularAmplitude, 
                    :ventricularPulseWidth, :ventricularSensitivity, :VRP, :Hysteresis, :rateSmoothing,
                    :atrialAmplitude, :atrialPulseWidth, :atrialSensitivity, :ARP, :PVARP
                )
            """, user_data)


    def getUserByUsername(self, username):
        self.c.execute("SELECT * FROM Users WHERE username = ?", (username,))
        return self.c.fetchone()

    def delete_user(self, username):
        with self.conn:
            self.c.execute("DELETE FROM Users WHERE username = ?", (username,))

    def close(self):
        self.conn.close()
