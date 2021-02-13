import tkinter as Tik
import random as r
from PIL import ImageTk
import os

class Interface():
    def __init__(self):
        # Comfigurations principale
        self.root = Tik.Tk()
        self.root.title(' GESTION COMPTE')
        self.root.geometry('700x500+180+80')
        self.root.resizable(width=False, height=False)

    def corps(self): 
        # Solde
        self.solde = 4536
        self.solde_lbl = Tik.Label(self.root, text="Solde du compte : "+str(self.solde)+"€" , fg='white').place(relx=0.1, rely=0.1)
 
        # Les entée pour l'identification
        self.compte = Tik.StringVar()
        self.compte_list = ('compte A','compte B','compte C','compte D')
        self.compte.set(self.compte_list[0])
        Tik.OptionMenu(self.root, self.compte, *self.compte_list).place(relx=0.5, rely=0.08, width=300, height=30)


        # Le Tableau des comptes et transactions 
        self.tableau = Tik.Frame(self.root, bg="white")

        self.title = ['Date','Libélé','Motant','budget','Type','Vérification']
        for i in self.title:
            self.tab_title = Tik.Button(self.tableau, text=i, borderwidth='.06c', font="Verdana 9 bold", fg='black',bg='white',width=8,height=1).grid(row=0,column=self.title.index(i))

        self.data = [
            ['25/03/21','F-Society',"25 €",'alimentaire','CB','OK'],
            ['25/03/21','F-Society',"25 €",'alimentaire','CB','OK'],
            ['25/03/21','F-Society',"25 €",'alimentaire','CB','OK'],
        ]
        i = 1
        for x in self.data:
            for j in range(len(x)):
                Tik.Label(self.tableau, text=x[j], font = "Verdana 9", fg='black',bg='white',width=8,height=1).grid(row=i,column=j)
            i += 1

        self.tableau.place(relx=0.15, rely=0.2, height=300)

        self.img_btn1 = ImageTk.PhotoImage(file='Assets/plus.png')
        Tik.Button(self.root, image=self.img_btn1, borderwidth='0.1c', highlightthickness=0, command=lambda: self.redirection('compte/operation')).place(relx=0.02, rely=0.25)
        Tik.Label(self.root, text='Opérations' , fg='white').place(relx=0.015, rely=0.37)

        Tik.Button(self.root, image=self.img_btn1, borderwidth='0.1c', highlightthickness=0, command=lambda: self.redirection('compte/virement')).place(relx=0.02, rely=0.45)
        Tik.Label(self.root, text='Virement' , fg='white').place(relx=0.02, rely=0.57)

        Tik.Button(self.root, image=self.img_btn1, borderwidth='0.1c', highlightthickness=0, command=lambda: self.redirection('compte/compte')).place(relx=0.02, rely=0.65)
        Tik.Label(self.root, text='Compte' , fg='white').place(relx=0.025, rely=0.77)


        Tik.Label(self.root, text='''Trier les opérations en cliquant sur l'intitulé d'une colonne\n
            pour modifiers son contenu''' , fg='white').place(relx=0.25, rely=0.85)

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
