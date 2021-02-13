import tkinter as Tik
from PIL import ImageTk

class Interface():
    def __init__(self):
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x350+180+80')
        self.root.resizable(width=False, height=False)


    def corps(self):
        # Montant empruntée
        self.mt_emprunt = Tik.IntVar()
        Tik.Label(self.root, text="Montant empruntée :", fg='white').place(relx=0.1, rely=0.1, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.mt_emprunt, bg='white',font=18, borderwidth='0c',fg='blue').place(relx=0.4, rely=0.1, width=180, height=30)

        # Taux emprunt:
        self.tx_emprunt = Tik.IntVar()
        Tik.Label(self.root, text="Taux emprunt:", fg='white').place(relx=0.1, rely=0.2, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.tx_emprunt, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.4, rely=0.2, width=180, height=30)

        # Remb. Mensuel
        self.rb_mensuel  = Tik.IntVar()
        Tik.Label(self.root, text="Remb. Mensuel :", fg='white').place(relx=0.1, rely=0.3, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.rb_mensuel, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.4, rely=0.3, width=180, height=30)

        # Durrée Remb.
        self.duree_remb = Tik.IntVar()
        Tik.Label(self.root, text="Durrée Remb.:", fg='white').place(relx=0.1, rely=0.4, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.duree_remb, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.4, rely=0.4, width=180, height=30)

        # Montant Total
        self.mt_total = Tik.IntVar()
        Tik.Label(self.root, text="Montant Total :", fg='white').place(relx=0.1, rely=0.5, width=180, height=30)
        Tik.Entry(self.root, textvariable=self.mt_total, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.4, rely=0.5, width=180, height=30)

        # Montant empruntée
        self.img_btn = ImageTk.PhotoImage(file='Assets/btn.png')
        Tik.Button(self.root, image=self.img_btn, overrelief="flat", borderwidth='0c', highlightthickness=0).place(relx=0.55, rely=0.7)
        Tik.Button(self.root, text="Calculer", bg='#00bcd4', fg='black', font=18, overrelief="flat", borderwidth='0c', highlightthickness=0,activebackground='#00bcd4').place(relx=0.60, rely=0.72)


    def finale(self):
        self.root.mainloop()
    

if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
