import tkinter as tk

class User:
    def __init__(self, username, password):
        self.username = username
        self.password= password
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def setUsername(self, name):
        self.username = name

    def setPassword(self, p):
        self.password = p

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
            MyGUI.userlist.append(User(inputName, inputPassword))
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
        self.configModeWindow= tk.Toplevel(self.defaultWindow)
        self.configModeWindow.geometry("800x800")
        self.fix2= tk.Label(self.configModeWindow, text="IN PROGRESS",font=('Arial', 18))
        self.fix2.pack()

MyGUI()