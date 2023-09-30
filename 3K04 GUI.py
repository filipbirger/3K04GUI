
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

    #def userLimitReached(self):


MyGUI()
