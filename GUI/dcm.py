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

        self.startTitle = tk.Label(self.startWindow, text="Welcome To 3K04 Pacemaker", font=('Arial', 24))
        self.startTitle.place(relx=0.3, rely=0.1)

        self.newUserButton = tk.Button(self.startWindow, text="New User", command=self.createNewUser)
        self.newUserButton.place(relx=0.6, rely=0.2, relheight=0.1, relwidth=0.2)

        self.signInButton = tk.Button(self.startWindow, text="Sign In", command=self.createLoginWindow)
        self.signInButton.place(relx=0.2, rely=0.2, relheight=0.1, relwidth=0.2)


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
                self.newUser = userClass.userClass(username=inputName, password=inputPassword)
                self.newUserWindow.destroy()
                self.db.insertUser(self.newUser)


    

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

        if user and user[1] == inputPassword:  
            self.loginWindow.destroy()
            self.currentUser = userClass.userClass(username=user[0], password=user[1])
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



    def getPrevMode(self):
        self.prevInfoWindow = tk.Toplevel(self.startWindow)
        self.prevInfoWindow.geometry("800x800")

        user_data = self.db.getUser(self.currentUser.username)

        y_position = 0.1
        for attribute, value in user_data.items():
            label = tk.Label(self.prevInfoWindow, text=f"{attribute}: {value}", font=('Arial', 18))
            label.place(relx=0.1, rely=y_position)
            y_position += 0.05

        self.prevPaceMode= tk.Label(self.prevInfoWindow, text="IN PROGRESS",font=('Arial', 18))
        self.prevPaceMode.pack()

    def configPaceMode(self):
        self.defaultWindow=tk.Toplevel(self.startWindow)
        self.defaultWindow.geometry("800x800")

        self.pickDefault= tk.Label(self.defaultWindow, text="Would you like to configure the pacing mode or use a default pacing mode?", font=('Arial', 12))
        self.pickDefault.pack()
        self.pickDefault.place(relx=0.5, rely=0.3, anchor='center')

        self.useDefaultButtonYes= tk.Button(self.defaultWindow, text="Default", command= self.useDefault)
        self.useDefaultButtonYes.pack()
        self.useDefaultButtonYes.place(relx=0.1, rely=0.5, relwidth=0.3, relheight=0.05)

        self.useConfigButtonNo= tk.Button(self.defaultWindow, text="Configure", command= self.useConfigure)
        self.useConfigButtonNo.pack()
        self.useConfigButtonNo.place(relx=0.6, rely=0.5, relwidth=0.3, relheight=0.05)


    def useDefault(self):
        self.defaultModeWindow=tk.Toplevel(self.defaultWindow)
        self.defaultModeWindow.geometry("800x800")
        self.fix1= tk.Label(self.defaultModeWindow, text="IN PROGRESS",font=('Arial', 18))
        self.fix1.pack()

    def useConfigure(self):
        self.configModeWindow = tk.Toplevel(self.defaultWindow)
        self.configModeWindow.geometry("800x800")
        self.fix2= tk.Label(self.configModeWindow, text="IN PROGRESS",font=('Arial', 18))
        self.fix2.pack()

        self.VOOButton = tk.Button(self.configModeWindow, text = "Set VOO Option", command=self.VOOConfig)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.2, rely=0.2, relwidth=0.3, relheight=0.05)

        self.AOOButton = tk.Button(self.configModeWindow, text = "Set AOO Option", command=self.AOOConfig)
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.05)

        self.AAIButton = tk.Button(self.configModeWindow, text = "Set AAI Option", command=self.AAIConfig)
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.2, rely=0.4, relwidth=0.3, relheight=0.05)


        self.VVIButton = tk.Button(self.configModeWindow, text = "Set VVI Option", command=self.VVIConfig)
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.05)
    
    def VOOConfig(self):
        self.VOOConfigWindow= tk.Toplevel(self.configModeWindow)
        self.VOOConfigWindow.geometry("800x800")

        self.LRLimitLabel= tk.Label(self.VOOConfigWindow, text="Lower Rate Limit: ")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1,rely=0.2)
        self.LRLimitTextField = tk.Entry(self.VOOConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.3, rely=0.2)
        
        self.LRLimitWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 30-50 ppm incremented by 5 ppm\n values between 50-90 ppm incremented by 1 ppm\n values between 90-175 ppm incremented by 5 ppm",font=('Arial', 6) )
        self.LRLimitWarningLabel.pack()
        self.LRLimitWarningLabel.place(relx=0.1, rely=0.25)
        
        self.URLimitLabel= tk.Label(self.VOOConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.4)
        self.URLimitTextField = tk.Entry(self.VOOConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.4)
        
        self.URLimitWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 50-175 ppm incremented by 5 ppm",font=('Arial', 6) )
        self.URLimitWarningLabel.pack()
        self.URLimitWarningLabel.place(relx=0.1, rely=0.45)

        self.VentricularAmplitudeLabel= tk.Label(self.VOOConfigWindow, text="Ventricular Amplitude: ")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1,rely=0.6)
        self.VentricularAmplitudeTextField = tk.Entry(self.VOOConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.3, rely=0.6)

        self.VentricularAmplitudeWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: values between 0.5-3.2 V with 0.1 V increment (if device is OFF)\n values between 3.5-7 V with 0.5 V increment (if device is ON)",font=('Arial', 6) )
        self.VentricularAmplitudeWarningLabel.pack()
        self.VentricularAmplitudeWarningLabel.place(relx=0.1, rely=0.65)

        self.VentricularPulseWidthLabel= tk.Label(self.VOOConfigWindow, text="Ventricular Pulse Width: ")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1,rely=0.8)
        self.VentricularPulseWidthTextField = tk.Entry(self.VOOConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.3, rely=0.8)

        self.VentricularPulseWidthWarningLabel= tk.Label(self.VOOConfigWindow, text="Valid inputs are: 0.05 ms\n values between 0.1-1.9 ms with 0.1 ms increment (if device is ON)",font=('Arial', 6) )
        self.VentricularPulseWidthWarningLabel.pack()
        self.VentricularPulseWidthWarningLabel.place(relx=0.1, rely=0.85)

        self.VOOButton = tk.Button(self.VOOConfigWindow, text = "submit", command=self.submitVOO)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.3)

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

        self.LRLimitLabel= tk.Label(self.AOOConfigWindow, text="Lower Rate Limit: ")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1,rely=0.2)
        self.LRLimitTextField = tk.Entry(self.AOOConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.3, rely=0.2)

        self.URLimitLabel= tk.Label(self.AOOConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.4)
        self.URLimitTextField = tk.Entry(self.AOOConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.4)

        self.AtrialAmplitudeLabel= tk.Label(self.AOOConfigWindow, text="Atrial Amplitude: ")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1,rely=0.6)
        self.AtrialAmplitudeTextField = tk.Entry(self.AOOConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.3, rely=0.6)

        self.AtrialPulseWidthLabel= tk.Label(self.AOOConfigWindow, text="Atrial Pulse Width: ")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1,rely=0.8)
        self.AtrialPulseWidthTextField = tk.Entry(self.AOOConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.3, rely=0.8)

        self.AOOButton = tk.Button(self.AOOConfigWindow, text = "submit", command=self.submitAOO)
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.3)

    def submitAOO(self):
        self.AOOLRLimit= self.LRLimitTextField.get().strip()
        self.AOOURLimit= self.URLimitTextField.get().strip()
        self.AOOAtrialAmplitude= self.AtrialAmplitudeTextField.get().strip()
        self.AOOAtrialPulseWidth= self.AtrialPulseWidthTextField.get().strip()

        self.currentUser.AOO(self.AOOLRLimit, self.AOOURLimit, self.AOOAtrialAmplitude, self.AOOAtrialPulseWidth)
        self.db.updateUser(self.currentUser)


    def AAIConfig(self):
        self.AAIConfigWindow= tk.Toplevel(self.configModeWindow)
        self.AAIConfigWindow.geometry("800x800")

        self.LRLimitLabel= tk.Label(self.AAIConfigWindow, text="Lower Rate Limit: ")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1,rely=0.15)
        self.LRLimitTextField = tk.Entry(self.AAIConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.3, rely=0.15)

        self.URLimitLabel= tk.Label(self.AAIConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.35)
        self.URLimitTextField = tk.Entry(self.AAIConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.35)

        self.AtrialAmplitudeLabel= tk.Label(self.AAIConfigWindow, text="Atrial Amplitude: ")
        self.AtrialAmplitudeLabel.pack()
        self.AtrialAmplitudeLabel.place(relx=0.1,rely=0.55)
        self.AtrialAmplitudeTextField = tk.Entry(self.AAIConfigWindow)
        self.AtrialAmplitudeTextField.pack()
        self.AtrialAmplitudeTextField.place(relx=0.3, rely=0.55)

        self.AtrialPulseWidthLabel= tk.Label(self.AAIConfigWindow, text="Atrial Pulse Width: ")
        self.AtrialPulseWidthLabel.pack()
        self.AtrialPulseWidthLabel.place(relx=0.1,rely=0.75)
        self.AtrialPulseWidthTextField = tk.Entry(self.AAIConfigWindow)
        self.AtrialPulseWidthTextField.pack()
        self.AtrialPulseWidthTextField.place(relx=0.3, rely=0.75)

        self.AtrialSensitivityLabel= tk.Label(self.AAIConfigWindow, text="Atrial Sensitivity: ")
        self.AtrialSensitivityLabel.pack()
        self.AtrialSensitivityLabel.place(relx=0.6,rely=0.15)
        self.AtrialSensitivityTextField = tk.Entry(self.AAIConfigWindow)
        self.AtrialSensitivityTextField.pack()
        self.AtrialSensitivityTextField.place(relx=0.8, rely=0.15)

        self.ARPLabel= tk.Label(self.AAIConfigWindow, text="ARP: ")
        self.ARPLabel.pack()
        self.ARPLabel.place(relx=0.6,rely=0.35)
        self.ARPTextField = tk.Entry(self.AAIConfigWindow)
        self.ARPTextField.pack()
        self.ARPTextField.place(relx=0.8, rely=0.35)

        self.PVARPLabel= tk.Label(self.AAIConfigWindow, text="PVARP: ")
        self.PVARPLabel.pack()
        self.PVARPLabel.place(relx=0.6,rely=0.55)
        self.PVARPTextField = tk.Entry(self.AAIConfigWindow)
        self.PVARPTextField.pack()
        self.PVARPTextField.place(relx=0.8, rely=0.55)

        self.HysteresisLabel= tk.Label(self.AAIConfigWindow, text="Hysteresis: ")
        self.HysteresisLabel.pack()
        self.HysteresisLabel.place(relx=0.6,rely=0.75)
        self.HysteresisTextField = tk.Entry(self.AAIConfigWindow)
        self.HysteresisTextField.pack()
        self.HysteresisTextField.place(relx=0.8, rely=0.75)

        self.RateSmoothingLabel= tk.Label(self.AAIConfigWindow, text="Rate Smoothing: ")
        self.RateSmoothingLabel.pack()
        self.RateSmoothingLabel.place(relx=0.3,rely=0.825)
        self.RateSmoothingTextField = tk.Entry(self.AAIConfigWindow)
        self.RateSmoothingTextField.pack()
        self.RateSmoothingTextField.place(relx=0.5, rely=0.825)

        self.AAIButton = tk.Button(self.AAIConfigWindow, text = "submit", command=self.submitAAI)
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.3)

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

        self.currentUser.AAI(self.AAILRLimit, self.AAIURLimit, self.AAIAtrialAmplitude, self.AAIAtrialPulseWidth, self.AAIAtrialSensitivity, self.AAIARP, self.AAIPVARP, self.AAIHysteresis, self.AAIRateSmoothing)
        self.db.updateUser(self.currentUser)

    def VVIConfig(self):
        self.VVIConfigWindow= tk.Toplevel(self.configModeWindow)
        self.VVIConfigWindow.geometry("800x800")

        self.LRLimitLabel= tk.Label(self.VVIConfigWindow, text="Lower Rate Limit: ")
        self.LRLimitLabel.pack()
        self.LRLimitLabel.place(relx=0.1,rely=0.2)
        self.LRLimitTextField = tk.Entry(self.VVIConfigWindow)
        self.LRLimitTextField.pack()
        self.LRLimitTextField.place(relx=0.3, rely=0.2)

        self.URLimitLabel= tk.Label(self.VVIConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.4)
        self.URLimitTextField = tk.Entry(self.VVIConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.4)

        self.VentricularAmplitudeLabel= tk.Label(self.VVIConfigWindow, text="Ventricular Amplitude: ")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1,rely=0.6)
        self.VentricularAmplitudeTextField = tk.Entry(self.VVIConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.3, rely=0.6)

        self.VentricularPulseWidthLabel= tk.Label(self.VVIConfigWindow, text="Ventricular Pulse Width: ")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1,rely=0.8)
        self.VentricularPulseWidthTextField = tk.Entry(self.VVIConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.3, rely=0.8)

        self.VentricularSensitivityLabel= tk.Label(self.VVIConfigWindow, text="Ventricular Sensitivity: ")
        self.VentricularSensitivityLabel.pack()
        self.VentricularSensitivityLabel.place(relx=0.6,rely=0.2)
        self.VentricularSensitivityTextField = tk.Entry(self.VVIConfigWindow)
        self.VentricularSensitivityTextField.pack()
        self.VentricularSensitivityTextField.place(relx=0.8, rely=0.2)

        self.VRPLabel= tk.Label(self.VVIConfigWindow, text="VRP: ")
        self.VRPLabel.pack()
        self.VRPLabel.place(relx=0.6,rely=0.4)
        self.VRPTextField = tk.Entry(self.VVIConfigWindow)
        self.VRPTextField.pack()
        self.VRPTextField.place(relx=0.8, rely=0.4)

        self.RateSmoothingLabel= tk.Label(self.VVIConfigWindow, text="Rate Smoothing: ")
        self.RateSmoothingLabel.pack()
        self.RateSmoothingLabel.place(relx=0.6,rely=0.6)
        self.RateSmoothingTextField = tk.Entry(self.VVIConfigWindow)
        self.RateSmoothingTextField.pack()
        self.RateSmoothingTextField.place(relx=0.8, rely=0.6)

        self.HysteresisLabel= tk.Label(self.VVIConfigWindow, text="Hysteresis: ")
        self.HysteresisLabel.pack()
        self.HysteresisLabel.place(relx=0.6,rely=0.8)
        self.HysteresisTextField = tk.Entry(self.VVIConfigWindow)
        self.HysteresisTextField.pack()
        self.HysteresisTextField.place(relx=0.8, rely=0.8)

        self.VVIButton = tk.Button(self.VVIConfigWindow, text = "submit", command=self.submitVVI)
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.3)

    def submitVVI(self):
        self.VVILRLimit= self.LRLimitTextField.get().strip()
        self.VVIURLimit= self.URLimitTextField.get().strip()
        self.VVIVentricularAmplitude= self.VentricularAmplitudeTextField.get().strip()
        self.VVIVentricularPulseWidth= self.VentricularPulseWidthTextField.get().strip()
        self.VVIVentricularSensitivity= self.VentricularSensitivityTextField.get().strip()
        self.VVIVRP= self.VRPTextField.get().strip()
        self.VVIHysteresis= self.HysteresisTextField.get().strip()
        self.VVIRateSmoothing= self.RateSmoothingTextField.get().strip()


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
