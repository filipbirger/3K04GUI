import tkinter as tk
import userClass 


class MyGUI:

    userlist = []

    def __init__(self):
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
        if len(MyGUI.userlist) < 10:
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
        else:
            print("Cannot create more users, limit reached.")

    def populateUserInfo(self):
        inputName = self.userNameTextField.get().strip()
        inputPassword = self.userPasswordTextField.get().strip()
        if inputName and inputPassword:
            MyGUI.userlist.append(userClass.userClass(inputName, inputPassword))
            print([user.username for user in MyGUI.userlist])
            self.newUserWindow.destroy()

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

        for user in MyGUI.userlist:
            if user.username == inputName and user.password == inputPassword:
                self.loginWindow.destroy()
                self.createMainSettingWindow()
                return
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

    #def userLimitReached(self):

    def getPrevMode(self):
        #ADD CONDITION IF NEW USER PRESSES THE YES BUTTON SAYING ERROR
        self.prevInfoWindow = tk.Toplevel(self.startWindow)
        self.prevInfoWindow.geometry("800x800")

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

        self.URLimitLabel= tk.Label(self.VOOConfigWindow, text="Upper Rate Limit: ")
        self.URLimitLabel.pack()
        self.URLimitLabel.place(relx=0.1,rely=0.4)
        self.URLimitTextField = tk.Entry(self.VOOConfigWindow)
        self.URLimitTextField.pack()
        self.URLimitTextField.place(relx=0.3, rely=0.4)

        self.VentricularAmplitudeLabel= tk.Label(self.VOOConfigWindow, text="Ventricular Amplitude: ")
        self.VentricularAmplitudeLabel.pack()
        self.VentricularAmplitudeLabel.place(relx=0.1,rely=0.6)
        self.VentricularAmplitudeTextField = tk.Entry(self.VOOConfigWindow)
        self.VentricularAmplitudeTextField.pack()
        self.VentricularAmplitudeTextField.place(relx=0.3, rely=0.6)

        self.VentricularPulseWidthLabel= tk.Label(self.VOOConfigWindow, text="Ventricular Pulse Width: ")
        self.VentricularPulseWidthLabel.pack()
        self.VentricularPulseWidthLabel.place(relx=0.1,rely=0.8)
        self.VentricularPulseWidthTextField = tk.Entry(self.VOOConfigWindow)
        self.VentricularPulseWidthTextField.pack()
        self.VentricularPulseWidthTextField.place(relx=0.3, rely=0.8)

        VOOLRLimit= self.LRLimitTextField
        VOOURLimit= self.URLimitTextField
        VOOVentricularAmplitude= self.VentricularAmplitudeTextField
        VOOVentricularPulseWidth= self.VentricularPulseWidthTextField
    
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

        AOOLRLimit= self.LRLimitTextField
        AOOURLimit= self.URLimitTextField
        AOOAtrialAmplitude= self.AtrialAmplitudeTextField
        AOOAtrialPulseWidth= self.AtrialPulseWidthTextField

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


        AAILRLimit= self.LRLimitTextField
        AAIURLimit= self.URLimitTextField
        AAIAtrialAmplitude= self.AtrialAmplitudeTextField
        AAIAtrialPulseWidth= self.AtrialPulseWidthTextField
        AAIAtrialSensitivity= self.AtrialSensitivityTextField
        AAIARP= self.ARPTextField
        AAIPVARP= self.PVARPTextField
        AAIHysteresis= self.HysteresisTextField
        AAIRateSmoothing= self.RateSmoothingTextField

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

        VVILRLimit= self.LRLimitTextField
        VVIURLimit= self.URLimitTextField
        VVIVentricularAmplitude= self.VentricularAmplitudeTextField
        VVIVentricularPulseWidth= self.VentricularPulseWidthTextField
        VVIVentricularSensitivity= self.VentricularSensitivityTextField
        VVIVRP= self.VRPTextField
        VVIHysteresis= self.HysteresisTextField
        VVIRateSmoothing= self.RateSmoothingTextField

MyGUI()
