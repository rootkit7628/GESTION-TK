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
        # self.image = PhotoImage(file='main.interphace.PNG')
        # self.background = Label(self.root, image=self.image).place(relx=0, rely=0)

        #Nom d'utilisateur 
        self.username = "Arleme Johson"
        self.welcome = Tik.Label(self.root, text="Bienvenu, \n"+self.username, fg='white', font=25).place(relx=0.1, rely=0.2)

        # Image user
        self.logo_img = ImageTk.PhotoImage(file='Assets/user.png')
        self.logo = Tik.Label(self.root, image=self.logo_img).place(relx=0.7, rely=0.15)

        self.jauge = Tik.Frame(self.root, bg='white')
        self.jauge.place(relx=0.6, rely=0.4)


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
