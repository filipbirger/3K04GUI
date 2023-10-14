import tkinter as tk
import userClass 
import sqlite3
from DataBase import DataBase

class MyGUI:

    def __init__(self):
        
        self.db = DataBase()

        self.startWindow = tk.Tk()
        self.startWindow.geometry("800x800")
        self.startWindow.title("3K04 Pacemaker")

        self.connceted = True
        self.deviceId = 1

        self.startTitle = tk.Label(self.startWindow, text="Welcome To 3K04 Pacemaker", font=('Arial', 24))
        self.startTitle.place(relx=0.3, rely=0.1)
        if (self.connceted == True):
            self.newUserButton = tk.Button(self.startWindow, text="New User", command=self.createNewUser)
            self.newUserButton.place(relx=0.6, rely=0.2, relheight=0.1, relwidth=0.2)
            self.newUserLabel=tk.Label(self.startWindow, text="Click 'New User' to set up your\n profile and start\n configuring your pacemaker", font=("Arial",8))
            self.newUserLabel.pack()
            self.newUserLabel.place(relx=0.6, rely=0.3)

            self.signInButton = tk.Button(self.startWindow, text="Sign In", command=self.createLoginWindow)
            self.signInButton.place(relx=0.2, rely=0.2, relheight=0.1, relwidth=0.2)
            self.signInLabel=tk.Label(self.startWindow, text="Click 'Sign in' if you are\n an existing user", font=("Arial",8))
            self.signInLabel.pack()
            self.signInLabel.place(relx=0.22, rely=0.3)

            self.aboutButton = tk.Button (self.startWindow, text="About", command=self.aboutDevice)
            self.aboutButton.place(relx=0.4, rely=0.6, relheight=0.1, relwidth=0.2)
            self.aboutLabel=tk.Label(self.startWindow, text="Click 'About' for more\n information about your pacemaker", font=("Arial",8))
            self.aboutLabel.pack()
            self.aboutLabel.place(relx=0.385,rely=0.7)
        else:
            self.notConnectedLabel = tk.Label(self.startWindow, text="Not Connceted To Device", font=('Arial', 24))
            self.notConnectedLabel.pack()
        self.startWindow.mainloop()

    def createNewUser(self):
        self.newUserWindow = tk.Toplevel(self.startWindow)
        self.newUserWindow.geometry("300x200")
        self.newUserWindow.title("Create New User")

        self.userNameLabel = tk.Label(self.newUserWindow, text="Username:")
        self.userNameLabel.pack()
        self.userNameTextField = tk.Entry(self.newUserWindow)
        self.userNameTextField.pack()

        self.userPasswordLabel = tk.Label(self.newUserWindow, text="Password:")
        self.userPasswordLabel.pack()
        self.userPasswordTextField = tk.Entry(self.newUserWindow, show="*")
        self.userPasswordTextField.pack()

        self.enterButton = tk.Button(self.newUserWindow, text="Submit", command=self.populateUserInfo)
        self.enterButton.pack()
        
    def populateUserInfo(self):
        allUsersSize = self.db.getAllUsers()
        if len(allUsersSize)>=10:
            self.maxUserReachedText = tk.Label(self.startWindow, text="Error: Maximum number of users reached!", command=self.createLoginWindow)
            print("")
            return
        else:
            inputName = self.userNameTextField.get().strip()
            inputPassword = self.userPasswordTextField.get().strip()
            if inputName and inputPassword:
                self.newUser = userClass.userClass(username=inputName, password=inputPassword, DeviceId=self.deviceId)
                self.newUserWindow.destroy()
                self.db.insertUser(self.newUser)


    def aboutDevice(self):
        self.aboutWindow = tk.Toplevel(self.startWindow)
        self.aboutWindow.geometry("300x200")
        self.aboutWindow.title("About")
        self.applicationModelNumberLabel = tk.Label(self.aboutWindow, text="Application model number:", font=('Arial', 12))
        self.applicationModelNumberLabel.pack(padx=0.1)
        self.revisionNumberLabel = tk.Label(self.aboutWindow, text="Revision Number:", font=('Arial', 12))
        self.revisionNumberLabel.pack(padx=0.1)
        self.DCMNumberLabel = tk.Label(self.aboutWindow, text="DCM serial number:1", font=('Arial', 12))
        self.DCMNumberLabel.pack(padx=0.1)
        self.instituteNameLabel = tk.Label(self.aboutWindow, text="Institution name: McMaster U", font=('Arial', 12))
        self.instituteNameLabel.pack(padx=0.1)

    def createLoginWindow(self):
        self.loginWindow = tk.Toplevel(self.startWindow)
        self.loginWindow.geometry("300x200")
        self.loginWindow.title("Login")

        self.loginNameLabel = tk.Label(self.loginWindow, text="Username:")
        self.loginNameLabel.pack()
        self.loginNameTextField = tk.Entry(self.loginWindow)
        self.loginNameTextField.pack()

        self.loginPasswordLabel = tk.Label(self.loginWindow, text="Password:")
        self.loginPasswordLabel.pack()
        self.loginPasswordTextField = tk.Entry(self.loginWindow, show="*")
        self.loginPasswordTextField.pack()

        self.loginButton = tk.Button(self.loginWindow, text="Login", command=self.verifyLogin)
        self.loginButton.pack()

        self.errorLabel = tk.Label(self.loginWindow, text="", fg="red")
        self.errorLabel.pack()

    def verifyLogin(self):
        inputName = self.loginNameTextField.get().strip()
        inputPassword = self.loginPasswordTextField.get().strip()

        user = self.db.getUserByUsername(inputName)

        if user and user['password'] == inputPassword:
            self.loginWindow.destroy()
            self.currentUser = userClass.userClass(username=user['username'], password=user['password'])
            self.createMainSettingWindow()
        else:
            self.errorLabel.config(text="Invalid username or password")


    def createMainSettingWindow(self):
        for widget in self.startWindow.winfo_children():
            widget.destroy()  # Destroy all widgets in the startWindow

        self.startWindow.title("Main Settings")

        self.settingLabel = tk.Label(self.startWindow, text="Welcome to Main Settings", font=('Arial', 18))
        self.settingLabel.pack()

        self.prevInfoLabel = tk.Label(self.startWindow,text="Would you like to use your previous pacing mode?", font=('Arial', 12))
        self.prevInfoLabel.pack()
        self.prevInfoLabel.place(relx=0.5, rely=0.3, anchor='center')

        self.prevInfoButtonYes= tk.Button(self.startWindow, text="Yes", command= self.getPrevMode)
        self.prevInfoButtonYes.pack()
        self.prevInfoButtonYes.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)

        self.warningYes= tk.Label(self.startWindow, text="By clicking 'Yes' you agree to have your\n previous pacing mode stored in our database", font=('Arial', 8))
        self.warningYes.pack()
        self.warningYes.place(relx=0.1, rely=0.55)

        self.prevInfoButtonNo= tk.Button(self.startWindow, text="No", command= self.configPaceMode)
        self.prevInfoButtonNo.pack()
        self.prevInfoButtonNo.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.05)

        self.warningNo= tk.Label(self.startWindow, text="By clicking 'No' you are choosing to\n configure your pacing mode manually", font=('Arial', 8))
        self.warningNo.pack()
        self.warningNo.place(relx=0.625, rely=0.55)

        self.deleteUserButton = tk.Button(self.startWindow, text = "Delete User", command=self.deleteUser)
        self.deleteUserButton.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.05)
        self.deleteUserLabel= tk.Label(self.startWindow, text="By clicking 'Delete User', you are choosing to\n permanently delete your profile and pacing\n history from our database", font=("Arial",8))
        self.deleteUserLabel.pack()
        self.deleteUserLabel.place(relx=0.355,rely=0.75)

    def getPrevMode(self):
        self.prevInfoWindow = tk.Toplevel(self.startWindow)
        self.prevInfoWindow.geometry("800x800")
        
        self.prevInfoLabel=tk.Label(self.prevInfoWindow, text="Previous Pacing Mode", font=('Arial',18))
        self.prevInfoLabel.pack()
        self.prevInfoLabel.place(relx=0.4, rely=0.05)

        user_data = self.db.getUserByUsername(self.currentUser.username)

        y_position = 0.1
        for attribute, value in user_data.items():
            label = tk.Label(self.prevInfoWindow, text=f"{attribute}: {value}", font=('Arial', 12))
            label.place(relx=0.1, rely=y_position)
            y_position += 0.05

    def configPaceMode(self):
        self.defaultWindow=tk.Toplevel(self.startWindow)
        self.defaultWindow.geometry("800x800")

        self.pickDefault= tk.Label(self.defaultWindow, text="Would you like to configure the pacing mode or use a default pacing mode?", font=('Arial', 12))
        self.pickDefault.pack()
        self.pickDefault.place(relx=0.5, rely=0.3, anchor='center')

        self.useDefaultButtonYes= tk.Button(self.defaultWindow, text="Default", command= self.useDefault)
        self.useDefaultButtonYes.pack()
        self.useDefaultButtonYes.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)
        self.useDefaultLabel=tk.Label(self.defaultWindow, text="By clicking 'Default', you will get the option\n to choose your pacing mode with it's\n corresponding default values", font=('Arial',8))
        self.useDefaultLabel.pack()
        self.useDefaultLabel.place(relx=0.125,rely=0.55)

        self.useConfigButtonNo= tk.Button(self.defaultWindow, text="Configure", command= self.useConfigure)
        self.useConfigButtonNo.pack()
        self.useConfigButtonNo.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.05)
        self.useConfigLabel=tk.Label(self.defaultWindow,text="By clicking 'Configure', you will\n select your desired pacing mode\n and input your own parameters", font=('Arial',8))
        self.useConfigLabel.pack()
        self.useConfigLabel.place(relx=0.65,rely=0.55)

    def useDefault(self):
        self.defaultModeWindow=tk.Toplevel(self.defaultWindow)
        self.defaultModeWindow.geometry("800x800")
        
        self.defaultModeLabel=tk.Label(self.defaultModeWindow, text="Please Select Your Pacing Mode", font=("Arial",18))
        self.defaultModeLabel.pack()
        self.defaultModeLabel.place(relx=0.3, rely=0.05)

        self.VOOButton = tk.Button(self.defaultModeWindow, text = "Default VOO", command=self.defaultVOO)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.15, rely=0.25, relwidth=0.3, relheight=0.05)

        self.AOOButton = tk.Button(self.defaultModeWindow, text = "Default AOO", command=self.defaultAOO)
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.25, relwidth=0.3, relheight=0.05)

        self.AAIButton = tk.Button(self.defaultModeWindow, text = "Default AAI", command=self.defaultAAI)
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.15, rely=0.45, relwidth=0.3, relheight=0.05)

        self.VVIButton = tk.Button(self.defaultModeWindow, text = "Default VVI", command=self.defaultVVI)
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.45, relwidth=0.3, relheight=0.05)

    
    def defaultVOO(self):
        self.defVOOWindow=tk.Toplevel(self.defaultModeWindow)
        self.defVOOWindow.geometry("800x800")

        self.defVOOLabel=tk.Label(self.defVOOWindow, text="Default VOO Parameters", font=("Arial",18))
        self.defVOOLabel.pack()
        self.defVOOLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVOOWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVOOWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVOOWindow, text="Ventricular Amplitude: 3.5 V", font=('Arial', 12))
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.VentricularPulseWidthLabel= tk.Label(self.defVOOWindow, text="Ventricular Pulse Width: 0.4 ms", font=('Arial', 12))
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.7)
 
        self.VOOButton = tk.Button(self.defVOOWindow, text = "submit", command=self.submitDefVOO)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefVOO(self):
        self.VOOLRLimit=60.0
        self.VOOURLimit=120.0
        self.VOOVentricularAmplitude=3.5
        self.VOOVentricularPulseWidth=0.4

        self.currentUser.VOO(self.VOOLRLimit, self.VOOURLimit, self.VOOVentricularAmplitude, self.VOOVentricularPulseWidth)
        self.db.updateUser(self.currentUser)
    
    def defaultAOO(self):
        self.defAOOWindow=tk.Toplevel(self.defaultModeWindow)
        self.defAOOWindow.geometry("800x800")

        self.defAOOLabel=tk.Label(self.defAOOWindow, text="Default AOO Parameters", font=("Arial",18))
        self.defAOOLabel.pack()
        self.defAOOLabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAOOWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAOOWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAOOWindow, text="Atrial Amplitude: 3.5 V", font=('Arial', 12))
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.AtrialPulseWidthLabel= tk.Label(self.defAOOWindow, text="Atrial Pulse Width: 0.4 ms", font=('Arial', 12))
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.7)
 
        self.AOOButton = tk.Button(self.defAOOWindow, text = "submit", command=self.submitDefAOO)
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def submitDefAOO(self):
        self.AOOLRLimit=60.0
        self.AOOURLimit=120.0
        self.AOOAtrialAmplitude=3.5
        self.AOOAtrialPulseWidth=0.4

        self.currentUser.AOO(self.AOOLRLimit, self.AOOURLimit, self.AOOAtrialAmplitude, self.AOOAtrialPulseWidth)
        self.db.updateUser(self.currentUser)

    def defaultAAI(self):
        self.defAAIWindow=tk.Toplevel(self.defaultModeWindow)
        self.defAAIWindow.geometry("800x800")

        self.defAAILabel=tk.Label(self.defAAIWindow, text="Default AAI Parameters", font=("Arial",18))
        self.defAAILabel.pack()
        self.defAAILabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defAAIWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defAAIWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.AtrialAmplitudeLabel= tk.Label(self.defAAIWindow, text="Atrial Amplitude: 3.5 V", font=('Arial', 12))
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.AtrialPulseWidthLabel= tk.Label(self.defAAIWindow, text="Atrial Pulse Width: 0.4 ms", font=('Arial', 12))
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1, rely=0.7)

        self.AtrialSensitivityLabel= tk.Label(self.defAAIWindow, text="Atrial Sensitivity: 0.75 mV", font=('Arial', 12))
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

        self.AAIButton = tk.Button(self.defAAIWindow, text = "submit", command=self.submitDefAAI)
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefAAI(self):
        self.AAILRLimit=60.0
        self.AAIURLimit=120.0
        self.AAIAtrialAmplitude=3.5
        self.AAIAtrialPulseWidth=0.4
        self.AAIAtrialSensitivity=0.75
        self.AAIARP=250.0
        self.AAIPVARP=250.0
        self.AAIHysteresis=0.0
        self.AAIRateSmoothing=0.0

        self.currentUser.AAI(self.AAILRLimit, self.AAIURLimit, self.AAIAtrialAmplitude, self.AAIAtrialPulseWidth, self.AAIAtrialSensitivity, self.AAIARP, self.AAIPVARP, self.AAIHysteresis, self.AAIRateSmoothing)
        self.db.updateUser(self.currentUser)


    def defaultVVI(self):
        self.defVVIWindow=tk.Toplevel(self.defaultModeWindow)
        self.defVVIWindow.geometry("800x800")

        self.defVVILabel=tk.Label(self.defVVIWindow, text="Default VVI Parameters", font=("Arial",18))
        self.defVVILabel.pack()
        self.defVVILabel.place(relx=0.35, rely=0.05)

        self.LRLimitLabel= tk.Label(self.defVVIWindow, text="Lower Rate Limit: 60 ppm", font=('Arial', 12))
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1, rely=0.15)

        self.URLimitLabel= tk.Label(self.defVVIWindow, text="Upper Rate Limit: 120 ppm", font=('Arial', 12))
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1, rely=0.3)

        self.VentricularAmplitudeLabel= tk.Label(self.defVVIWindow, text="Ventricular Amplitude: 3.5 V", font=('Arial', 12))
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1, rely=0.5)

        self.VentricularPulseWidthLabel= tk.Label(self.defVVIWindow, text="Ventricular Pulse Width: 0.4 ms", font=('Arial', 12))
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1, rely=0.7)

        self.VentricularSensitivityLabel= tk.Label(self.defVVIWindow, text="Ventricular Sensitivity: 2.5 mV", font=('Arial', 12))
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

        self.VVIButton = tk.Button(self.defVVIWindow, text = "submit", command=self.submitDefVVI)
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitDefVVI(self):
        self.VVILRLimit=60.0
        self.VVIURLimit=120.0
        self.VVIVentricularAmplitude=3.5
        self.VVIVentricularPulseWidth=0.4
        self.VVIVentricularSensitivity=2.5
        self.VVIVRP=320.0
        self.VVIHysteresis=0.0
        self.VVIRateSmoothing=0.0

        self.currentUser.VVI(self.VVILRLimit, self.VVIURLimit, self.VVIVentricularAmplitude, self.VVIVentricularPulseWidth, self.VVIVentricularSensitivity, self.VVIVRP, self.VVIHysteresis, self.VVIRateSmoothing )
        self.db.updateUser(self.currentUser)


    def useConfigure(self):
        self.configModeWindow = tk.Toplevel(self.defaultWindow)
        self.configModeWindow.geometry("800x800")

        self.configModeLabel=tk.Label(self.configModeWindow, text="Please Select Your Pacing Mode", font=("Arial",18))
        self.configModeLabel.pack()
        self.configModeLabel.place(relx=0.3, rely=0.05)

        self.VOOButton = tk.Button(self.configModeWindow, text = "Set VOO Option", command=self.VOOConfig)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.15, rely=0.25, relwidth=0.3, relheight=0.05)

        self.AOOButton = tk.Button(self.configModeWindow, text = "Set AOO Option", command=self.AOOConfig)
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.25, relwidth=0.3, relheight=0.05)

        self.AAIButton = tk.Button(self.configModeWindow, text = "Set AAI Option", command=self.AAIConfig)
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.15, rely=0.45, relwidth=0.3, relheight=0.05)

        self.VVIButton = tk.Button(self.configModeWindow, text = "Set VVI Option", command=self.VVIConfig)
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.45, relwidth=0.3, relheight=0.05)
    
    def VOOConfig(self):
        self.VOOConfigWindow= tk.Toplevel(self.configModeWindow)
        self.VOOConfigWindow.geometry("800x800")

        self.VOOConfigLabel=tk.Label(self.VOOConfigWindow, text="Configure Your VOO Parameters", font=("Arial",18))
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

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 0, 0.5-3.2 V with 0.1 V increment\n values between 3.5-7 V with 0.5 V increment",font=('Arial', 7) )
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

        self.VOOButton = tk.Button(self.VOOConfigWindow, text = "submit", command=self.submitVOO)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitVOO(self):
        self.VOOLRLimit= self.LRLimitTextField.get().strip()
        self.VOOURLimit= self.URLimitTextField.get().strip()
        self.VOOVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.VOOVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        self.VOOLRLimit = float(self.VOOLRLimit)
        self.VOOURLimit = float(self.VOOURLimit)
        self.VOOVentricularAmplitude = float(self.VOOVentricularAmplitude)
        self.VOOVentricularPulseWidth = float(self.VOOVentricularPulseWidth)

        if ((30<= self.VOOLRLimit<=50 and self.VOOLRLimit % 5 == 0) or (50<= self.VOOLRLimit<=90) or  (90 <= self.VOOLRLimit <= 175 and self.VOOLRLimit % 5 == 0)):
            pass
        elif ((50<= self.VOOLRLimit<=175 and self.VOOLRLimit % 5 == 0)):
            pass
        elif (0.36 <= self.VOOVentricularAmplitude <= 2.3 and self.VOOVentricularAmplitude%0.1==0) or (2.5 <= self.VOOVentricularAmplitude <= 5 and self.VOOVentricularAmplitude%0.5==0): 
            pass
        elif((self.VOOVentricularPulseWidth == 0.05 )or (0.1<= self.VOOVentricularPulseWidth <= 1.9 and self.VOOVentricularPulseWidth %0.1==0)):
            pass    
        else:
            MyGUI.errorWindow(self)
        
        self.currentUser.VOO(self.VOOLRLimit, self.VOOURLimit, self.VOOVentricularAmplitude, self.VOOVentricularPulseWidth)
        self.db.updateUser(self.currentUser)
        


    def AOOConfig(self):
        self.AOOConfigWindow= tk.Toplevel(self.configModeWindow)
        self.AOOConfigWindow.geometry("800x800")

        self.AOOConfigLabel=tk.Label(self.AOOConfigWindow, text="Configure Your AOO Parameters", font=("Arial",18))
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

        self.AtrialAmplitudeWarningLabel= tk.Label(self.AOOConfigWindow, text="Valid inputs are: values between 0,0.5-3.2 V with 0.1 V increment\n values between 3.5-7 V with 0.5 V increment",font=('Arial', 7) )
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

        self.AOOButton = tk.Button(self.AOOConfigWindow, text = "submit", command=self.submitAOO)
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def submitAOO(self):
        self.AOOLRLimit= self.LRLimitTextField.get().strip()
        self.AOOURLimit= self.URLimitTextField.get().strip()
        self.AOOAtrialAmplitude= self.AtrialAmplitudeTextField.get().strip()
        self.AOOAtrialPulseWidth= self.AtrialPulseWidthTextField.get().strip()
        self.AOOLRLimit= float(self.AOOLRLimit)
        self.AOOURLimit= float(self.AOOURLimit)
        self.AOOAtrialAmplitude= float(self.AOOAtrialAmplitude)
        self.AOOAtrialPulseWidth= float(self.AOOAtrialPulseWidth)

        if ((30<= self.AOOLRLimit<=50 and self.AOOLRLimit % 5 == 0) or (50<= self.AOOLRLimit<=90) or  (90 <= self.AOOLRLimit <= 175 and self.AOOLRLimit % 5 == 0)):
            pass
        elif ((50<= self.AOOLRLimit<=175 and self.AOOLRLimit % 5 == 0)):
            pass
        elif (0.36 <= self.AOOAtrialAmplitude <= 2.3 and self.AOOAtrialAmplitude%0.1==0) or (2.5 <= self.VOOVentricularAmplitude <= 5 and self.VOOVentricularAmplitude%0.5==0): 
            pass
        elif((self.AOOAtrialPulseWidth == 0.05 )or (0.1<= self.AOOAtrialPulseWidth <= 1.9 and self.VOOVentricularPulseWidth %0.1==0)):
            pass    
        else:
            MyGUI.errorWindow(self)

        self.currentUser.AOO(self.AOOLRLimit, self.AOOURLimit, self.AOOAtrialAmplitude, self.AOOAtrialPulseWidth)
        self.db.updateUser(self.currentUser)


    def AAIConfig(self):
        self.AAIConfigWindow= tk.Toplevel(self.configModeWindow)
        self.AAIConfigWindow.geometry("800x800")

        self.AAIConfigLabel=tk.Label(self.AAIConfigWindow, text="Configure Your AAI Parameters", font=("Arial",18))
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

        self.AtrialAmplitudeWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: values between 0, 0.5-3.2 V with 0.1 V increment\n values between 3.5-7 V with 0.5 V increment",font=('Arial', 7) )
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

        self.AtrialSensitivityWarningLabel= tk.Label(self.AAIConfigWindow, text="Valid inputs are: 0.25, 0.5, 0.75 mV\n values between 1.0-10 mV with 0.5 mV increment",font=('Arial', 7) )
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

        self.AAIButton = tk.Button(self.AAIConfigWindow, text = "submit", command=self.submitAAI)
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

        self.AAILRLimit= float(self.AAILRLimit)
        self.AAIURLimit= float(self.AAIURLimit)
        self.AAIAtrialAmplitude= float(self.AAIAtrialAmplitude)
        self.AAIAtrialPulseWidth= float(self.AAIAtrialPulseWidth)
        self.AAIAtrialSensitivity= float(self.AAIAtrialSensitivity)
        self.AAIARP= float(self.AAIARP)
        self.AAIPVARP= float(self.AAIPVARP)
        self.AAIHysteresis= float(self.AAIHysteresis)
        self.AAIRateSmoothing= float(self.AAIRateSmoothing)

        if ((30<= self.AAILRLimit<=50 and self.AAILRLimit % 5 == 0) or (50<= self.AAILRLimit<=90) or  (90 <= self.AAILRLimit <= 175 and self.AAILRLimit % 5 == 0)):
            pass
        elif ((50<= self.AAIURLimit<=175 and self.AAIURLimit % 5 == 0)):
            pass
        elif (0.36 <= self.AAIAtrialAmplitude <= 2.3 and self.AAIAtrialAmplitude%0.1==0) or (2.5 <= self.AAIAtrialAmplitude <= 5 and self.AAIAtrialAmplitude%0.5==0): 
            pass
        elif((self.AAIAtrialPulseWidth == 0.05 )or (0.1<= self.AAIAtrialPulseWidth <= 1.9 and self.AAIAtrialPulseWidth %0.1==0)):
            pass 
        elif((self.AAIAtrialSensitivity==0.178 or self.AAIAtrialSensitivity==0.357 or self.AAIAtrialSensitivity==0.54)or (0.07<=self.AAIAtrialSensitivity<=0.72 and self.AAIAtrialSensitivity%0.5==0)):   
            pass
        elif ((150<= self.AAIARP<=500 and self.AAIARP % 10 == 0)):
            pass
        elif ((150<= self.AAIPVARP<=500 and self.AAIPVARP % 10 == 0)):
            pass
        elif ((30<= self.AAIHysteresis<=50 and self.AAIHysteresis % 5 == 0) or (50<= self.AAIHysteresis<=90) or  (90 <= self.AAIHysteresis <= 175 and self.AAIHysteresis % 5 == 0)):
            pass
        elif((self.AAIRateSmoothing == 3) or (self.AAIRateSmoothing == 6) or (self.AAIRateSmoothing == 9) or (self.AAIRateSmoothing == 12) or (self.AAIRateSmoothing == 15) or (self.AAIRateSmoothing == 18) or (self.AAIRateSmoothing == 21) or (self.AAIRateSmoothing == 25)):
            pass
        else:
            MyGUI.errorWindow(self)

        self.currentUser.AAI(self.AAILRLimit, self.AAIURLimit, self.AAIAtrialAmplitude, self.AAIAtrialPulseWidth, self.AAIAtrialSensitivity, self.AAIARP, self.AAIPVARP, self.AAIHysteresis, self.AAIRateSmoothing)
        self.db.updateUser(self.currentUser)

    def VVIConfig(self):
        self.VVIConfigWindow= tk.Toplevel(self.configModeWindow)
        self.VVIConfigWindow.geometry("800x800")

        self.VVIConfigLabel=tk.Label(self.VVIConfigWindow, text="Configure Your VVI Parameters", font=("Arial",18))
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

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: values between 0, 0.5-3.2 V with 0.1 V increment\n values between 3.5-7 V with 0.5 V increment",font=('Arial', 7) )
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

        self.VentricularSensitivityWarningLabel= tk.Label(self.VVIConfigWindow, text="Valid inputs are: 0.25, 0.5, 0.75 mV\n values between 1.0-10 mV with 0.5 mV increment",font=('Arial', 7) )
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

        self.VVIButton = tk.Button(self.VVIConfigWindow, text = "submit", command=self.submitVVI)
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

        self.VVILRLimit= float(self.VVILRLimit)
        self.VVIURLimit= float(self.VVIURLimit)
        self.VVIVentricularAmplitude= float(self.VVIVentricularAmplitude)
        self.VVIVentricularPulseWidth= float(self.VVIVentricularPulseWidth)
        self.VVIVentricularSensitivity= float(self.VVIVentricularSensitivity)
        self.VVIVRP= float(self.VVIVRP)
        self.VVIHysteresis= float(self.VVIHysteresis)
        self.VVIRateSmoothing= float(self.VVIRateSmoothing)

        if ((30<= self.VVILRLimit<=50 and self.VVILRLimit % 5 == 0) or (50<= self.VVILRLimit<=90) or  (90 <= self.VVILRLimit <= 175 and self.VVILRLimit % 5 == 0)):
            pass
        elif ((50<= self.VVIURLimit<=175 and self.VVIURLimit % 5 == 0)):
            pass
        elif (0.36 <= self.VVIVentricularAmplitude <= 2.3 and self.VVIVentricularAmplitude%0.1==0) or (2.5 <= self.VVIVentricularAmplitude <= 5 and self.VVIVentricularAmplitude%0.5==0): 
            pass
        elif((self.VVIVentricularPulseWidth == 0.05 )or (0.1<= self.VVIVentricularPulseWidth <= 1.9 and self.VVIVentricularPulseWidth %0.1==0)):
            pass 
        elif((self.VVIVentricularSensitivity==0.178 or self.VVIVentricularSensitivity==0.357 or self.VVIVentricularSensitivity==0.54)or (0.07<=self.VVIVentricularSensitivity<=0.72 and self.VVIVentricularSensitivity%0.5==0)):   
            pass
        elif ((150<= self.VVIVRP<=500 and self.VVIVRP % 10 == 0)):
            pass
        elif ((30<= self.VVIHysteresis<=50 and self.VVIHysteresis % 5 == 0) or (50<= self.VVIHysteresis<=90) or  (90 <= self.VVIHysteresis <= 175 and self.VVIHysteresis % 5 == 0)):
            pass
        elif((self.VVIRateSmoothing == 3) or (self.VVIRateSmoothing == 6) or (self.VVIRateSmoothing == 9) or (self.VVIRateSmoothing == 12) or (self.VVIRateSmoothing == 15) or (self.VVIRateSmoothing == 18) or (self.VVIRateSmoothing == 21) or (self.VVIRateSmoothing == 25)):
            pass
        else:
            MyGUI.errorWindow(self)


        self.currentUser.VVI(self.VVILRLimit, self.VVIURLimit, self.VVIVentricularAmplitude, self.VVIVentricularPulseWidth, self.VVIVentricularSensitivity, self.VVIVRP, self.VVIHysteresis, self.VVIRateSmoothing)
        self.db.updateUser(self.currentUser)
    
    def deleteUser(self):
        self.db.delete_user(self.currentUser.username)
        
        print("User successfully deleted!")  
        
        self.startWindow.destroy()
        self.__init__() 
    
    def __del__(self):
        self.db.close()

    def errorWindow(self):
        self.errorScreen = tk.Toplevel(self.configModeWindow)
        self.errorScreen.geometry("200x100")
        self.errorScreenLabel = tk.Label(self.errorScreen, text = "Values Entered Are Not in Range", fg="red")
        self.errorScreenLabel.pack()

MyGUI()
