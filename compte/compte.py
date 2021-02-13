import tkinter as Tik
from PIL import ImageTk


class Interface():
    def __init__(self):
        # Configurations princpale
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x200+180+80')
        self.root.resizable(width=False, height=False)


    def corps(self):

        # Libéllée du compte
        self.mt_operation  = Tik.StringVar()
        Tik.Label(self.root, text="Libéllée du compte :", fg='white').place(relx=0.1, rely=0.1, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.mt_operation, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.1, width=180, height=30)

         # Solde de compte
        self.libelle  = Tik.StringVar()
        Tik.Label(self.root, text="Solde de compte :", fg='white').place(relx=0.1, rely=0.3, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.libelle, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.5, rely=0.3, width=180, height=30)

 
         # Boutton valider
        self.img_btn = ImageTk.PhotoImage(file='Assets/btn.png')
        Tik.Button(self.root, image=self.img_btn, overrelief="flat", borderwidth='0c', highlightthickness=0).place(relx=0.7, rely=0.5)
        Tik.Button(self.root, text="Valider", bg='#00bcd4', fg='black', font=18, overrelief="flat", borderwidth='0c', highlightthickness=0,activebackground='#00bcd4').place(relx=0.75, rely=0.55)


    
    def finale(self):
        self.root.mainloop()


if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
