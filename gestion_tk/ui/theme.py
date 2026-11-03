"""Colours, fonts and ttk styles: a bank statement on cool paper, green for money in and actions,
brick red for money out. Amounts are always set in a monospace face, right-aligned."""

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

PAPER = "#F3F5F4"
SURFACE = "#FFFFFF"
INK = "#1D2B2A"
MUTED = "#5C6B69"
LINE = "#D4DCDA"
SIDEBAR = "#16302C"
SIDEBAR_HOVER = "#21423D"
PRIMARY = "#0E7C66"
PRIMARY_DARK = "#0B6453"
CREDIT = "#1F7A4D"
DEBIT = "#B4432B"
WARN = "#A86206"

SANS_CHOICES = ["IBM Plex Sans", "Ubuntu", "Noto Sans", "DejaVu Sans", "Cantarell", "Helvetica"]
MONO_CHOICES = ["IBM Plex Mono", "DM Mono", "Ubuntu Mono", "DejaVu Sans Mono", "Courier"]

FONTS: dict[str, tkfont.Font] = {}


def _pick(choices: list[str]) -> str:
    available = {f.lower(): f for f in tkfont.families()}
    for name in choices:
        if name.lower() in available:
            return available[name.lower()]
    return choices[-1]


def setup(root: tk.Tk) -> None:
    sans, mono = _pick(SANS_CHOICES), _pick(MONO_CHOICES)
    spec = {
        "body": (sans, 11),
        "small": (sans, 9),
        "bold": (sans, 11, "bold"),
        "h1": (sans, 22, "bold"),
        "h2": (sans, 15, "bold"),
        "label": (sans, 9, "bold"),
        "amount": (mono, 11),
        "amount_small": (mono, 9),
        "amount_big": (mono, 22, "bold"),
        "amount_huge": (mono, 30, "bold"),
        "key": (mono, 18, "bold"),
        "pin": (mono, 26, "bold"),
    }
    for name, args in spec.items():
        FONTS[name] = tkfont.Font(
            root=root, family=args[0], size=args[1], weight=args[2] if len(args) > 2 else "normal"
        )
    tkfont.nametofont("TkDefaultFont").configure(family=sans, size=11)
    tkfont.nametofont("TkTextFont").configure(family=sans, size=11)

    root.configure(background=PAPER)
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        ".",
        background=PAPER,
        foreground=INK,
        font=FONTS["body"],
        bordercolor=LINE,
        focuscolor=PRIMARY,
        lightcolor=SURFACE,
        darkcolor=LINE,
    )
    style.configure("TFrame", background=PAPER)
    style.configure("Card.TFrame", background=SURFACE, relief="solid", borderwidth=1)
    style.configure("Plain.TFrame", background=SURFACE, borderwidth=0)
    style.configure("Side.TFrame", background=SIDEBAR)
    style.configure("TLabel", background=PAPER, foreground=INK)
    style.configure("Card.TLabel", background=SURFACE)
    style.configure("Muted.TLabel", foreground=MUTED)
    style.configure("CardMuted.TLabel", background=SURFACE, foreground=MUTED)
    style.configure("Field.TLabel", background=SURFACE, foreground=MUTED, font=FONTS["label"])
    style.configure("H1.TLabel", font=FONTS["h1"])
    style.configure("H2.TLabel", font=FONTS["h2"])
    style.configure("CardH2.TLabel", background=SURFACE, font=FONTS["h2"])
    style.configure("Error.TLabel", background=SURFACE, foreground=DEBIT)
    style.configure("Ok.TLabel", background=SURFACE, foreground=CREDIT)
    style.configure("Amount.TLabel", background=SURFACE, font=FONTS["amount_big"])
    style.configure("AmountHuge.TLabel", font=FONTS["amount_huge"])

    style.configure(
        "TButton",
        padding=(14, 8),
        background=SURFACE,
        foreground=INK,
        borderwidth=1,
        relief="solid",
        bordercolor=LINE,
    )
    style.map("TButton", background=[("active", PAPER), ("pressed", LINE)])
    style.configure(
        "Primary.TButton",
        background=PRIMARY,
        foreground="#FFFFFF",
        bordercolor=PRIMARY,
        font=FONTS["bold"],
    )
    style.map(
        "Primary.TButton",
        background=[("disabled", LINE), ("active", PRIMARY_DARK)],
        foreground=[("disabled", MUTED)],
    )
    style.configure(
        "Link.TButton", background=SURFACE, foreground=PRIMARY, borderwidth=0, padding=(0, 4)
    )
    style.map(
        "Link.TButton", background=[("active", SURFACE)], foreground=[("active", PRIMARY_DARK)]
    )
    style.configure(
        "Key.TButton", font=FONTS["key"], padding=(0, 10), background=PAPER, bordercolor=LINE
    )
    style.map("Key.TButton", background=[("active", "#E3EAE8"), ("pressed", LINE)])

    style.configure("TEntry", padding=8, fieldbackground=SURFACE, bordercolor=LINE)
    style.map("TEntry", bordercolor=[("focus", PRIMARY)])
    style.configure("TCombobox", padding=6, fieldbackground=SURFACE, bordercolor=LINE)
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", SURFACE)],
        selectbackground=[("readonly", SURFACE)],
        selectforeground=[("readonly", INK)],
    )
    style.configure("TSpinbox", padding=6, fieldbackground=SURFACE, bordercolor=LINE)
    style.configure("TRadiobutton", background=SURFACE)
    style.configure("TNotebook", background=PAPER, borderwidth=0)

    style.configure(
        "Treeview",
        background=SURFACE,
        fieldbackground=SURFACE,
        rowheight=30,
        bordercolor=LINE,
        borderwidth=0,
        font=FONTS["body"],
    )
    style.configure(
        "Treeview.Heading",
        background=PAPER,
        foreground=MUTED,
        font=FONTS["label"],
        relief="flat",
        padding=(8, 6),
    )
    style.map("Treeview", background=[("selected", "#DCEFEA")], foreground=[("selected", INK)])

    for name, color in (("Good", CREDIT), ("Warn", WARN), ("Over", DEBIT)):
        style.configure(
            f"{name}.Horizontal.TProgressbar",
            troughcolor="#E6ECEA",
            background=color,
            bordercolor="#E6ECEA",
            lightcolor=color,
            darkcolor=color,
            thickness=10,
        )
