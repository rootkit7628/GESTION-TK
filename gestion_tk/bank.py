"""The bank: customers, accounts, operations, transfers and budgets, stored in SQLite.

Every money movement runs inside one SQLite transaction, so a transfer can never be half done.
"""

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from . import security
from .money import fmt

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customer (
    id            INTEGER PRIMARY KEY,
    number        TEXT NOT NULL UNIQUE CHECK (length(number) = 8),
    name          TEXT NOT NULL,
    pin_hash      TEXT NOT NULL,
    failed        INTEGER NOT NULL DEFAULT 0,
    locked_until  TEXT
);

CREATE TABLE IF NOT EXISTS account (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customer (id) ON DELETE CASCADE,
    kind        TEXT NOT NULL CHECK (kind IN ('courant', 'livret')),
    label       TEXT NOT NULL,
    -- how far below zero the balance may go (current accounts only)
    overdraft   INTEGER NOT NULL DEFAULT 0 CHECK (overdraft >= 0)
);

CREATE TABLE IF NOT EXISTS movement (
    id          INTEGER PRIMARY KEY,
    account_id  INTEGER NOT NULL REFERENCES account (id) ON DELETE CASCADE,
    day         TEXT NOT NULL,
    amount      INTEGER NOT NULL CHECK (amount != 0),
    label       TEXT NOT NULL,
    category    TEXT NOT NULL DEFAULT '',
    -- both halves of a transfer share the same id
    transfer    TEXT
);

CREATE TABLE IF NOT EXISTS budget (
    customer_id INTEGER NOT NULL REFERENCES customer (id) ON DELETE CASCADE,
    category    TEXT NOT NULL,
    monthly     INTEGER NOT NULL CHECK (monthly > 0),
    PRIMARY KEY (customer_id, category)
);

CREATE INDEX IF NOT EXISTS movement_account ON movement (account_id, day);
"""

CATEGORIES = [
    "Alimentation",
    "Transport",
    "Logement",
    "Santé",
    "Éducation",
    "Loisirs",
    "Famille",
    "Autre",
]


class BankError(Exception):
    """A refusal to show to the customer as is."""


@dataclass(frozen=True)
class Customer:
    id: int
    number: str
    name: str


@dataclass(frozen=True)
class Account:
    id: int
    kind: str
    label: str
    overdraft: int
    balance: int

    @property
    def available(self) -> int:
        return self.balance + self.overdraft


@dataclass(frozen=True)
class Movement:
    id: int
    day: date
    amount: int
    label: str
    category: str
    balance_after: int


@dataclass(frozen=True)
class BudgetLine:
    category: str
    monthly: int
    spent: int

    @property
    def left(self) -> int:
        return self.monthly - self.spent

    @property
    def ratio(self) -> float:
        return self.spent / self.monthly


def default_path() -> Path:
    base = Path.home() / ".local" / "share" / "gestion-tk"
    base.mkdir(parents=True, exist_ok=True)
    return base / "banque.sqlite3"


class Bank:
    def __init__(self, path: str | Path = ":memory:", today=date.today, now=datetime.now):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self.today = today
        self.now = now

    @contextmanager
    def _tx(self):
        with self.db:
            yield self.db

    # --- Customers ------------------------------------------------------------------------

    def open_customer(self, name: str, pin: str) -> Customer:
        """Create a customer with a current account and a savings account."""
        name = " ".join(name.split())
        if not 2 <= len(name) <= 60:
            raise BankError("Indique ton nom (2 à 60 caractères).")
        if not security.valid_pin(pin):
            raise BankError("Le code doit faire exactement 6 chiffres.")
        if len(set(pin)) == 1 or pin in "0123456789" or pin in "9876543210":
            raise BankError("Ce code est trop facile à deviner : évite les suites et répétitions.")
        with self._tx() as db:
            last = db.execute("SELECT MAX(CAST(number AS INTEGER)) FROM customer").fetchone()[0]
            number = str((last or 10000000) + 1)
            cur = db.execute(
                "INSERT INTO customer (number, name, pin_hash) VALUES (?, ?, ?)",
                (number, name, security.hash_pin(pin)),
            )
            cid = cur.lastrowid
            db.execute(
                "INSERT INTO account (customer_id, kind, label, overdraft) VALUES (?, 'courant', "
                "'Compte courant', 0), (?, 'livret', 'Livret d''épargne', 0)",
                (cid, cid),
            )
        return Customer(cid, number, name)

    def login(self, number: str, pin: str) -> Customer:
        row = self.db.execute(
            "SELECT * FROM customer WHERE number = ?", (number.strip(),)
        ).fetchone()
        if row is None:
            raise BankError("Numéro client ou code incorrect.")
        if row["locked_until"] and datetime.fromisoformat(row["locked_until"]) > self.now():
            wait = datetime.fromisoformat(row["locked_until"]) - self.now()
            minutes = int(wait.total_seconds() // 60) + 1
            raise BankError(f"Trop d'essais : accès bloqué encore {minutes} min.")
        if not security.check_pin(pin, row["pin_hash"]):
            failed = row["failed"] + 1
            locked = None
            if failed >= security.MAX_ATTEMPTS:
                locked = (self.now() + timedelta(minutes=security.LOCK_MINUTES)).isoformat()
                failed = 0
            with self._tx() as db:
                db.execute(
                    "UPDATE customer SET failed = ?, locked_until = ? WHERE id = ?",
                    (failed, locked, row["id"]),
                )
            if locked:
                raise BankError(
                    f"Code incorrect 3 fois : accès bloqué {security.LOCK_MINUTES} min."
                )
            left = security.MAX_ATTEMPTS - failed
            tries = "1 essai restant" if left == 1 else f"{left} essais restants"
            raise BankError(f"Numéro client ou code incorrect ({tries}).")
        with self._tx() as db:
            db.execute(
                "UPDATE customer SET failed = 0, locked_until = NULL WHERE id = ?", (row["id"],)
            )
        return Customer(row["id"], row["number"], row["name"])

    # --- Accounts and movements -----------------------------------------------------------

    def accounts(self, customer: Customer) -> list[Account]:
        rows = self.db.execute(
            """SELECT a.*, COALESCE(SUM(m.amount), 0) AS balance
               FROM account a LEFT JOIN movement m ON m.account_id = a.id
               WHERE a.customer_id = ? GROUP BY a.id ORDER BY a.id""",
            (customer.id,),
        ).fetchall()
        return [Account(r["id"], r["kind"], r["label"], r["overdraft"], r["balance"]) for r in rows]

    def _own_account(self, customer: Customer, account_id: int) -> Account:
        for acc in self.accounts(customer):
            if acc.id == account_id:
                return acc
        raise BankError("Ce compte ne t'appartient pas.")

    def history(self, customer: Customer, account_id: int, limit: int = 200) -> list[Movement]:
        """Most recent first, each with the balance right after it."""
        self._own_account(customer, account_id)
        rows = self.db.execute(
            """SELECT id, day, amount, label, category,
                      SUM(amount) OVER (ORDER BY day, id) AS after
               FROM movement WHERE account_id = ? ORDER BY day DESC, id DESC LIMIT ?""",
            (account_id, limit),
        ).fetchall()
        return [
            Movement(
                r["id"],
                date.fromisoformat(r["day"]),
                r["amount"],
                r["label"],
                r["category"],
                r["after"],
            )
            for r in rows
        ]

    def deposit(
        self, customer: Customer, account_id: int, amount: int, label: str = "Dépôt"
    ) -> None:
        self._own_account(customer, account_id)
        self._check_amount(amount)
        with self._tx() as db:
            db.execute(
                "INSERT INTO movement (account_id, day, amount, label) VALUES (?, ?, ?, ?)",
                (account_id, self.today().isoformat(), amount, label.strip() or "Dépôt"),
            )

    def withdraw(
        self,
        customer: Customer,
        account_id: int,
        amount: int,
        label: str = "Retrait",
        category: str = "",
    ) -> None:
        acc = self._own_account(customer, account_id)
        self._check_amount(amount)
        if category and category not in CATEGORIES:
            raise BankError("Catégorie inconnue.")
        if amount > acc.available:
            raise BankError(f"Solde insuffisant : {fmt(acc.available)} disponibles.")
        with self._tx() as db:
            db.execute(
                "INSERT INTO movement (account_id, day, amount, label, category) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    account_id,
                    self.today().isoformat(),
                    -amount,
                    label.strip() or "Retrait",
                    category,
                ),
            )

    def transfer(
        self, customer: Customer, from_id: int, to_number_or_id, amount: int, label: str = ""
    ) -> None:
        """Between the customer's own accounts (account id) or to another customer's current account
        (8-digit customer number)."""
        source = self._own_account(customer, from_id)
        self._check_amount(amount)
        if isinstance(to_number_or_id, int):
            target = self._own_account(customer, to_number_or_id)
            if target.id == source.id:
                raise BankError("Choisis deux comptes différents.")
            target_id, target_name = target.id, target.label
        else:
            row = self.db.execute(
                """SELECT a.id, c.name FROM customer c JOIN account a ON a.customer_id = c.id
                   WHERE c.number = ? AND a.kind = 'courant' AND c.id != ?""",
                (str(to_number_or_id).strip(), customer.id),
            ).fetchone()
            if row is None:
                raise BankError("Aucun autre client ne porte ce numéro.")
            target_id, target_name = row["id"], row["name"]
        if amount > source.available:
            raise BankError(f"Solde insuffisant : {fmt(source.available)} disponibles.")
        tid = f"t{self.now().strftime('%Y%m%d%H%M%S%f')}"
        day = self.today().isoformat()
        text = label.strip()
        with self._tx() as db:
            db.execute(
                "INSERT INTO movement (account_id, day, amount, label, category, transfer) "
                "VALUES (?, ?, ?, ?, '', ?)",
                (source.id, day, -amount, text or f"Virement vers {target_name}", tid),
            )
            db.execute(
                "INSERT INTO movement (account_id, day, amount, label, category, transfer) "
                "VALUES (?, ?, ?, ?, '', ?)",
                (target_id, day, amount, text or f"Virement de {customer.name}", tid),
            )

    # --- Budget ---------------------------------------------------------------------------

    def set_budget(self, customer: Customer, category: str, monthly: int | None) -> None:
        if category not in CATEGORIES:
            raise BankError("Catégorie inconnue.")
        with self._tx() as db:
            if monthly:
                self._check_amount(monthly)
                db.execute(
                    "INSERT INTO budget VALUES (?, ?, ?) "
                    "ON CONFLICT DO UPDATE SET monthly = excluded.monthly",
                    (customer.id, category, monthly),
                )
            else:
                db.execute(
                    "DELETE FROM budget WHERE customer_id = ? AND category = ?",
                    (customer.id, category),
                )

    def budget(self, customer: Customer, month: date | None = None) -> list[BudgetLine]:
        """Each budgeted category with what was spent from all accounts in the month."""
        month = (month or self.today()).replace(day=1)
        end = (month + timedelta(days=32)).replace(day=1)
        rows = self.db.execute(
            """SELECT b.category, b.monthly,
                      COALESCE((SELECT -SUM(m.amount)
                                FROM movement m JOIN account a ON a.id = m.account_id
                                WHERE a.customer_id = b.customer_id AND m.category = b.category
                                  AND m.amount < 0 AND m.day >= ? AND m.day < ?), 0) AS spent
               FROM budget b WHERE b.customer_id = ? ORDER BY b.category""",
            (month.isoformat(), end.isoformat(), customer.id),
        ).fetchall()
        return [BudgetLine(r["category"], r["monthly"], r["spent"]) for r in rows]

    # --- Helpers --------------------------------------------------------------------------

    @staticmethod
    def _check_amount(amount: int) -> None:
        if not isinstance(amount, int) or amount <= 0:
            raise BankError("Le montant doit être un nombre entier positif d'Ariary.")
        if amount > 10_000_000_000:
            raise BankError("Montant trop élevé.")
