"""Sign-in with a shuffled keypad, and opening a new customer file."""

import tkinter as tk
from tkinter import ttk

from .. import security
from ..bank import BankError
from . import theme
from .widgets import Message, card


class Brand(tk.Frame):
    """The dark left panel shown on the sign-in screens."""

    def __init__(self, parent):
        super().__init__(parent, bg=theme.SIDEBAR, padx=48, pady=48)
        tk.Label(
            self, text="Gestion TK", bg=theme.SIDEBAR, fg="#FFFFFF", font=theme.FONTS["h1"]
        ).pack(anchor="w")
        tk.Label(
            self,
            text="Ta banque, sur ton bureau.",
            bg=theme.SIDEBAR,
            fg="#9FC3BA",
            font=theme.FONTS["body"],
        ).pack(anchor="w", pady=(6, 0))
        tk.Frame(self, bg=theme.SIDEBAR).pack(fill="both", expand=True)
        for line in (
            "Code saisi au clavier virtuel, chiffres mélangés",
            "Accès bloqué 15 minutes après 3 erreurs",
            "Déconnexion automatique après 5 minutes",
        ):
            tk.Label(
                self, text=f"■  {line}", bg=theme.SIDEBAR, fg="#9FC3BA", font=theme.FONTS["small"]
            ).pack(anchor="w", pady=3)


class LoginScreen(ttk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.pin = ""

        Brand(self).pack(side="left", fill="y")
        right = ttk.Frame(self, padding=40)
        right.pack(side="left", fill="both", expand=True)
        box = card(right, padding=32)
        box.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(box, text="Connexion", style="CardH2.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w"
        )
        ttk.Label(box, text="NUMÉRO CLIENT", style="Field.TLabel").grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(18, 4)
        )
        check = (self.register(lambda v: v == "" or (v.isdigit() and len(v) <= 8)), "%P")
        self.number = ttk.Entry(
            box, validate="key", validatecommand=check, font=theme.FONTS["amount"]
        )
        self.number.grid(row=2, column=0, columnspan=3, sticky="ew")

        ttk.Label(
            box, text="CODE SECRET (6 CHIFFRES, AVEC LE CLAVIER CI-DESSOUS)", style="Field.TLabel"
        ).grid(row=3, column=0, columnspan=3, sticky="w", pady=(18, 4))
        self.dots = ttk.Label(
            box, text="", style="Card.TLabel", font=theme.FONTS["pin"], anchor="center"
        )
        self.dots.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        # Ten digits in a new order at each sign-in, then "erase" and "validate"
        digits = security.keypad_layout()
        cells = digits[:9] + ["⌫", digits[9], "OK"]
        for i, label in enumerate(cells):
            r, c = divmod(i, 3)
            if label == "⌫":
                cmd, style = self.erase, "Key.TButton"
            elif label == "OK":
                cmd, style, label = self.submit, "Primary.TButton", "Valider"
            else:
                cmd, style = (lambda d=label: self.press(d)), "Key.TButton"
            ttk.Button(box, text=label, style=style, command=cmd, width=6).grid(
                row=5 + r, column=c, sticky="nsew", padx=3, pady=3
            )

        self.message = Message(box)
        self.message.grid(row=9, column=0, columnspan=3, sticky="w", pady=(12, 0))
        ttk.Button(
            box,
            text="Nouveau client ? Ouvrir un compte",
            style="Link.TButton",
            command=lambda: app.show(OpenScreen),
        ).grid(row=10, column=0, columnspan=3, sticky="w", pady=(8, 0))
        box.columnconfigure((0, 1, 2), weight=1, uniform="keys")
        self.bind_all(
            "<BackSpace>", lambda e: self.erase() if self.focus_get() != self.number else None
        )
        self.number.focus_set()
        self.number.bind("<Return>", lambda e: self.submit())

    def press(self, digit: str) -> None:
        if len(self.pin) < security.PIN_LENGTH:
            self.pin += digit
            self._show_pin()

    def erase(self) -> None:
        self.pin = self.pin[:-1]
        self._show_pin()

    def _show_pin(self) -> None:
        self.dots.configure(
            text=" ".join("●" * len(self.pin) + "○" * (security.PIN_LENGTH - len(self.pin)))
        )
        self.message.clear()

    def submit(self) -> None:
        number = self.number.get().strip()
        if len(number) != 8:
            self.message.error("Le numéro client compte 8 chiffres.")
            return
        if len(self.pin) != security.PIN_LENGTH:
            self.message.error("Compose les 6 chiffres de ton code.")
            return
        try:
            customer = self.app.bank.login(number, self.pin)
        except BankError as err:
            self.pin = ""
            self._show_pin()
            self.message.error(str(err))
            return
        self.app.signed_in(customer)

    def destroy(self):
        self.unbind_all("<BackSpace>")
        super().destroy()


class OpenScreen(ttk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        Brand(self).pack(side="left", fill="y")
        right = ttk.Frame(self, padding=40)
        right.pack(side="left", fill="both", expand=True)
        box = card(right, padding=32)
        box.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(box, text="Ouvrir un compte", style="CardH2.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            box,
            text="Tu recevras un compte courant et un livret d'épargne.",
            style="CardMuted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 8))
        self.name = self._entry(box, "NOM COMPLET", 2)
        self.pin = self._entry(box, "CODE SECRET : 6 CHIFFRES", 4, secret=True)
        self.pin2 = self._entry(box, "CONFIRME LE CODE", 6, secret=True)
        self.message = Message(box)
        self.message.grid(row=8, column=0, sticky="w", pady=(12, 0))
        actions = ttk.Frame(box, style="Plain.TFrame")
        actions.grid(row=9, column=0, sticky="ew", pady=(14, 0))
        ttk.Button(
            actions, text="Ouvrir mon compte", style="Primary.TButton", command=self.submit
        ).pack(side="left")
        ttk.Button(actions, text="Retour", command=lambda: app.show(LoginScreen)).pack(
            side="left", padx=8
        )
        self.name.focus_set()

    def _entry(self, box, label, row, secret=False):
        ttk.Label(box, text=label, style="Field.TLabel").grid(
            row=row, column=0, sticky="w", pady=(12, 4)
        )
        e = ttk.Entry(box, width=34, show="●" if secret else "")
        e.grid(row=row + 1, column=0, sticky="ew")
        e.bind("<Return>", lambda ev: self.submit())
        return e

    def submit(self) -> None:
        if self.pin.get() != self.pin2.get():
            self.message.error("Les deux codes sont différents.")
            return
        try:
            customer = self.app.bank.open_customer(self.name.get(), self.pin.get())
        except BankError as err:
            self.message.error(str(err))
            return
        self.app.show(Welcome, customer=customer)


class Welcome(ttk.Frame):
    def __init__(self, app, customer):
        super().__init__(app.root)
        Brand(self).pack(side="left", fill="y")
        right = ttk.Frame(self, padding=40)
        right.pack(side="left", fill="both", expand=True)
        box = card(right, padding=32)
        box.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(box, text=f"Bienvenue, {customer.name}", style="CardH2.TLabel").pack(anchor="w")
        ttk.Label(
            box, text="Ton numéro client, à garder pour te connecter :", style="CardMuted.TLabel"
        ).pack(anchor="w", pady=(12, 4))
        ttk.Label(box, text=customer.number, style="Amount.TLabel").pack(anchor="w")
        ttk.Button(
            box, text="Me connecter", style="Primary.TButton", command=lambda: app.show(LoginScreen)
        ).pack(anchor="w", pady=(20, 0))
