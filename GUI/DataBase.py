import sqlite3

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
                recoveryTime REAL
            )
        """)
        self.conn.commit()


  
    def insertUser(self, user):
        #pushes the newly created user to the table while mapping the parameters to the appropriate column
        with self.conn:
            user_data = {
                "username": user.username,
                "password": user.password,
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
                "recoveryTime" : user.recoveryTime
            }
            self.c.execute("""
                INSERT INTO Users VALUES (
                    :username, :password, :DeviceId, :lowerRateLimit, :upperRateLimit, :ventricularAmplitude, 
                    :ventricularPulseWidth, :VRP,
                    :atrialAmplitude, :atrialPulseWidth, :ARP,:maximumSensorRate,
                    :reactionTime,:responseFactor,:recoveryTime
                )
            """, user_data)


  
    def updateUser(self, user):
        #updates users already found in the table given username is the input 
        with self.conn:
            user_data = {
                "username": user.username,
                "password": user.password,
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
                "recoveryTime": float(user.recoveryTime) if user.recoveryTime else None
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
        #Allows us to fetch a specific user, it provides us the ability to return any user from the list 
        self.c.execute("SELECT * FROM Users WHERE username = ?", (username,))
        data = self.c.fetchone()
        
        # Fetching column names from the cursor description
        columns = [column[0] for column in self.c.description]
        
        # Creating a dictionary with column names as keys
        user_data_dict = dict(zip(columns, data))
        
        return user_data_dict
   
   
    def close(self):
        #closes the connection to the database
        self.conn.close()