import tkinter as Tik
import random as r
from PIL import ImageTk

class Interface():
    def __init__(self):
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x500+180+80')
        self.root.resizable(width=False, height=False)
        #self.root.iconbitmap("icon.png")

    def corps(self):

        #Les entée pour l'identification
        self.ident = Tik.StringVar()
        Tik.Label(self.root, text="N identifiant :", fg='white').place(relx=0.3, rely=0.1, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.ident, bg='white',font=18, borderwidth='0c',fg='blue').place(relx=0.6, rely=0.1, width=180, height=30)

        self.passw = Tik.StringVar()
        Tik.Label(self.root, text="Password :", fg='white').place(relx=0.3, rely=0.2, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.passw, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.6, rely=0.2, width=180, height=30)

        # Clavier virtuel
        self.clavierVirtual = Tik.Frame(self.root)
        self.list_btn = [x for x in range(0,10)]
        r.shuffle(self.list_btn)
        self.list_btn = [self.list_btn[0:3],self.list_btn[3:6],self.list_btn[6:9],['X',self.list_btn[9],'V']]
        for i in range(4):
            for j in range(3):
                Tik.Button(self.clavierVirtual, text=str(self.list_btn[i][j]), borderwidth='.2c', font=18, fg='black',bg='white').grid(row=i,column=j)
        self.clavierVirtual.place(relx=0.6, rely=0.4)

        # Le logo
        self.logo_img = ImageTk.PhotoImage(file='Assets/logo.png')
        Tik.Label(self.root, image=self.logo_img).place(relx=0.15, rely=0.4)
    
    def click(self,bouton):
        return

    def finale(self):
        self.root.mainloop()


if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
