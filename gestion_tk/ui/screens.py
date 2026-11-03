"""The signed-in screens: dashboard, accounts, transfer, loan simulator and budget."""

import tkinter as tk
from tkinter import messagebox, ttk

from .. import loan as loans
from ..bank import CATEGORIES, BankError
from ..money import fmt, parse
from . import theme
from .widgets import Message, card, ledger, scrolled

MONTHS = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
]


def fill_ledger(tree: ttk.Treeview, movements, accounts: dict | None = None) -> None:
    """Fill a ledger; `accounts` maps a movement id to its account's short name."""
    tree.delete(*tree.get_children())
    for i, m in enumerate(movements):
        tags = ("credit" if m.amount > 0 else "debit",) + (("odd",) if i % 2 else ())
        tree.insert(
            "",
            "end",
            values=(
                m.day.strftime("%d/%m/%Y"),
                (accounts or {}).get(m.id, ""),
                m.label,
                m.category or "—",
                fmt(m.amount, sign=True),
                fmt(m.balance_after),
            ),
            tags=tags,
        )


class Page(ttk.Frame):
    title = ""

    def __init__(self, shell):
        super().__init__(shell.content, padding=(36, 28))
        self.shell = shell
        self.bank = shell.app.bank
        self.customer = shell.app.customer
        ttk.Label(self, text=self.title, style="H1.TLabel").pack(anchor="w", pady=(0, 18))

    def account_names(self):
        return {f"{a.label}  ({fmt(a.balance)})": a for a in self.bank.accounts(self.customer)}


class Dashboard(Page):
    title = "Tableau de bord"

    def __init__(self, shell):
        super().__init__(shell)
        accounts = self.bank.accounts(self.customer)
        total = sum(a.balance for a in accounts)

        top = ttk.Frame(self)
        top.pack(fill="x")
        ttk.Label(top, text="Avoir total", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(
            top,
            text=fmt(total),
            style="AmountHuge.TLabel",
            foreground=theme.DEBIT if total < 0 else theme.INK,
        ).pack(anchor="w")

        row = ttk.Frame(self)
        row.pack(fill="x", pady=(18, 0))
        for acc in accounts:
            c = card(row)
            c.pack(side="left", fill="x", expand=True, padx=(0, 12))
            ttk.Label(c, text=acc.label, style="CardMuted.TLabel").pack(anchor="w")
            ttk.Label(
                c,
                text=fmt(acc.balance),
                style="Amount.TLabel",
                foreground=theme.DEBIT if acc.balance < 0 else theme.INK,
            ).pack(anchor="w", pady=(4, 10))
            ttk.Button(
                c,
                text="Voir le relevé",
                style="Link.TButton",
                command=lambda a=acc: shell.go(Accounts, account_id=a.id),
            ).pack(anchor="w")

        lower = ttk.Frame(self)
        lower.pack(fill="both", expand=True, pady=(22, 0))
        lower.columnconfigure(0, weight=3, uniform="lower")
        lower.columnconfigure(1, weight=2, uniform="lower")

        recent = card(lower)
        recent.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        ttk.Label(recent, text="Dernières opérations", style="CardH2.TLabel").pack(
            anchor="w", pady=(0, 10)
        )
        short = {"courant": "Courant", "livret": "Livret"}
        owner = {}
        movements = []
        for a in accounts:
            for m in self.bank.history(self.customer, a.id, limit=8):
                owner[m.id] = short[a.kind]
                movements.append(m)
        movements = sorted(movements, key=lambda m: (m.day, m.id), reverse=True)[:8]
        if movements:
            tree = ledger(recent, height=8, account=True)
            tree["displaycolumns"] = ("day", "account", "label", "amount")
            fill_ledger(tree, movements, owner)
            tree.pack(fill="both", expand=True)
        else:
            ttk.Label(
                recent,
                text="Aucune opération pour l'instant. Fais un premier dépôt depuis « Comptes ».",
                style="CardMuted.TLabel",
                wraplength=380,
            ).pack(anchor="w")

        budget = card(lower)
        budget.grid(row=0, column=1, sticky="nsew")
        today = self.bank.today()
        ttk.Label(budget, text=f"Budget de {MONTHS[today.month - 1]}", style="CardH2.TLabel").pack(
            anchor="w", pady=(0, 10)
        )
        lines = self.bank.budget(self.customer)
        if not lines:
            ttk.Label(budget, text="Aucun plafond défini.", style="CardMuted.TLabel").pack(
                anchor="w"
            )
            ttk.Button(
                budget,
                text="Définir mon budget",
                style="Link.TButton",
                command=lambda: shell.go(Budget),
            ).pack(anchor="w")
        for line in lines[:5]:
            budget_row(budget, line)


def budget_row(parent, line, label: bool = True) -> None:
    """Spent / ceiling for one category, with a bar: green, amber from 80 %, red when over."""
    style = "Good" if line.ratio < 0.8 else "Warn" if line.ratio <= 1 else "Over"
    head = ttk.Frame(parent, style="Plain.TFrame")
    head.pack(fill="x", pady=(8, 2))
    if label:
        ttk.Label(head, text=line.category, style="Card.TLabel").pack(side="left")
    ttk.Label(
        head,
        text=f"{fmt(line.spent)} / {fmt(line.monthly)}",
        style="CardMuted.TLabel",
        font=theme.FONTS["amount_small"],
    ).pack(side="right")
    bar = ttk.Progressbar(
        parent,
        style=f"{style}.Horizontal.TProgressbar",
        maximum=100,
        value=min(100, line.ratio * 100),
    )
    bar.pack(fill="x")
    if line.left < 0:
        ttk.Label(
            parent,
            text=f"Dépassé de {fmt(-line.left)}",
            style="Error.TLabel",
            font=theme.FONTS["small"],
        ).pack(anchor="w")


class Accounts(Page):
    title = "Comptes"

    def __init__(self, shell, account_id=None):
        super().__init__(shell)
        self.accounts = self.bank.accounts(self.customer)
        self.current = next((a for a in self.accounts if a.id == account_id), self.accounts[0])

        tabs = ttk.Frame(self)
        tabs.pack(fill="x")
        self.choice = tk.IntVar(value=self.current.id)
        for acc in self.accounts:
            ttk.Radiobutton(
                tabs,
                text=acc.label,
                value=acc.id,
                variable=self.choice,
                style="Toolbutton",
                command=self.switch,
            ).pack(side="left", padx=(0, 6))
        self.balance = ttk.Label(tabs, style="AmountHuge.TLabel")
        self.balance.pack(side="right")

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, pady=(16, 0))
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        self.tree = ledger(body, height=14)
        scrolled(body, self.tree).grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        form = card(body)
        form.grid(row=0, column=1, sticky="n")
        ttk.Label(form, text="Nouvelle opération", style="CardH2.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        self.kind = tk.StringVar(value="out")
        ttk.Radiobutton(
            form, text="Retrait / dépense", value="out", variable=self.kind, command=self.toggle
        ).grid(row=1, column=0, sticky="w", pady=(12, 0))
        ttk.Radiobutton(
            form, text="Dépôt", value="in", variable=self.kind, command=self.toggle
        ).grid(row=1, column=1, sticky="w", pady=(12, 0))
        self.amount = self._field(
            form, "MONTANT (AR)", 2, ttk.Entry(form, font=theme.FONTS["amount"], width=26)
        )
        self.label = self._field(form, "LIBELLÉ", 4, ttk.Entry(form, width=26))
        self.category_label = ttk.Label(form, text="CATÉGORIE", style="Field.TLabel")
        self.category = ttk.Combobox(form, values=CATEGORIES, state="readonly", width=24)
        self.category_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(12, 4))
        self.category.grid(row=7, column=0, columnspan=2, sticky="ew")
        self.message = Message(form)
        self.message.configure(wraplength=260)
        self.message.grid(row=8, column=0, columnspan=2, sticky="w", pady=(10, 0))
        ttk.Button(form, text="Enregistrer", style="Primary.TButton", command=self.save).grid(
            row=9, column=0, columnspan=2, sticky="ew", pady=(12, 0)
        )
        self.amount.bind("<Return>", lambda e: self.save())
        self.refresh()

    def _field(self, form, label, row, widget):
        ttk.Label(form, text=label, style="Field.TLabel").grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(12, 4)
        )
        widget.grid(row=row + 1, column=0, columnspan=2, sticky="ew")
        return widget

    def toggle(self) -> None:
        show = self.kind.get() == "out"
        for w in (self.category_label, self.category):
            w.grid() if show else w.grid_remove()

    def switch(self) -> None:
        self.current = next(a for a in self.accounts if a.id == self.choice.get())
        self.message.clear()
        self.refresh()

    def refresh(self) -> None:
        self.accounts = self.bank.accounts(self.customer)
        self.current = next(a for a in self.accounts if a.id == self.current.id)
        self.balance.configure(
            text=fmt(self.current.balance),
            foreground=theme.DEBIT if self.current.balance < 0 else theme.INK,
        )
        fill_ledger(self.tree, self.bank.history(self.customer, self.current.id))

    def save(self) -> None:
        try:
            amount = parse(self.amount.get())
            if self.kind.get() == "in":
                self.bank.deposit(
                    self.customer, self.current.id, amount, self.label.get() or "Dépôt"
                )
            else:
                self.bank.withdraw(
                    self.customer,
                    self.current.id,
                    amount,
                    self.label.get() or "Retrait",
                    self.category.get(),
                )
        except (ValueError, BankError) as err:
            self.message.error(str(err))
            return
        self.amount.delete(0, "end")
        self.label.delete(0, "end")
        self.message.ok("Opération enregistrée.")
        self.refresh()


class Transfer(Page):
    title = "Virement"

    def __init__(self, shell):
        super().__init__(shell)
        box = card(self, padding=28)
        box.pack(anchor="w")
        box.columnconfigure(0, minsize=420)
        names = self.account_names()

        ttk.Label(box, text="DEPUIS", style="Field.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 4)
        )
        self.source = ttk.Combobox(box, values=list(names), state="readonly")
        self.source.current(0)
        self.source.grid(row=1, column=0, sticky="ew")

        ttk.Label(box, text="VERS", style="Field.TLabel").grid(
            row=2, column=0, sticky="w", pady=(16, 4)
        )
        self.mode = tk.StringVar(value="own")
        modes = ttk.Frame(box, style="Plain.TFrame")
        modes.grid(row=3, column=0, sticky="w")
        ttk.Radiobutton(
            modes, text="Un de mes comptes", value="own", variable=self.mode, command=self.toggle
        ).pack(side="left")
        ttk.Radiobutton(
            modes, text="Un autre client", value="other", variable=self.mode, command=self.toggle
        ).pack(side="left", padx=(16, 0))
        self.target = ttk.Combobox(box, values=list(names), state="readonly")
        self.target.current(1 if len(names) > 1 else 0)
        self.target.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        check = (self.register(lambda v: v == "" or (v.isdigit() and len(v) <= 8)), "%P")
        self.number = ttk.Entry(
            box, validate="key", validatecommand=check, font=theme.FONTS["amount"]
        )
        self.number_hint = ttk.Label(
            box, text="Numéro client du bénéficiaire (8 chiffres)", style="CardMuted.TLabel"
        )

        ttk.Label(box, text="MONTANT (AR)", style="Field.TLabel").grid(
            row=6, column=0, sticky="w", pady=(16, 4)
        )
        self.amount = ttk.Entry(box, font=theme.FONTS["amount"])
        self.amount.grid(row=7, column=0, sticky="ew")
        ttk.Label(box, text="MOTIF (FACULTATIF)", style="Field.TLabel").grid(
            row=8, column=0, sticky="w", pady=(16, 4)
        )
        self.label = ttk.Entry(box)
        self.label.grid(row=9, column=0, sticky="ew")
        self.message = Message(box)
        self.message.grid(row=10, column=0, sticky="w", pady=(12, 0))
        ttk.Button(
            box, text="Vérifier et envoyer", style="Primary.TButton", command=self.send
        ).grid(row=11, column=0, sticky="w", pady=(14, 0))
        self.names = names

    def toggle(self) -> None:
        if self.mode.get() == "own":
            self.number.grid_remove()
            self.number_hint.grid_remove()
            self.target.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        else:
            self.target.grid_remove()
            self.number.grid(row=4, column=0, sticky="ew", pady=(8, 0))
            self.number_hint.grid(row=5, column=0, sticky="w", pady=(4, 0))
            self.number.focus_set()

    def send(self) -> None:
        source = self.names[self.source.get()]
        try:
            amount = parse(self.amount.get())
        except ValueError as err:
            self.message.error(str(err))
            return
        if self.mode.get() == "own":
            target, to_text = self.names[self.target.get()].id, self.names[self.target.get()].label
        else:
            target = self.number.get().strip()
            if len(target) != 8:
                self.message.error("Le numéro du bénéficiaire compte 8 chiffres.")
                return
            to_text = f"client n° {target}"
        if not messagebox.askyesno(
            "Confirmer le virement",
            f"Envoyer {fmt(amount)}\ndepuis {source.label}\nvers {to_text} ?",
            parent=self,
        ):
            return
        try:
            self.bank.transfer(self.customer, source.id, target, amount, self.label.get())
        except BankError as err:
            self.message.error(str(err))
            return
        self.shell.go(Transfer)
        self.shell.page.message.ok(f"Virement de {fmt(amount)} effectué.")


class Loan(Page):
    title = "Simulateur d'emprunt"

    def __init__(self, shell):
        super().__init__(shell)
        top = ttk.Frame(self)
        top.pack(fill="x")

        inputs = card(top)
        inputs.pack(side="left", fill="y")
        self.amount = self._entry(inputs, "MONTANT EMPRUNTÉ (AR)", 0, "5 000 000")
        self.rate = self._entry(inputs, "TAUX ANNUEL (%)", 2, "14")
        self.months = self._entry(inputs, "DURÉE (MOIS)", 4, "24")
        self.message = Message(inputs)
        self.message.configure(wraplength=240)
        self.message.grid(row=6, column=0, sticky="w", pady=(10, 0))

        result = card(top)
        result.pack(side="left", fill="both", expand=True, padx=(16, 0))
        ttk.Label(result, text="Mensualité", style="CardMuted.TLabel").pack(anchor="w")
        self.payment = ttk.Label(result, style="Amount.TLabel", font=theme.FONTS["amount_huge"])
        self.payment.pack(anchor="w", pady=(2, 14))
        self.cost = ttk.Label(result, style="Card.TLabel", font=theme.FONTS["amount"])
        self.cost.pack(anchor="w")
        self.total = ttk.Label(result, style="CardMuted.TLabel", font=theme.FONTS["amount"])
        self.total.pack(anchor="w", pady=(4, 0))
        ttk.Label(
            result,
            text="Simulation indicative : le taux réel dépend de ta banque et de ton dossier.",
            style="CardMuted.TLabel",
            font=theme.FONTS["small"],
        ).pack(anchor="w", pady=(14, 0))

        columns = ("month", "payment", "interest", "principal", "remaining")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col, title in zip(
            columns, ("Mois", "Mensualité", "Intérêts", "Capital", "Reste dû"), strict=True
        ):
            self.table.heading(col, text=title, anchor="e" if col != "month" else "w")
            self.table.column(
                col, anchor="e" if col != "month" else "w", width=70 if col == "month" else 150
            )
        self.table.tag_configure("row", font=theme.FONTS["amount"])
        wrap = scrolled(self, self.table)
        wrap.pack(fill="both", expand=True, pady=(18, 0))
        for e in (self.amount, self.rate, self.months):
            e.bind("<KeyRelease>", lambda ev: self.update_result())
        self.update_result()

    def _entry(self, box, label, row, value):
        ttk.Label(box, text=label, style="Field.TLabel").grid(
            row=row, column=0, sticky="w", pady=(10, 4)
        )
        e = ttk.Entry(box, font=theme.FONTS["amount"], width=22)
        e.insert(0, value)
        e.grid(row=row + 1, column=0, sticky="ew")
        return e

    def update_result(self) -> None:
        try:
            amount = parse(self.amount.get())
        except ValueError as err:
            self.message.error(str(err))
            return
        try:
            rate = float(self.rate.get().replace(",", ".").replace("%", "").strip())
            months = int(self.months.get().strip())
        except ValueError:
            self.message.error("Le taux et la durée doivent être des nombres.")
            return
        try:
            result = loans.simulate(amount, rate, months)
        except ValueError as err:
            self.message.error(str(err))
            return
        self.message.clear()
        self.payment.configure(text=fmt(result.monthly_payment))
        self.cost.configure(text=f"Intérêts : {fmt(result.total_interest)}")
        self.total.configure(text=f"Coût total : {fmt(result.total_cost)} en {months} mois")
        self.table.delete(*self.table.get_children())
        for i in result.schedule:
            self.table.insert(
                "",
                "end",
                values=(
                    i.month,
                    fmt(i.payment),
                    fmt(i.interest),
                    fmt(i.principal),
                    fmt(i.remaining),
                ),
                tags=("row",),
            )


class Budget(Page):
    title = "Budget du mois"

    def __init__(self, shell):
        super().__init__(shell)
        today = self.bank.today()
        ttk.Label(
            self,
            text=f"Dépenses de {MONTHS[today.month - 1]} {today.year} par catégorie, tous comptes "
            "confondus. Laisse un plafond vide pour ne pas suivre la catégorie.",
            style="Muted.TLabel",
            wraplength=720,
        ).pack(anchor="w", pady=(0, 14))
        box = card(self)
        box.pack(fill="x")
        box.columnconfigure(1, weight=1)
        current = {line.category: line for line in self.bank.budget(self.customer)}
        self.entries = {}
        for r, category in enumerate(CATEGORIES):
            ttk.Label(box, text=category, style="Card.TLabel", font=theme.FONTS["bold"]).grid(
                row=r * 2, column=0, sticky="w", pady=(10, 0), padx=(0, 16)
            )
            line = current.get(category)
            holder = ttk.Frame(box, style="Plain.TFrame")
            holder.grid(row=r * 2, column=1, rowspan=2, sticky="ew", pady=(6, 0))
            if line:
                budget_row(holder, line, label=False)
            else:
                ttk.Label(holder, text="Pas de plafond", style="CardMuted.TLabel").pack(
                    anchor="w", pady=(8, 0)
                )
            entry = ttk.Entry(box, width=14, font=theme.FONTS["amount"], justify="right")
            if line:
                entry.insert(0, str(line.monthly))
            entry.grid(row=r * 2, column=2, rowspan=2, padx=(16, 0), pady=(6, 0))
            self.entries[category] = entry
        self.message = Message(box)
        self.message.grid(row=len(CATEGORIES) * 2, column=0, columnspan=2, sticky="w", pady=(14, 0))
        ttk.Button(
            box, text="Enregistrer les plafonds", style="Primary.TButton", command=self.save
        ).grid(row=len(CATEGORIES) * 2, column=2, sticky="e", pady=(14, 0))

    def save(self) -> None:
        try:
            for category, entry in self.entries.items():
                text = entry.get().strip()
                self.bank.set_budget(self.customer, category, parse(text) if text else None)
        except (ValueError, BankError) as err:
            self.message.error(str(err))
            return
        self.shell.go(Budget)
        self.shell.page.message.ok("Plafonds enregistrés.")
