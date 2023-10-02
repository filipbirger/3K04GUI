
import sqlite3
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
            widget.destroy()  
        
        self.startWindow.title("Main Settings")
        
        self.settingLabel = tk.Label(self.startWindow, text="Welcome to Main Settings", font=('Arial', 18))
        self.userDataBook()

        self.settingLabel.pack()

    
    def submit(self):
            
            self.userNameDB.delete(0,tk.END)
            self.passwordDB.delete(0,tk.END)
            self.var1DB.delete(0,tk.END)
            self.var2DB.delete(0,tk.END)
            self.var3DB.delete(0,tk.END)
            self.var4DB.delete(0,tk.END)
            self.var5DB.delete(0,tk.END)
            self.var6DB.delete(0,tk.END)
            self.var7DB.delete(0,tk.END)
            self.var8DB.delete(0,tk.END)

   
    def userDataBook(self):
        
        userDatabase = sqlite3.connect("User_Book.db")

        cursor = userDatabase.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                userName text,
                password text,
                var1 float,
                var2 float,
                var3 float,
                var4 float,
                var5 float,
                var6 float,
                var7 float,
                var8 float,
                var9 float,
                var10 float
            )""")
         
        userDatabase.commit()
        print("worked")

        userDatabase.close()

        self.userNameDB = tk.Entry(self.startWindow, width = 30)
        self.userNameDB.grid(row = 0, column=1)
        self.passwordDB = tk.Entry(self.startWindow, width = 30)
        self.passwordDB.grid(row = 1, column=1)
        self.var1DB = tk.Entry(self.startWindow, width = 30)
        self.var1DB.grid(row = 2, column=1)
        self.var2DB = tk.Entry(self.startWindow, width = 30)
        self.var2DB.grid(row = 3, column=1)
        self.var3DB = tk.Entry(self.startWindow, width = 30)
        self.var3DB.grid(row = 4, column=1)
        self.var4DB = tk.Entry(self.startWindow, width = 30)
        self.var4DB.grid(row = 5, column=1)
        self.var5DB = tk.Entry(self.startWindow, width = 30)
        self.var5DB.grid(row = 6, column=1)
        self.var6DB = tk.Entry(self.startWindow, width = 30)
        self.var6DB.grid(row = 7, column=1)
        self.var7DB = tk.Entry(self.startWindow, width = 30)
        self.var7DB.grid(row = 8, column=1)
        self.var8DB = tk.Entry(self.startWindow, width = 30)
        self.var8DB.grid(row = 9, column=1)


        userNameLabel = tk.Label(self.startWindow, text="User Name")
        userNameLabel.grid(row=0, column=0)
        passwordLabel = tk.Label(self.startWindow, text="Password")
        passwordLabel.grid(row=1, column=0)
        var1Label = tk.Label(self.startWindow, text="var1Label")
        var1Label.grid(row=2, column=0)
        var2Label = tk.Label(self.startWindow, text="var2Label")
        var2Label.grid(row=3, column=0)
        var3Label = tk.Label(self.startWindow, text="var3Label")
        var3Label.grid(row=4, column=0)
        var4Label = tk.Label(self.startWindow, text="var4Label")
        var4Label.grid(row=5, column=0)
        var5Label = tk.Label(self.startWindow, text="var5Label")
        var5Label.grid(row=6, column=0)
        var6Label = tk.Label(self.startWindow, text="var6Label")
        var6Label.grid(row=7, column=0)
        var7Label = tk.Label(self.startWindow, text="var7Label")
        var7Label.grid(row=8, column=0)
        var8Label = tk.Label(self.startWindow, text="var8Label")
        var8Label.grid(row=9, column=0)

        submitButton = tk.Button(self.startWindow, text = "Push To DB", command=self.submit)
        submitButton.grid(row = 10, column=0, columnspan= 2, padx=10, pady= 10)
        
        


    




MyGUI()
