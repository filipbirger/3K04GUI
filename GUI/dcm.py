import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import userClass
import sqlite3
from DataBase import DataBase

class MyGUI:

    def __init__(self): #constructor
        
        self.db = DataBase()

        self.startWindow = ThemedTk(theme="yaru") #Generates initial login screen
        self.startWindow.geometry("800x800")
        self.startWindow.title("3K04 Pacemaker")

        self.connceted = True#verifies device is connected
        self.deviceId = 2 #gives device an identification number

        self.startTitle = tk.Label(self.startWindow, text="Pacemaker", font=('Arial', 24))
        self.startTitle.place(relx=0.4, rely=0.1)
        if (self.connceted == True):
            self.newUserButton = tk.Button(self.startWindow, text="New User", command=self.createNewUser) #Functionality to create New User
            self.newUserButton.place(relx=0.6, rely=0.2, relheight=0.1, relwidth=0.2)
            self.newUserLabel=tk.Label(self.startWindow, text="Click 'New User' to set up your\n profile and start\n configuring your pacemaker", font=("Arial",8))
            self.newUserLabel.pack()
            self.newUserLabel.place(relx=0.6, rely=0.3)
            self.signInButton = tk.Button(self.startWindow, text="Sign In", command=self.createLoginWindow) #Functionality to Sign In
            self.signInButton.place(relx=0.2, rely=0.2, relheight=0.1, relwidth=0.2)
            self.signInLabel=tk.Label(self.startWindow, text="Click 'Sign in' if you are\n an existing user", font=("Arial",8))
            self.signInLabel.pack()
            self.signInLabel.place(relx=0.22, rely=0.3)

            self.aboutButton = tk.Button (self.startWindow, text="About", command=self.aboutDevice) #Provides ‘About’ information 
            self.aboutButton.place(relx=0.4, rely=0.6, relheight=0.1, relwidth=0.2)
            self.aboutLabel=tk.Label(self.startWindow, text="Click 'About' for more\n information about your pacemaker", font=("Arial",8))
            self.aboutLabel.pack()
            self.aboutLabel.place(relx=0.385,rely=0.7)
        else:
            self.notConnectedLabel = tk.Label(self.startWindow, text="No Device In Range", font=('Arial', 24)) #Checks if device is not connected
            self.notConnectedLabel.pack()
        self.startWindow.mainloop()

    def createNewUser(self):
        self.newUserWindow = tk.Toplevel(self.startWindow)#Called when New User button is clicked
        self.newUserWindow.geometry("300x200")
        self.newUserWindow.title("Create New User")

        self.userNameLabel = tk.Label(self.newUserWindow, text="Username:")#Gathers Username from the New User
        self.userNameLabel.pack()
        self.userNameTextField = tk.Entry(self.newUserWindow)
        self.userNameTextField.pack()

        self.userPasswordLabel = tk.Label(self.newUserWindow, text="Password:")#Gathers Password from the New User
        self.userPasswordLabel.pack()
        self.userPasswordTextField = tk.Entry(self.newUserWindow, show="*") #Hides password characters
        self.userPasswordTextField.pack()

        self.enterButton = tk.Button(self.newUserWindow, text="Submit", command=self.populateUserInfo) 
        self.enterButton.pack()
        
    def populateUserInfo(self):
        allUsersSize = self.db.getAllUsers()#Gathers number of current users from the database and checks if there are less than 10
        if len(allUsersSize)>=10: #If there are currently more than 10 users, it prohibits the new user from signing up
            self.maxUserReachedText = tk.Label(self.newUserWindow, text="Error: Maximum number of users reached!", fg="red")
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
        self.applicationModelNumberLabel = tk.Label(self.aboutWindow, text="Application model number: 7", font=('Arial', 12)) #Displays the device’s information
        self.applicationModelNumberLabel.pack(padx=0.1)
        self.revisionNumberLabel = tk.Label(self.aboutWindow, text="Revision Number: 1.3", font=('Arial', 12))
        self.revisionNumberLabel.pack(padx=0.1)
        self.DCMNumberLabel = tk.Label(self.aboutWindow, text="DCM serial number: 1", font=('Arial', 12))
        self.DCMNumberLabel.pack(padx=0.1)
        self.instituteNameLabel = tk.Label(self.aboutWindow, text="Institution name: McMaster U", font=('Arial', 12))
        self.instituteNameLabel.pack(padx=0.1)

    def createLoginWindow(self):
        self.loginWindow = tk.Toplevel(self.startWindow)#Generates when ‘Sign In’ is clicked
        self.loginWindow.geometry("300x200")
        self.loginWindow.title("Login")

        self.loginNameLabel = tk.Label(self.loginWindow, text="Username:")#Prompts user to sign in with their Username 
        self.loginNameLabel.pack()
        self.loginNameTextField = tk.Entry(self.loginWindow)
        self.loginNameTextField.pack()

        self.loginPasswordLabel = tk.Label(self.loginWindow, text="Password:")#Prompts user to sign in with their password
        self.loginPasswordLabel.pack()
        self.loginPasswordTextField = tk.Entry(self.loginWindow, show="*")#Hides password characters
        self.loginPasswordTextField.pack()

        self.loginButton = tk.Button(self.loginWindow, text="Login", command=self.verifyLogin)
        self.loginButton.pack()

        self.errorLabel = tk.Label(self.loginWindow, text="", fg="red")
        self.errorLabel.pack()

    def verifyLogin(self):
        inputName = self.loginNameTextField.get().strip() #strips unnecessary characters from username and password
        inputPassword = self.loginPasswordTextField.get().strip()

        user = self.db.getUserByUsername(inputName)

        if user and user['password'] == inputPassword: #Checks to make sure that the user signing in already exists in the database
            self.loginWindow.destroy()
            self.currentUser = userClass.userClass(username=user['username'], password=user['password'])
            self.createMainSettingWindow()
        else:
            self.errorLabel.config(text="Invalid username or password")


    def createMainSettingWindow(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()  # Destroy all widgets in the startWindow

        
        self.startWindow.title("Main Settings")

        self.settingLabel = tk.Label(self.startWindow, text="Welcome to Main Settings", font=('Arial', 18)) #Generates after the user has signed in
        self.settingLabel.pack()

        self.prevInfoLabel = tk.Label(self.startWindow,text="Would you like to use your previous pacing mode?", font=('Arial', 12)) #Asks user to choose between using their previous pacing mode or configuring their pacing mode
        self.prevInfoLabel.pack()
        self.prevInfoLabel.place(relx=0.5, rely=0.3, anchor='center')

        self.prevInfoButtonYes= tk.Button(self.startWindow, text="Yes", command=self.getPrevMode) #Allows user to select their previous pacing mode
        self.prevInfoButtonYes.pack()
        self.prevInfoButtonYes.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)

        self.warningYes= tk.Label(self.startWindow, text="By clicking 'Yes' you agree to have your\n previous pacing mode stored in our database", font=('Arial', 8))
        self.warningYes.pack()
        self.warningYes.place(relx=0.1, rely=0.55)

        self.prevInfoButtonNo= tk.Button(self.startWindow, text="No", command= self.configPaceMode) #Allows user to select to not use their previous mode
        self.prevInfoButtonNo.pack()
        self.prevInfoButtonNo.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.05)

        self.warningNo= tk.Label(self.startWindow, text="By clicking 'No' you are choosing to\n configure your pacing mode manually", font=('Arial', 8))
        self.warningNo.pack()
        self.warningNo.place(relx=0.625, rely=0.55)

        self.deleteUserButton = tk.Button(self.startWindow, text = "Delete User", command=self.deleteUser) #Gives the user the option to delete their profile from the database
        self.deleteUserButton.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.05)
        self.deleteUserLabel= tk.Label(self.startWindow, text="By clicking 'Delete User', you are choosing to\n permanently delete your profile and pacing\n history from our database", font=("Arial",8))
        self.deleteUserLabel.pack()
        self.deleteUserLabel.place(relx=0.355,rely=0.75)

    def getPrevMode(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.createMainSettingWindow)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)


        self.prevInfoWindow = self.startWindow
        #self.prevInfoWindow.geometry("800x800")
        
        self.prevInfoLabel=tk.Label(self.prevInfoWindow, text="Previous Pacing Mode", font=('Arial',18)) #Accesses user’s previous pacing parameters from the database
        self.prevInfoLabel.pack()
        self.prevInfoLabel.place(relx=0.4, rely=0.05)

        user_data = self.db.getUserByUsername(self.currentUser.username)

        y_position = 0.1
        for attribute, value in user_data.items(): #Displays the information for the user to view and submit
            label = tk.Label(self.prevInfoWindow, text=f"{attribute}: {value}", font=('Arial', 12))
            label.place(relx=0.1, rely=y_position)
            y_position += 0.05

    def configPaceMode(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.createMainSettingWindow)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defaultWindow = self.startWindow

        self.pickDefault= tk.Label(self.defaultWindow, text="Would you like to configure the pacing mode or use a default pacing mode?", font=('Arial', 12)) #Gives the user the option to either configure the pacing mode manually or use default parameters
        self.pickDefault.pack()
        self.pickDefault.place(relx=0.5, rely=0.3, anchor='center')

        self.useDefaultButtonYes= tk.Button(self.defaultWindow, text="Default", command= self.useDefault) #Allows user to select to configure using default parameters
        self.useDefaultButtonYes.pack()
        self.useDefaultButtonYes.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)
        self.useDefaultLabel=tk.Label(self.defaultWindow, text="By clicking 'Default', you will get the option\n to choose your pacing mode with it's\n corresponding default values", font=('Arial',8))
        self.useDefaultLabel.pack()
        self.useDefaultLabel.place(relx=0.125,rely=0.55)

        self.useConfigButtonNo= tk.Button(self.defaultWindow, text="Configure", command= self.useConfigure) #Allow user to select to configure manually
        self.useConfigButtonNo.pack()
        self.useConfigButtonNo.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.05)
        self.useConfigLabel=tk.Label(self.defaultWindow,text="By clicking 'Configure', you will\n select your desired pacing mode\n and input your own parameters", font=('Arial',8))
        self.useConfigLabel.pack()
        self.useConfigLabel.place(relx=0.65,rely=0.55)

    def useDefault(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.configPaceMode)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defaultModeWindow = self.startWindow
        
        self.defaultModeLabel=tk.Label(self.defaultModeWindow, text="Please Select Your Pacing Mode", font=("Arial",18)) #Prompts user to pick which pacing mode they want to use (VOO, AOO, AAI, VVI)
        self.defaultModeLabel.pack()
        self.defaultModeLabel.place(relx=0.3, rely=0.05)

        self.VOOButton = tk.Button(self.defaultModeWindow, text = "Default VOO", command=self.defaultVOO)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.15, rely=0.15, relwidth=0.3, relheight=0.05)

        self.AOOButton = tk.Button(self.defaultModeWindow, text = "Default AOO", command=self.defaultAOO)
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.15, relwidth=0.3, relheight=0.05)

        self.AAIButton = tk.Button(self.defaultModeWindow, text = "Default AAI", command=self.defaultAAI)
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.15, rely=0.35, relwidth=0.3, relheight=0.05)

        self.VVIButton = tk.Button(self.defaultModeWindow, text = "Default VVI", command=self.defaultVVI)
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.35, relwidth=0.3, relheight=0.05)

        self.VOORButton=tk.Button(self.defaultModeWindow, text= "Default VOOR", command=self.defaultVOOR)
        self.VOORButton.pack()
        self.VOORButton.place(relx=0.15, rely=0.55, relwidth=0.3, relheight=0.05)
        
        self.AOORButton=tk.Button(self.defaultModeWindow, text= "Default AOOR", command=self.defaultAOOR)
        self.AOORButton.pack()
        self.AOORButton.place(relx=0.6, rely=0.55, relwidth=0.3, relheight=0.05)

        self.AAIRButton=tk.Button(self.defaultModeWindow, text= "Default AAIR", command=self.defaultAAIR)
        self.AAIRButton.pack()
        self.AAIRButton.place(relx=0.15, rely=0.75, relwidth=0.3, relheight=0.05)
        
        self.VVIRButton=tk.Button(self.defaultModeWindow, text= "Default VVIR", command=self.defaultVVIR)
        self.VVIRButton.pack()
        self.VVIRButton.place(relx=0.6, rely=0.75, relwidth=0.3, relheight=0.05)
    
    def defaultVOO(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defVOOWindow = self.startWindow

        self.defVOOLabel=tk.Label(self.defVOOWindow, text="Default VOO Parameters", font=("Arial",18)) #Displays default VOO parameters
        self.defVOOLabel.pack()
        self.defVOOLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVOOWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVOOWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVOOWindow, text="Ventricular Amplitude: 4.9 V", font=('Arial', 12))
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.VentricularPulseWidthLabel= tk.Label(self.defVOOWindow, text="Ventricular Pulse Width: 0.4 ms", font=('Arial', 12))
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.7)
 
        self.VOOButton = tk.Button(self.defVOOWindow, text = "submit", command=self.submitDefVOO) #Allows the user to submit the parameters to their device
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefVOO(self):
        self.VOOLRLimit=60.0
        self.VOOURLimit=120.0
        self.VOOVentricularAmplitude=4.9
        self.VOOVentricularPulseWidth=0.4
        MyGUI.successfulSubmitted(self,self.defVOOWindow)


        self.currentUser.VOO(self.VOOLRLimit, self.VOOURLimit, self.VOOVentricularAmplitude, self.VOOVentricularPulseWidth) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)
    
    def defaultAOO(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defAOOWindow = self.startWindow

        self.defAOOLabel=tk.Label(self.defAOOWindow, text="Default AOO Parameters", font=("Arial",18))
        self.defAOOLabel.pack()
        self.defAOOLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAOOWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAOOWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAOOWindow, text="Atrial Amplitude: 4.9 V", font=('Arial', 12))
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.AtrialPulseWidthLabel= tk.Label(self.defAOOWindow, text="Atrial Pulse Width: 0.4 ms", font=('Arial', 12))
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.7)
 
        self.AOOButton = tk.Button(self.defAOOWindow, text = "submit", command=self.submitDefAOO)#Allows the user to submit the parameters to their device
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefAOO(self):
        self.AOOLRLimit=60.0
        self.AOOURLimit=120.0
        self.AOOAtrialAmplitude=4.9
        self.AOOAtrialPulseWidth=0.4

        self.currentUser.AOO(self.AOOLRLimit, self.AOOURLimit, self.AOOAtrialAmplitude, self.AOOAtrialPulseWidth)#Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)
        MyGUI.successfulSubmitted(self,self.defAOOWindow)

    def defaultAAI(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defAAIWindow = self.startWindow

        self.defAAILabel=tk.Label(self.defAAIWindow, text="Default AAI Parameters", font=("Arial",18))#Displays default AAI parameters
        self.defAAILabel.pack()
        self.defAAILabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAAIWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAAIWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAAIWindow, text="Atrial Amplitude: 4.9 V", font=('Arial', 12))
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.AtrialPulseWidthLabel= tk.Label(self.defAAIWindow, text="Atrial Pulse Width: 0.4 ms", font=('Arial', 12))
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.7)

        self.AtrialSensitivityLabel= tk.Label(self.defAAIWindow, text="Atrial Sensitivity: 1.05 mV", font=('Arial', 12))
        self.AtrialSensitivityLabel.pack()
        self.AtrialSensitivityLabel.place(relx=0.525, rely=0.15)

        self.ARPLabel= tk.Label(self.defAAIWindow, text="ARP: 250 ms", font=('Arial', 12))
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.525, rely=0.3)

        self.PVARPLabel= tk.Label(self.defAAIWindow, text="PVARP: 250 ms", font=('Arial', 12))
        self.PVARPLabel.pack()
        self.PVARPLabel.place(relx=0.525, rely=0.5)

        self.HysteresisLabel= tk.Label(self.defAAIWindow, text="Hysteresis: 0 ppm", font=('Arial', 12))
        self.HysteresisLabel.pack()
        self.HysteresisLabel.place(relx=0.525, rely=0.7)

        self.RateSmoothingLabel= tk.Label(self.defAAIWindow, text="Rate Smoothing: 0%", font=('Arial', 12))
        self.RateSmoothingLabel.pack()
        self.RateSmoothingLabel.place(relx=0.1, rely=0.8)

        self.AAIButton = tk.Button(self.defAAIWindow, text = "submit", command=self.submitDefAAI)#Allows the user to submit the parameters to their device
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefAAI(self):
        self.AAILRLimit=60.0
        self.AAIURLimit=120.0
        self.AAIAtrialAmplitude=4.9
        self.AAIAtrialPulseWidth=0.4
        self.AAIAtrialSensitivity=1.05
        self.AAIARP=250.0
        self.AAIPVARP=250.0
        self.AAIHysteresis=0.0
        self.AAIRateSmoothing=0.0

        self.currentUser.AAI(self.AAILRLimit, self.AAIURLimit, self.AAIAtrialAmplitude, self.AAIAtrialPulseWidth, self.AAIAtrialSensitivity, self.AAIARP, self.AAIPVARP, self.AAIHysteresis, self.AAIRateSmoothing)#Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)
        MyGUI.successfulSubmitted(self, self.defAAIWindow)

    def defaultVVI(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defVVIWindow = self.startWindow

        self.defVVILabel=tk.Label(self.defVVIWindow, text="Default VVI Parameters", font=("Arial",18)) #Displays default VVI parameters
        self.defVVILabel.pack()
        self.defVVILabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVVIWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVVIWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVVIWindow, text="Ventricular Amplitude: 4.9 V", font=('Arial', 12))
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.VentricularPulseWidthLabel= tk.Label(self.defVVIWindow, text="Ventricular Pulse Width: 0.4 ms", font=('Arial', 12))
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.7)

        self.VentricularSensitivityLabel= tk.Label(self.defVVIWindow, text="Ventricular Sensitivity: 3.5 mV", font=('Arial', 12))
        self.VentricularSensitivityLabel.pack()
        self.VentricularSensitivityLabel.place(relx=0.525, rely=0.15)

        self.VRPLabel= tk.Label(self.defVVIWindow, text="VRP: 320 ms", font=('Arial', 12))
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.525, rely=0.3)

        self.HysteresisLabel= tk.Label(self.defVVIWindow, text="Hysteresis: 0 ppm", font=('Arial', 12))
        self.HysteresisLabel.pack()
        self.HysteresisLabel.place(relx=0.525, rely=0.5)

        self.RateSmoothingLabel= tk.Label(self.defVVIWindow, text="Rate Smoothing: 0%", font=('Arial', 12))
        self.RateSmoothingLabel.pack()
        self.RateSmoothingLabel.place(relx=0.55, rely=0.7)

        self.VVIButton = tk.Button(self.defVVIWindow, text = "submit", command=self.submitDefVVI)#Allows the user to submit the parameters to their device
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefVVI(self):
        self.VVILRLimit=60.0
        self.VVIURLimit=120.0
        self.VVIVentricularAmplitude=4.9
        self.VVIVentricularPulseWidth=0.4
        self.VVIVentricularSensitivity=3.5
        self.VVIVRP=320.0
        self.VVIHysteresis=0.0
        self.VVIRateSmoothing=0.0

        self.currentUser.VVI(self.VVILRLimit, self.VVIURLimit, self.VVIVentricularAmplitude, self.VVIVentricularPulseWidth, self.VVIVentricularSensitivity, self.VVIVRP, self.VVIHysteresis, self.VVIRateSmoothing )#Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)
        MyGUI.successfulSubmitted(self, self.defVVIWindow)
    
    def defaultVOOR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defVOORWindow = self.startWindow

        self.defVOORLabel=tk.Label(self.defVOORWindow, text="Default VOOR Parameters", font=("Arial",18)) #Displays default VOO parameters
        self.defVOORLabel.pack()
        self.defVOORLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVOORWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVOORWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVOORWindow, text="Ventricular Amplitude: 4.9 V", font=('Arial', 12))
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.VentricularPulseWidthLabel= tk.Label(self.defVOORWindow, text="Ventricular Pulse Width: 0.4 ms", font=('Arial', 12))
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.7)

        self.MaxSensorRateLabel=tk.Label(self.defVOORWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 12))
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.525, rely=0.15)

        self.ActivityThreshLabel=tk.Label(self.defVOORWindow, text="Activity Threshold: Medium", font=('Arial',12))
        self.ActivityThreshLabel.pack()
        self.ActivityThreshLabel.place(relx=0.525, rely=0.3)

        self.ReactionTimeLabel=tk.Label(self.defVOORWindow, text="Reaction Time: 30 sec", font=('Arial',12))
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.5)

        self.ResponseFactorLabel=tk.Label(self.defVOORWindow, text="Response Factor: 8", font=('Arial',12))
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.7)

        self.RecoveryTimeLabel=tk.Label(self.defVOORWindow, text="Recovery Time: 5 min", font=('Arial',12))
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.1, rely=0.8)

        self.VOORButton = tk.Button(self.defVOORWindow, text = "submit", command=self.submitDefVOOR) #Allows the user to submit the parameters to their device
        self.VOORButton.pack()
        self.VOORButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefVOOR(self):
        self.VOORLRLimit=60.0
        self.VOORURLimit=120.0
        self.VOORVentricularAmplitude=4.9
        self.VOORVentricularPulseWidth=0.4
        self.VOORMaxSensorRate=120
        self.VOORActivityThresh=2
        self.VOORReactionTime=30
        self.VOORResponseFactor=8
        self.VOORRecoveryTime=5
        MyGUI.successfulSubmitted(self,self.defVOORWindow)

        self.currentUser.VOOR(self.VOORLRLimit, self.VOORURLimit, self.VOORVentricularAmplitude, self.VOORVentricularPulseWidth, self.VOORMaxSensorRate, self.VOORActivityThresh,self.VOORReactionTime,self.VOORResponseFactor, self.VOORRecoveryTime) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)


    def defaultAOOR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)
        
        self.defAOORWindow=self.startWindow

        self.defAOORLabel=tk.Label(self.defAOORWindow, text="Default AOOR Parameters", font=("Arial",18)) #Displays default VOO parameters
        self.defAOORLabel.pack()
        self.defAOORLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAOORWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAOORWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAOORWindow, text="Atrial Amplitude: 4.9 V", font=('Arial', 12))
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.AtrialPulseWidthLabel= tk.Label(self.defAOORWindow, text="Atrial Pulse Width: 0.4 ms", font=('Arial', 12))
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.7)

        self.MaxSensorRateLabel=tk.Label(self.defAOORWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 12))
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.525, rely=0.15)

        self.ActivityThreshLabel=tk.Label(self.defAOORWindow, text="Activity Threshold: Medium", font=('Arial',12))
        self.ActivityThreshLabel.pack()
        self.ActivityThreshLabel.place(relx=0.525, rely=0.3)

        self.ReactionTimeLabel=tk.Label(self.defAOORWindow, text="Reaction Time: 30 sec", font=('Arial',12))
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.5)

        self.ResponseFactorLabel=tk.Label(self.defAOORWindow, text="Response Factor: 8", font=('Arial',12))
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.7)

        self.RecoveryTimeLabel=tk.Label(self.defAOORWindow, text="Recovery Time: 5 min", font=('Arial',12))
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.1, rely=0.8)

        self.AOORButton = tk.Button(self.defAOORWindow, text = "submit", command=self.submitDefAOOR) #Allows the user to submit the parameters to their device
        self.AOORButton.pack()
        self.AOORButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefAOOR(self):
        self.AOORLRLimit=60.0
        self.AOORURLimit=120.0
        self.AOORAtrialAmplitude=4.9
        self.AOORAtrialPulseWidth=0.4
        self.AOORMaxSensorRate=120
        self.AOORActivityThresh=2
        self.AOORReactionTime=30
        self.AOORResponseFactor=8
        self.AOORRecoveryTime=5
        MyGUI.successfulSubmitted(self,self.defAOORWindow)

        self.currentUser.AOOR(self.AOORLRLimit, self.AOORURLimit, self.AOORAtrialAmplitude, self.AOORAtrialPulseWidth, self.AOORMaxSensorRate, self.AOORActivityThresh,self.AOORReactionTime,self.AOORResponseFactor, self.AOORRecoveryTime) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)

    
    def defaultAAIR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defAAIRWindow=self.startWindow
        
        self.defAAIRLabel=tk.Label(self.defAAIRWindow, text="Default AAIR Parameters", font=("Arial",18)) #Displays default VOO parameters
        self.defAAIRLabel.pack()
        self.defAAIRLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAAIRWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAAIRWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.25)

        self.AtrialAmplitudeLabel= tk.Label(self.defAAIRWindow, text="Atrial Amplitude: 4.9 V", font=('Arial', 12))
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.35)

        self.AtrialPulseWidthLabel= tk.Label(self.defAAIRWindow, text="Atrial Pulse Width: 0.4 ms", font=('Arial', 12))
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.45)

        self.RecoveryTimeLabel=tk.Label(self.defAAIRWindow, text="Recovery Time: 5 min", font=('Arial',12))
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.1, rely=0.55)

        self.MaxSensorRateLabel=tk.Label(self.defAAIRWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 12))
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.525, rely=0.15)

        self.ActivityThreshLabel=tk.Label(self.defAAIRWindow, text="Activity Threshold: Medium", font=('Arial',12))
        self.ActivityThreshLabel.pack()
        self.ActivityThreshLabel.place(relx=0.525, rely=0.25)

        self.ReactionTimeLabel=tk.Label(self.defAAIRWindow, text="Reaction Time: 30 sec", font=('Arial',12))
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.35)

        self.ResponseFactorLabel=tk.Label(self.defAAIRWindow, text="Response Factor: 8", font=('Arial',12))
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.45)

        self.AtrialSensitivity=tk.Label(self.defAAIRWindow, text="Atrial Sensitivity: 1.05 mv", font=('Arial', 12))
        self.AtrialSensitivity.pack()
        self.AtrialSensitivity.place(relx=0.525, rely=0.55)

        self.ARPLabel=tk.Label(self.defAAIRWindow, text=' ARP: 250 ms', font=('Arial', 12))
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.1 ,rely=0.65)

        self.PVARPLabel=tk.Label(self.defAAIRWindow, text="PVARP: 250 ms", font=("Arial",12))
        self.PVARPLabel.pack()
        self.PVARPLabel.place(relx=0.525,rely=0.65)

        self.HysteresisLabel=tk.Label(self.defAAIRWindow, text="Hysteresis: 0 ppm", font=("Arial",12))
        self.HysteresisLabel.pack()
        self.HysteresisLabel.place(relx=0.1,rely=0.75)

        self.RateSmoothingLabel=tk.Label(self.defAAIRWindow, text="Rate Smoothing: 0%", font=("Arial",12))
        self.RateSmoothingLabel.pack()
        self.RateSmoothingLabel.place(relx=0.525,rely=0.75)  

        self.AAIRButton = tk.Button(self.defAAIRWindow, text = "submit", command=self.submitDefAAIR) #Allows the user to submit the parameters to their device
        self.AAIRButton.pack()
        self.AAIRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefAAIR(self):
        self.AAIRLRLimit=60.0
        self.AAIRURLimit=120.0
        self.AAIRAtrialAmplitude=4.9
        self.AAIRAtrialPulseWidth=0.4
        self.AAIRMaxSensorRate=120
        self.AAIRActivityThresh=2
        self.AAIRReactionTime=30
        self.AAIRResponseFactor=8
        self.AAIRRecoveryTime=5
        self.AAIRAtrialSensitivity=1.05
        self.AAIRARP=250
        self.AAIRPVARP=250
        self.AAIRHysteresis=0
        self.AAIRRateSmoothing=0
        MyGUI.successfulSubmitted(self,self.defAAIRWindow)

        self.currentUser.AAIR(self.AAIRLRLimit, self.AAIRURLimit, self.AAIRAtrialAmplitude, self.AAIRAtrialPulseWidth, self.AAIRMaxSensorRate, self.AAIRActivityThresh,self.AAIRReactionTime,self.AAIRResponseFactor, self.AAIRRecoveryTime,self.AAIRAtrialSensitivity,self.AAIRARP,self.AAIRPVARP,self.AAIRHysteresis,self.AAIRRateSmoothing) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)      

    def defaultVVIR(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useDefault)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.defVVIRWindow=self.startWindow
        
        self.defVVIRLabel=tk.Label(self.defVVIRWindow, text="Default VVIR Parameters", font=("Arial",18)) #Displays default VOO parameters
        self.defVVIRLabel.pack()
        self.defVVIRLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVVIRWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVVIRWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.25)

        self.VentricularAmplitudeLabel= tk.Label(self.defVVIRWindow, text="Ventricular Amplitude: 4.9 V", font=('Arial', 12))
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.35)

        self.VentricularPulseWidthLabel= tk.Label(self.defVVIRWindow, text="Ventricular Pulse Width: 0.4 ms", font=('Arial', 12))
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.45)

        self.RecoveryTimeLabel=tk.Label(self.defVVIRWindow, text="Recovery Time: 5 min", font=('Arial',12))
        self.RecoveryTimeLabel.pack()
        self.RecoveryTimeLabel.place(relx=0.1, rely=0.55)

        self.MaxSensorRateLabel=tk.Label(self.defVVIRWindow, text="Maximum Sensor Rate: 120 ppm", font=('Arial', 12))
        self.MaxSensorRateLabel.pack()
        self.MaxSensorRateLabel.place(relx=0.525, rely=0.15)

        self.ActivityThreshLabel=tk.Label(self.defVVIRWindow, text="Activity Threshold: Medium", font=('Arial',12))
        self.ActivityThreshLabel.pack()
        self.ActivityThreshLabel.place(relx=0.525, rely=0.25)

        self.ReactionTimeLabel=tk.Label(self.defVVIRWindow, text="Reaction Time: 30 sec", font=('Arial',12))
        self.ReactionTimeLabel.pack()
        self.ReactionTimeLabel.place(relx=0.525, rely=0.35)

        self.ResponseFactorLabel=tk.Label(self.defVVIRWindow, text="Response Factor: 8", font=('Arial',12))
        self.ResponseFactorLabel.pack()
        self.ResponseFactorLabel.place(relx=0.525, rely=0.45)

        self.VentricularSensitivity=tk.Label(self.defVVIRWindow, text="Ventricular Sensitivity: 3.5 mv", font=('Arial', 12))
        self.VentricularSensitivity.pack()
        self.VentricularSensitivity.place(relx=0.525, rely=0.55)

        self.VRPLabel=tk.Label(self.defVVIRWindow, text=' ARP: 320 ms', font=('Arial', 12))
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.1 ,rely=0.65)

        self.HysteresisLabel=tk.Label(self.defVVIRWindow, text="Hysteresis: 0 ppm", font=("Arial",12))
        self.HysteresisLabel.pack()
        self.HysteresisLabel.place(relx=0.1,rely=0.75)

        self.RateSmoothingLabel=tk.Label(self.defVVIRWindow, text="Rate Smoothing: 0%", font=("Arial",12))
        self.RateSmoothingLabel.pack()
        self.RateSmoothingLabel.place(relx=0.525,rely=0.65)

        self.VVIRButton = tk.Button(self.defVVIRWindow, text = "submit", command=self.submitDefVVIR) #Allows the user to submit the parameters to their device
        self.VVIRButton.pack()
        self.VVIRButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefVVIR(self):
        self.VVIRLRLimit=60.0
        self.VVIRURLimit=120.0
        self.VVIRVentricularAmplitude=4.9
        self.VVIRVentricularPulseWidth=0.4
        self.VVIRMaxSensorRate=120
        self.VVIRActivityThresh=2
        self.VVIRReactionTime=30
        self.VVIRResponseFactor=8
        self.VVIRRecoveryTime=5
        self.VVIRVentricularSensitivity=3.5
        self.VVIRVRP=320
        self.VVIRHysteresis=0
        self.VVIRRateSmoothing=0
        MyGUI.successfulSubmitted(self,self.defVVIRWindow)

        self.currentUser.AAIR(self.VVIRLRLimit, self.VVIRURLimit, self.VVIRVentricularAmplitude, self.VVIRVentricularPulseWidth, self.VVIRMaxSensorRate, self.VVIRActivityThresh,self.VVIRReactionTime,self.VVIRResponseFactor, self.VVIRRecoveryTime,self.VVIRVentricularSensitivity,self.VVIRVRP,self.VVIRHysteresis,self.VVIRRateSmoothing) #Updates the user’s chosen parameters to the database
        self.db.updateUser(self.currentUser)  


    def useConfigure(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.configPaceMode)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.configModeWindow = self.startWindow

        self.configModeLabel=tk.Label(self.configModeWindow, text="Please Select Your Pacing Mode", font=("Arial",18)) #Asks user to pick between the four pacing modes (VOO, AOO, AAI, VVI)
        self.configModeLabel.pack()
        self.configModeLabel.place(relx=0.3, rely=0.05)

        self.VOOButton = tk.Button(self.configModeWindow, text = "Configure VOO", command=self.VOOConfig)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.15, rely=0.15, relwidth=0.3, relheight=0.05)

        self.AOOButton = tk.Button(self.configModeWindow, text = "Configure AOO", command=self.AOOConfig)
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.15, relwidth=0.3, relheight=0.05)

        self.AAIButton = tk.Button(self.configModeWindow, text = "Configure AAI", command=self.AAIConfig)
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.15, rely=0.35, relwidth=0.3, relheight=0.05)

        self.VVIButton = tk.Button(self.configModeWindow, text = "Configure VVI", command=self.VVIConfig)
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.35, relwidth=0.3, relheight=0.05)
        '''
        self.VOORButton=tk.Button(self.configModeWindow, text= "Configure VOOR", command=self.VOORConfig)
        self.VOORButton.pack()
        self.VOORButton.place(relx=0.15, rely=0.55, relwidth=0.3, relheight=0.05)
        
        self.AOORButton=tk.Button(self.configModeWindow, text= "Configure AOOR", command=self.AOORConfig)
        self.AOORButton.pack()
        self.AOORButton.place(relx=0.6, rely=0.55, relwidth=0.3, relheight=0.05)

        self.AAIRButton=tk.Button(self.configModeWindow, text= "Configure AAIR", command=self.AAIRConfig)
        self.AAIRButton.pack()
        self.AAIRButton.place(relx=0.15, rely=0.75, relwidth=0.3, relheight=0.05)
        
        self.VVIRButton=tk.Button(self.configModeWindow, text= "Configure VVIR", command=self.VVIRConfig)
        self.VVIRButton.pack()
        self.VVIRButton.place(relx=0.6, rely=0.75, relwidth=0.3, relheight=0.05)
        '''
    
    def VOOConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()
        
        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.VOOConfigWindow = self.startWindow

        self.VOOConfigLabel=tk.Label(self.VOOConfigWindow, text="Configure Your VOO Parameters", font=("Arial",18)) #Gathers the necessary parameters to configure VOO from the user
        self.VOOConfigLabel.pack()
        self.VOOConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.VOOConfigWindow, text="Lower Rate Limit: ")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1,rely=0.2)
        self.LRLimitTextField = tk.Entry(self.VOOConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.3, rely=0.2)
        
        self.LRLimitWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 30-50 ppm incremented by 5 ppm\n values between 50-90 ppm incremented by 1 ppm\n values between 90-175 ppm incremented by 5 ppm",font=('Arial', 7) )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.1, rely=0.25)
        
        self.URLimitLabel= tk.Label(self.VOOConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.4)
        self.URLimitTextField = tk.Entry(self.VOOConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.4)
        
        self.URLimitWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 50-175 ppm incremented by 5 ppm",font=('Arial', 7) )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.1, rely=0.45)

        self.VentricularAmplitudeLabel= tk.Label(self.VOOConfigWindow, text="Ventricular Amplitude: ")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1,rely=0.6)
        self.VentricularAmplitudeTextField = tk.Entry(self.VOOConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.3, rely=0.6)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 0, 0.36-2.3 V with 0.1 V increment\n values between 2.5-5.0 V with 0.5 V increment",font=('Arial', 7) )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.1, rely=0.65)

        self.VentricularPulseWidthLabel= tk.Label(self.VOOConfigWindow, text="Ventricular Pulse Width: ")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1,rely=0.8)
        self.VentricularPulseWidthTextField = tk.Entry(self.VOOConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.3, rely=0.8)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: 0.05 ms\n values between 0.1-1.9 ms with 0.1 ms increment",font=('Arial', 7) )
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.1, rely=0.85)

        self.VOOButton = tk.Button(self.VOOConfigWindow, text = "submit", command=self.submitVOO) #Submit parameters to the device
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitVOO(self):
        self.VOOLRLimit= self.LRLimitTextField.get().strip()
        self.VOOURLimit= self.URLimitTextField.get().strip()
        self.VOOVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.VOOVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
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
        elif not ((self.VOOVentricularAmplitude == 0) or (0.36 <= self.VOOVentricularAmplitude <= 2.3 and self.VOOVentricularAmplitude*10%1==0) or (2.5 <= self.VOOVentricularAmplitude <= 5 and self.VOOVentricularAmplitude*10%5==0)): 
            MyGUI.errorWindow(self)
        elif not((self.VOOVentricularPulseWidth == 0.05 )or (0.1<= self.VOOVentricularPulseWidth <= 1.9 and self.VOOVentricularPulseWidth*10 % 1==0)):
            MyGUI.errorWindow(self)  
        else:
            MyGUI.successfulSubmitted(self, self.VOOConfigWindow)
            self.currentUser.VOO(self.VOOLRLimit, self.VOOURLimit, self.VOOVentricularAmplitude, self.VOOVentricularPulseWidth)
            self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
        
    def AOOConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.AOOConfigWindow = self.startWindow

        self.AOOConfigLabel=tk.Label(self.AOOConfigWindow, text="Configure Your AOO Parameters", font=("Arial",18))#Gathers the necessary parameters to configure AOO from the user
        self.AOOConfigLabel.pack()
        self.AOOConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.AOOConfigWindow, text="Lower Rate Limit: ")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1,rely=0.2)
        self.LRLimitTextField = tk.Entry(self.AOOConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.3, rely=0.2)
        
        self.LRLimitWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: values between 30-50 ppm incremented by 5 ppm\n values between 50-90 ppm incremented by 1 ppm\n values between 90-175 ppm incremented by 5 ppm",font=('Arial', 7) )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.1, rely=0.25)

        self.URLimitLabel= tk.Label(self.AOOConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.4)
        self.URLimitTextField = tk.Entry(self.AOOConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.4)

        self.URLimitWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: values between 50-175 ppm incremented by 5 ppm",font=('Arial', 7) )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.1, rely=0.45)

        self.AtrialAmplitudeLabel= tk.Label(self.AOOConfigWindow, text="Atrial Amplitude: ")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1,rely=0.6)
        self.AtrialAmplitudeTextField = tk.Entry(self.AOOConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.3, rely=0.6)

        self.AtrialAmplitudeWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: values between 0,0.36-2.3 V with 0.1 V increment\n values between 2.5-5 V with 0.5 V increment",font=('Arial', 7) )
        self.AtrialAmplitudeWarningLabel.pack()
        self.AtrialAmplitudeWarningLabel.place(relx=0.1, rely=0.65)

        self.AtrialPulseWidthLabel= tk.Label(self.AOOConfigWindow, text="Atrial Pulse Width: ")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1,rely=0.8)
        self.AtrialPulseWidthTextField = tk.Entry(self.AOOConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.3, rely=0.8)

        self.AtrialPulseWidthWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: 0.05 ms\n values between 0.1-1.9 ms with 0.1 ms increment",font=('Arial', 7) )
        self.AtrialPulseWidthWarningLabel.pack()
        self.AtrialPulseWidthWarningLabel.place(relx=0.1, rely=0.85)

        self.AOOButton = tk.Button(self.AOOConfigWindow, text = "submit", command=self.submitAOO) #Submits parameters to the device
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitAOO(self):
        self.AOOLRLimit= self.LRLimitTextField.get().strip()
        self.AOOURLimit= self.URLimitTextField.get().strip()
        self.AOOAtrialAmplitude= self.AtrialAmplitudeTextField.get().strip()
        self.AOOAtrialPulseWidth= self.AtrialPulseWidthTextField.get().strip()
        

        if self.AOOAtrialAmplitude == "0":
            self.AOOAtrialAmplitde =0
        else:
            self.AOOLRLimit= float(self.AOOLRLimit)
        self.AOOURLimit= float(self.AOOURLimit)
        self.AOOAtrialAmplitude= float(self.AOOAtrialAmplitude)
        self.AOOAtrialPulseWidth= float(self.AOOAtrialPulseWidth)
        #Checks to make sure the values inputted are valid
        if not ((30<= self.AOOLRLimit<=50 and self.AOOLRLimit % 5 == 0) or (50<= self.AOOLRLimit<=90) or  (90 <= self.AOOLRLimit <= 175 and self.AOOLRLimit % 5 == 0)):
            MyGUI.errorWindow(self)
        elif not ((50<= self.AOOURLimit<=175 and self.AOOURLimit % 5 == 0)):
            MyGUI.errorWindow(self)
        elif not ((self.AOOAtrialAmplitude == 0) or (0.36 <= self.AOOAtrialAmplitude <= 2.3 and self.AOOAtrialAmplitude*10 %1==0) or (2.5 <= self.AOOAtrialAmplitude <= 5 and self.AOOAtrialAmplitude*10 %5==0)): 
            MyGUI.errorWindow(self)
        elif not ((self.AOOAtrialPulseWidth == 0.05 )or (0.1<= self.AOOAtrialPulseWidth <= 1.9 and self.AOOAtrialPulseWidth*10 % 1 ==0)):
            MyGUI.errorWindow(self)    
        else:
            self.currentUser.AOO(self.AOOLRLimit, self.AOOURLimit, self.AOOAtrialAmplitude, self.AOOAtrialPulseWidth)
            self.db.updateUser(self.currentUser)
            MyGUI.successfulSubmitted(self,self.AOOConfigWindow)#Updates the user’s chosen parameters to the database


    def AAIConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.AAIConfigWindow = self.startWindow

        self.AAIConfigLabel=tk.Label(self.AAIConfigWindow, text="Configure Your AAI Parameters", font=("Arial",18))#Gathers the necessary parameters to configure AAI from the user
        self.AAIConfigLabel.pack()
        self.AAIConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.AAIConfigWindow, text="Lower Rate Limit: ")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.AAIConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.3, rely=0.15)

        self.LRLimitWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between 30-50 ppm incremented by 5 ppm\n values between 50-90 ppm incremented by 1 ppm\n values between 90-175 ppm incremented by 5 ppm",font=('Arial', 7) )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.1, rely=0.2)

        self.URLimitLabel= tk.Label(self.AAIConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.3)
        self.URLimitTextField = tk.Entry(self.AAIConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.3)

        self.URLimitWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between 50-175 ppm incremented by 5 ppm",font=('Arial', 7) )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.1, rely=0.35)

        self.AtrialAmplitudeLabel= tk.Label(self.AAIConfigWindow, text="Atrial Amplitude: ")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1,rely=0.45)
        self.AtrialAmplitudeTextField = tk.Entry(self.AAIConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.3, rely=0.45)

        self.AtrialAmplitudeWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between 0, 0.36-2.3 V with 0.1 V increment\n values between 2.5-5 V with 0.5 V increment",font=('Arial', 7) )
        self.AtrialAmplitudeWarningLabel.pack()
        self.AtrialAmplitudeWarningLabel.place(relx=0.1, rely=0.5)

        self.AtrialPulseWidthLabel= tk.Label(self.AAIConfigWindow, text="Atrial Pulse Width: ")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1,rely=0.6)
        self.AtrialPulseWidthTextField = tk.Entry(self.AAIConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.3, rely=0.6)

        self.AtrialPulseWidthWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: 0.05 ms\n values between 0.1-1.9 ms with 0.1 ms increment",font=('Arial', 7) )
        self.AtrialPulseWidthWarningLabel.pack()
        self.AtrialPulseWidthWarningLabel.place(relx=0.1, rely=0.65)

        self.AtrialSensitivityLabel= tk.Label(self.AAIConfigWindow, text="Atrial Sensitivity: ")
        self.AtrialSensitivityLabel.pack()
        self.AtrialSensitivityLabel.place(relx=0.6,rely=0.15)
        self.AtrialSensitivityTextField = tk.Entry(self.AAIConfigWindow)
        self.AtrialSensitivityTextField.pack()
        self.AtrialSensitivityTextField.place(relx=0.8, rely=0.15)

        self.AtrialSensitivityWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: 0.178, 0.375, 0.54 mV\n values between 0.07-0.72 mV with 0.5 mV increment",font=('Arial', 7) )
        self.AtrialSensitivityWarningLabel.pack()
        self.AtrialSensitivityWarningLabel.place(relx=0.6, rely=0.2)

        self.ARPLabel= tk.Label(self.AAIConfigWindow, text="ARP: ")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.6,rely=0.3)
        self.ARPTextField = tk.Entry(self.AAIConfigWindow)
        self.ARPTextField.pack()
        self.ARPTextField.place(relx=0.8, rely=0.3)

        self.ARPWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between 150-500 ms with 10 ms increment",font=('Arial', 7) )
        self.ARPWarningLabel.pack()
        self.ARPWarningLabel.place(relx=0.6, rely=0.35)

        self.PVARPLabel= tk.Label(self.AAIConfigWindow, text="PVARP: ")
        self.PVARPLabel.pack()
        self.PVARPLabel.place(relx=0.6,rely=0.45)
        self.PVARPTextField = tk.Entry(self.AAIConfigWindow)
        self.PVARPTextField.pack()
        self.PVARPTextField.place(relx=0.8, rely=0.45)

        self.PVARPWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between 150-500 ms with 10 ms increment",font=('Arial', 7) )
        self.PVARPWarningLabel.pack()
        self.PVARPWarningLabel.place(relx=0.6, rely=0.5)

        self.HysteresisLabel= tk.Label(self.AAIConfigWindow, text="Hysteresis: ")
        self.HysteresisLabel.pack()
        self.HysteresisLabel.place(relx=0.6,rely=0.6)
        self.HysteresisTextField = tk.Entry(self.AAIConfigWindow)
        self.HysteresisTextField.pack()
        self.HysteresisTextField.place(relx=0.8, rely=0.6)

        self.HysteresisWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between 30-50 ppm incremented by 5 ppm\n values between 50-90 ppm incremented by 1 ppm\n values between 90-175 ppm incremented by 5 ppm\n 0 (if turned OFF)",font=('Arial', 7) )
        self.HysteresisWarningLabel.pack()
        self.HysteresisWarningLabel.place(relx=0.6, rely=0.65)

        self.RateSmoothingLabel= tk.Label(self.AAIConfigWindow, text="Rate Smoothing: ")
        self.RateSmoothingLabel.pack()
        self.RateSmoothingLabel.place(relx=0.3,rely=0.725)
        self.RateSmoothingTextField = tk.Entry(self.AAIConfigWindow)
        self.RateSmoothingTextField.pack()
        self.RateSmoothingTextField.place(relx=0.5, rely=0.725)

        self.RateSmoothingWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: 0 (if turned OFF)\n 3, 6, 9, 12, 15, 18, 21, 25 %(if turned ON)",font=('Arial', 7) )
        self.RateSmoothingWarningLabel.pack()
        self.RateSmoothingWarningLabel.place(relx=0.3, rely=0.775)

        self.AAIButton = tk.Button(self.AAIConfigWindow, text = "submit", command=self.submitAAI) #Submits parameters to the device
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitAAI(self):
        self.AAILRLimit= self.LRLimitTextField.get().strip()
        self.AAIURLimit= self.URLimitTextField.get().strip()
        self.AAIAtrialAmplitude= self.AtrialAmplitudeTextField.get().strip()
        self.AAIAtrialPulseWidth= self.AtrialPulseWidthTextField.get().strip()
        self.AAIAtrialSensitivity= self.AtrialSensitivityTextField.get().strip()
        self.AAIARP= self.ARPTextField.get().strip()
        self.AAIPVARP= self.PVARPTextField.get().strip()
        self.AAIHysteresis= self.HysteresisTextField.get().strip()
        self.AAIRateSmoothing= self.RateSmoothingTextField.get().strip()

        if  self.AAIAtrialAmplitude== "0":
            self.AAIAtrialAmplitude = 0
        else:
            self.AAIAtrialAmplitude= float(self.AAIAtrialAmplitude)

        if  self.AAIHysteresis== "0":
            self.AAIHysteresis = 0
        else:
            self.AAIHysteresis= float(self.AAIHysteresis)

        if  self.AAIRateSmoothing== "0":
            self.AAIRateSmoothing = 0
        else:
            self.AAIRateSmoothing= float(self.AAIRateSmoothing)
            
        self.AAILRLimit= float(self.AAILRLimit)
        self.AAIURLimit= float(self.AAIURLimit)
        self.AAIAtrialPulseWidth= float(self.AAIAtrialPulseWidth)
        self.AAIAtrialSensitivity= float(self.AAIAtrialSensitivity)
        self.AAIARP= float(self.AAIARP)
        self.AAIPVARP= float(self.AAIPVARP)
        #Checks to make sure the values inputted are valid
        if not ((30<= self.AAILRLimit<=50 and self.AAILRLimit % 5 == 0) or (50<= self.AAILRLimit<=90) or  (90 <= self.AAILRLimit <= 175 and self.AAILRLimit % 5 == 0)):
            MyGUI.errorWindow(self)
        elif not ((50<= self.AAIURLimit<=175 and self.AAIURLimit % 5 == 0)):
            MyGUI.errorWindow(self)
        elif not ((self.AAIAtrialAmplitude==0) or (0.36 <= self.AAIAtrialAmplitude <= 2.3 and self.AAIAtrialAmplitude*10 %1==0) or (2.5 <= self.AAIAtrialAmplitude <= 5 and self.AAIAtrialAmplitude * 10 %5==0)): 
            MyGUI.errorWindow(self)
        elif not ((self.AAIAtrialPulseWidth == 0.05 )or (0.1<= self.AAIAtrialPulseWidth <= 1.9 and self.AAIAtrialPulseWidth*10 % 1==0)):
            MyGUI.errorWindow(self)
        elif not ((self.AAIAtrialSensitivity==0.178 or self.AAIAtrialSensitivity==0.357 or self.AAIAtrialSensitivity==0.54)or (0.07<=self.AAIAtrialSensitivity<=0.72 and self.AAIAtrialSensitivity*10 % 5==0)):   
            MyGUI.errorWindow(self)
        elif not ((150<= self.AAIARP<=500 and self.AAIARP % 10 == 0)):
            MyGUI.errorWindow(self)
        elif not ((150<= self.AAIPVARP<=500 and self.AAIPVARP % 10 == 0)):
            MyGUI.errorWindow(self)
        elif not ((self.AAIHysteresis==0 ) or (30<= self.AAIHysteresis<=50 and self.AAIHysteresis % 5 == 0) or (50<= self.AAIHysteresis<=90) or  (90 <= self.AAIHysteresis <= 175 and self.AAIHysteresis % 5 == 0)):
            pass
        elif not (((self.AAIRateSmoothing == 0)) or (self.AAIRateSmoothing == 3) or (self.AAIRateSmoothing == 6) or (self.AAIRateSmoothing == 9) or (self.AAIRateSmoothing == 12) or (self.AAIRateSmoothing == 15) or (self.AAIRateSmoothing == 18) or (self.AAIRateSmoothing == 21) or (self.AAIRateSmoothing == 25)):
            MyGUI.errorWindow(self)
        else:
            self.currentUser.AAI(self.AAILRLimit, self.AAIURLimit, self.AAIAtrialAmplitude, self.AAIAtrialPulseWidth, self.AAIAtrialSensitivity, self.AAIARP, self.AAIPVARP, self.AAIHysteresis, self.AAIRateSmoothing)
            self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
            MyGUI.successfulSubmitted(self,self.AAIConfigWindow)

    def VVIConfig(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()

        self.backButton = tk.Button(self.startWindow, text = "Back", command=self.useConfigure)
        self.backButton.pack()
        self.backButton.place(relx=0.075, rely=0.85, relwidth=0.1, relheight=0.05)

        self.VVIConfigWindow = self.startWindow


        self.VVIConfigLabel=tk.Label(self.VVIConfigWindow, text="Configure Your VVI Parameters", font=("Arial",18))#Gathers the necessary parameters to configure VVI from the user
        self.VVIConfigLabel.pack()
        self.VVIConfigLabel.place(relx=0.3,rely=0.05)

        self.LRLimitLabel= tk.Label(self.VVIConfigWindow, text="Lower Rate Limit: ")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.VVIConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.3, rely=0.15)

        self.LRLimitWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between 30-50 ppm incremented by 5 ppm\n values between 50-90 ppm incremented by 1 ppm\n values between 90-175 ppm incremented by 5 ppm",font=('Arial', 7) )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.1, rely=0.2)

        self.URLimitLabel= tk.Label(self.VVIConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.3)
        self.URLimitTextField = tk.Entry(self.VVIConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.3)

        self.URLimitWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between 50-175 ppm incremented by 5 ppm",font=('Arial', 7) )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.1, rely=0.35) 

        self.VentricularAmplitudeLabel= tk.Label(self.VVIConfigWindow, text="Ventricular Amplitude: ")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1,rely=0.45)
        self.VentricularAmplitudeTextField = tk.Entry(self.VVIConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.3, rely=0.45)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between 0, 0.36-2.3 V with 0.1 V increment\n values between 2.5-5 V with 0.5 V increment",font=('Arial', 7) )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.1, rely=0.5)

        self.VentricularPulseWidthLabel= tk.Label(self.VVIConfigWindow, text="Ventricular Pulse Width: ")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1,rely=0.6)
        self.VentricularPulseWidthTextField = tk.Entry(self.VVIConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.3, rely=0.6)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: 0.05 ms\n values between 0.1-1.9 ms with 0.1 ms increment",font=('Arial', 7) )
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.1, rely=0.65)

        self.VentricularSensitivityLabel= tk.Label(self.VVIConfigWindow, text="Ventricular Sensitivity: ")
        self.VentricularSensitivityLabel.pack()
        self.VentricularSensitivityLabel.place(relx=0.6,rely=0.15)
        self.VentricularSensitivityTextField = tk.Entry(self.VVIConfigWindow)
        self.VentricularSensitivityTextField.pack()
        self.VentricularSensitivityTextField.place(relx=0.8, rely=0.15)

        self.VentricularSensitivityWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: 0.178, 0.375, 0.54 mV\n values between 0.07-0.72 mV with 0.5 mV increment",font=('Arial', 7) )
        self.VentricularSensitivityWarningLabel.pack()
        self.VentricularSensitivityWarningLabel.place(relx=0.6, rely=0.2)

        self.VRPLabel= tk.Label(self.VVIConfigWindow, text="VRP: ")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.6,rely=0.3)
        self.VRPTextField = tk.Entry(self.VVIConfigWindow)
        self.VRPTextField.pack()
        self.VRPTextField.place(relx=0.8, rely=0.3)

        self.VRPWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between 150-500 ms with 10 ms increment",font=('Arial', 7) )
        self.VRPWarningLabel.pack()
        self.VRPWarningLabel.place(relx=0.6, rely=0.35)

        self.RateSmoothingLabel= tk.Label(self.VVIConfigWindow, text="Rate Smoothing: ")
        self.RateSmoothingLabel.pack()
        self.RateSmoothingLabel.place(relx=0.6,rely=0.45)
        self.RateSmoothingTextField = tk.Entry(self.VVIConfigWindow)
        self.RateSmoothingTextField.pack()
        self.RateSmoothingTextField.place(relx=0.8, rely=0.45)

        self.RateSmoothingWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: 0 (if turned OFF)\n 3, 6, 9, 12, 15, 18, 21, 25 %(if turned ON)",font=('Arial', 7) )
        self.RateSmoothingWarningLabel.pack()
        self.RateSmoothingWarningLabel.place(relx=0.6, rely=0.5)

        self.HysteresisLabel= tk.Label(self.VVIConfigWindow, text="Hysteresis: ")
        self.HysteresisLabel.pack()
        self.HysteresisLabel.place(relx=0.6,rely=0.6)
        self.HysteresisTextField = tk.Entry(self.VVIConfigWindow)
        self.HysteresisTextField.pack()
        self.HysteresisTextField.place(relx=0.8, rely=0.6)

        self.HysteresisWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between 30-50 ppm incremented by 5 ppm\n values between 50-90 ppm incremented by 1 ppm\n values between 90-175 ppm incremented by 5 ppm\n 0 (if turned OFF)",font=('Arial', 7) )
        self.HysteresisWarningLabel.pack()
        self.HysteresisWarningLabel.place(relx=0.6, rely=0.65)

        self.VVIButton = tk.Button(self.VVIConfigWindow, text = "submit", command=self.submitVVI) #Submits parameters to the device
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitVVI(self):
        self.VVILRLimit= self.LRLimitTextField.get().strip()
        self.VVIURLimit= self.URLimitTextField.get().strip()
        self.VVIVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.VVIVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        self.VVIVentricularSensitivity= self.VentricularSensitivityTextField.get().strip()
        self.VVIVRP= self.VRPTextField.get().strip()
        self.VVIHysteresis= self.HysteresisTextField.get().strip()
        self.VVIRateSmoothing= self.RateSmoothingTextField.get().strip()
        #Checks to make sure the values inputted are valid
        if self.VVIVentricularAmplitude == "0":
            self.VVIVentricularAmplitude =0
        else:
            self.VVIVentricularAmplitude= float(self.VVIVentricularAmplitude)
        
        if self.VVIHysteresis == "0":
            self.VVIHysteresis=0
        else: 
            self.VVIHysteresis= float(self.VVIHysteresis)

        if self.VVIRateSmoothing == "0":
            self.VVIRateSmoothing=0
        else: 
            self.VVIRateSmoothing= float(self.VVIRateSmoothing)
                
        self.VVILRLimit= float(self.VVILRLimit)
        self.VVIURLimit= float(self.VVIURLimit)
        self.VVIVentricularPulseWidth= float(self.VVIVentricularPulseWidth)
        self.VVIVentricularSensitivity= float(self.VVIVentricularSensitivity)
        self.VVIVRP= float(self.VVIVRP)
        self.VVIHysteresis= float(self.VVIHysteresis)
        self.VVIRateSmoothing= float(self.VVIRateSmoothing)

        if not ((30<= self.VVILRLimit<=50 and self.VVILRLimit % 5 == 0) or (50<= self.VVILRLimit<=90) or  (90 <= self.VVILRLimit <= 175 and self.VVILRLimit % 5 == 0)):
            MyGUI.errorWindow(self)
        elif not ((50<= self.VVIURLimit<=175 and self.VVIURLimit % 5 == 0)):
            MyGUI.errorWindow(self)
        elif not  ((0.36 <= self.VVIVentricularAmplitude <= 2.3 and self.VVIVentricularAmplitude*10 %1==0) or (2.5 <= self.VVIVentricularAmplitude <= 5 and self.VVIVentricularAmplitude*10 %5==0) or (self.VVIVentricularAmplitude ==0)): 
            MyGUI.errorWindow(self)
        elif not ((self.VVIVentricularPulseWidth == 0.05 )or (0.1<= self.VVIVentricularPulseWidth <= 1.9 and self.VVIVentricularPulseWidth*10 %1==0)):
            MyGUI.errorWindow(self)
        elif not ((self.VVIVentricularSensitivity==0.178 or self.VVIVentricularSensitivity==0.357 or self.VVIVentricularSensitivity==0.54)or (0.07<=self.VVIVentricularSensitivity<=0.72 and self.VVIVentricularSensitivity*10 %5==0)):   
            MyGUI.errorWindow(self)
        elif not ((150<= self.VVIVRP<=500 and self.VVIVRP % 10 == 0)):
            MyGUI.errorWindow(self)
        elif not ((self.VVIHysteresis ==0) or (30<= self.VVIHysteresis<=50 and self.VVIHysteresis % 5 == 0) or (50<= self.VVIHysteresis<=90) or  (90 <= self.VVIHysteresis <= 175 and self.VVIHysteresis % 5 == 0)):
            MyGUI.errorWindow(self)
        elif not ((self.VVIRateSmoothing==0) or (self.VVIRateSmoothing == 3) or (self.VVIRateSmoothing == 6) or (self.VVIRateSmoothing == 9) or (self.VVIRateSmoothing == 12) or (self.VVIRateSmoothing == 15) or (self.VVIRateSmoothing == 18) or (self.VVIRateSmoothing == 21) or (self.VVIRateSmoothing == 25)):
            MyGUI.errorWindow(self)
        else:
            self.currentUser.VVI(self.VVILRLimit, self.VVIURLimit, self.VVIVentricularAmplitude, self.VVIVentricularPulseWidth, self.VVIVentricularSensitivity, self.VVIVRP, self.VVIHysteresis, self.VVIRateSmoothing)
            self.db.updateUser(self.currentUser)#Updates the user’s chosen parameters to the database
            MyGUI.successfulSubmitted(self,self.VVIConfigWindow)


        self.currentUser.VVI(self.VVILRLimit, self.VVIURLimit, self.VVIVentricularAmplitude, self.VVIVentricularPulseWidth, self.VVIVentricularSensitivity, self.VVIVRP, self.VVIHysteresis, self.VVIRateSmoothing)
        self.db.updateUser(self.currentUser)
    
    
    def deleteUser(self):
        self.db.delete_user(self.currentUser.username)#Deletes user that is currently signed in from the database
        
        print("User successfully deleted!")  
        
        self.startWindow.destroy()
        self.__init__() #Calls the constructor
    
    def __del__(self):#Destructor
        self.db.close()#Closes the database

    def errorWindow(self):
        self.errorScreen = tk.Toplevel(self.configModeWindow)#Displays when the values inputted by the user are invalid
        self.errorScreen.geometry("200x100")
        self.errorScreenLabel = tk.Label(self.errorScreen, text = "Values Entered Are Not in Range", fg="red")
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
