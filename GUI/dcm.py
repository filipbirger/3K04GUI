import tkinter as tk
import userClass
import sqlite3
from DataBase import DataBase
import SerialComm
import Egram
from SerialTesting import SerialTesting

class MyGUI:

    def __init__(self): #constructor
        
        self.db = DataBase()
        
        
        self.startWindow=tk.Tk()
        self.startWindow.geometry("800x800")
        self.startWindow.title("3K04 Pacemaker")
        self.startWindow.configure(bg="azure2")

        self.deviceId = 2 #gives device an identification number
        self.connected = True

        self.startTitle = tk.Label(self.startWindow, text="Pacemaker", font=('Arial', 24), bg="azure2")
        self.startTitle.place(relx=0.4, rely=0.1)
        
        '''
        try:
            serComm = SerialComm.SerialComm()
            serComm.connect()
            self.connected = serComm.isConnected
        except:
            pass
        '''
        
        if (self.connected == True):
            self.newUserButton = tk.Button(self.startWindow, text="New User", command=self.createNewUser, font=("Arial",12)) #Functionality to create New User
            self.newUserButton.place(relx=0.6, rely=0.2, relheight=0.1, relwidth=0.2)
            self.newUserLabel=tk.Label(self.startWindow, text="Click 'New User' to set up your\n profile and start\n configuring your pacemaker", font=("Arial",8),bg="azure2")
            self.newUserLabel.pack()
            self.newUserLabel.place(relx=0.6, rely=0.3)
            self.signInButton = tk.Button(self.startWindow, text="Sign In", command=self.createLoginWindow, font=("Arial",12)) #Functionality to Sign In
            self.signInButton.place(relx=0.2, rely=0.2, relheight=0.1, relwidth=0.2)
            self.signInLabel=tk.Label(self.startWindow, text="Click 'Sign in' if you are\n an existing user", font=("Arial",8),bg="azure2")
            self.signInLabel.pack()
            self.signInLabel.place(relx=0.22, rely=0.3)

            self.aboutButton = tk.Button (self.startWindow, text="About", command=self.aboutDevice, font=("Arial",12)) #Provides ‘About’ information 
            self.aboutButton.place(relx=0.4, rely=0.6, relheight=0.1, relwidth=0.2)
            self.aboutLabel=tk.Label(self.startWindow, text="Click 'About' for more\n information about your pacemaker", font=("Arial",8),bg="azure2")
            self.aboutLabel.pack()
            self.aboutLabel.place(relx=0.385,rely=0.7)
        else:
            self.notConnectedLabel = tk.Label(self.startWindow, text="No Device In Range", font=('Arial', 48),bg="azure2") #Checks if device is not connected
            self.notConnectedLabel.place(x=180, y= 300)
        self.startWindow.mainloop()

    def createNewUser(self):
        self.newUserWindow = tk.Toplevel(self.startWindow)#Called when New User button is clicked
        self.newUserWindow.geometry("300x200")
        self.newUserWindow.title("Create New User")
        self.newUserWindow.configure(bg="azure2")

        self.userNameLabel = tk.Label(self.newUserWindow, text="Username:",bg="azure2")#Gathers Username from the New User
        self.userNameLabel.pack()
        self.userNameTextField = tk.Entry(self.newUserWindow)
        self.userNameTextField.pack()

        self.userPasswordLabel = tk.Label(self.newUserWindow, text="Password:",bg="azure2")#Gathers Password from the New User
        self.userPasswordLabel.pack()
        self.userPasswordTextField = tk.Entry(self.newUserWindow, show="*") #Hides password characters
        self.userPasswordTextField.pack()

        self.enterButton = tk.Button(self.newUserWindow, text="Submit", command=self.populateUserInfo) 
        self.enterButton.pack()
        self.enterButton.place(relx=0.42,rely=0.5)
        
    def populateUserInfo(self):
        allUsersSize = self.db.getAllUsers()#Gathers number of current users from the database and checks if there are less than 10
        if len(allUsersSize)>=10: #If there are currently more than 10 users, it prohibits the new user from signing up
            self.maxUserReachedText = tk.Label(self.newUserWindow, text="Error: Maximum number of users reached!", fg="red",bg="azure2")
            self.maxUserReachedText.pack()
            print("")
            return
        else: #If there are less than 10 users, it inserts the new user’s information to the database
            inputName = self.userNameTextField.get().strip()
            inputPassword = self.userPasswordTextField.get().strip()
            if inputName and inputPassword:
                self.newUser = userClass.userClass(username=inputName, password=inputPassword, DeviceId=self.deviceId)
                self.newUserWindow.destroy()
                self.db.insertUser(self.newUser)


    def aboutDevice(self):
        self.aboutWindow = tk.Toplevel(self.startWindow) #Generates when ‘About’ button is clicked
        self.aboutWindow.geometry("300x200")
        self.aboutWindow.title("About")
        self.aboutWindow.configure(bg="azure2")
        self.applicationModelNumberLabel = tk.Label(self.aboutWindow, text="Application model number: 7", font=('Arial', 12), bg="azure2") #Displays the device’s information
        self.applicationModelNumberLabel.pack(padx=0.1)
        self.revisionNumberLabel = tk.Label(self.aboutWindow, text="Revision Number: 1.3", font=('Arial', 12), bg="azure2")
        self.revisionNumberLabel.pack(padx=0.1)
        self.DCMNumberLabel = tk.Label(self.aboutWindow, text="DCM serial number: 1", font=('Arial', 12), bg="azure2")
        self.DCMNumberLabel.pack(padx=0.1)
        self.instituteNameLabel = tk.Label(self.aboutWindow, text="Institution name: McMaster U", font=('Arial', 12), bg="azure2")
        self.instituteNameLabel.pack(padx=0.1)

    def createLoginWindow(self):
        self.loginWindow = tk.Toplevel(self.startWindow)#Generates when ‘Sign In’ is clicked
        self.loginWindow.geometry("300x200")
        self.loginWindow.title("Login")
        self.loginWindow.configure(bg="azure2")

        self.loginNameLabel = tk.Label(self.loginWindow, text="Username:", bg="azure2")#Prompts user to sign in with their Username 
        self.loginNameLabel.pack()
        self.loginNameTextField = tk.Entry(self.loginWindow)
        self.loginNameTextField.pack()

        self.loginPasswordLabel = tk.Label(self.loginWindow, text="Password:", bg="azure2")#Prompts user to sign in with their password
        self.loginPasswordLabel.pack()
        self.loginPasswordTextField = tk.Entry(self.loginWindow, show="*")#Hides password characters
        self.loginPasswordTextField.pack()

        self.loginButton = tk.Button(self.loginWindow, text="Login", command=self.verifyLogin)
        self.loginButton.pack()
        self.loginButton.place(relx=0.42, rely=0.5)

        self.errorLabel = tk.Label(self.loginWindow, text="", fg="red")
        self.errorLabel.pack()

    def verifyLogin(self):
        inputName = self.loginNameTextField.get().strip() #strips unnecessary characters from username and password
        inputPassword = self.loginPasswordTextField.get().strip()

        shift = 3  # Use the same shift value used for encryption in the database
        encrypted_inputName = self.db.caesar_cipher_encrypt(inputName, shift)
        encrypted_inputPassword = self.db.caesar_cipher_encrypt(inputPassword, shift)


        user = self.db.getUserByUsername(encrypted_inputName)

        if user and user['password'] == inputPassword: #Checks to make sure that the user signing in already exists in the database
            self.loginWindow.destroy()
            self.currentUser = userClass.userClass(username=user['username'], password=user['password'],DeviceId=user['DeviceId'])
            self.createMainSettingWindow()
        else:
            self.errorLabel.config(text="Invalid username or password")


    def createMainSettingWindow(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()  # Destroy all widgets in the startWindow

        
        self.startWindow.title("Main Settings")

        self.settingLabel = tk.Label(self.startWindow, text="Welcome to Main Settings", font=('Arial', 18), bg="azure2") #Generates after the user has signed in
        self.settingLabel.pack()

        self.prevInfoLabel = tk.Label(self.startWindow,text="Would you like to use your previous pacing mode?", font=('Arial', 14), bg="azure2") #Asks user to choose between using their previous pacing mode or configuring their pacing mode
        self.prevInfoLabel.pack()
        self.prevInfoLabel.place(relx=0.5, rely=0.3, anchor='center')

        self.prevInfoButtonYes= tk.Button(self.startWindow, text="Yes", command=self.getPrevMode, font=("Arial",12)) #Allows user to select their previous pacing mode
        self.prevInfoButtonYes.pack()
        self.prevInfoButtonYes.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)

        self.warningYes= tk.Label(self.startWindow, text="By clicking 'Yes' you agree to have your\n previous pacing mode stored in our database", font=('Arial', 8), bg="azure2")
        self.warningYes.pack()
        self.warningYes.place(relx=0.1, rely=0.55)

        self.prevInfoButtonNo= tk.Button(self.startWindow, text="No", command= self.configPaceMode, font=("Arial",12)) #Allows user to select to not use their previous mode
        self.prevInfoButtonNo.pack()
        self.prevInfoButtonNo.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.05)

        self.warningNo= tk.Label(self.startWindow, text="By clicking 'No' you are choosing to\n configure your pacing mode manually", font=('Arial', 8), bg="azure2")
        self.warningNo.pack()
        self.warningNo.place(relx=0.625, rely=0.55)

        self.deleteUserButton = tk.Button(self.startWindow, text = "Delete User", command=self.deleteUser, font=("Arial",12)) #Gives the user the option to delete their profile from the database
        self.deleteUserButton.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.05)
        self.deleteUserLabel= tk.Label(self.startWindow, text="By clicking 'Delete User', you are choosing to\n permanently delete your profile and pacing\n history from our database", font=("Arial",8), bg="azure2")
        self.deleteUserLabel.pack()
        self.deleteUserLabel.place(relx=0.355,rely=0.75)

    def getPrevMode(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.createMainSettingWindow)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.prevInfoWindow = self.startWindow
        
        self.prevInfoLabel=tk.Label(self.prevInfoWindow, text="Previous Pacing Mode", font=('Arial',18), bg="azure2") #Accesses user’s previous pacing parameters from the database
        self.prevInfoLabel.pack()
        self.prevInfoLabel.place(relx=0.35, rely=0.05)

        shift = 3  # Use the same shift value used for encryption in the database
        encrypted_inputName = self.db.caesar_cipher_encrypt(self.currentUser.username, shift)
        user_data = self.db.getUserByUsername(encrypted_inputName)

        y_position = 0.1
        y2_position= 0.1
        for attribute, value in user_data.items(): #Displays the information for the user to view and submit
            label = tk.Label(self.prevInfoWindow, text=f"{attribute}: {value}", font=('Arial', 14), bg="azure2")
            if y_position<=0.75:    
                y_position += 0.048
                label.place(relx=0.1, rely=y_position)
            else:
                y2_position+=0.048
                label.place(relx=0.6, rely=y2_position)
                
                
    def configPaceMode(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.createMainSettingWindow)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defaultWindow = self.startWindow

        self.pickDefault= tk.Label(self.defaultWindow, text="Would you like to configure the pacing mode or use a default pacing mode?", font=('Arial', 14), bg="azure2") #Gives the user the option to either configure the pacing mode manually or use default parameters
        self.pickDefault.pack()
        self.pickDefault.place(relx=0.5, rely=0.3, anchor='center')

        self.useDefaultButtonYes= tk.Button(self.defaultWindow, text="Default", command= self.useDefault, font=("Arial",12)) #Allows user to select to configure using default parameters
        self.useDefaultButtonYes.pack()
        self.useDefaultButtonYes.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)
        self.useDefaultLabel=tk.Label(self.defaultWindow, text="By clicking 'Default', you will get the option\n to choose your pacing mode with it's\n corresponding default values", font=('Arial',8), bg="azure2")
        self.useDefaultLabel.pack()
        self.useDefaultLabel.place(relx=0.125,rely=0.55)

        self.useConfigButtonNo= tk.Button(self.defaultWindow, text="Configure", command= self.useConfigure, font=("Arial",12)) #Allow user to select to configure manually
        self.useConfigButtonNo.pack()
        self.useConfigButtonNo.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.05)
        self.useConfigLabel=tk.Label(self.defaultWindow,text="By clicking 'Configure', you will\n select your desired pacing mode\n and input your own parameters", font=('Arial',8), bg="azure2")
        self.useConfigLabel.pack()
        self.useConfigLabel.place(relx=0.65,rely=0.55)

    def useDefault(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.configPaceMode)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defaultModeWindow = self.startWindow
        
        self.defaultModeLabel=tk.Label(self.defaultModeWindow, text="Please Select Your Pacing Mode", font=("Arial",18), bg="azure2") #Prompts user to pick which pacing mode they want to use (VOO, AOO, AAI, VVI)
        self.defaultModeLabel.pack()
        self.defaultModeLabel.place(relx=0.3, rely=0.05)

        self.VOOButton = tk.Button(self.defaultModeWindow, text = "Default VOO", command=self.defaultVOO,font=("Arial",12))
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.15, rely=0.15, relwidth=0.3, relheight=0.05)

        self.AOOButton = tk.Button(self.defaultModeWindow, text = "Default AOO", command=self.defaultAOO,font=("Arial",12))
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.15, relwidth=0.3, relheight=0.05)

        self.AAIButton = tk.Button(self.defaultModeWindow, text = "Default AAI", command=self.defaultAAI,font=("Arial",12))
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.15, rely=0.3, relwidth=0.3, relheight=0.05)

        self.VVIButton = tk.Button(self.defaultModeWindow, text = "Default VVI", command=self.defaultVVI,font=("Arial",12))
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.3, relwidth=0.3, relheight=0.05)

        self.VOORButton=tk.Button(self.defaultModeWindow, text= "Default VOOR", command=self.defaultVOOR,font=("Arial",12))
        self.VOORButton.pack()
        self.VOORButton.place(relx=0.15, rely=0.45, relwidth=0.3, relheight=0.05)
        
        self.AOORButton=tk.Button(self.defaultModeWindow, text= "Default AOOR", command=self.defaultAOOR,font=("Arial",12))
        self.AOORButton.pack()
        self.AOORButton.place(relx=0.6, rely=0.45, relwidth=0.3, relheight=0.05)

        self.AAIRButton=tk.Button(self.defaultModeWindow, text= "Default AAIR", command=self.defaultAAIR,font=("Arial",12))
        self.AAIRButton.pack()
        self.AAIRButton.place(relx=0.15, rely=0.6, relwidth=0.3, relheight=0.05)
        
        self.VVIRButton=tk.Button(self.defaultModeWindow, text= "Default VVIR", command=self.defaultVVIR,font=("Arial",12))
        self.VVIRButton.pack()
        self.VVIRButton.place(relx=0.6, rely=0.6, relwidth=0.3, relheight=0.05)

        self.DDDButton=tk.Button(self.defaultModeWindow, text="Default DDD", command=self.defaultDDD, font=("Arial", 12))
        self.DDDButton.pack()
        self.DDDButton.place(relx=0.15,rely=0.75,relwidth=0.3,relheight=0.05)

        self.DDDRButton=tk.Button(self.defaultModeWindow, text="Default DDDR", command=self.defaultDDDR, font=("Arial",12))
        self.DDDRButton.pack()
        self.DDDRButton.place(relx=0.6,rely=0.75, relwidth=0.3, relheight=0.05)
    
    def defaultVOO(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defVOOWindow = self.startWindow

        self.defVOOLabel=tk.Label(self.defVOOWindow, text="Default VOO Parameters", font=("Arial",18),bg="azure2") #Displays default VOO parameters
        self.defVOOLabel.pack()
        self.defVOOLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVOOWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14),bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVOOWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14),bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVOOWindow, text="Ventricular Amplitude: 5.0 V", font=('Arial', 14),bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.VentricularPulseWidthLabel= tk.Label(self.defVOOWindow, text="Ventricular Pulse Width: 1.0 ms", font=('Arial', 14),bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.6)
 
        self.VOOButton = tk.Button(self.defVOOWindow, text = "Submit", command=self.submitDefVOO) #Allows the user to submit the parameters to their device
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefVOO(self):
        self.VOOLRLimit=60.0
        self.VOOURLimit=120.0
        self.VOOVentricularAmplitude=5.0
        self.VOOVentricularPulseWidth=1.0
        MyGUI.successfulSubmitted(self,self.defVOOWindow)
        
        self.currentUser.VOO(self.VOOLRLimit, self.VOOURLimit, self.VOOVentricularAmplitude, self.VOOVentricularPulseWidth) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)
        
        #Serial comm to pacemaker when the function is submitted
        self.conn = SerialComm.SerialComm()
        
        self.conn.connect()
        self.conn.serWriteAOO(1,self.currentUser)

       
        
        self.egramWindow = Egram.Egram(self.conn)
        self.egramWindow.run(self.defVOOWindow)

    
    def defaultAOO(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defAOOWindow = self.startWindow

        self.defAOOLabel=tk.Label(self.defAOOWindow, text="Default AOO Parameters", font=("Arial",18), bg="azure2")
        self.defAOOLabel.pack()
        self.defAOOLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAOOWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAOOWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAOOWindow, text="Atrial Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.AtrialPulseWidthLabel= tk.Label(self.defAOOWindow, text="Atrial Pulse Width: 1.0 ms", font=('Arial', 14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.6)
 
        self.AOOButton = tk.Button(self.defAOOWindow, text = "Submit", command=self.submitDefAOO)#Allows the user to submit the parameters to their device
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefAOO(self):
        self.AOOLRLimit=60.0
        self.AOOURLimit=120.0
        self.AOOAtrialAmplitude=3.5
        self.AOOAtrialPulseWidth=10.0

        self.currentUser.AOO(self.AOOLRLimit, self.AOOURLimit, self.AOOAtrialAmplitude, self.AOOAtrialPulseWidth)#Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)
       
       
        self.conn = SerialComm.SerialComm()
        self.conn.connect()
        self.conn.serWriteAOO(0,self.currentUser)

       
        MyGUI.successfulSubmitted(self,self.defAOOWindow)
        
        self.egramWindow = Egram.Egram(self.conn)
        self.egramWindow.run(self.defAOOWindow)
        
        
    def defaultAAI(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defAAIWindow = self.startWindow

        self.defAAILabel=tk.Label(self.defAAIWindow, text="Default AAI Parameters", font=("Arial",18), bg="azure2")#Displays default AAI parameters
        self.defAAILabel.pack()
        self.defAAILabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAAIWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAAIWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAAIWindow, text="Atrial Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.AtrialPulseWidthLabel= tk.Label(self.defAAIWindow, text="Atrial Pulse Width: 1.0 ms", font=('Arial', 14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.6)

        self.ARPLabel= tk.Label(self.defAAIWindow, text="ARP: 250 ms", font=('Arial', 14), bg="azure2")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.525, rely=0.15)

        self.AAIButton = tk.Button(self.defAAIWindow, text = "Submit", command=self.submitDefAAI)#Allows the user to submit the parameters to their device
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefAAI(self):
        self.AAILRLimit=60.0
        self.AAIURLimit=120.0
        self.AAIAtrialAmplitude=5.0
        self.AAIAtrialPulseWidth=1.0
        self.AAIARP=250.0

        self.currentUser.AAI(self.AAILRLimit, self.AAIURLimit, self.AAIAtrialAmplitude, self.AAIAtrialPulseWidth,  self.AAIARP)#Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)
        #Serial comm to pacemaker when the function is submitted
   
        MyGUI.successfulSubmitted(self, self.defAAIWindow)
        self.conn = SerialComm.SerialComm()
        
        self.conn.connect()
        self.conn.serWriteAOO(2,self.currentUser)

       
        
        self.egramWindow = Egram.Egram(self.conn)
        self.egramWindow.run(self.defAAIWindow)


    def defaultVVI(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defVVIWindow = self.startWindow

        self.defVVILabel=tk.Label(self.defVVIWindow, text="Default VVI Parameters", font=("Arial",18), bg="azure2") #Displays default VVI parameters
        self.defVVILabel.pack()
        self.defVVILabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVVIWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVVIWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVVIWindow, text="Ventricular Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.VentricularPulseWidthLabel= tk.Label(self.defVVIWindow, text="Ventricular Pulse Width: 1.0 ms", font=('Arial', 14), bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.6)

        self.VRPLabel= tk.Label(self.defVVIWindow, text="VRP: 320 ms", font=('Arial', 14), bg="azure2")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.525, rely=0.15)

        self.VVIButton = tk.Button(self.defVVIWindow, text = "Submit", command=self.submitDefVVI)#Allows the user to submit the parameters to their device
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefVVI(self):
        self.VVILRLimit=60.0
        self.VVIURLimit=120.0
        self.VVIVentricularAmplitude=5.0
        self.VVIVentricularPulseWidth=1.0
        self.VVIVRP=320.0

        self.currentUser.VVI(self.VVILRLimit, self.VVIURLimit, self.VVIVentricularAmplitude, self.VVIVentricularPulseWidth, self.VVIVRP)#Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)
        #Serial comm to pacemaker when the function is submitted
        self.conn = SerialComm.SerialComm()
        self.conn.connect()

        self.conn.serWriteAOO(3,self.currentUser)
        MyGUI.successfulSubmitted(self, self.defVVIWindow)
        
        self.egramWindow = Egram.Egram(self.conn)
        self.egramWindow.run(self.defVVIWindow)
    
    def defaultVOOR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defVOORWindow = self.startWindow

        self.defVOORLabel=tk.Label(self.defVOORWindow, text="Default VOOR Parameters", font=("Arial",18), bg="azure2") #Displays default VOO parameters
        self.defVOORLabel.pack()
        self.defVOORLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVOORWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVOORWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVOORWindow, text="Ventricular Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.VentricularPulseWidthLabel= tk.Label(self.defVOORWindow, text="Ventricular Pulse Width: 1.0 ms", font=('Arial', 14),bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.6)

        self.MaxSensorRateLabel=tk.Label(self.defVOORWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 14), bg="azure2")
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.525, rely=0.15)

        self.ReactionTimeLabel=tk.Label(self.defVOORWindow, text="Reaction Time: 30 sec", font=('Arial',14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.45)

        self.ResponseFactorLabel=tk.Label(self.defVOORWindow, text="Response Factor: 8", font=('Arial',14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.6)

        self.RecoveryTimeLabel=tk.Label(self.defVOORWindow, text="Recovery Time: 5 min", font=('Arial',14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.525, rely=0.3)

        self.VOORButton = tk.Button(self.defVOORWindow, text = "Submit", command=self.submitDefVOOR) #Allows the user to submit the parameters to their device
        self.VOORButton.pack()
        self.VOORButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefVOOR(self):
        self.VOORLRLimit=60.0
        self.VOORURLimit=120.0
        self.VOORVentricularAmplitude=5.0
        self.VOORVentricularPulseWidth=1.0
        self.VOORMaxSensorRate=120
        self.VOORReactionTime=30
        self.VOORResponseFactor=8
        self.VOORRecoveryTime=5
        MyGUI.successfulSubmitted(self,self.defVOORWindow)

        self.currentUser.VOOR(self.VOORLRLimit, self.VOORURLimit, self.VOORVentricularAmplitude, self.VOORVentricularPulseWidth, self.VOORMaxSensorRate,self.VOORReactionTime,self.VOORResponseFactor, self.VOORRecoveryTime) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)

        #Serial comm to pacemaker when the function is submitted
        self.conn = SerialComm.SerialComm()
        self.conn.connect()

        self.conn.serWriteAOO(5,self.currentUser)

       
        self.egramWindow = Egram.Egram(self.conn)
        self.egramWindow.run(self.defVOORWindow)
    
        


    def defaultAOOR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)
        
        self.defAOORWindow=self.startWindow

        self.defAOORLabel=tk.Label(self.defAOORWindow, text="Default AOOR Parameters", font=("Arial",18), bg="azure2") #Displays default VOO parameters
        self.defAOORLabel.pack()
        self.defAOORLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAOORWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAOORWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAOORWindow, text="Atrial Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.AtrialPulseWidthLabel= tk.Label(self.defAOORWindow, text="Atrial Pulse Width: 0.1 ms", font=('Arial', 14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.6)

        self.MaxSensorRateLabel=tk.Label(self.defAOORWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 14), bg="azure2")
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.525, rely=0.15)

        self.ReactionTimeLabel=tk.Label(self.defAOORWindow, text="Reaction Time: 30 sec", font=('Arial',14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.45)

        self.ResponseFactorLabel=tk.Label(self.defAOORWindow, text="Response Factor: 8", font=('Arial',14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.6)

        self.RecoveryTimeLabel=tk.Label(self.defAOORWindow, text="Recovery Time: 5 min", font=('Arial',14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.525, rely=0.3)

        self.AOORButton = tk.Button(self.defAOORWindow, text = "Submit", command=self.submitDefAOOR) #Allows the user to submit the parameters to their device
        self.AOORButton.pack()
        self.AOORButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefAOOR(self):
        self.AOORLRLimit=60.0
        self.AOORURLimit=120.0
        self.AOORAtrialAmplitude=5.0
        self.AOORAtrialPulseWidth=1.0
        self.AOORMaxSensorRate=120
        self.AOORReactionTime=30
        self.AOORResponseFactor=8
        self.AOORRecoveryTime=5
        MyGUI.successfulSubmitted(self,self.defAOORWindow)

        self.currentUser.AOOR(self.AOORLRLimit, self.AOORURLimit, self.AOORAtrialAmplitude, self.AOORAtrialPulseWidth, self.AOORMaxSensorRate, self.AOORReactionTime,self.AOORResponseFactor, self.AOORRecoveryTime) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)

        #Serial comm to pacemaker when the function is submitted
        self.conn = SerialComm.SerialComm()
        self.conn.connect()
        self.conn.serWriteAOO(4,self.currentUser)

        self.egramWindow = Egram.Egram(self.conn)
        self.egramWindow.run(self.defAOORWindow)


    
    def defaultAAIR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defAAIRWindow=self.startWindow
        
        self.defAAIRLabel=tk.Label(self.defAAIRWindow, text="Default AAIR Parameters", font=("Arial",18), bg="azure2") #Displays default VOO parameters
        self.defAAIRLabel.pack()
        self.defAAIRLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAAIRWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAAIRWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAAIRWindow, text="Atrial Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.AtrialPulseWidthLabel= tk.Label(self.defAAIRWindow, text="Atrial Pulse Width: 1.0 ms", font=('Arial', 14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.6)

        self.RecoveryTimeLabel=tk.Label(self.defAAIRWindow, text="Recovery Time: 5 min", font=('Arial',14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.525, rely=0.6)

        self.MaxSensorRateLabel=tk.Label(self.defAAIRWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 14), bg="azure2")
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.525, rely=0.15)

        self.ReactionTimeLabel=tk.Label(self.defAAIRWindow, text="Reaction Time: 30 sec", font=('Arial',14),bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.3)

        self.ResponseFactorLabel=tk.Label(self.defAAIRWindow, text="Response Factor: 8", font=('Arial',14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.45)

        self.ARPLabel=tk.Label(self.defAAIRWindow, text=' ARP: 250 ms', font=('Arial', 14), bg="azure2")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.1 ,rely=0.75) 

        self.AAIRButton = tk.Button(self.defAAIRWindow, text = "Submit", command=self.submitDefAAIR) #Allows the user to submit the parameters to their device
        self.AAIRButton.pack()
        self.AAIRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefAAIR(self):
        self.AAIRLRLimit=60.0
        self.AAIRURLimit=120.0
        self.AAIRAtrialAmplitude=5.0
        self.AAIRAtrialPulseWidth=1.0
        self.AAIRMaxSensorRate=120
        self.AAIRReactionTime=30
        self.AAIRResponseFactor=8
        self.AAIRRecoveryTime=5
        self.AAIRARP=250
        MyGUI.successfulSubmitted(self,self.defAAIRWindow)

        self.currentUser.AAIR(self.AAIRLRLimit, self.AAIRURLimit, self.AAIRAtrialAmplitude, self.AAIRAtrialPulseWidth, self.AAIRMaxSensorRate,self.AAIRReactionTime,self.AAIRResponseFactor, self.AAIRRecoveryTime,self.AAIRARP) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)      

        self.conn = SerialComm.SerialComm()
        self.conn.connect()
        self.conn.serWriteAOO(6,self.currentUser)

        self.egramWindow = Egram.Egram(self.conn)
        self.egramWindow.run(self.defAAIRWindow)



    def defaultVVIR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defVVIRWindow=self.startWindow
        
        self.defVVIRLabel=tk.Label(self.defVVIRWindow, text="Default VVIR Parameters", font=("Arial",18), bg="azure2") #Displays default VOO parameters
        self.defVVIRLabel.pack()
        self.defVVIRLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVVIRWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVVIRWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVVIRWindow, text="Ventricular Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.VentricularPulseWidthLabel= tk.Label(self.defVVIRWindow, text="Ventricular Pulse Width: 1.0 ms", font=('Arial', 14), bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.6)

        self.RecoveryTimeLabel=tk.Label(self.defVVIRWindow, text="Recovery Time: 5 min", font=('Arial',14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.525, rely=0.6)

        self.MaxSensorRateLabel=tk.Label(self.defVVIRWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 14), bg="azure2")
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.525, rely=0.15)

        self.ReactionTimeLabel=tk.Label(self.defVVIRWindow, text="Reaction Time: 30 sec", font=('Arial',14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.3)

        self.ResponseFactorLabel=tk.Label(self.defVVIRWindow, text="Response Factor: 8", font=('Arial',14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.45)

        self.VRPLabel=tk.Label(self.defVVIRWindow, text=' VRP: 320 ms', font=('Arial', 14), bg="azure2")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.1 ,rely=0.75)

        self.VVIRButton = tk.Button(self.defVVIRWindow, text = "Submit", command=self.submitDefVVIR) #Allows the user to submit the parameters to their device
        self.VVIRButton.pack()
        self.VVIRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefVVIR(self):
        self.VVIRLRLimit=60.0
        self.VVIRURLimit=120.0
        self.VVIRVentricularAmplitude=5.0
        self.VVIRVentricularPulseWidth=1.0
        self.VVIRMaxSensorRate=120
        self.VVIRReactionTime=30
        self.VVIRResponseFactor=8
        self.VVIRRecoveryTime=5
        self.VVIRVRP=320
        MyGUI.successfulSubmitted(self,self.defVVIRWindow)

        self.currentUser.VVIR(self.VVIRLRLimit, self.VVIRURLimit, self.VVIRVentricularAmplitude, self.VVIRVentricularPulseWidth, self.VVIRMaxSensorRate,self.VVIRReactionTime,self.VVIRResponseFactor, self.VVIRRecoveryTime,self.VVIRVRP) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)  

        
        self.conn = SerialComm.SerialComm()
        self.conn.connect()
        self.conn.serWriteAOO(7,self.currentUser)

        self.egramWindow = Egram.Egram(self.conn)
        self.egramWindow.run(self.defVVIRWindow)
    
    def defaultDDD(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defDDDWindow=self.startWindow

        self.defDDDLabel=tk.Label(self.defDDDWindow, text="Default DDD Parameters", font=("Arial",18),bg="azure2") #Displays default VOO parameters
        self.defDDDLabel.pack()
        self.defDDDLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defDDDWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14),bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defDDDWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14),bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defDDDWindow, text="Ventricular Amplitude: 5.0 V", font=('Arial', 14),bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.VentricularPulseWidthLabel= tk.Label(self.defDDDWindow, text="Ventricular Pulse Width: 1.0 ms", font=('Arial', 14),bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.6)

        self.AtrialAmplitudeLabel= tk.Label(self.defDDDWindow, text="Atrial Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.525, rely=0.15)

        self.AtrialPulseWidthLabel= tk.Label(self.defDDDWindow, text="Atrial Pulse Width: 1.0 ms", font=('Arial', 14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.525, rely=0.3)

        self.ARPLabel= tk.Label(self.defDDDWindow, text="ARP: 250 ms", font=('Arial', 14), bg="azure2")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.525, rely=0.45)

        self.VRPLabel=tk.Label(self.defDDDWindow, text=' VRP: 320 ms', font=('Arial', 14), bg="azure2")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.525 ,rely=0.6)

        self.DDDButton = tk.Button(self.defDDDWindow, text = "Next", command=self.nextDDD) #Allows the user to submit the parameters to their device
        self.DDDButton.pack()
        self.DDDButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def nextDDD(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.nextDDDWindow=self.startWindow

        self.defDDDLabel=tk.Label(self.nextDDDWindow, text="Default DDD Parameters", font=("Arial",18),bg="azure2") #Displays default VOO parameters
        self.defDDDLabel.pack()
        self.defDDDLabel.place(relx=0.35, rely=0.05)

        self.FixedAVLabel=tk.Label(self.nextDDDWindow, text="Fixed AV Delay: 150 ms", font=("Arial", 14), bg="azure2")
        self.FixedAVLabel.pack()
        self.FixedAVLabel.place(relx=0.1,rely=0.15)

        self.DynamicAVLabel=tk.Label(self.nextDDDWindow, text="Dynamic AV Delay: Off", font=("Arial",14), bg="azure2")
        self.DynamicAVLabel.pack()
        self.DynamicAVLabel.place(relx=0.1,rely=0.3)

        self.SensedAVLabel=tk.Label(self.nextDDDWindow, text="Sensed AV Delay Offset: Off", font=("Arial",14),bg="azure2")
        self.SensedAVLabel.pack()
        self.SensedAVLabel.place(relx=0.1,rely=0.45)

        self.ATRDurationLabel=tk.Label(self.nextDDDWindow, text="ATR Duration: 20 cc", font=("Arial",14), bg="azure2")
        self.ATRDurationLabel.pack()
        self.ATRDurationLabel.place(relx=0.525,rely=0.15)

        self.ATRFallbackModeLabel=tk.Label(self.nextDDDWindow, text="ATR Fallback Mode: Off", font=("Arial",14), bg="azure2")
        self.ATRFallbackModeLabel.pack()
        self.ATRFallbackModeLabel.place(relx=0.525, rely=0.3)

        self.ATRFallbackTimeLabel=tk.Label(self.nextDDDWindow, text="ATR Fallback Timing: 1 min", font=("Arial",14), bg="azure2")
        self.ATRFallbackTimeLabel.pack()
        self.ATRFallbackTimeLabel.place(relx=0.525,rely=0.45)

        self.DDDNextButton = tk.Button(self.nextDDDWindow, text = "Submit", command=self.submitDefDDD) #Allows the user to submit the parameters to their device
        self.DDDNextButton.pack()
        self.DDDNextButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefDDD(self):
        self.DDDLRLimit=60.0
        self.DDDURLimit=120.0
        self.DDDVentricularAmplitude=5.0
        self.DDDVentricularPulseWidth=1.0
        self.DDDVRP=320.0
        self.DDDAtrialAmplitude=5.0
        self.DDDAtrialPulseWidth=1.0
        self.DDDARP=250
        self.DDDFixedAVDelay=150
        self.DDDDynamicAV=0
        self.DDDSensedAV=0
        self.DDDATRDuration=20
        self.DDDATRFallbackMode=0
        self.DDDATRFallbackTime=1
        MyGUI.successfulSubmitted(self, self.nextDDDWindow)

        self.currentUser.DDD(self.DDDLRLimit, self.DDDURLimit, self.DDDVentricularAmplitude, self.DDDVentricularPulseWidth, self.DDDVRP, self.DDDAtrialAmplitude, self.DDDAtrialPulseWidth, self.DDDARP, self.DDDFixedAVDelay, self.DDDDynamicAV, self.DDDSensedAV,self.DDDATRDuration, self.DDDATRFallbackMode, self.DDDATRFallbackTime) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)  


    def defaultDDDR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defDDDRWindow=self.startWindow

        self.defDDDRLabel=tk.Label(self.defDDDRWindow, text="Default DDDR Parameters", font=("Arial",18),bg="azure2") #Displays default VOO parameters
        self.defDDDRLabel.pack()
        self.defDDDRLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defDDDRWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 14),bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defDDDRWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 14),bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defDDDRWindow, text="Ventricular Amplitude: 5.0 V", font=('Arial', 14),bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.45)

        self.VentricularPulseWidthLabel= tk.Label(self.defDDDRWindow, text="Ventricular Pulse Width: 1.0 ms", font=('Arial', 14),bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.6)

        self.AtrialAmplitudeLabel= tk.Label(self.defDDDRWindow, text="Atrial Amplitude: 5.0 V", font=('Arial', 14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.525, rely=0.15)

        self.AtrialPulseWidthLabel= tk.Label(self.defDDDRWindow, text="Atrial Pulse Width: 1.0 ms", font=('Arial', 14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.525, rely=0.3)

        self.ARPLabel= tk.Label(self.defDDDRWindow, text="ARP: 250 ms", font=('Arial', 14), bg="azure2")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.525, rely=0.45)

        self.VRPLabel=tk.Label(self.defDDDRWindow, text=' VRP: 320 ms', font=('Arial', 14), bg="azure2")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.525 ,rely=0.6)

        self.DDDRButton = tk.Button(self.defDDDRWindow, text = "Next", command=self.nextDDDR) #Allows the user to submit the parameters to their device
        self.DDDRButton.pack()
        self.DDDRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def nextDDDR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.nextDDDRWindow=self.startWindow

        self.defDDDRLabel=tk.Label(self.nextDDDRWindow, text="Default DDDR Parameters", font=("Arial",18),bg="azure2") #Displays default VOO parameters
        self.defDDDRLabel.pack()
        self.defDDDRLabel.place(relx=0.35, rely=0.05)

        self.FixedAVLabel=tk.Label(self.nextDDDRWindow, text="Fixed AV Delay: 150 ms", font=("Arial", 14), bg="azure2")
        self.FixedAVLabel.pack()
        self.FixedAVLabel.place(relx=0.1,rely=0.15)

        self.DynamicAVLabel=tk.Label(self.nextDDDRWindow, text="Dynamic AV Delay: Off", font=("Arial",14), bg="azure2")
        self.DynamicAVLabel.pack()
        self.DynamicAVLabel.place(relx=0.1,rely=0.3)

        self.SensedAVLabel=tk.Label(self.nextDDDRWindow, text="Sensed AV Delay Offset: Off", font=("Arial",14),bg="azure2")
        self.SensedAVLabel.pack()
        self.SensedAVLabel.place(relx=0.1,rely=0.45)

        self.ATRDurationLabel=tk.Label(self.nextDDDRWindow, text="ATR Duration: 20 cc", font=("Arial",14), bg="azure2")
        self.ATRDurationLabel.pack()
        self.ATRDurationLabel.place(relx=0.525,rely=0.15)

        self.ATRFallbackModeLabel=tk.Label(self.nextDDDRWindow, text="ATR Fallback Mode: Off", font=("Arial",14), bg="azure2")
        self.ATRFallbackModeLabel.pack()
        self.ATRFallbackModeLabel.place(relx=0.525, rely=0.3)

        self.ATRFallbackTimeLabel=tk.Label(self.nextDDDRWindow, text="ATR Fallback Timing: 1 min", font=("Arial",14), bg="azure2")
        self.ATRFallbackTimeLabel.pack()
        self.ATRFallbackTimeLabel.place(relx=0.525,rely=0.45)

        self.RecoveryTimeLabel=tk.Label(self.defDDDRWindow, text="Recovery Time: 5 min", font=('Arial',14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.1, rely=0.6)

        self.MaxSensorRateLabel=tk.Label(self.defDDDRWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 14), bg="azure2")
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.1, rely=0.75)

        self.ReactionTimeLabel=tk.Label(self.defDDDRWindow, text="Reaction Time: 30 sec", font=('Arial',14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.6)

        self.ResponseFactorLabel=tk.Label(self.defDDDRWindow, text="Response Factor: 8", font=('Arial',14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.75)

        self.DDDRNextButton = tk.Button(self.nextDDDRWindow, text = "Submit", command=self.submitDefDDDR) #Allows the user to submit the parameters to their device
        self.DDDRNextButton.pack()
        self.DDDRNextButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefDDDR(self):
        self.DDDRLRLimit=60.0
        self.DDDRURLimit=120.0
        self.DDDRVentricularAmplitude=5.0
        self.DDDRVentricularPulseWidth=1.0
        self.DDDRVRP=320.0
        self.DDDRAtrialAmplitude=5.0
        self.DDDRAtrialPulseWidth=1.0
        self.DDDRARP=250
        self.DDDRFixedAVDelay=150
        self.DDDRDynamicAV=0
        self.DDDRSensedAV=0
        self.DDDRATRDuration=20
        self.DDDRATRFallbackMode=0
        self.DDDRATRFallbackTime=1
        self.DDDRMaxSensorRate=120
        self.DDDRReactionTime=30
        self.DDDRResponseFactor=8
        self.DDDRRecoveryTime=5
        self.DDDRVRP=320
        MyGUI.successfulSubmitted(self,self.nextDDDRWindow)

        self.currentUser.DDDR(self.DDDRLRLimit, self.DDDRURLimit, self.DDDRVentricularAmplitude, self.DDDRVentricularPulseWidth, self.DDDRVRP, self.DDDRAtrialAmplitude, self.DDDRAtrialPulseWidth, self.DDDRARP, self.DDDRFixedAVDelay, self.DDDRDynamicAV, self.DDDRSensedAV,self.DDDRATRDuration, self.DDDRATRFallbackMode, self.DDDRATRFallbackTime, self.DDDRMaxSensorRate, self.DDDRRecoveryTime, self.DDDRResponseFactor, self.DDDRReactionTime) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser) 

        #Serial comm to pacemaker when the function is submitted
        self.conn = SerialComm.SerialComm()
        self.conn.serWriteAOO(7,self.currentUser)

    def useConfigure(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.configPaceMode)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.configModeWindow = self.startWindow

        self.configModeLabel=tk.Label(self.configModeWindow, text="Please Select Your Pacing Mode", font=("Arial",18), bg="azure2") #Asks user to pick between the four pacing modes (VOO, AOO, AAI, VVI)
        self.configModeLabel.pack()
        self.configModeLabel.place(relx=0.3, rely=0.05)

        self.VOOButton = tk.Button(self.configModeWindow, text = "Configure VOO", command=self.VOOConfig,font=("Arial",12))
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.15, rely=0.15, relwidth=0.3, relheight=0.05)

        self.AOOButton = tk.Button(self.configModeWindow, text = "Configure AOO", command=self.AOOConfig,font=("Arial",12))
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.15, relwidth=0.3, relheight=0.05)

        self.AAIButton = tk.Button(self.configModeWindow, text = "Configure AAI", command=self.AAIConfig,font=("Arial",12))
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.15, rely=0.3, relwidth=0.3, relheight=0.05)

        self.VVIButton = tk.Button(self.configModeWindow, text = "Configure VVI", command=self.VVIConfig,font=("Arial",12))
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.3, relwidth=0.3, relheight=0.05)
        
        self.VOORButton=tk.Button(self.configModeWindow, text= "Configure VOOR", command=self.VOORConfig,font=("Arial",12))
        self.VOORButton.pack()
        self.VOORButton.place(relx=0.15, rely=0.45, relwidth=0.3, relheight=0.05)
        
        self.AOORButton=tk.Button(self.configModeWindow, text= "Configure AOOR", command=self.AOORConfig,font=("Arial",12))
        self.AOORButton.pack()
        self.AOORButton.place(relx=0.6, rely=0.45, relwidth=0.3, relheight=0.05)

        self.AAIRButton=tk.Button(self.configModeWindow, text= "Configure AAIR", command=self.AAIRConfig,font=("Arial",12))
        self.AAIRButton.pack()
        self.AAIRButton.place(relx=0.15, rely=0.6, relwidth=0.3, relheight=0.05)
        
        self.VVIRButton=tk.Button(self.configModeWindow, text= "Configure VVIR", command=self.VVIRConfig,font=("Arial",12))
        self.VVIRButton.pack()
        self.VVIRButton.place(relx=0.6, rely=0.6, relwidth=0.3, relheight=0.05)

        self.DDDButton=tk.Button(self.configModeWindow, text="Configure DDD", command=self.DDDConfig, font=("Arial", 12))
        self.DDDButton.pack()
        self.DDDButton.place(relx=0.15, rely=0.75, relwidth=0.3, relheight=0.05)

        self.DDDRButton=tk.Button(self.configModeWindow, text="Configure DDDR", command=self.DDDRConfig, font=("Arial",12))
        self.DDDRButton.pack()
        self.DDDRButton.place(relx=0.6, rely=0.75, relwidth=0.3, relheight=0.05)
        
    def VOOConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.VOOConfigWindow = self.startWindow

        self.VOOConfigLabel=tk.Label(self.VOOConfigWindow, text="Configure Your VOO Parameters", font=("Arial",18), bg="azure2") #Gathers the necessary parameters to configure VOO from the user
        self.VOOConfigLabel.pack()
        self.VOOConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.VOOConfigWindow, text="Lower Rate Limit: ", font=("Arial", 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.VOOConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)
        
        self.URLimitLabel= tk.Label(self.VOOConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.VOOConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 50-175 ppm\n incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.VentricularAmplitudeLabel= tk.Label(self.VOOConfigWindow, text="Ventricular Amplitude: ", font=("Arial",14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.VentricularAmplitudeTextField = tk.Entry(self.VOOConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.VentricularPulseWidthLabel= tk.Label(self.VOOConfigWindow, text="Ventricular Pulse Width: ", font=("Arial",14), bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.VentricularPulseWidthTextField = tk.Entry(self.VOOConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.VOOButton = tk.Button(self.VOOConfigWindow, text = "Submit", command=self.submitVOO) #Submit parameters to the device
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitVOO(self):
        self.VOOLRLimit= self.LRLimitTextField.get().strip()
        self.VOOURLimit= self.URLimitTextField.get().strip()
        self.VOOVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.VOOVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        try:
            if  self.VOOVentricularAmplitude == "0":
                self.VOOVentricularAmplitude = 0
            else:
                self.VOOVentricularAmplitude = float(self.VOOVentricularAmplitude)

            self.VOOLRLimit = float(self.VOOLRLimit)
            self.VOOURLimit = float(self.VOOURLimit)
            self.VOOVentricularPulseWidth = int(self.VOOVentricularPulseWidth)
        
            #Checks to make sure the values inputted are valid
            if not ((30<= self.VOOLRLimit<=50 and self.VOOLRLimit % 5 == 0) or (50<= self.VOOLRLimit<=90) or  (90 <= self.VOOLRLimit <= 175 and self.VOOLRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.VOOURLimit<=175 and self.VOOURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.VOOVentricularAmplitude == 0) or (0.1 <= self.VOOVentricularAmplitude <= 5.0 and self.VOOVentricularAmplitude*10%1==0)): 
                MyGUI.errorWindow(self)
            elif not((1.0<= self.VOOVentricularPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)  
            else:
                MyGUI.successfulSubmitted(self, self.VOOConfigWindow)
                self.currentUser.VOO(self.VOOLRLimit, self.VOOURLimit, self.VOOVentricularAmplitude, self.VOOVentricularPulseWidth)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
            self.conn = SerialComm.SerialComm()
            self.conn.connect()
            self.conn.serWriteAOO(1,self.currentUser)

            self.egramWindow = Egram.Egram(self.conn)
            self.egramWindow.run(self.VOOConfigWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)
            
    def AOOConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.AOOConfigWindow = self.startWindow

        self.AOOConfigLabel=tk.Label(self.AOOConfigWindow, text="Configure Your AOO Parameters", font=("Arial",18), bg="azure2")#Gathers the necessary parameters to configure AOO from the user
        self.AOOConfigLabel.pack()
        self.AOOConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.AOOConfigWindow, text="Lower Rate Limit: ", font=("Arial",14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.AOOConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)

        self.URLimitLabel= tk.Label(self.AOOConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.AOOConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: values between 50-175 ppm\n incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.AtrialAmplitudeLabel= tk.Label(self.AOOConfigWindow, text="Atrial Amplitude: ",font=("Arial",14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.AtrialAmplitudeTextField = tk.Entry(self.AOOConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.AtrialAmplitudeWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialAmplitudeWarningLabel.pack()
        self.AtrialAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.AtrialPulseWidthLabel= tk.Label(self.AOOConfigWindow, text="Atrial Pulse Width: ", font=("Arial",14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.AtrialPulseWidthTextField = tk.Entry(self.AOOConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.AtrialPulseWidthWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialPulseWidthWarningLabel.pack()
        self.AtrialPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.AOOButton = tk.Button(self.AOOConfigWindow, text = "Submit", command=self.submitAOO) #Submits parameters to the device
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitAOO(self):
        self.AOOLRLimit= self.LRLimitTextField.get().strip()
        self.AOOURLimit= self.URLimitTextField.get().strip()
        self.AOOAtrialAmplitude= self.AtrialAmplitudeTextField.get().strip()
        self.AOOAtrialPulseWidth= self.AtrialPulseWidthTextField.get().strip()

        try:
            if self.AOOAtrialAmplitude == "0":
                self.AOOAtrialAmplitde =0
        
            self.AOOLRLimit= float(self.AOOLRLimit)
            self.AOOURLimit= float(self.AOOURLimit)
            self.AOOAtrialAmplitude= float(self.AOOAtrialAmplitude)
            self.AOOAtrialPulseWidth= float(self.AOOAtrialPulseWidth)
            
            #Checks to make sure the values inputted are valid
            if not ((30<= self.AOOLRLimit<=50 and self.AOOLRLimit % 5 == 0) or (50<= self.AOOLRLimit<=90) or  (90 <= self.AOOLRLimit <= 175 and self.AOOLRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.AOOURLimit<=175 and self.AOOURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.AOOAtrialAmplitude == 0) or (0.1 <= self.AOOAtrialAmplitude <= 5.0 and self.AOOAtrialAmplitude*10 %1==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.AOOAtrialPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)    
            else:
                self.currentUser.AOO(self.AOOLRLimit, self.AOOURLimit, self.AOOAtrialAmplitude, self.AOOAtrialPulseWidth)
                self.db.updateUser(self.currentUser)
                MyGUI.successfulSubmitted(self,self.AOOConfigWindow)#Updates the user’s chosen parameters to the database

            self.conn = SerialComm.SerialComm()
            self.conn.connect()
            self.conn.serWriteAOO(0,self.currentUser)

            self.egramWindow = Egram.Egram(self.conn)
            self.egramWindow.run(self.AOOConfigWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)

    def AAIConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.AAIConfigWindow = self.startWindow

        self.AAIConfigLabel=tk.Label(self.AAIConfigWindow, text="Configure Your AAI Parameters", font=("Arial",18), bg="azure2")#Gathers the necessary parameters to configure AAI from the user
        self.AAIConfigLabel.pack()
        self.AAIConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.AAIConfigWindow, text="Lower Rate Limit: ", font=("Arial",14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.AAIConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)

        self.URLimitLabel= tk.Label(self.AAIConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.AAIConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)

        self.URLimitWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between\n 50-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.AtrialAmplitudeLabel= tk.Label(self.AAIConfigWindow, text="Atrial Amplitude: ",font=("Arial",14),bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.AtrialAmplitudeTextField = tk.Entry(self.AAIConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.AtrialAmplitudeWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialAmplitudeWarningLabel.pack()
        self.AtrialAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.AtrialPulseWidthLabel= tk.Label(self.AAIConfigWindow, text="Atrial Pulse Width: ", font=("Arial",14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.AtrialPulseWidthTextField = tk.Entry(self.AAIConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.AtrialPulseWidthWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialPulseWidthWarningLabel.pack()
        self.AtrialPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.ARPLabel= tk.Label(self.AAIConfigWindow, text="ARP: ", font=("Arial", 14),bg="azure2")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.55,rely=0.15)
        self.ARPTextField = tk.Entry(self.AAIConfigWindow)
        self.ARPTextField.pack()
        self.ARPTextField.place(relx=0.7, rely=0.15)

        self.ARPWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between\n 150-500 ms with 10 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.ARPWarningLabel.pack()
        self.ARPWarningLabel.place(relx=0.55, rely=0.2)

        self.AAIButton = tk.Button(self.AAIConfigWindow, text = "Submit", command=self.submitAAI) #Submits parameters to the device
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitAAI(self):
        self.AAILRLimit= self.LRLimitTextField.get().strip()
        self.AAIURLimit= self.URLimitTextField.get().strip()
        self.AAIAtrialAmplitude= self.AtrialAmplitudeTextField.get().strip()
        self.AAIAtrialPulseWidth= self.AtrialPulseWidthTextField.get().strip()
        self.AAIARP= self.ARPTextField.get().strip()
        try:
            if  self.AAIAtrialAmplitude== "0":
                self.AAIAtrialAmplitude = 0
            else:
                self.AAIAtrialAmplitude= float(self.AAIAtrialAmplitude)
                
            self.AAILRLimit= float(self.AAILRLimit)
            self.AAIURLimit= float(self.AAIURLimit)
            self.AAIAtrialPulseWidth= float(self.AAIAtrialPulseWidth)
            self.AAIARP= float(self.AAIARP)
            
            #Checks to make sure the values inputted are valid
            if not ((30<= self.AAILRLimit<=50 and self.AAILRLimit % 5 == 0) or (50<= self.AAILRLimit<=90) or  (90 <= self.AAILRLimit <= 175 and self.AAILRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.AAIURLimit<=175 and self.AAIURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.AAIAtrialAmplitude==0) or (0.1 <= self.AAIAtrialAmplitude <= 5.0 and self.AAIAtrialAmplitude*10 %1==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.AAIAtrialPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((150<= self.AAIARP<=500 and self.AAIARP % 10 == 0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.AAI(self.AAILRLimit, self.AAIURLimit, self.AAIAtrialAmplitude, self.AAIAtrialPulseWidth, self.AAIARP)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.successfulSubmitted(self,self.AAIConfigWindow)
            
            
            self.conn = SerialComm.SerialComm()
            self.conn.connect()
            self.conn.serWriteAOO(2,self.currentUser)

            self.egramWindow = Egram.Egram(self.conn)
            self.egramWindow.run(self.AAIConfigWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)

    def VVIConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.VVIConfigWindow = self.startWindow

        self.VVIConfigLabel=tk.Label(self.VVIConfigWindow, text="Configure Your VVI Parameters", font=("Arial",18), bg="azure2")#Gathers the necessary parameters to configure VVI from the user
        self.VVIConfigLabel.pack()
        self.VVIConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.VVIConfigWindow, text="Lower Rate Limit: ", font=("Arial",14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.VVIConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)

        self.URLimitLabel= tk.Label(self.VVIConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.VVIConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between\n 50-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue" , bg="azure2")
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.VentricularAmplitudeLabel= tk.Label(self.VVIConfigWindow, text="Ventricular Amplitude: ",font=("Arial",14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.VentricularAmplitudeTextField = tk.Entry(self.VVIConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.VentricularPulseWidthLabel= tk.Label(self.VVIConfigWindow, text="Ventricular Pulse Width: ", font=("Arial",14), bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.VentricularPulseWidthTextField = tk.Entry(self.VVIConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2")
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.VRPLabel= tk.Label(self.VVIConfigWindow, text="VRP: ", font=("Arial",14), bg="azure2")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.55,rely=0.15)
        self.VRPTextField = tk.Entry(self.VVIConfigWindow)
        self.VRPTextField.pack()
        self.VRPTextField.place(relx=0.7, rely=0.15)

        self.VRPWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between\n 150-500 ms with 10 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VRPWarningLabel.pack()
        self.VRPWarningLabel.place(relx=0.55, rely=0.2)

        self.VVIButton = tk.Button(self.VVIConfigWindow, text = "Submit", command=self.submitVVI) #Submits parameters to the device
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitVVI(self):
        self.VVILRLimit= self.LRLimitTextField.get().strip()
        self.VVIURLimit= self.URLimitTextField.get().strip()
        self.VVIVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.VVIVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        self.VVIVRP= self.VRPTextField.get().strip()
        #Checks to make sure the values inputted are valid
        try:
            if self.VVIVentricularAmplitude == "0":
                self.VVIVentricularAmplitude =0
            else:
                self.VVIVentricularAmplitude= float(self.VVIVentricularAmplitude)
                    
            self.VVILRLimit= float(self.VVILRLimit)
            self.VVIURLimit= float(self.VVIURLimit)
            self.VVIVentricularPulseWidth= float(self.VVIVentricularPulseWidth)
            self.VVIVRP= float(self.VVIVRP)
        
            if not ((30<= self.VVILRLimit<=50 and self.VVILRLimit % 5 == 0) or (50<= self.VVILRLimit<=90) or  (90 <= self.VVILRLimit <= 175 and self.VVILRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.VVIURLimit<=175 and self.VVIURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not  ((0.1 <= self.VVIVentricularAmplitude <= 5.0 and self.VVIVentricularAmplitude*10 %1==0) or (self.VVIVentricularAmplitude ==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.VVIVentricularPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((150<= self.VVIVRP<=500 and self.VVIVRP % 10 == 0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.VVI(self.VVILRLimit, self.VVIURLimit, self.VVIVentricularAmplitude, self.VVIVentricularPulseWidth, self.VVIVRP)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.successfulSubmitted(self,self.VVIConfigWindow)
            
            self.conn = SerialComm.SerialComm()
            self.conn.connect()
            self.conn.serWriteAOO(3,self.currentUser)

            self.egramWindow = Egram.Egram(self.conn)
            self.egramWindow.run(self.VVIConfigWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)
        
    def VOORConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.VOORConfigWindow = self.startWindow

        self.VOORConfigLabel=tk.Label(self.VOORConfigWindow, text="Configure Your VOOR Parameters", font=("Arial",18), bg="azure2") #Gathers the necessary parameters to configure VOO from the user
        self.VOORConfigLabel.pack()
        self.VOORConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.VOORConfigWindow, text="Lower Rate Limit: ", font=("Arial", 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.VOORConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.VOORConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)
        
        self.URLimitLabel= tk.Label(self.VOORConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.VOORConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.VOORConfigWindow, text="Valid inputs are: values between\n 50-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.VentricularAmplitudeLabel= tk.Label(self.VOORConfigWindow, text="Ventricular Amplitude: ", font=("Arial",14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.VentricularAmplitudeTextField = tk.Entry(self.VOORConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VOORConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.VentricularPulseWidthLabel= tk.Label(self.VOORConfigWindow, text="Ventricular Pulse Width: ", font=("Arial",14), bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.VentricularPulseWidthTextField = tk.Entry(self.VOORConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.VOORConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.MaximumSensorRateLabel=tk.Label(self.VOORConfigWindow, text="Maximum Sensor Rate: ", font=("Arial",14), bg="azure2")
        self.MaximumSensorRateLabel.pack()
        self.MaximumSensorRateLabel.place(relx=0.55, rely=0.15)
        self.MaximumSensorRateTextField=tk.Entry(self.VOORConfigWindow)
        self.MaximumSensorRateTextField.pack()
        self.MaximumSensorRateTextField.place(relx=0.825, rely=0.15)

        self.MaximumSensorRateWarningLabel=tk.Label(self.VOORConfigWindow, text="Valid inputs are: values between\n 50-175 ppm with 5 ppm increment", font=("Arial",12), fg="blue", bg="azure2")
        self.MaximumSensorRateWarningLabel.pack()
        self.MaximumSensorRateWarningLabel.place(relx=0.55, rely=0.2)

        self.ReactionTimeLabel=tk.Label(self.VOORConfigWindow, text="Reaction Time: ", font=("Arial",14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.55, rely=0.35)
        self.ReactionTimeTextField=tk.Entry(self.VOORConfigWindow)
        self.ReactionTimeTextField.pack()
        self.ReactionTimeTextField.place(relx=0.825,rely=0.35)

        self.ReactionTimeWarningLabel=tk.Label(self.VOORConfigWindow,text="Valid input are: values between 10-50 sec\n with a 10 sec increment", font=("Arial",12), fg="blue", bg="azure2")
        self.ReactionTimeWarningLabel.pack()
        self.ReactionTimeWarningLabel.place(relx=0.55,rely=0.4)

        self.ResponseFactorLabel=tk.Label(self.VOORConfigWindow, text="Response Factor: ", font=("Arial",14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.55,rely=0.5)
        self.ResponseFactorTextField=tk.Entry(self.VOORConfigWindow)
        self.ResponseFactorTextField.pack()
        self.ResponseFactorTextField.place(relx=0.825, rely=0.5)

        self.ResponseFactorWarningLabel=tk.Label(self.VOORConfigWindow, text="Valid inputs are: values between\n 1-16 with an increment of 1", font=("Arial",12), fg="blue", bg="azure2")
        self.ResponseFactorWarningLabel.pack()
        self.ResponseFactorWarningLabel.place(relx=0.55,rely=0.55)

        self.RecoveryTimeLabel=tk.Label(self.VOORConfigWindow, text="Recovery Time: ", font=("Arial",14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.55, rely=0.65)
        self.RecoveryTimeTextField=tk.Entry(self.VOORConfigWindow)
        self.RecoveryTimeTextField.pack()
        self.RecoveryTimeTextField.place(relx=0.825,rely=0.65)

        self.RecoveryTimeWarningLabel=tk.Label(self.VOORConfigWindow, text="Valid inputs are: values between\n 2-16 min with a 1 min increment", font=("Arial",12), fg="blue", bg="azure2")
        self.RecoveryTimeWarningLabel.pack()
        self.RecoveryTimeWarningLabel.place(relx=0.55,rely=0.7)

        self.VOORButton = tk.Button(self.VOORConfigWindow, text = "Submit", command=self.submitVOOR) #Submit parameters to the device
        self.VOORButton.pack()
        self.VOORButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitVOOR(self):
        self.VOORLRLimit= self.LRLimitTextField.get().strip()
        self.VOORURLimit= self.URLimitTextField.get().strip()
        self.VOORVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.VOORVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        self.VOORMaxSensorRate=self.MaximumSensorRateTextField.get().strip()
        self.VOORReactionTime=self.ReactionTimeTextField.get().strip()
        self.VOORResponseFactor=self.ResponseFactorTextField.get().strip()
        self.VOORRecoveryTime=self.RecoveryTimeTextField.get().strip()

        try:
            if  self.VOORVentricularAmplitude == "0":
                self.VOORVentricularAmplitude = 0
            else:
                self.VOORVentricularAmplitude = float(self.VOORVentricularAmplitude)

            self.VOORLRLimit = float(self.VOORLRLimit)
            self.VOORURLimit = float(self.VOORURLimit)
            self.VOORVentricularPulseWidth = float(self.VOORVentricularPulseWidth)
            self.VOORMaxSensorRate= float(self.VOORMaxSensorRate)
            self.VOORReactionTime= float(self.VOORReactionTime)
            self.VOORResponseFactor=float(self.VOORResponseFactor)
            self.VOORRecoveryTime= float(self.VOORRecoveryTime)
        
            #Checks to make sure the values inputted are valid
            if not ((30<= self.VOORLRLimit<=50 and self.VOORLRLimit % 5 == 0) or (50<= self.VOORLRLimit<=90) or  (90 <= self.VOORLRLimit <= 175 and self.VOORLRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.VOORURLimit<=175 and self.VOORURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.VOORVentricularAmplitude == 0) or (0.1 <= self.VOORVentricularAmplitude <= 5.0 and self.VOORVentricularAmplitude*10%1==0)): 
                MyGUI.errorWindow(self)
            elif not((1.0<= self.VOORVentricularPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((50<=self.VOORMaxSensorRate<=175 and self.VOORMaxSensorRate %5==0)):
                MyGUI.errorWindow(self)
            elif not ((10<=self.VOORReactionTime<=50 and self.VOORReactionTime%10==0)):
                MyGUI.errorWindow(self)
            elif not ((1<=self.VOORResponseFactor<=16)):
                MyGUI.errorWindow(self)
            elif not ((2<=self.VOORRecoveryTime<=16)):
                MyGUI.errorWindow(self)
            else:
                MyGUI.successfulSubmitted(self, self.VOORConfigWindow)
                self.currentUser.VOOR(self.VOORLRLimit, self.VOORURLimit, self.VOORVentricularAmplitude, self.VOORVentricularPulseWidth, self.VOORMaxSensorRate, self.VOORResponseFactor, self.VOORReactionTime, self.VOORRecoveryTime)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database 
            
            self.conn = SerialComm.SerialComm()
            self.conn.connect()
            self.conn.serWriteAOO(5,self.currentUser)

            self.egramWindow = Egram.Egram(self.conn)
            self.egramWindow.run(self.VOORConfigWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)

    def AOORConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.AOORConfigWindow = self.startWindow

        self.AOORConfigLabel=tk.Label(self.AOORConfigWindow, text="Configure Your AOOR Parameters", font=("Arial",18), bg="azure2")#Gathers the necessary parameters to configure AOO from the user
        self.AOORConfigLabel.pack()
        self.AOORConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.AOORConfigWindow, text="Lower Rate Limit: ", font=("Arial",14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.AOORConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.AOORConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)

        self.URLimitLabel= tk.Label(self.AOORConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.AOORConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.AOORConfigWindow, text="Valid inputs are: values between\n 50-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.AtrialAmplitudeLabel= tk.Label(self.AOORConfigWindow, text="Atrial Amplitude: ",font=("Arial",14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.AtrialAmplitudeTextField = tk.Entry(self.AOORConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.AtrialAmplitudeWarningLabel= tk.Label(self.AOORConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialAmplitudeWarningLabel.pack()
        self.AtrialAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.AtrialPulseWidthLabel= tk.Label(self.AOORConfigWindow, text="Atrial Pulse Width: ", font=("Arial",14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.AtrialPulseWidthTextField = tk.Entry(self.AOORConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.AtrialPulseWidthWarningLabel= tk.Label(self.AOORConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialPulseWidthWarningLabel.pack()
        self.AtrialPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.MaximumSensorRateLabel=tk.Label(self.AOORConfigWindow, text="Maximum Sensor Rate: ", font=("Arial",14), bg="azure2")
        self.MaximumSensorRateLabel.pack()
        self.MaximumSensorRateLabel.place(relx=0.55, rely=0.15)
        self.MaximumSensorRateTextField=tk.Entry(self.AOORConfigWindow)
        self.MaximumSensorRateTextField.pack()
        self.MaximumSensorRateTextField.place(relx=0.825, rely=0.15)

        self.MaximumSensorRateWarningLabel=tk.Label(self.AOORConfigWindow, text="Valid inputs are: values between\n 50-175 ppm with 5 ppm increment", font=("Arial",12), fg="blue", bg="azure2")
        self.MaximumSensorRateWarningLabel.pack()
        self.MaximumSensorRateWarningLabel.place(relx=0.55, rely=0.2)

        self.ReactionTimeLabel=tk.Label(self.AOORConfigWindow, text="Reaction Time: ", font=("Arial",14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.55, rely=0.35)
        self.ReactionTimeTextField=tk.Entry(self.AOORConfigWindow)
        self.ReactionTimeTextField.pack()
        self.ReactionTimeTextField.place(relx=0.825,rely=0.35)

        self.ReactionTimeWarningLabel=tk.Label(self.AOORConfigWindow,text="Valid input are: values between 10-50 sec\n with a 10 sec increment", font=("Arial",12), fg="blue", bg="azure2")
        self.ReactionTimeWarningLabel.pack()
        self.ReactionTimeWarningLabel.place(relx=0.55,rely=0.4)

        self.ResponseFactorLabel=tk.Label(self.AOORConfigWindow, text="Response Factor: ", font=("Arial",14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.55,rely=0.5)
        self.ResponseFactorTextField=tk.Entry(self.AOORConfigWindow)
        self.ResponseFactorTextField.pack()
        self.ResponseFactorTextField.place(relx=0.825, rely=0.5)

        self.ResponseFactorWarningLabel=tk.Label(self.AOORConfigWindow, text="Valid inputs are: values between 1-16\n with an increment of 1", font=("Arial",12), fg="blue", bg="azure2")
        self.ResponseFactorWarningLabel.pack()
        self.ResponseFactorWarningLabel.place(relx=0.55,rely=0.55)

        self.RecoveryTimeLabel=tk.Label(self.AOORConfigWindow, text="Recovery Time: ", font=("Arial",14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.55, rely=0.65)
        self.RecoveryTimeTextField=tk.Entry(self.AOORConfigWindow)
        self.RecoveryTimeTextField.pack()
        self.RecoveryTimeTextField.place(relx=0.825,rely=0.65)

        self.RecoveryTimeWarningLabel=tk.Label(self.AOORConfigWindow, text="Valid inputs are: values between\n 2-16 min with a 1 min increment", font=("Arial",12), fg="blue", bg="azure2")
        self.RecoveryTimeWarningLabel.pack()
        self.RecoveryTimeWarningLabel.place(relx=0.55,rely=0.7)

        self.AOORButton = tk.Button(self.AOORConfigWindow, text = "Submit", command=self.submitAOOR) #Submits parameters to the device
        self.AOORButton.pack()
        self.AOORButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitAOOR(self):
        self.AOORLRLimit= self.LRLimitTextField.get().strip()
        self.AOORURLimit= self.URLimitTextField.get().strip()
        self.AOORAtrialAmplitude= self.AtrialAmplitudeTextField.get().strip()
        self.AOORAtrialPulseWidth= self.AtrialPulseWidthTextField.get().strip()
        self.AOORMaxSensorRate=self.MaximumSensorRateTextField.get().strip()
        self.AOORReactionTime=self.ReactionTimeTextField.get().strip()
        self.AOORResponseFactor=self.ResponseFactorTextField.get().strip()
        self.AOORRecoveryTime=self.RecoveryTimeTextField.get().strip()

        try:
            if self.AOORAtrialAmplitude == "0":
                self.AOORAtrialAmplitude = 0
            else:
                self.AOORAtrialAmplitude= float(self.AOORAtrialAmplitude)
            
            self.AOORLRLimit= float(self.AOORLRLimit)
            self.AOORURLimit= float(self.AOORURLimit)
            self.AOORAtrialPulseWidth= float(self.AOORAtrialPulseWidth)
            self.AOORMaxSensorRate=float(self.AOORMaxSensorRate)
            self.AOORReactionTime=float(self.AOORReactionTime)
            self.AOORResponseFactor=float(self.AOORResponseFactor)
            self.AOORRecoveryTime=float(self.AOORRecoveryTime)
        
            #Checks to make sure the values inputted are valid
            if not ((30<= self.AOORLRLimit<=50 and self.AOORLRLimit % 5 == 0) or (50<= self.AOORLRLimit<=90) or  (90 <= self.AOORLRLimit <= 175 and self.AOORLRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.AOORURLimit<=175 and self.AOORURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.AOORAtrialAmplitude==0) or (0.1 <= self.AOORAtrialAmplitude <= 5.0 and self.AOORAtrialAmplitude*10 %1==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.AOORAtrialPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((50.0<=self.AOORMaxSensorRate<=175.0 and self.AOORMaxSensorRate %5==0)):
                MyGUI.errorWindow(self)
            elif not ((10.0<=self.AOORReactionTime<=50.0 and self.AOORReactionTime%10==0)):
                MyGUI.errorWindow(self)
            elif not ((1.0<=self.AOORResponseFactor<=16.0)):
                MyGUI.errorWindow(self)
            elif not ((2.0<=self.AOORRecoveryTime<=16.0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.AOOR(self.AOORLRLimit, self.AOORURLimit, self.AOORAtrialAmplitude, self.AOORAtrialPulseWidth, self.AOORMaxSensorRate, self.AOORResponseFactor, self.AOORReactionTime, self.AOORRecoveryTime)
                self.db.updateUser(self.currentUser)
                MyGUI.successfulSubmitted(self,self.AOORConfigWindow)#Updates the user’s chosen parameters to the database
            
            self.conn = SerialComm.SerialComm()
            self.conn.connect()
            self.conn.serWriteAOO(4,self.currentUser)

            self.egramWindow = Egram.Egram(self.conn)
            self.egramWindow.run(self.AOORConfigWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)
        
    def AAIRConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.AAIRConfigWindow = self.startWindow

        self.AAIRConfigLabel=tk.Label(self.AAIRConfigWindow, text="Configure Your AAIR Parameters", font=("Arial", 18), bg="azure2")#Gathers the necessary parameters to configure AAI from the user
        self.AAIRConfigLabel.pack()
        self.AAIRConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.AAIRConfigWindow, text="Lower Rate Limit: ", font=("Arial",14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.AAIRConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.AAIRConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)

        self.URLimitLabel= tk.Label(self.AAIRConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.AAIRConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.AAIRConfigWindow, text="Valid inputs are: values between\n 50-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.AtrialAmplitudeLabel= tk.Label(self.AAIRConfigWindow, text="Atrial Amplitude: ",font=("Arial",14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.AtrialAmplitudeTextField = tk.Entry(self.AAIRConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.AtrialAmplitudeWarningLabel= tk.Label(self.AAIRConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialAmplitudeWarningLabel.pack()
        self.AtrialAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.AtrialPulseWidthLabel= tk.Label(self.AAIRConfigWindow, text="Atrial Pulse Width: ", font=("Arial",14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.AtrialPulseWidthTextField = tk.Entry(self.AAIRConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.AtrialPulseWidthWarningLabel= tk.Label(self.AAIRConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialPulseWidthWarningLabel.pack()
        self.AtrialPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.ARPLabel= tk.Label(self.AAIRConfigWindow, text="ARP: ", font=("Arial", 14), bg="azure2")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.325,rely=0.8)
        self.ARPTextField = tk.Entry(self.AAIRConfigWindow)
        self.ARPTextField.pack()
        self.ARPTextField.place(relx=0.425, rely=0.8)

        self.ARPWarningLabel= tk.Label(self.AAIRConfigWindow, text="Valid inputs are: values between\n 150-500 ms with 10 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.ARPWarningLabel.pack()
        self.ARPWarningLabel.place(relx=0.325, rely=0.85)

        self.MaximumSensorRateLabel=tk.Label(self.AAIRConfigWindow, text="Maximum Sensor Rate: ", font=("Arial",14), bg="azure2")
        self.MaximumSensorRateLabel.pack()
        self.MaximumSensorRateLabel.place(relx=0.55, rely=0.15)
        self.MaximumSensorRateTextField=tk.Entry(self.AAIRConfigWindow)
        self.MaximumSensorRateTextField.pack()
        self.MaximumSensorRateTextField.place(relx=0.825, rely=0.15)

        self.MaximumSensorRateWarningLabel=tk.Label(self.AAIRConfigWindow, text="Valid inputs are: values between\n 50-175 ppm with 5 ppm increment", font=("Arial",12), fg="blue", bg="azure2")
        self.MaximumSensorRateWarningLabel.pack()
        self.MaximumSensorRateWarningLabel.place(relx=0.55, rely=0.2)

        self.ReactionTimeLabel=tk.Label(self.AAIRConfigWindow, text="Reaction Time: ", font=("Arial",14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.55, rely=0.35)
        self.ReactionTimeTextField=tk.Entry(self.AAIRConfigWindow)
        self.ReactionTimeTextField.pack()
        self.ReactionTimeTextField.place(relx=0.825,rely=0.35)

        self.ReactionTimeWarningLabel=tk.Label(self.AAIRConfigWindow,text="Valid input are: values between\n 10-50 sec with a 10 sec increment", font=("Arial",12), fg="blue",bg="azure2")
        self.ReactionTimeWarningLabel.pack()
        self.ReactionTimeWarningLabel.place(relx=0.55,rely=0.4)

        self.ResponseFactorLabel=tk.Label(self.AAIRConfigWindow, text="Response Factor: ", font=("Arial",14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.55,rely=0.5)
        self.ResponseFactorTextField=tk.Entry(self.AAIRConfigWindow)
        self.ResponseFactorTextField.pack()
        self.ResponseFactorTextField.place(relx=0.825, rely=0.5)

        self.ResponseFactorWarningLabel=tk.Label(self.AAIRConfigWindow, text="Valid inputs are: values between\n 1-16 with an increment of 1", font=("Arial",12), fg="blue", bg="azure2")
        self.ResponseFactorWarningLabel.pack()
        self.ResponseFactorWarningLabel.place(relx=0.55,rely=0.55)

        self.RecoveryTimeLabel=tk.Label(self.AAIRConfigWindow, text="Recovery Time: ", font=("Arial",14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.55, rely=0.65)
        self.RecoveryTimeTextField=tk.Entry(self.AAIRConfigWindow)
        self.RecoveryTimeTextField.pack()
        self.RecoveryTimeTextField.place(relx=0.825,rely=0.65)

        self.RecoveryTimeWarningLabel=tk.Label(self.AAIRConfigWindow, text="Valid inputs are: values between\n 2-16 min with a 1 min increment", font=("Arial",12), fg="blue", bg="azure2")
        self.RecoveryTimeWarningLabel.pack()
        self.RecoveryTimeWarningLabel.place(relx=0.55,rely=0.7)


        self.AAIRButton = tk.Button(self.AAIRConfigWindow, text = "Submit", command=self.submitAAIR) #Submits parameters to the device
        self.AAIRButton.pack()
        self.AAIRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitAAIR(self):
        self.AAIRLRLimit= self.LRLimitTextField.get().strip()
        self.AAIRURLimit= self.URLimitTextField.get().strip()
        self.AAIRAtrialAmplitude= self.AtrialAmplitudeTextField.get().strip()
        self.AAIRAtrialPulseWidth= self.AtrialPulseWidthTextField.get().strip()
        self.AAIRARP= self.ARPTextField.get().strip()
        self.AAIRMaxSensorRate= self.MaximumSensorRateTextField.get().strip()
        self.AAIRReactionTime=self.ReactionTimeTextField.get().strip()
        self.AAIRResponseFactor=self.ResponseFactorTextField.get().strip()
        self.AAIRRecoveryTime= self.RecoveryTimeTextField.get().strip()
        try:
            if  self.AAIRAtrialAmplitude== "0":
                self.AAIRAtrialAmplitude = 0
            else:
                self.AAIRAtrialAmplitude= float(self.AAIRAtrialAmplitude)
                
            self.AAIRLRLimit= float(self.AAIRLRLimit)
            self.AAIRURLimit= float(self.AAIRURLimit)
            self.AAIRAtrialPulseWidth= float(self.AAIRAtrialPulseWidth)
            self.AAIRARP= float(self.AAIRARP)
            self.AAIRMaxSensorRate= float(self.AAIRMaxSensorRate)
            self.AAIRReactionTime=float(self.AAIRReactionTime)
            self.AAIRResponseFactor=float(self.AAIRResponseFactor)
            self.AAIRRecoveryTime= float(self.AAIRRecoveryTime)
        
            #Checks to make sure the values inputted are valid
            if not ((30<= self.AAIRLRLimit<=50 and self.AAIRLRLimit % 5 == 0) or (50<= self.AAIRLRLimit<=90) or  (90 <= self.AAIRLRLimit <= 175 and self.AAIRLRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.AAIRURLimit<=175 and self.AAIRURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.AAIRAtrialAmplitude==0) or (0.1 <= self.AAIRAtrialAmplitude <= 5.0 and self.AAIRAtrialAmplitude*10 %1==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.AAIRAtrialPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((150<= self.AAIRARP<=500 and self.AAIRARP % 10 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50.0<=self.AAIRMaxSensorRate<=175.0 and self.AAIRMaxSensorRate %5==0)):
                MyGUI.errorWindow(self)
            elif not ((10.0<=self.AAIRReactionTime<=50.0 and self.AAIRReactionTime%10==0)):
                MyGUI.errorWindow(self)
            elif not ((1.0<=self.AAIRResponseFactor<=16.0)):
                MyGUI.errorWindow(self)
            elif not ((2.0<=self.AAIRRecoveryTime<=16.0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.AAIR(self.AAIRLRLimit, self.AAIRURLimit, self.AAIRAtrialAmplitude, self.AAIRAtrialPulseWidth, self.AAIRARP, self.AAIRMaxSensorRate, self.AAIRReactionTime, self.AAIRResponseFactor, self.AAIRRecoveryTime)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.successfulSubmitted(self,self.AAIRConfigWindow)
            
            self.conn = SerialComm.SerialComm()
            self.conn.connect()
            self.conn.serWriteAOO(6,self.currentUser)

            self.egramWindow = Egram.Egram(self.conn)
            self.egramWindow.run(self.AAIRConfigWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)

    def VVIRConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.VVIRConfigWindow = self.startWindow

        self.VVIRConfigLabel=tk.Label(self.VVIRConfigWindow, text="Configure Your VVIR Parameters", font=("Arial",18), bg="azure2")#Gathers the necessary parameters to configure VVI from the user
        self.VVIRConfigLabel.pack()
        self.VVIRConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.VVIRConfigWindow, text="Lower Rate Limit: ", font=("Arial",14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.VVIRConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.VVIRConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)

        self.URLimitLabel= tk.Label(self.VVIRConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.VVIRConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.VVIRConfigWindow, text="Valid inputs are: values between\n 50-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.VentricularAmplitudeLabel= tk.Label(self.VVIRConfigWindow, text="Ventricular Amplitude: ",font=("Arial",14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.VentricularAmplitudeTextField = tk.Entry(self.VVIRConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VVIRConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.VentricularPulseWidthLabel= tk.Label(self.VVIRConfigWindow, text="Ventricular Pulse Width: ", font=("Arial",14), bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.VentricularPulseWidthTextField = tk.Entry(self.VVIRConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.VVIRConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.VRPLabel= tk.Label(self.VVIRConfigWindow, text="VRP: ", font=("Arial",14), bg="azure2")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.325,rely=0.8)
        self.VRPTextField = tk.Entry(self.VVIRConfigWindow)
        self.VRPTextField.pack()
        self.VRPTextField.place(relx=0.425, rely=0.8)

        self.VRPWarningLabel= tk.Label(self.VVIRConfigWindow, text="Valid inputs are: values between\n 150-500 ms with 10 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VRPWarningLabel.pack()
        self.VRPWarningLabel.place(relx=0.325, rely=0.85)

        self.MaximumSensorRateLabel=tk.Label(self.VVIRConfigWindow, text="Maximum Sensor Rate: ", font=("Arial",14), bg="azure2")
        self.MaximumSensorRateLabel.pack()
        self.MaximumSensorRateLabel.place(relx=0.55, rely=0.15)
        self.MaximumSensorRateTextField=tk.Entry(self.VVIRConfigWindow)
        self.MaximumSensorRateTextField.pack()
        self.MaximumSensorRateTextField.place(relx=0.825, rely=0.15)

        self.MaximumSensorRateWarningLabel=tk.Label(self.VVIRConfigWindow, text="Valid inputs are: values between\n 50-175 ppm with 5 ppm increment", font=("Arial",12), fg="blue", bg="azure2")
        self.MaximumSensorRateWarningLabel.pack()
        self.MaximumSensorRateWarningLabel.place(relx=0.55, rely=0.2)

        self.ReactionTimeLabel=tk.Label(self.VVIRConfigWindow, text="Reaction Time: ", font=("Arial",14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.55, rely=0.35)
        self.ReactionTimeTextField=tk.Entry(self.VVIRConfigWindow)
        self.ReactionTimeTextField.pack()
        self.ReactionTimeTextField.place(relx=0.825,rely=0.35)

        self.ReactionTimeWarningLabel=tk.Label(self.VVIRConfigWindow,text="Valid input are: values between\n 10-50 sec with a 10 sec increment", font=("Arial",12), fg="blue", bg="azure2")
        self.ReactionTimeWarningLabel.pack()
        self.ReactionTimeWarningLabel.place(relx=0.55,rely=0.4)

        self.ResponseFactorLabel=tk.Label(self.VVIRConfigWindow, text="Response Factor: ", font=("Arial",14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.55,rely=0.5)
        self.ResponseFactorTextField=tk.Entry(self.VVIRConfigWindow)
        self.ResponseFactorTextField.pack()
        self.ResponseFactorTextField.place(relx=0.825, rely=0.5)

        self.ResponseFactorWarningLabel=tk.Label(self.VVIRConfigWindow, text="Valid inputs are: values between\n 1-16 with an increment of 1", font=("Arial",12), fg="blue", bg="azure2")
        self.ResponseFactorWarningLabel.pack()
        self.ResponseFactorWarningLabel.place(relx=0.55,rely=0.55)

        self.RecoveryTimeLabel=tk.Label(self.VVIRConfigWindow, text="Recovery Time: ", font=("Arial",14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.55, rely=0.65)
        self.RecoveryTimeTextField=tk.Entry(self.VVIRConfigWindow)
        self.RecoveryTimeTextField.pack()
        self.RecoveryTimeTextField.place(relx=0.825,rely=0.65)

        self.RecoveryTimeWarningLabel=tk.Label(self.VVIRConfigWindow, text="Valid inputs are: values between\n 2-16 min with a 1 min increment", font=("Arial",12), fg="blue", bg="azure2")
        self.RecoveryTimeWarningLabel.pack()
        self.RecoveryTimeWarningLabel.place(relx=0.55,rely=0.7)

        self.VVIRButton = tk.Button(self.VVIRConfigWindow, text = "Submit", command=self.submitVVIR) #Submits parameters to the device
        self.VVIRButton.pack()
        self.VVIRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitVVIR(self):
        self.VVIRLRLimit= self.LRLimitTextField.get().strip()
        self.VVIRURLimit= self.URLimitTextField.get().strip()
        self.VVIRVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.VVIRVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        self.VVIRVRP= self.VRPTextField.get().strip()
        self.VVIRMaxSensorRate= self.MaximumSensorRateTextField.get().strip()
        self.VVIRReactionTime= self.ReactionTimeTextField.get().strip()
        self.VVIRRecoveryTime= self.RecoveryTimeTextField.get().strip()
        self.VVIRResponseFactor= self.ResponseFactorTextField.get().strip()

        #Checks to make sure the values inputted are valid
        try:
            if self.VVIRVentricularAmplitude == "0":
                self.VVIRVentricularAmplitude =0
            else:
                self.VVIRVentricularAmplitude= float(self.VVIRVentricularAmplitude)
                    
            self.VVIRLRLimit= float(self.VVIRLRLimit)
            self.VVIRURLimit= float(self.VVIRURLimit)
            self.VVIRVentricularPulseWidth= float(self.VVIRVentricularPulseWidth)
            self.VVIRVRP= float(self.VVIRVRP)
            self.VVIRMaxSensorRate= float(self.VVIRMaxSensorRate)
            self.VVIRRecoveryTime= float(self.VVIRRecoveryTime)
            self.VVIRResponseFactor= float(self.VVIRResponseFactor)
            self.VVIRReactionTime= float(self.VVIRReactionTime)

            if not ((30<= self.VVIRLRLimit<=50 and self.VVIRLRLimit % 5 == 0) or (50<= self.VVIRLRLimit<=90) or  (90 <= self.VVIRLRLimit <= 175 and self.VVIRLRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.VVIRURLimit<=175 and self.VVIRURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not  ((0.1 <= self.VVIRVentricularAmplitude <= 5.0 and self.VVIRVentricularAmplitude*10 %1==0) or (self.VVIRVentricularAmplitude ==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.VVIRVentricularPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((150<= self.VVIRVRP<=500 and self.VVIRVRP % 10 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50.0<=self.VVIRMaxSensorRate<=175.0 and self.VVIRMaxSensorRate %5==0)):
                MyGUI.errorWindow(self)
            elif not ((10.0<=self.VVIRReactionTime<=50.0 and self.VVIRReactionTime%10==0)):
                MyGUI.errorWindow(self)
            elif not ((1.0<=self.VVIRResponseFactor<=16.0)):
                MyGUI.errorWindow(self)
            elif not ((2.0<=self.VVIRRecoveryTime<=16.0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.VVIR(self.VVIRLRLimit, self.VVIRURLimit, self.VVIRVentricularAmplitude, self.VVIRVentricularPulseWidth, self.VVIRVRP, self.VVIRMaxSensorRate, self.VVIRReactionTime, self.VVIRResponseFactor, self.VVIRRecoveryTime)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.successfulSubmitted(self,self.VVIRConfigWindow)
            
            self.conn = SerialComm.SerialComm()
            self.conn.connect()
            self.conn.serWriteAOO(7,self.currentUser)

            self.egramWindow = Egram.Egram(self.conn)
            self.egramWindow.run(self.VVIRConfigWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)
        
    def DDDConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.DDDConfigWindow = self.startWindow

        self.DDDConfigLabel=tk.Label(self.DDDConfigWindow, text="Configure Your DDD Parameters", font=("Arial",18), bg="azure2") #Gathers the necessary parameters to configure VOO from the user
        self.DDDConfigLabel.pack()
        self.DDDConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.DDDConfigWindow, text="Lower Rate Limit: ", font=("Arial", 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.DDDConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.DDDConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)
        
        self.URLimitLabel= tk.Label(self.DDDConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.DDDConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.DDDConfigWindow, text="Valid inputs are: values between 50-175 ppm\n incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.VentricularAmplitudeLabel= tk.Label(self.DDDConfigWindow, text="Ventricular Amplitude: ", font=("Arial",14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.VentricularAmplitudeTextField = tk.Entry(self.DDDConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.DDDConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.VentricularPulseWidthLabel= tk.Label(self.DDDConfigWindow, text="Ventricular Pulse Width: ", font=("Arial",14), bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.VentricularPulseWidthTextField = tk.Entry(self.DDDConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.DDDConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.AtrialAmplitudeLabel= tk.Label(self.DDDConfigWindow, text="Atrial Amplitude: ",font=("Arial",14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.55,rely=0.15)
        self.AtrialAmplitudeTextField = tk.Entry(self.DDDConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.825, rely=0.15)

        self.AtrialAmplitudeWarningLabel= tk.Label(self.DDDConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialAmplitudeWarningLabel.pack()
        self.AtrialAmplitudeWarningLabel.place(relx=0.55, rely=0.2)

        self.AtrialPulseWidthLabel= tk.Label(self.DDDConfigWindow, text="Atrial Pulse Width: ", font=("Arial",14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.55,rely=0.35)
        self.AtrialPulseWidthTextField = tk.Entry(self.DDDConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.825, rely=0.35)

        self.AtrialPulseWidthWarningLabel= tk.Label(self.DDDConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialPulseWidthWarningLabel.pack()
        self.AtrialPulseWidthWarningLabel.place(relx=0.55, rely=0.4)

        self.VRPLabel= tk.Label(self.DDDConfigWindow, text="VRP: ", font=("Arial",14), bg="azure2")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.55,rely=0.5)
        self.VRPTextField = tk.Entry(self.DDDConfigWindow)
        self.VRPTextField.pack()
        self.VRPTextField.place(relx=0.825, rely=0.5)

        self.VRPWarningLabel= tk.Label(self.DDDConfigWindow, text="Valid inputs are: values between\n 150-500 ms with 10 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VRPWarningLabel.pack()
        self.VRPWarningLabel.place(relx=0.55, rely=0.55)

        self.ARPLabel= tk.Label(self.DDDConfigWindow, text="ARP: ", font=("Arial", 14), bg="azure2")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.55,rely=0.65)
        self.ARPTextField = tk.Entry(self.DDDConfigWindow)
        self.ARPTextField.pack()
        self.ARPTextField.place(relx=0.825, rely=0.65)

        self.ARPWarningLabel= tk.Label(self.DDDConfigWindow, text="Valid inputs are: values between\n 150-500 ms with 10 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.ARPWarningLabel.pack()
        self.ARPWarningLabel.place(relx=0.55, rely=0.7)
        
        self.DDDButton = tk.Button(self.DDDConfigWindow, text = "Next", command=self.subConfigDDD1) #Submits parameters to the device
        self.DDDButton.pack()
        self.DDDButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def subConfigDDD1(self):
        self.DDDLRLimit= self.LRLimitTextField.get().strip()
        self.DDDURLimit= self.URLimitTextField.get().strip()
        self.DDDVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.DDDVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        self.DDDVRP= self.VRPTextField.get().strip()
        self.DDDAtrialAmplitude = self.AtrialAmplitudeTextField.get().strip()
        self.DDDAtrialPulseWidth = self.AtrialPulseWidthTextField.get().strip()
        self.DDDARP = self.ARPTextField.get().strip()
        try:
            if self.DDDVentricularAmplitude == "0":
                self.DDDVentricularAmplitude =  0
            else:
                self.DDDVentricularAmplitude= float(self.DDDVentricularAmplitude)

            if self.DDDAtrialAmplitude == "0":
                self.DDDAtrialAmplitude =0
            else:
                self.DDDAtrialAmplitude= float(self.DDDAtrialAmplitude) 

            self.DDDLRLimit= float(self.DDDLRLimit)
            self.DDDURLimit= float(self.DDDURLimit)
            self.DDDVentricularPulseWidth= float(self.DDDVentricularPulseWidth)
            self.DDDVRP= float(self.DDDVRP)
            self.DDDAtrialPulseWidth = float(self.DDDAtrialPulseWidth)
            self.DDDARP = float(self.DDDARP)

            if not ((30<= self.DDDLRLimit<=50 and self.DDDLRLimit % 5 == 0) or (50<= self.DDDLRLimit<=90) or  (90 <= self.DDDLRLimit <= 175 and self.DDDLRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.DDDURLimit<=175 and self.DDDURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not  ((0.1 <= self.DDDVentricularAmplitude <= 5.0 and self.DDDVentricularAmplitude*10 %1==0) or (self.DDDVentricularAmplitude ==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.DDDVentricularPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((150<= self.DDDVRP<=500 and self.DDDVRP % 10 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDAtrialAmplitude==0) or (0.1 <= self.DDDAtrialAmplitude <= 5.0 and self.DDDAtrialAmplitude*10 %1==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.DDDAtrialPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((150<= self.DDDARP<=500 and self.DDDARP % 10 == 0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.DDD(self.DDDLRLimit, self.DDDURLimit, self.DDDVentricularAmplitude, self.DDDVentricularPulseWidth, self.DDDVRP, self.DDDAtrialAmplitude, self.DDDAtrialPulseWidth, self.DDDARP, 0,0,0,0,0,0)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.nextConfigDDD(self)
        except ValueError as error:
            MyGUI.valueErrorWindow(self)

    def nextConfigDDD(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.nextConfigDDDWindow = self.startWindow

        self.DDDConfigLabel=tk.Label(self.nextConfigDDDWindow, text="Configure Your DDD Parameters", font=("Arial",18), bg="azure2") #Gathers the necessary parameters to configure VOO from the user
        self.DDDConfigLabel.pack()
        self.DDDConfigLabel.place(relx=0.3,rely=0.05)

        self.FixedAVDelayLabel=tk.Label(self.nextConfigDDDWindow, text="Fixed AV Delay: ", font=("Arial",14), bg="azure2")
        self.FixedAVDelayLabel.pack()
        self.FixedAVDelayLabel.place(relx=0.045, rely=0.15)
        self.FixedAVDelayTextField=tk.Entry(self.nextConfigDDDWindow)
        self.FixedAVDelayTextField.pack()
        self.FixedAVDelayTextField.place(relx=0.325, rely=0.15)

        self.FixedAVDelayWarningLabel=tk.Label(self.nextConfigDDDWindow, text="Valid inputs are: values between 70-300 ms\n incremented by 10 ms", font=("Arial",12), fg="blue", bg="azure2")
        self.FixedAVDelayWarningLabel.pack()
        self.FixedAVDelayWarningLabel.place(relx=0.045,rely=0.2)

        self.DynamicAVDelayLabel=tk.Label(self.nextConfigDDDWindow, text="Dynamic AV Delay: ", font=("Arial", 14), bg="azure2")
        self.DynamicAVDelayLabel.pack()
        self.DynamicAVDelayLabel.place(relx=0.045, rely=0.35)
        self.DynamicAVDelayTextField= tk.Entry(self.nextConfigDDDWindow)
        self.DynamicAVDelayTextField.pack()
        self.DynamicAVDelayTextField.place(relx=0.325, rely=0.35)

        self.DynamicAVDelayWarningLabel=tk.Label(self.nextConfigDDDWindow, text="Valid inputs are: Off or On", font=("Arial", 12), fg="blue", bg="azure2")
        self.DynamicAVDelayWarningLabel.pack()
        self.DynamicAVDelayWarningLabel.place(relx=0.045, rely=0.4)

        self.SensedAVDelayLabel=tk.Label(self.nextConfigDDDWindow, text="Sensed AV Delay Offset: ", font=("Arial",14), bg="azure2")
        self.SensedAVDelayLabel.pack()
        self.SensedAVDelayLabel.place(relx=0.045, rely=0.5)
        self.SensedAVDelayTextField=tk.Entry(self.nextConfigDDDWindow)
        self.SensedAVDelayTextField.pack()
        self.SensedAVDelayTextField.place(relx=0.325, rely=0.5)

        self.SensedAVDelayWarningLabel=tk.Label(self.nextConfigDDDWindow, text="Valid inputs are: Off, values between\n -10 to -100 ms incremented by -10 ms",font=("Arial",12), fg="blue", bg="azure2")
        self.SensedAVDelayWarningLabel.pack()
        self.SensedAVDelayWarningLabel.place(relx=0.045, rely=0.55)

        self.ATRModeLabel=tk.Label(self.nextConfigDDDWindow, text="ATR Fallback Mode: ", fon=("Arial", 14), bg="azure2")
        self.ATRModeLabel.pack()
        self.ATRModeLabel.place(relx=0.55, rely=0.15)
        self.ATRModeTextField=tk.Entry(self.nextConfigDDDWindow)
        self.ATRModeTextField.pack()
        self.ATRModeTextField.place(relx=0.825, rely=0.15)

        self.ATRModeWarningLabel=tk.Label(self.nextConfigDDDWindow, text="Valid inputs are: Off or On", font=("Arial",12), fg="blue", bg="azure2")
        self.ATRModeWarningLabel.pack()
        self.ATRModeWarningLabel.place(relx=0.55, rely=0.2)

        self.ATRDurationLabel=tk.Label(self.nextConfigDDDWindow, text="ATR Duration: ", font=("Arial", 14), bg="azure2")
        self.ATRDurationLabel.pack()
        self.ATRDurationLabel.place(relx=0.55, rely=0.35)
        self.ATRDurationTextField=tk.Entry(self.nextConfigDDDWindow)
        self.ATRDurationTextField.pack()
        self.ATRDurationTextField.place(relx=0.825, rely=0.35)

        self.ATRDurationWarningLabel=tk.Label(self.nextConfigDDDWindow, text="Valid inputs are: 10 cc, values between\n 20-80 cc incremented by 20 cc, values between\n 100-2000 cc incremented by 100 cc", font=("Arial", 12), fg="blue", bg="azure2")
        self.ATRDurationWarningLabel.pack()
        self.ATRDurationWarningLabel.place(relx=0.55, rely=0.4)

        self.ATRFallbackTimeLabel=tk.Label(self.nextConfigDDDWindow, text="ATR Fallback Time: ", font=("Arial", 14), bg="azure2")
        self.ATRFallbackTimeLabel.pack()
        self.ATRFallbackTimeLabel.place(relx=0.55, rely= 0.5)
        self.ATRFallbackTimeTextField=tk.Entry(self.nextConfigDDDWindow)
        self.ATRFallbackTimeTextField.pack()
        self.ATRFallbackTimeTextField.place(relx=0.825, rely=0.5)

        self.ATRFallbackTimeWarningLabel=tk.Label(self.nextConfigDDDWindow, text="Valid inputs are: 1-5 min incremented by 1 min", font=("Arial", 12), fg="blue", bg="azure2")
        self.ATRFallbackTimeWarningLabel.pack()
        self.ATRFallbackTimeWarningLabel.place(relx=0.55, rely=0.55)

        self.nextConfigDDDButton = tk.Button(self.nextConfigDDDWindow, text = "Submit", command=self.submitDDD) #Submits parameters to the device
        self.nextConfigDDDButton.pack()
        self.nextConfigDDDButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDDD(self):
        self.DDDFixedAV = self.FixedAVDelayTextField.get().strip()
        self.DDDDynamicAV= self.DynamicAVDelayTextField.get().strip()
        self.DDDSensedAV = self.SensedAVDelayTextField.get().strip()
        self.DDDATRDuration = self.ATRDurationTextField.get().strip()
        self.DDDATRFallbackMode = self.ATRModeTextField.get().strip()
        self.DDDATRFallbackTime = self.ATRFallbackTimeTextField.get().strip()
        
        #Checks to make sure the values inputted are valid
        try:
            if self.DDDDynamicAV == "Off" or self.DDDDynamicAV=="off":
                self.DDDDynamicAV = 0
            elif self.DDDDynamicAV == "On" or self.DDDDynamicAV=="on":
                self.DDDDynamicAV = 1
            else:
                self.DDDDynamicAV=50

            if self.DDDATRFallbackMode == "Off" or self.DDDATRFallbackMode == "off":
                self.DDDATRFallbackMode = 0
            elif self.DDDATRFallbackMode == "On" or self.DDDATRFallbackMode == "on":
                self.DDDATRFallbackMode = 1
            else:
                self.DDDATRFallbackMode=50

            if self.DDDSensedAV == "Off" or self.DDDSensedAV == "off":
                self.DDDSensedAV = 0
            else:
                self.DDDSensedAV= float(self.DDDSensedAV)

    
            self.DDDFixedAV = float(self.DDDFixedAV)
            self.DDDATRDuration = float(self.DDDATRDuration)
            self.DDDATRFallbackTime = float(self.DDDATRFallbackTime)
            
            if not ((70<= self.DDDFixedAV <=300 and self.DDDFixedAV % 10 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDDynamicAV == 0) or (self.DDDDynamicAV == 1)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDSensedAV == 0) or (-100<=self.DDDSensedAV<=-10 and self.DDDSensedAV % 10 ==0)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDATRFallbackMode == 0) or (self.DDDATRFallbackMode == 1)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDATRDuration == 10) or (20<=self.DDDATRDuration<=80 and self.DDDATRDuration % 20 ==0) or (100<=self.DDDATRDuration<=2000 and self.DDDATRDuration % 100 ==0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.DDD(self.DDDLRLimit, self.DDDURLimit, self.DDDVentricularAmplitude, self.DDDVentricularPulseWidth, self.DDDVRP, self.DDDAtrialAmplitude, self.DDDAtrialPulseWidth, self.DDDARP, self.DDDFixedAV, self.DDDDynamicAV, self.DDDSensedAV, self.DDDATRFallbackMode, self.DDDATRDuration, self.DDDATRFallbackTime)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.successfulSubmitted(self,self.nextConfigDDDWindow)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)

    def DDDRConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.DDDRConfigWindow = self.startWindow

        self.DDDRConfigLabel=tk.Label(self.DDDRConfigWindow, text="Configure Your DDDR Parameters", font=("Arial",18), bg="azure2") #Gathers the necessary parameters to configure VOO from the user
        self.DDDRConfigLabel.pack()
        self.DDDRConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.DDDRConfigWindow, text="Lower Rate Limit: ", font=("Arial", 14), bg="azure2")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.045,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.DDDRConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.325, rely=0.15)
        
        self.LRLimitWarningLabel= tk.Label(self.DDDRConfigWindow, text="Valid inputs are: values between 30-50 ppm\n incremented by 5 ppm, values between\n 50-90 ppm incremented by 1 ppm, values\n between 90-175 ppm incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.045, rely=0.2)
        
        self.URLimitLabel= tk.Label(self.DDDRConfigWindow, text="Upper Rate Limit: ", font=("Arial",14), bg="azure2")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.045,rely=0.35)
        self.URLimitTextField = tk.Entry(self.DDDRConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.325, rely=0.35)
        
        self.URLimitWarningLabel= tk.Label(self.DDDRConfigWindow, text="Valid inputs are: values between 50-175 ppm\n incremented by 5 ppm",font=('Arial', 12), fg="blue", bg="azure2" )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.045, rely=0.4)

        self.VentricularAmplitudeLabel= tk.Label(self.DDDRConfigWindow, text="Ventricular Amplitude: ", font=("Arial",14), bg="azure2")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.045,rely=0.5)
        self.VentricularAmplitudeTextField = tk.Entry(self.DDDRConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.325, rely=0.5)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.DDDRConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.045, rely=0.55)

        self.VentricularPulseWidthLabel= tk.Label(self.DDDRConfigWindow, text="Ventricular Pulse Width: ", font=("Arial",14), bg="azure2")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.045,rely=0.65)
        self.VentricularPulseWidthTextField = tk.Entry(self.DDDRConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.325, rely=0.65)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.DDDRConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.045, rely=0.7)

        self.AtrialAmplitudeLabel= tk.Label(self.DDDRConfigWindow, text="Atrial Amplitude: ",font=("Arial",14), bg="azure2")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.55,rely=0.15)
        self.AtrialAmplitudeTextField = tk.Entry(self.DDDRConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.825, rely=0.15)

        self.AtrialAmplitudeWarningLabel= tk.Label(self.DDDRConfigWindow, text="Valid inputs are: 0 or between\n 0.1-5.0 V with 0.1 V increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialAmplitudeWarningLabel.pack()
        self.AtrialAmplitudeWarningLabel.place(relx=0.55, rely=0.2)

        self.AtrialPulseWidthLabel= tk.Label(self.DDDRConfigWindow, text="Atrial Pulse Width: ", font=("Arial",14), bg="azure2")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.55,rely=0.35)
        self.AtrialPulseWidthTextField = tk.Entry(self.DDDRConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.825, rely=0.35)

        self.AtrialPulseWidthWarningLabel= tk.Label(self.DDDRConfigWindow, text="Valid inputs are: values between\n 1-30 ms with 1 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.AtrialPulseWidthWarningLabel.pack()
        self.AtrialPulseWidthWarningLabel.place(relx=0.55, rely=0.4)

        self.VRPLabel= tk.Label(self.DDDRConfigWindow, text="VRP: ", font=("Arial",14), bg="azure2")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.55,rely=0.5)
        self.VRPTextField = tk.Entry(self.DDDRConfigWindow)
        self.VRPTextField.pack()
        self.VRPTextField.place(relx=0.825, rely=0.5)

        self.VRPWarningLabel= tk.Label(self.DDDRConfigWindow, text="Valid inputs are: values between\n 150-500 ms with 10 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.VRPWarningLabel.pack()
        self.VRPWarningLabel.place(relx=0.55, rely=0.55)

        self.ARPLabel= tk.Label(self.DDDRConfigWindow, text="ARP: ", font=("Arial", 14), bg="azure2")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.55,rely=0.65)
        self.ARPTextField = tk.Entry(self.DDDRConfigWindow)
        self.ARPTextField.pack()
        self.ARPTextField.place(relx=0.825, rely=0.65)

        self.ARPWarningLabel= tk.Label(self.DDDRConfigWindow, text="Valid inputs are: values between\n 150-500 ms with 10 ms increment",font=('Arial', 12), fg="blue", bg="azure2" )
        self.ARPWarningLabel.pack()
        self.ARPWarningLabel.place(relx=0.55, rely=0.7)

        self.DDDRButton = tk.Button(self.DDDRConfigWindow, text = "Next", command=self.subConfigDDDR1) #Submits parameters to the device
        self.DDDRButton.pack()
        self.DDDRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def subConfigDDDR1(self):
        self.DDDRLRLimit= self.LRLimitTextField.get().strip()
        self.DDDRURLimit= self.URLimitTextField.get().strip()
        self.DDDRVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.DDDRVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        self.DDDRVRP= self.VRPTextField.get().strip()
        self.DDDRAtrialAmplitude = self.AtrialAmplitudeTextField.get().strip()
        self.DDDRAtrialPulseWidth = self.AtrialPulseWidthTextField.get().strip()
        self.DDDRARP = self.ARPTextField.get().strip()

        try:
            if self.DDDRVentricularAmplitude == "0":
                self.DDDRVentricularAmplitude =  0
            else:
                self.DDDRVentricularAmplitude= float(self.DDDRVentricularAmplitude)

            if self.DDDRAtrialAmplitude == "0":
                self.DDDRAtrialAmplitude=0
            else:
                self.DDDRAtrialAmplitude=float(self.DDDRAtrialAmplitude)
            
            self.DDDRLRLimit= float(self.DDDRLRLimit)
            self.DDDRURLimit= float(self.DDDRURLimit)
            self.DDDRVentricularPulseWidth= float(self.DDDRVentricularPulseWidth)
            self.DDDRVRP= float(self.DDDRVRP)
            self.DDDRAtrialPulseWidth = float(self.DDDRAtrialPulseWidth)
            self.DDDRARP = float(self.DDDRARP)
        
            if not ((30<= self.DDDRLRLimit<=50 and self.DDDRLRLimit % 5 == 0) or (50<= self.DDDRLRLimit<=90) or  (90 <= self.DDDRLRLimit <= 175 and self.DDDRLRLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not ((50<= self.DDDRURLimit<=175 and self.DDDRURLimit % 5 == 0)):
                MyGUI.errorWindow(self)
            elif not  ((0.1 <= self.DDDRVentricularAmplitude <= 5.0 and self.DDDRVentricularAmplitude*10 %1==0) or (self.DDDRVentricularAmplitude ==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.DDDRVentricularPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((150<= self.DDDRVRP<=500 and self.DDDRVRP % 10 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDRAtrialAmplitude==0) or (0.1 <= self.DDDRAtrialAmplitude <= 5.0 and self.DDDRAtrialAmplitude*10 %1==0)): 
                MyGUI.errorWindow(self)
            elif not ((1.0<= self.DDDRAtrialPulseWidth <= 30.0)):
                MyGUI.errorWindow(self)
            elif not ((150<= self.DDDRARP<=500 and self.DDDRARP % 10 == 0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.DDDR(self.DDDRLRLimit, self.DDDRURLimit, self.DDDRVentricularAmplitude, self.DDDRVentricularPulseWidth, self.DDDRVRP, self.DDDRAtrialAmplitude, self.DDDRAtrialPulseWidth, self.DDDRARP, 0,0,0,0,0,0,0,0,0,0)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.nextConfigDDDR(self)
        except (ValueError,TypeError) as error:
                MyGUI.valueErrorWindow(self)
    
    def nextConfigDDDR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.nextConfigDDDRWindow = self.startWindow

        self.DDDRConfigLabel=tk.Label(self.nextConfigDDDRWindow, text="Configure Your DDDR Parameters", font=("Arial",18), bg="azure2") #Gathers the necessary parameters to configure VOO from the user
        self.DDDRConfigLabel.pack()
        self.DDDRConfigLabel.place(relx=0.3,rely=0.05)

        self.FixedAVDelayLabel=tk.Label(self.nextConfigDDDRWindow, text="Fixed AV Delay: ", font=("Arial",14), bg="azure2")
        self.FixedAVDelayLabel.pack()
        self.FixedAVDelayLabel.place(relx=0.045, rely=0.15)
        self.FixedAVDelayTextField=tk.Entry(self.nextConfigDDDRWindow)
        self.FixedAVDelayTextField.pack()
        self.FixedAVDelayTextField.place(relx=0.325, rely=0.15)

        self.FixedAVDelayWarningLabel=tk.Label(self.nextConfigDDDRWindow, text="Valid inputs are: values between 70-300 ms\n incremented by 10 ms", font=("Arial",12), fg="blue", bg="azure2")
        self.FixedAVDelayWarningLabel.pack()
        self.FixedAVDelayWarningLabel.place(relx=0.045,rely=0.2)

        self.DynamicAVDelayLabel=tk.Label(self.nextConfigDDDRWindow, text="Dynamic AV Delay: ", font=("Arial", 14), bg="azure2")
        self.DynamicAVDelayLabel.pack()
        self.DynamicAVDelayLabel.place(relx=0.045, rely=0.35)
        self.DynamicAVDelayTextField= tk.Entry(self.nextConfigDDDRWindow)
        self.DynamicAVDelayTextField.pack()
        self.DynamicAVDelayTextField.place(relx=0.325, rely=0.35)

        self.DynamicAVDelayWarningLabel=tk.Label(self.nextConfigDDDRWindow, text="Valid inputs are: Off or On", font=("Arial", 12), fg="blue", bg="azure2")
        self.DynamicAVDelayWarningLabel.pack()
        self.DynamicAVDelayWarningLabel.place(relx=0.045, rely=0.4)

        self.SensedAVDelayLabel=tk.Label(self.nextConfigDDDRWindow, text="Sensed AV Delay Offset: ", font=("Arial",14), bg="azure2")
        self.SensedAVDelayLabel.pack()
        self.SensedAVDelayLabel.place(relx=0.045, rely=0.5)
        self.SensedAVDelayTextField=tk.Entry(self.nextConfigDDDRWindow)
        self.SensedAVDelayTextField.pack()
        self.SensedAVDelayTextField.place(relx=0.325, rely=0.5)

        self.SensedAVDelayWarningLabel=tk.Label(self.nextConfigDDDRWindow, text="Valid inputs are: Off, values between\n -10 to -100 ms incremented by -10 ms",font=("Arial",12), fg="blue", bg="azure2")
        self.SensedAVDelayWarningLabel.pack()
        self.SensedAVDelayWarningLabel.place(relx=0.045, rely=0.55)

        self.ATRModeLabel=tk.Label(self.nextConfigDDDRWindow, text="ATR Fallback Mode: ", fon=("Arial", 14), bg="azure2")
        self.ATRModeLabel.pack()
        self.ATRModeLabel.place(relx=0.55, rely=0.15)
        self.ATRModeTextField=tk.Entry(self.nextConfigDDDRWindow)
        self.ATRModeTextField.pack()
        self.ATRModeTextField.place(relx=0.825, rely=0.15)

        self.ATRModeWarningLabel=tk.Label(self.nextConfigDDDRWindow, text="Valid inputs are: Off or On", font=("Arial",12), fg="blue", bg="azure2")
        self.ATRModeWarningLabel.pack()
        self.ATRModeWarningLabel.place(relx=0.55, rely=0.2)

        self.ATRDurationLabel=tk.Label(self.nextConfigDDDRWindow, text="ATR Duration: ", font=("Arial", 14), bg="azure2")
        self.ATRDurationLabel.pack()
        self.ATRDurationLabel.place(relx=0.55, rely=0.35)
        self.ATRDurationTextField=tk.Entry(self.nextConfigDDDRWindow)
        self.ATRDurationTextField.pack()
        self.ATRDurationTextField.place(relx=0.825, rely=0.35)

        self.ATRDurationWarningLabel=tk.Label(self.nextConfigDDDRWindow, text="Valid inputs are: 10 cc, values between\n 20-80 cc incremented by 20 cc, values between\n 100-2000 cc incremented by 100 cc", font=("Arial", 12), fg="blue", bg="azure2")
        self.ATRDurationWarningLabel.pack()
        self.ATRDurationWarningLabel.place(relx=0.55, rely=0.4)

        self.ATRFallbackTimeLabel=tk.Label(self.nextConfigDDDRWindow, text="ATR Fallback Time: ", font=("Arial", 14), bg="azure2")
        self.ATRFallbackTimeLabel.pack()
        self.ATRFallbackTimeLabel.place(relx=0.55, rely= 0.5)
        self.ATRFallbackTimeTextField=tk.Entry(self.nextConfigDDDRWindow)
        self.ATRFallbackTimeTextField.pack()
        self.ATRFallbackTimeTextField.place(relx=0.825, rely=0.5)

        self.ATRFallbackTimeWarningLabel=tk.Label(self.nextConfigDDDRWindow, text="Valid inputs are: 1-5 min incremented by 1 min", font=("Arial", 12), fg="blue", bg="azure2")
        self.ATRFallbackTimeWarningLabel.pack()
        self.ATRFallbackTimeWarningLabel.place(relx=0.55, rely=0.55)

        self.nextConfigDDDRButton = tk.Button(self.nextConfigDDDRWindow, text = "Next", command=self.subConfigDDDR2) #Submits parameters to the device
        self.nextConfigDDDRButton.pack()
        self.nextConfigDDDRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def subConfigDDDR2(self):
        self.DDDRFixedAV = self.FixedAVDelayTextField.get().strip()
        self.DDDRDynamicAV= self.DynamicAVDelayTextField.get().strip()
        self.DDDRSensedAV = self.SensedAVDelayTextField.get().strip()
        self.DDDRATRDuration = self.ATRDurationTextField.get().strip()
        self.DDDRATRFallbackMode = self.ATRModeTextField.get().strip()
        self.DDDRATRFallbackTime = self.ATRFallbackTimeTextField.get().strip()
        
        #Checks to make sure the values inputted are valid
        try:
            if self.DDDRDynamicAV == "Off" or self.DDDRDynamicAV== "off":
                self.DDDRDynamicAV = 0
            elif self.DDDRDynamicAV == "On" or self.DDDRDynamicAV== "on":
                self.DDDRDynamicAV = 1
            else:
                self.DDDRDynamicAV=50

            if self.DDDRATRFallbackMode == "Off" or self.DDDRATRFallbackMode == "off":
                self.DDDRATRFallbackMode = 0
            elif self.DDDRATRFallbackMode == "On" or self.DDDRATRFallbackMode == "on":
                self.DDDRATRFallbackMode = 1
            else:
                self.DDDRATRFallbackMode=50

            if self.DDDRSensedAV == "Off" or self.DDDRSensedAV=="off":
                self.DDDRSensedAV = 0
            else:
                self.DDDRSensedAV= float(self.DDDRSensedAV)
    
            self.DDDRFixedAV = float(self.DDDRFixedAV)
            self.DDDRATRDuration = float(self.DDDRATRDuration)
            self.DDDRATRFallbackTime = float(self.DDDRATRFallbackTime)

            if not ((70<= self.DDDRFixedAV <=300 and self.DDDRFixedAV % 10 == 0)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDRDynamicAV == 0) or (self.DDDRDynamicAV == 1)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDRSensedAV == 0) or (-100<=self.DDDRSensedAV<=-10 and self.DDDRSensedAV % 10 ==0)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDRATRFallbackMode == 0) or (self.DDDRATRFallbackMode == 1)):
                MyGUI.errorWindow(self)
            elif not ((self.DDDRATRDuration == 10) or (20<=self.DDDRATRDuration<=80 and self.DDDRATRDuration % 20 ==0) or (100<=self.DDDRATRDuration<=2000 and self.DDDRATRDuration % 100 ==0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.DDDR(self.DDDRLRLimit, self.DDDRURLimit, self.DDDRVentricularAmplitude, self.DDDRVentricularPulseWidth, self.DDDRVRP, self.DDDRAtrialAmplitude, self.DDDRAtrialPulseWidth, self.DDDRARP, self.DDDRFixedAV, self.DDDRDynamicAV, self.DDDRSensedAV, self.DDDRATRFallbackMode, self.DDDRATRDuration, self.DDDRATRFallbackTime,0,0,0,0)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.nextConfigDDDR2(self)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)

    def nextConfigDDDR2(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.nextConfigDDDR2Window = self.startWindow

        self.DDDRConfigLabel=tk.Label(self.nextConfigDDDR2Window, text="Configure Your DDDR Parameters", font=("Arial",18), bg="azure2") #Gathers the necessary parameters to configure VOO from the user
        self.DDDRConfigLabel.pack()
        self.DDDRConfigLabel.place(relx=0.3,rely=0.05)

        self.MaximumSensorRateLabel=tk.Label(self.nextConfigDDDR2Window, text="Maximum Sensor Rate: ", font=("Arial",14), bg="azure2")
        self.MaximumSensorRateLabel.pack()
        self.MaximumSensorRateLabel.place(relx=0.045, rely=0.15)
        self.MaximumSensorRateTextField=tk.Entry(self.nextConfigDDDR2Window)
        self.MaximumSensorRateTextField.pack()
        self.MaximumSensorRateTextField.place(relx=0.325, rely=0.15)

        self.MaximumSensorRateWarningLabel=tk.Label(self.nextConfigDDDR2Window, text="Valid inputs are: values between\n 50-175 ppm with 5 ppm increment", font=("Arial",12), fg="blue", bg="azure2")
        self.MaximumSensorRateWarningLabel.pack()
        self.MaximumSensorRateWarningLabel.place(relx=0.045, rely=0.2)

        self.ReactionTimeLabel=tk.Label(self.nextConfigDDDR2Window, text="Reaction Time: ", font=("Arial",14), bg="azure2")
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.045, rely=0.35)
        self.ReactionTimeTextField=tk.Entry(self.nextConfigDDDR2Window)
        self.ReactionTimeTextField.pack()
        self.ReactionTimeTextField.place(relx=0.325,rely=0.35)

        self.ReactionTimeWarningLabel=tk.Label(self.nextConfigDDDR2Window,text="Valid input are: values between\n 10-50 sec with a 10 sec increment", font=("Arial",12), fg="blue", bg="azure2")
        self.ReactionTimeWarningLabel.pack()
        self.ReactionTimeWarningLabel.place(relx=0.045,rely=0.4)

        self.ResponseFactorLabel=tk.Label(self.nextConfigDDDR2Window, text="Response Factor: ", font=("Arial",14), bg="azure2")
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.045,rely=0.5)
        self.ResponseFactorTextField=tk.Entry(self.nextConfigDDDR2Window)
        self.ResponseFactorTextField.pack()
        self.ResponseFactorTextField.place(relx=0.325, rely=0.5)

        self.ResponseFactorWarningLabel=tk.Label(self.nextConfigDDDR2Window, text="Valid inputs are: values between\n 1-16 with an increment of 1", font=("Arial",12), fg="blue", bg="azure2")
        self.ResponseFactorWarningLabel.pack()
        self.ResponseFactorWarningLabel.place(relx=0.045,rely=0.55)

        self.RecoveryTimeLabel=tk.Label(self.nextConfigDDDR2Window, text="Recovery Time: ", font=("Arial",14), bg="azure2")
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.045, rely=0.65)
        self.RecoveryTimeTextField=tk.Entry(self.nextConfigDDDR2Window)
        self.RecoveryTimeTextField.pack()
        self.RecoveryTimeTextField.place(relx=0.325,rely=0.65)

        self.RecoveryTimeWarningLabel=tk.Label(self.nextConfigDDDR2Window, text="Valid inputs are: values between\n 2-16 min with a 1 min increment", font=("Arial",12), fg="blue", bg="azure2")
        self.RecoveryTimeWarningLabel.pack()
        self.RecoveryTimeWarningLabel.place(relx=0.045,rely=0.7)

        self.nextConfigDDDRButton = tk.Button(self.nextConfigDDDRWindow, text = "Submit", command=self.submitConfigDDDR) #Submits parameters to the device
        self.nextConfigDDDRButton.pack()
        self.nextConfigDDDRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitConfigDDDR(self):
        self.DDDRMaxSensorRate= self.MaximumSensorRateTextField.get().strip()
        self.DDDRReactionTime= self.ReactionTimeTextField.get().strip()
        self.DDDRRecoveryTime= self.RecoveryTimeTextField.get().strip()
        self.DDDRResponseFactor= self.ResponseFactorTextField.get().strip()

        try:
            self.DDDRMaxSensorRate= float(self.DDDRMaxSensorRate)
            self.DDDRRecoveryTime= float(self.DDDRRecoveryTime)
            self.DDDRResponseFactor= float(self.DDDRResponseFactor)
            self.DDDRReactionTime= float(self.DDDRReactionTime)
        
            if not ((50.0<=self.DDDRMaxSensorRate<=175.0 and self.DDDRMaxSensorRate %5==0)):
                MyGUI.errorWindow(self)
            elif not ((10.0<=self.DDDRReactionTime<=50.0 and self.DDDRReactionTime%10==0)):
                MyGUI.errorWindow(self)
            elif not ((1.0<=self.DDDRResponseFactor<=16.0)):
                MyGUI.errorWindow(self)
            elif not ((2.0<=self.DDDRRecoveryTime<=16.0)):
                MyGUI.errorWindow(self)
            else:
                self.currentUser.DDDR(self.DDDRLRLimit, self.DDDRURLimit, self.DDDRVentricularAmplitude, self.DDDRVentricularPulseWidth, self.DDDRVRP, self.DDDRAtrialAmplitude, self.DDDRAtrialPulseWidth, self.DDDRARP, self.DDDRFixedAV, self.DDDRDynamicAV, self.DDDRSensedAV, self.DDDRATRFallbackMode, self.DDDRATRDuration, self.DDDRATRFallbackTime,self.DDDRMaxSensorRate, self.DDDRReactionTime, self.DDDRRecoveryTime, self.DDDRResponseFactor)
                self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
                MyGUI.successfulSubmitted(self,self.nextConfigDDDR2Window)
        except (ValueError,TypeError) as error:
            MyGUI.valueErrorWindow(self)
        
    def deleteUser(self):

        shift = 3  # Use the same shift value used for encryption in the database
        encrypted_inputName = self.db.caesar_cipher_encrypt(self.currentUser.username, shift)
       

        self.db.delete_user(encrypted_inputName)#Deletes user that is currently signed in from the database
        
        print("User successfully deleted!")  
        
        self.startWindow.destroy()
        self.__init__() #Calls the constructor
    
    

    def errorWindow(self):
        self.errorScreen = tk.Toplevel(self.configModeWindow)#Displays when the values inputted by the user are invalid
        self.errorScreen.geometry("200x100")
        self.errorScreenLabel = tk.Label(self.errorScreen, text = "Values Entered Are Not in Range", fg="red")
        self.errorScreenLabel.pack()

    def valueErrorWindow(self):
        self.errorScreen = tk.Toplevel(self.configModeWindow)#Displays when the values inputted by the user are invalid
        self.errorScreen.geometry("300x100")
        self.errorScreenLabel = tk.Label(self.errorScreen, text = "Values Entered Are Not A Float or An Integer", fg="red")
        self.errorScreenLabel.pack()

    def successfulSubmitted(self,window):
        self.errorScreen = tk.Toplevel(window)#Generates when the user successfully submits their pacing mode to their device
        self.errorScreen.geometry("200x100")
        self.errorScreenLabel = tk.Label(self.errorScreen, text = "Submitted", fg="red")
        self.errorScreenLabel.pack()

    def clearScreen(self,window):
        for widget in window.winfo_children():
            widget.destroy()

        

MyGUI()
