"""Small building blocks shared by the screens."""

import tkinter as tk
from tkinter import ttk

from . import theme


def card(parent, padding=20) -> ttk.Frame:
    return ttk.Frame(parent, style="Card.TFrame", padding=padding)


def field(parent, label: str, widget_factory, row: int, column: int = 0, columnspan: int = 1):
    """A label above an input, inside a card. Returns the input."""
    ttk.Label(parent, text=label.upper(), style="Field.TLabel").grid(
        row=row * 2, column=column, columnspan=columnspan, sticky="w", pady=(10, 4), padx=(0, 12)
    )
    widget = widget_factory(parent)
    widget.grid(row=row * 2 + 1, column=column, columnspan=columnspan, sticky="ew", padx=(0, 12))
    return widget


class Message(ttk.Label):
    """One line under a form: an error or a confirmation."""

    def __init__(self, parent, **kw):
        super().__init__(parent, text="", style="Error.TLabel", wraplength=420, **kw)

    def error(self, text: str) -> None:
        self.configure(text=text, style="Error.TLabel")

    def ok(self, text: str) -> None:
        self.configure(text=text, style="Ok.TLabel")

    def clear(self) -> None:
        self.configure(text="")


def ledger(parent, height=12, account=False) -> ttk.Treeview:
    """A statement table: date, label, category, amount, balance (and the account, if asked)."""
    columns = ("day", "account", "label", "category", "amount", "balance")
    tree = ttk.Treeview(
        parent, columns=columns, show="headings", height=height, selectmode="browse"
    )
    # Ask for the minimum widths and let the columns stretch: Tk clips a table that asked for more
    # room than it got instead of shrinking its columns.
    for col, title, width, anchor in (
        ("day", "Date", 100, "w"),
        ("account", "Compte", 66, "w"),
        ("label", "Libellé", 130, "w"),
        ("category", "Catégorie", 96, "w"),
        ("amount", "Montant", 112, "e"),
        ("balance", "Solde", 112, "e"),
    ):
        tree.heading(col, text=title, anchor=anchor)
        tree.column(col, width=width, minwidth=width, anchor=anchor, stretch=col == "label")
    if not account:
        tree["displaycolumns"] = ("day", "label", "category", "amount", "balance")
    tree.tag_configure("credit", foreground=theme.CREDIT)
    tree.tag_configure("debit", foreground=theme.DEBIT)
    tree.tag_configure("odd", background="#F7F9F8")
    return tree


def scrolled(parent, tree: ttk.Treeview) -> ttk.Frame:
    """Wrap a table (created in `parent`) in a bordered frame with a scrollbar."""
    frame = ttk.Frame(parent, style="Card.TFrame")
    bar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=bar.set)
    tree.pack(in_=frame, side="left", fill="both", expand=True, padx=1, pady=1)
    tree.lift(frame)  # the frame was created after the table and would hide it
    bar.pack(side="right", fill="y")
    return frame


class NavButton(tk.Label):
    """Sidebar entry: a plain label that behaves like a button (keyboard included)."""

    def __init__(self, parent, text: str, command, **kw):
        super().__init__(
            parent,
            text=text,
            anchor="w",
            padx=20,
            pady=11,
            bg=theme.SIDEBAR,
            fg="#CFE1DC",
            font=theme.FONTS["body"],
            cursor="hand2",
            takefocus=1,
            **kw,
        )
        self.command = command
        self.active = False
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Return>", lambda e: command())
        self.bind("<space>", lambda e: command())
        self.bind("<Enter>", lambda e: self._paint(hover=True))
        self.bind("<Leave>", lambda e: self._paint())
        self.bind("<FocusIn>", lambda e: self._paint(hover=True))
        self.bind("<FocusOut>", lambda e: self._paint())

    def set_active(self, active: bool) -> None:
        self.active = active
        self._paint()

    def _paint(self, hover: bool = False) -> None:
        if self.active:
            self.configure(bg=theme.PAPER, fg=theme.INK, font=theme.FONTS["bold"])
        else:
            self.configure(
                bg=theme.SIDEBAR_HOVER if hover else theme.SIDEBAR,
                fg="#CFE1DC",
                font=theme.FONTS["body"],
            )
