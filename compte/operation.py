import tkinter as Tik
from PIL import ImageTk


class Interface():
    def __init__(self):
        # Comfigurations principale
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x350+180+80')
        self.root.resizable(width=False, height=False)


    def corps(self):

        # Compte
        self.compte = Tik.StringVar()
        self.compte_list = ('compte A','compte B','compte C','compte D')
        self.compte.set(self.compte_list[0])
        Tik.Label(self.root, text="Compte :", fg='white').place(relx=0.1, rely=0.05, width=180, height=30)
        Tik.OptionMenu(self.root, self.compte, *self.compte_list).place(relx=0.2, rely=0.15, width=300, height=30)


        # Montant de l'opération
        self.mt_operation  = Tik.StringVar()
        Tik.Label(self.root, text="Montant de l'opération :", fg='white').place(relx=0.20, rely=0.30, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.mt_operation, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.30, width=180, height=30)

         # Libéllée
        self.libelle  = Tik.StringVar()
        Tik.Label(self.root, text="Libéllée de l'opération :", fg='white').place(relx=0.20, rely=0.40, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.libelle, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.40, width=180, height=30)

        # Raison du buget
        self.budget = Tik.StringVar()
        self.budget = ('sport','sortie','alimentaire','epargne')
        self.compte.set(self.compte_list[0])
        Tik.Label(self.root, text="Compte :", fg='white').place(relx=0.1, rely=0.50, width=180, height=30)
        Tik.OptionMenu(self.root, self.compte, *self.compte_list).place(relx=0.2, rely=0.60, width=300, height=30)

        # Vérifier
        Tik.Checkbutton(self.root, text = "vérifier", height = 2, width = 10).place(relx=0.2, rely=0.7)
        # Date
        self.date  = Tik.StringVar()
        Tik.Entry(self.root, textvariable=self.date, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.7, width=180, height=30)

         # Boutton valider
        self.img_btn = ImageTk.PhotoImage(file='Assets/btn.png')
        Tik.Button(self.root, image=self.img_btn, overrelief="flat", borderwidth='0c', highlightthickness=0).place(relx=0.7, rely=0.85)
        Tik.Button(self.root, text="Valider", bg='#00bcd4', fg='black', font=18, overrelief="flat", borderwidth='0c', highlightthickness=0,activebackground='#00bcd4').place(relx=0.75, rely=0.88)


    
    def finale(self):
        self.root.mainloop()


if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
