from tkinter import *

from tkinter import messagebox
import os
import numpy as np
from game import setup


# Load Database
database = np.load('database.npy').item()

# Setup window
root = Tk()
root.minsize(width=100, height=30)
root.title("Login")

# Global variables
cwd =  os.path.dirname(os.path.realpath(__file__)) # Current working directory
passwordFound = False


class MakeLabel:
    def __init__(self, type, rowNum, columnNum, input, win):
        if type == "label":
            label = Label(win, text=input)
            label.grid(row = rowNum, column = columnNum)
        if type == "entry":
            self.entry = Entry(win)
            self.entry.grid(row = rowNum, column = columnNum)
        if type == "button":
            button = Button(win, text=input, command= lambda: password.login(None))
            button.grid(column = columnNum)
        if type == "reg":
            button = Button(win, text=input, command= lambda: password.register(None))
            button.grid(column = columnNum)
        if type == "registerConfirm":
            button = Button(win, text=input, command= lambda: password.createUser(None))
            button.grid(column = columnNum)

    def next(self, event):
        password.entry.focus_set()

    def register(self, event):
        self.regWin = Toplevel(root)
        self.regWin.title("Register")
        MakeLabel("label", 0, 0, "New Username", self.regWin)
        self.newUsername = MakeLabel("entry", 0, 1, "", self.regWin)
        MakeLabel("label", 1, 0, "Password", self.regWin)
        self.newPassword = MakeLabel("entry", 1, 1, "", self.regWin)
        MakeLabel("label", 2, 0, "Verify Password", self.regWin)
        self.verifyPassword = MakeLabel("entry", 2, 1, "", self.regWin)
        MakeLabel("registerConfirm", 2, 0, "Confirm", self.regWin)
        self.newPassword.entry.config(show="*")
        self.verifyPassword.entry.config(show="*")


    def createUser(self, event):
        if self.newPassword.entry.get() == '':
            messagebox.showinfo("Error", "Please enter a new password")
        elif self.newPassword.entry.get() == self.verifyPassword.entry.get():
            if self.newUsername.entry.get() in database:
                messagebox.showinfo("Error", "Username already taken")
            else:
                database[self.newUsername.entry.get()] = self.newPassword.entry.get()
                np.save('database.npy', database)
                messagebox.showinfo("Success", "Registered")
                self.regWin.destroy()
        elif self.verifyPassword.entry.get() == '':
            messagebox.showinfo("Error", "Please verify your password")
        else:
            messagebox.showinfo("Error", "Passwords do not match")


    def login(self, event):
        global passwordFound
        if password.entry.get() == "":
            messagebox.showinfo("Error", "Please enter a password")
            return
        try:
            if database[username.entry.get()] == password.entry.get():
                messagebox.showinfo("Success", "Logging in")
                setup(username.entry.get())
            else:
                messagebox.showinfo("Error", "Password/username not found")
        except KeyError:
            messagebox.showinfo("Error", "Password/username not found")

# Use with caution
def clearDatabases():
    clear = {}
    np.save('database.npy', clear)
    np.save('scores.npy', clear)

# Setup Tkinter objects
MakeLabel("label", 0, 0, "Username", root)
username = MakeLabel("entry", 0, 1, "", root)
MakeLabel("label", 1, 0, "Password", root)
password = MakeLabel("entry", 1, 1, "", root)
MakeLabel("button", 2, 0, "Confirm", root)
MakeLabel("reg", 2, 0, "Register", root)
username.entry.bind("<Return>", username.next)
password.entry.bind("<Return>", password.login)
password.entry.config(show="*")

root.mainloop()
