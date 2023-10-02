import sqlite3 
import userClass
import tkinter as tk
import MyGUI

class DataBase:
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

    
    def __init__(self):
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

        userDatabase.commit()
        print("worked")

        userDatabase.close()
        