import tkinter as Tik
import random as r
from PIL import ImageTk

class Interface():
    def __init__(self):
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('300x400+180+80')
        self.root.resizable(width=False, height=False)
        #self.root.iconbitmap("icon.png")

    def corps(self):

        #Les entrée du calculatrice
        self.clcl = Tik.StringVar()
        Tik.Entry(self.root, textvariable=self.clcl, bg='white',font=18, borderwidth='0c',fg='blue').place(relx=0.1, rely=0.05, width=255, height=40)

        # Clavier virtuel
        self.clavierVirtual = Tik.Frame(self.root)
        self.list_btn = [x for x in range(0,10)]
        self.list_btn = [['+','-','*','/'],self.list_btn[7:10],self.list_btn[4:7],self.list_btn[1:4],['.',self.list_btn[0],'C']]
        for i in range(5):
            for j in range(3):
                Tik.Button(self.clavierVirtual, text=str(self.list_btn[i][j]), borderwidth='.1c', font=18, fg='black',bg='white',width=3,height=2).grid(row=i,column=j)
        Tik.Button(self.clavierVirtual, text='/', borderwidth='.1c', font=18, fg='black',bg='white',width=3,height=2).grid(row=0,column=4)
        Tik.Button(self.clavierVirtual, text='+', borderwidth='.1c', font=18, fg='black',bg='white',width=3,height=11).grid(row=1,column=4,rowspan=4)
        self.clavierVirtual.place(relx=0.1, rely=0.2)


    
    def click(self,bouton):
        return

    def finale(self):
        self.root.mainloop()

if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
