"""One window; screens are swapped inside it (the 2021 version started a new process per screen)."""

import tkinter as tk
from tkinter import ttk

from ..bank import Bank, Customer
from . import theme
from .login import LoginScreen
from .screens import Accounts, Budget, Dashboard, Loan, Transfer
from .widgets import NavButton

IDLE_LOGOUT_MS = 5 * 60 * 1000


class Shell(ttk.Frame):
    """Sidebar + content area for a signed-in customer."""

    PAGES = [
        ("Tableau de bord", Dashboard),
        ("Comptes", Accounts),
        ("Virement", Transfer),
        ("Emprunt", Loan),
        ("Budget", Budget),
    ]

    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        side = tk.Frame(self, bg=theme.SIDEBAR, width=230)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        tk.Label(
            side,
            text="Gestion TK",
            bg=theme.SIDEBAR,
            fg="#FFFFFF",
            font=theme.FONTS["h2"],
            anchor="w",
            padx=20,
            pady=22,
        ).pack(fill="x")
        self.nav = {}
        for title, page in self.PAGES:
            b = NavButton(side, title, lambda p=page: self.go(p))
            b.pack(fill="x")
            self.nav[page] = b
        tk.Frame(side, bg=theme.SIDEBAR).pack(fill="both", expand=True)
        tk.Label(
            side,
            text=app.customer.name,
            bg=theme.SIDEBAR,
            fg="#FFFFFF",
            font=theme.FONTS["bold"],
            anchor="w",
            padx=20,
        ).pack(fill="x")
        tk.Label(
            side,
            text=f"Client n° {app.customer.number}",
            bg=theme.SIDEBAR,
            fg="#9FC3BA",
            font=theme.FONTS["small"],
            anchor="w",
            padx=20,
        ).pack(fill="x", pady=(2, 10))
        NavButton(side, "Se déconnecter", app.sign_out).pack(fill="x", pady=(0, 16))

        self.content = ttk.Frame(self)
        self.content.pack(side="left", fill="both", expand=True)
        self.page = None
        self.go(Dashboard)

    def go(self, page_class, **kw) -> None:
        if self.page is not None:
            self.page.destroy()
        self.page = page_class(self, **kw)
        self.page.pack(fill="both", expand=True)
        for cls, button in self.nav.items():
            button.set_active(cls is page_class)


class App:
    def __init__(self, bank: Bank):
        self.bank = bank
        self.customer: Customer | None = None
        self.root = tk.Tk()
        self.root.title("Gestion TK")
        self.root.geometry("1180x760")
        self.root.minsize(980, 640)
        theme.setup(self.root)
        self.screen = None
        self._idle = None
        for event in ("<Motion>", "<KeyPress>", "<Button>"):
            self.root.bind_all(event, self._activity, add="+")
        self.show(LoginScreen)

    def show(self, screen_class, **kw) -> None:
        if self.screen is not None:
            self.screen.destroy()
        self.screen = screen_class(self, **kw)
        self.screen.pack(fill="both", expand=True)

    def signed_in(self, customer: Customer) -> None:
        self.customer = customer
        self.show(Shell)
        self._activity()

    def sign_out(self) -> None:
        self.customer = None
        if self._idle:
            self.root.after_cancel(self._idle)
            self._idle = None
        self.show(LoginScreen)

    def _activity(self, _event=None) -> None:
        """Sign out after 5 minutes without mouse or keyboard activity."""
        if self.customer is None:
            return
        if self._idle:
            self.root.after_cancel(self._idle)
        self._idle = self.root.after(IDLE_LOGOUT_MS, self.sign_out)

    def run(self) -> None:
        self.root.mainloop()
