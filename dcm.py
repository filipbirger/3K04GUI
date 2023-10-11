import tkinter as tk
import userClass 
import sqlite3
from DataBase import DataBase

class MyGUI:

    userlist = []

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
        
        print(user)


        if user and user[1] == inputPassword:  
            self.loginWindow.destroy()
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
        self.configModeWindow.geometry("700x800")
        self.fix2= tk.Label(self.configModeWindow, text="IN PROGRESS",font=('Arial', 18))
        self.fix2.pack()

        self.VOOButton = tk.Button(self.configModeWindow, text = "Set VOO Option", command=self.VOOWindow)
        self.VOOButton.pack()
        self.VOOButton.place(relx=0.2, rely=0.2, relwidth=0.3, relheight=0.05)

        self.AOOButton = tk.Button(self.configModeWindow, text = "Set AOO Option")
        self.AOOButton.pack()
        self.AOOButton.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.05)


        self.AAIButton = tk.Button(self.configModeWindow, text = "Set AAI Option")
        self.AAIButton.pack()
        self.AAIButton.place(relx=0.2, rely=0.4, relwidth=0.3, relheight=0.05)


        self.VVIButton = tk.Button(self.configModeWindow, text = "Set VVI Option")
        self.VVIButton.pack()
        self.VVIButton.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.05)

    def VOOWindow(self):
        self.vooWindow=tk.Toplevel(self.configModeWindow)
        self.vooWindow.geometry("800x800")

        self.lowerRateLimit = tk.Entry(self.vooWindow, width = 30)
        self.lowerRateLimit.grid(row=0, column=1, padx = 20)

        self.upperRateLimit = tk.Entry(self.vooWindow, width = 30)
        self.upperRateLimit.grid(row=1, column=1)
        
        self.ventricularAmplitude = tk.Entry(self.vooWindow, width = 30)
        self.ventricularAmplitude.grid(row=2, column=1)
        
        self.atrialPulseWidth = tk.Entry(self.vooWindow, width = 30)
        self.atrialPulseWidth.grid(row=3, column=1)
        


        self.lowerRateLimitLabel = tk.Label(self.vooWindow,text="Lower Rate Limit:")
        self.lowerRateLimitLabel.grid(row=0,column=0)

        self.upperRateLimitLabel = tk.Label(self.vooWindow,text="Upper Rate Limit:")
        self.upperRateLimitLabel.grid(row=1,column=0)

        self.ventricularAmplitudeLabel = tk.Label(self.vooWindow,text="Ventricular Amplitude:")
        self.ventricularAmplitudeLabel.grid(row=2,column=0)

        self.atrialPulseWidthLabel = tk.Label(self.vooWindow, text = "Atrial Pulse Width:")
        self.atrialPulseWidthLabel.grid(row=3,column=0)



        self.submitButton = tk.Button(self.vooWindow, text="Submit", command= self.submit)
        self.submitButton.grid(row=4, column=0 ,columnspan=2,padx=10,pady=10,ipadx=100)

    #def submit(self):
        
    def __del__(self):
        self.db.close()



    


MyGUI()
