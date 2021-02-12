import tkinter as Tik
import random as r
from PIL import ImageTk

class Interface():
    def __init__(self):
        self.root = Tik.Tk()
        self.root.title(' GESTION BANCAIRE TK')
        self.root.geometry('600x350+180+80')
        self.root.resizable(width=False, height=False)
        #self.root.iconbitmap("icon.png")

    def corps(self):
        # self.image = PhotoImage(file='main.interphace.PNG')
        # self.background = Label(self.root, image=self.image).place(relx=0, rely=0)

        #Les entée pour l'identification
        self.mt_emprunt = Tik.IntVar()
        self.mt_emprunt_lbl = Tik.Label(self.root, text="Montant empruntée :", fg='white').place(relx=0.1, rely=0.1, width=180, height=30)
        self.mt_emprunt_ipt = Tik.Entry(self.root, textvariable=self.mt_emprunt, bg='white',font=18, borderwidth='0c',fg='blue').place(relx=0.4, rely=0.1, width=180, height=30)

        self.tx_emprunt = Tik.IntVar()
        self.tx_emprunt_lbl = Tik.Label(self.root, text="Taux emprunt:", fg='white').place(relx=0.1, rely=0.2, width=180, height=30)
        self.tx_emprunt_ipt = Tik.Entry(self.root, textvariable=self.tx_emprunt, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.4, rely=0.2, width=180, height=30)

        self.rb_mensuel  = Tik.IntVar()
        self.rb_mensuel_lbl = Tik.Label(self.root, text="Remb. Mensuel :", fg='white').place(relx=0.1, rely=0.3, width=180, height=30)
        self.rb_mensuel_ipt = Tik.Entry(self.root, textvariable=self.rb_mensuel, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.4, rely=0.3, width=180, height=30)

        self.duree_remb = Tik.IntVar()
        self.duree_remb_lbl = Tik.Label(self.root, text="Durrée Remb.:", fg='white').place(relx=0.1, rely=0.4, width=180, height=30)
        self.duree_remb_ipt = Tik.Entry(self.root, textvariable=self.duree_remb, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.4, rely=0.4, width=180, height=30)

        self.mt_total = Tik.IntVar()
        self.mt_total_lbl = Tik.Label(self.root, text="Montant Total :", fg='white').place(relx=0.1, rely=0.5, width=180, height=30)
        self.mt_total_ipt = Tik.Entry(self.root, textvariable=self.mt_total, bg='white', font=18, borderwidth='0c',fg="blue").place(relx=0.4, rely=0.5, width=180, height=30)

        self.img_btn = ImageTk.PhotoImage(file='Assets/btn.png')
        self.btn_budget_img = Tik.Button(self.root, image=self.img_btn, overrelief="flat", borderwidth='0c', highlightthickness=0).place(relx=0.55, rely=0.7)
        self.btn_budget_lbl = Tik.Button(self.root, text="Calculer", bg='#00bcd4', fg='black', font=18, overrelief="flat", borderwidth='0c', highlightthickness=0,activebackground='#00bcd4').place(relx=0.60, rely=0.72)


    

    def finale(self):
        self.root.mainloop()
    
    # def conversion(self):
    #     self.nbr_final = base.turn_in_base(self.nbr_init.get(), self.base_init.get(), self.base_final.get())
    #     self.nbr_final_input.config(text = self.nbr_final)
    #     self.nbr_final_input.update()

if __name__ == "__main__":
    fen = Interface()
    fen.corps()
    fen.finale()
