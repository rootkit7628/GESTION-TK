import tkinter as Tik
from PIL import ImageTk


class Interface():
    def __init__(self):
        # Comfigurations princpale
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x350+180+80')
        self.root.resizable(width=False, height=False)
        #self.root.iconbitmap("icon.png")


    def corps(self):

        # Compte à débiter
        self.compte = Tik.StringVar()
        self.compte_list = ('compte A','compte B','compte C','compte D')
        self.compte.set(self.compte_list[0])
        Tik.Label(self.root, text="Compte à créditer :", fg='white').place(relx=0.1, rely=0.1, width=180, height=30)
        Tik.OptionMenu(self.root, self.compte, *self.compte_list).place(relx=0.2, rely=0.2, width=300, height=30)

        # Compte à débiter
        self.livret = Tik.StringVar()
        self.livret_list = ('Livret A','Livret B','Livret C','Livret D')
        self.livret.set(self.livret_list[0])
        Tik.Label(self.root, text="Compte à débiter :", fg='white').place(relx=0.1, rely=0.3, width=180, height=30)
        Tik.OptionMenu(self.root, self.livret, *self.livret_list).place(relx=0.2, rely=0.4, width=300, height=30)

        # Montant du virement
        self.mt_virem  = Tik.StringVar()
        Tik.Label(self.root, text="Montant du virement :", fg='white').place(relx=0.20, rely=0.55, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.mt_virem, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.55, width=180, height=30)

        # Vérifier
        Tik.Checkbutton(self.root, text = "vérifier", height = 2, width = 10).place(relx=0.2, rely=0.65)
        # Date
        self.date  = Tik.StringVar()
        Tik.Entry(self.root, textvariable=self.date, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.65, width=180, height=30)

         # Boutton valider
        self.img_btn = ImageTk.PhotoImage(file='Assets/btn.png')
        Tik.Button(self.root, image=self.img_btn, overrelief="flat", borderwidth='0c', highlightthickness=0).place(relx=0.6, rely=0.8)
        Tik.Button(self.root, text="Valider", bg='#00bcd4', fg='black', font=18, overrelief="flat", borderwidth='0c', highlightthickness=0,activebackground='#00bcd4').place(relx=0.65, rely=0.83)


    
    def finale(self):
        self.root.mainloop()


if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
