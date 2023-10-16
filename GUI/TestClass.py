import unittest
import userClass
import DataBase
import sqlite3


class TestDataBase(unittest.TestCase):

#creating a test database to store values for testing     
    @classmethod
    def setUpClass(cls):
        cls.db = DataBase()
        cls.db.conn = sqlite3.connect(':memory:')
        cls.db.c = cls.db.conn.cursor()
        cls.db.c.execute("""
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
        cls.db.conn.commit()

#creates test user with name and password, sotres and retrieves it, compares the retrived value to the known value
#asserts that the database is able to store and retrive without issues     
    def testInsertAndRetrieveUser(self):
        test_user = userClass("testuser", "testpassword")
        self.db.insertUser(test_user)
        retrieved_user = self.db.getUserByUsername("testuser")
        self.assertEqual(retrieved_user['username'], "testuser")
        self.assertEqual(retrieved_user['password'], "testpassword")
    
#creates test user, updates parameter and checks to see of the change is consistent      
    def testUpdateUser(self):
        test_user = userClass("testuser", "newpassword")
        self.db.updateUser(test_user)
        updated_user = self.db.getUserByUsername("testuser")
        self.assertEqual(updated_user['password'], "newpassword")

# deletes a user and checks in the user still exists     
    def testDeleteUser(self):
        self.db.delete_user("testuser")
        deleted_user = self.db.getUserByUsername("testuser")
        self.assertIsNone(deleted_user)

# closing the database after completion     
    @classmethod
    def tearDownClass(cls):
        cls.db.close()

if __name__ == "__main__":
    unittest.main()




class TestUserClass(unittest.TestCase):

#create an instance if user class and assert that name and passward are inisilized correctly
    def test_initialization(self):
        user = userClass("Alice", "password123")
        self.assertEqual(user.username, "Alice")
        self.assertEqual(user.password, "password123")

#test getters and setters    
    def test_setter_and_getter(self):
        user = userClass("Alice", "password123")
        user.username = "Bob"
        self.assertEqual(user.username, "Bob")
        user.password = "newpassword"
        self.assertEqual(user.password, "newpassword")

#testing AAI and VVI and making sure all the values are stores correctly    
    def test_AAI(self):
        user = userClass("Alice", "password123")
        user.AAI(70, 150, 3.5, 1.0, 0.75, 250, 300, 20, 15)
        self.assertEqual(user.lowerRateLimit, 70)
        self.assertEqual(user.upperRateLimit, 150)
        self.assertEqual(user.atrialAmplitude, 3.5)
        self.assertEqual(user.atrialPulseWidth, 1.0)
        self.assertEqual(user.atrialSensitivity, 0.75)
        self.assertEqual(user.ARP, 250)
        self.assertEqual(user.PVARP, 300)
        self.assertEqual(user.Hysteresis, 20)
        self.assertEqual(user.rateSmoothing, 15)
        self.assertEqual(user.ventricularAmplitude, 0)
        self.assertEqual(user.ventricularPulseWidth, 0)
        self.assertEqual(user.ventricularSensitivity, 0)
        self.assertEqual(user.VRP, 0)
    
    def test_VVI(self):
        user = userClass("Alice", "password123")
        user.VVI(70, 150, 3.5, 1.0, 0.75, 250, 20, 15)
        self.assertEqual(user.lowerRateLimit, 70)
        self.assertEqual(user.upperRateLimit, 150)
        self.assertEqual(user.ventricularAmplitude, 3.5)
        self.assertEqual(user.ventricularPulseWidth, 1.0)
        self.assertEqual(user.ventricularSensitivity, 0.75)
        self.assertEqual(user.VRP, 250)
        self.assertEqual(user.Hysteresis, 20)
        self.assertEqual(user.rateSmoothing, 15)
        self.assertEqual(user.atrialAmplitude, 0)
        self.assertEqual(user.atrialPulseWidth, 0)
        self.assertEqual(user.atrialSensitivity, 0)
        self.assertEqual(user.ARP, 0)
        self.assertEqual(user.PVARP, 0)
    
 #testing the delete methode    
    def test_delete(self):
        user = userClass("Alice", "password123")
        user.delete()
        with self.assertRaises(AttributeError):
            _ = user.username

if __name__ == "__main__":
    unittest.main()
