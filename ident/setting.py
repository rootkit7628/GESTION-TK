import tkinter as Tik
from PIL import ImageTk

class Interface():
    def __init__(self):
        # Configuration de la fenêtre
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x350+180+80')
        self.root.resizable(width=False, height=False)


    def corps(self):

        # Compte pour l'aperçu
        self.compte = Tik.StringVar()
        self.compte_list = ('compte A','compte B','compte C','compte D')
        self.compte.set(self.compte_list[0])
        Tik.Label(self.root, text="Compte pour l'aperçu :", fg='white', anchor="e", justify=Tik.LEFT).place(relx=0.1, rely=0.1, width=180, height=30)
        Tik.OptionMenu(self.root, self.compte, *self.compte_list).place(relx=0.2, rely=0.2, width=300, height=30)

        # Borne minimale
        self.borne_min = Tik.IntVar()
        Tik.Label(self.root, text="Borne minimale :", fg='white').place(relx=0.2, rely=0.4, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.borne_min, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.4, width=180, height=30)

        # Borne maximale
        self.borne_max  = Tik.IntVar()
        Tik.Label(self.root, text="Borne maximale :", fg='white').place(relx=0.2, rely=0.5, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.borne_max, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.5, width=180, height=30)

        self.img_btn = ImageTk.PhotoImage(file='Assets/btn.png')
        Tik.Button(self.root, image=self.img_btn, overrelief="flat", borderwidth='0c', highlightthickness=0).place(relx=0.55, rely=0.7)
        Tik.Button(self.root, text="Valider", bg='#00bcd4', fg='black', font=18, overrelief="flat", borderwidth='0c', highlightthickness=0,activebackground='#00bcd4').place(relx=0.60, rely=0.72)

    
    def finale(self):
        self.root.mainloop()
    

if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
