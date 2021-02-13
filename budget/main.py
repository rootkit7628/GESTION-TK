import tkinter as Tik
import random as r
from PIL import ImageTk
import os

class Interface():
    def __init__(self):
        # Comfigurations principale
        self.root = Tik.Tk()
        self.root.title('GESTION BUDGET')
        self.root.geometry('700x500+180+80')
        self.root.resizable(width=False, height=False)

    def corps(self): 
        
        # Compte
        self.compte = Tik.StringVar()
        self.compte_list = ('compte A','compte B','compte C','compte D')
        self.compte.set(self.compte_list[0])
        Tik.OptionMenu(self.root, self.compte, *self.compte_list).place(relx=0.45, rely=0.05, width=380, height=30)

        # Budget
        self.compte = Tik.StringVar()
        self.compte_list = ('alimentaire','épargne','sortie','sport')
        self.compte.set(self.compte_list[0])
        Tik.OptionMenu(self.root, self.compte, *self.compte_list).place(relx=0.45, rely=0.14, width=380, height=30)

        # Date
        self.compte = Tik.StringVar()
        self.compte_list = ('Oct 2010','Nov 2020','Dec 2020','Jan 2020')
        self.compte.set(self.compte_list[0])
        Tik.OptionMenu(self.root, self.compte, *self.compte_list).place(relx=0.45, rely=0.23, width=380, height=30)

        # Le Tableau des opérations
        self.tableau = Tik.Frame(self.root, bg="white")

        self.title = ['Date','Libélé','Motant','Type']
        for i in self.title:
            self.tab_title = Tik.Button(self.tableau, text=i, borderwidth='.06c', font="Verdana 9 bold", fg='black',bg='white',width=8,height=1).grid(row=0,column=self.title.index(i))

        self.data = [
            ['25/03/21','25 €','alimentaire','CB'],
            ['25/03/21','25 €','alimentaire','CB'],
            ['25/03/21','25 €','alimentaire','CB'],
        ]
        i = 1
        for x in self.data:
            for j in range(len(x)):
                Tik.Label(self.tableau, text=x[j], font = 'Verdana 9', fg='black',bg='white',width=8,height=1).grid(row=i,column=j)
            i += 1

        self.tableau.place(relx=0.45, rely=0.32, height=300)


        # Diagramme 
        self.diagramme = Tik.Frame(self.root)

        Tik.Label(self.diagramme, text='Compte A',fg='black').place(relx=0.3, rely=0.05)

        dessin = Tik.Canvas(self.diagramme, width =150, height =150)
        dessin.place(relx=0.1, rely=0.2)
        COLORS = ('#386898', '#e0edf9', '#669aca', '#669bce', '#a79aca')
        angle = 360/len(COLORS)
        for x, color in enumerate(COLORS):
            dessin.create_arc(10,10, 100, 100,style='pieslice', fill=color,start=x*angle, extent=angle)

        
        self.diagramme.place(relx=0.13, rely=0.05, width=200, height=200)


        # Bouton pour ajouté budget
        self.img_btn1 = ImageTk.PhotoImage(file='Assets/plus.png')
        Tik.Button(self.root, image=self.img_btn1, borderwidth='0.1c', highlightthickness=0, command=lambda: self.redirection('compte/budget')).place(relx=0.02, rely=0.10)
        Tik.Label(self.root, text='Virement' , fg='white').place(relx=0.02, rely=0.22)

        # Bouton pour modifier budget
        self.img_btn2 = ImageTk.PhotoImage(file='Assets/edit.png')
        Tik.Button(self.root, image=self.img_btn2, borderwidth='0.1c', highlightthickness=0, command=lambda: self.redirection('compte/budget')).place(relx=0.02, rely=0.35)
        Tik.Label(self.root, text='Compte' , fg='white').place(relx=0.025, rely=0.47)

        # Juste une note por l'uilisteur
        Tik.Label(self.root, text='Trier les opérations en cliquant sur les colonnes', fg='white').place(relx=0.5, rely=0.95)


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
