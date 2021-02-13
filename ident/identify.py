from sys import version_info
if version_info.major == 2:
    import Tkinter as Tik
elif version_info.major == 3:
    import tkinter as Tik

import os,sys
sys.path.append(os.path.abspath(''))
from ident.cryptage import cryptage

import random as r
from PIL import ImageTk

class Interface():
    def __init__(self):
        # Configuration de la fenêtre
        
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x500+350+80')
        self.root.resizable(width=False, height=False)        


    def corps(self):
        self.focus_ipt = None
        #Les entée pour l'identification
        self.ident = Tik.StringVar()
        Tik.Label(self.root, text="N identifiant :", fg='white').place(relx=0.3, rely=0.1, width=180, height=30)
        self.ident_ipt = Tik.Entry(self.root, textvariable=self.ident, bg='white',font=18, borderwidth='0c',fg='blue')
        self.ident_ipt.place(relx=0.6, rely=0.1, width=180, height=30)
        self.ident_ipt.bind("<FocusIn>", self.handle_focus)
        self.ident_ipt.bind("<FocusOut>", self.remove_focus)

        self.passw = Tik.StringVar()
        Tik.Label(self.root, text="Password :", fg='white').place(relx=0.3, rely=0.2, width=180, height=30)
        self.passw_ipt = Tik.Entry(self.root, textvariable=self.passw, bg='white', font=18, borderwidth='0c',fg="blue")
        self.passw_ipt.place(relx=0.6, rely=0.2, width=180, height=30)
        self.passw_ipt.bind("<FocusIn>", self.handle_focus)
        self.passw_ipt.bind("<FocusOut>", self.remove_focus)

        # Clavier virtuel
        self.clavierVirtual = Tik.Frame(self.root)
        self.list_btn = [x for x in range(0,10)]
        r.shuffle(self.list_btn)
        self.list_btn = [self.list_btn[0:3],self.list_btn[3:6],self.list_btn[6:9],['X',self.list_btn[9],'V']]
        self.list_btn_for=[]


        Tik.Button(self.clavierVirtual, text=str(self.list_btn[0][0]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[0][0]))).grid(row=0,column=0)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[0][1]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[0][1]))).grid(row=0,column=1)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[0][2]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[0][2]))).grid(row=0,column=2)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[1][0]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[1][0]))).grid(row=1,column=0)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[1][1]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[1][1]))).grid(row=1,column=1)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[1][2]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[1][2]))).grid(row=1,column=2)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[2][0]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[2][0]))).grid(row=2,column=0)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[2][1]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[2][1]))).grid(row=2,column=1)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[2][2]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[2][2]))).grid(row=2,column=2)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[3][0]), borderwidth='.2c', font=18, fg='black',bg='white', command=self.root.destroy).grid(row=3,column=0)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[3][1]), borderwidth='.2c', font=18, fg='black',bg='white', command=lambda: self.ecrire(str(self.list_btn[3][1]))).grid(row=3,column=1)
        Tik.Button(self.clavierVirtual, text=str(self.list_btn[3][2]), borderwidth='.2c', font=18, fg='black',bg='white', command=self.identifier).grid(row=3,column=2)


        self.clavierVirtual.place(relx=0.6, rely=0.4)

        # Le logo
        self.logo_img = ImageTk.PhotoImage(file='Assets/logo.png')
        Tik.Label(self.root, image=self.logo_img).place(relx=0.15, rely=0.4)
    

    def identifier(self):
        self.root.destroy()
        try:
            os.system('python ident/dashboard.py')
        except:
            os.system('python3 ident/dashboard.py')
            try:
                os.system('py ident/dashboard.py')
            except Exception as e:
                print('[ Erreur ] : ', e, 'Python is not installed in your computer')

    
    def ecrire(self,x):
       if self.focus_ipt:
        self.focus_ipt.insert(Tik.INSERT, x)
    

    def handle_focus(self, event):
        if self.ident_ipt == event.widget:
            self.focus_ipt = self.ident_ipt
        elif self.passw_ipt == event.widget:
            self.focus_ipt = self.passw_ipt

    def remove_focus(self, event):
        self.focus_ipt = None

    def finale(self):
        self.root.mainloop()


if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
