from sys import version_info
if version_info.major == 2:
    import Tkinter as Tik
elif version_info.major == 3:
    import tkinter as Tik

import random as r
from PIL import ImageTk
import os

class Interface():
    def __init__(self):
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x500+350+80')
        self.root.resizable(width=False, height=False)
        #self.root.iconbitmap("icon.png")

    def corps(self):
        # self.image = PhotoImage(file='main.interphace.PNG')
        # self.background = Label(self.root, image=self.image).place(relx=0, rely=0)

        #Nom d'utilisateur 
        self.username = "Lucie Voary"
        Tik.Label(self.root, text="Bienvenu, \n"+self.username, fg='white', font=25, anchor="e", justify=Tik.LEFT).place(relx=0.1, rely=0.1)

        # Image user
        self.logo_img = ImageTk.PhotoImage(file='Assets/user.png')
        Tik.Label(self.root, image=self.logo_img).place(relx=0.7, rely=0.05)

        # Jauge 
        self.jauge = Tik.Frame(self.root, bg='white', width=460, height=100)
        self.jauge.place(relx=0.1, rely=0.3)


        # Menu du dashboard 
        self.menu_frame1 = Tik.Frame(self.root, width=460, height=100)
        self.img_btn = ImageTk.PhotoImage(file='Assets/btn.png')

        Tik.Button(self.menu_frame1, image=self.img_btn, borderwidth='0c', highlightthickness=0, command=lambda: self.redirection('compte/main')).place(relx=0.15, rely=0.4)
        Tik.Button(self.menu_frame1, text="Comptes", bg='#00bcd4', fg='black', font=18, overrelief="flat", borderwidth='0c', highlightthickness=0,activebackground='#00bcd4', command=lambda: self.redirection('compte/main')).place(relx=0.20, rely=0.50)

        Tik.Button(self.menu_frame1, image=self.img_btn, borderwidth='0c', highlightthickness=0, command=lambda: self.redirection('compte/main')).place(relx=0.55, rely=0.4)
        Tik.Button(self.menu_frame1, text="Budget", bg='#00bcd4', fg='black', font=18, overrelief="flat", borderwidth='0c', highlightthickness=0,activebackground='#00bcd4', command=lambda: self.redirection('compte/main')).place(relx=0.60, rely=0.50)
        self.menu_frame1.place(relx=0.1, rely=0.5)

        # Menu du outils
        self.menu_frame2 = Tik.Frame(self.root, width=460, height=100)

        self.img_btn1 = ImageTk.PhotoImage(file='Assets/clcl.png')
        Tik.Button(self.menu_frame2, image=self.img_btn1, borderwidth='0.05c', highlightthickness=0, command=lambda: self.redirection('ident/calculate')).place(relx=0.20, rely=0.3)
        
        self.img_btn2 = ImageTk.PhotoImage(file='Assets/home.png')
        Tik.Button(self.menu_frame2, image=self.img_btn2, borderwidth='0.05c', highlightthickness=0, command=lambda: self.redirection('ident/emprunt')).place(relx=0.45, rely=0.3)
        
        self.img_btn3 = ImageTk.PhotoImage(file='Assets/edit.png')
        Tik.Button(self.menu_frame2, image=self.img_btn3, borderwidth='0.05c', highlightthickness=0, command=lambda: self.redirection('ident/setting')).place(relx=0.70, rely=0.3)
  
        self.menu_frame2.place(relx=0.1, rely=0.7)
         

    def redirection(self,path):
        try:
            os.system('python '+path+'.py')
        except:
            os.system('py '+path+'.py')
            try:
                os.system('python3 '+path+'.py')
            except: pass

    def finale(self):
        self.root.mainloop()


if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
