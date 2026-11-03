"""A demo customer with three months of plausible activity, to try the app."""

import random
from datetime import date, timedelta

from .bank import Bank, BankError, Customer

DEMO_NAME = "Rina Rakotomalala"
DEMO_PIN = "482913"

SPENDING = [
    ("Marché d'Analakely", "Alimentation", (15_000, 60_000)),
    ("Épicerie", "Alimentation", (5_000, 25_000)),
    ("Taxi-be", "Transport", (1_000, 3_000)),
    ("Carburant", "Transport", (20_000, 60_000)),
    ("JIRAMA électricité", "Logement", (40_000, 90_000)),
    ("Pharmacie", "Santé", (8_000, 40_000)),
    ("Frais de scolarité", "Éducation", (80_000, 150_000)),
    ("Cinéma", "Loisirs", (10_000, 20_000)),
    ("Envoi à la famille", "Famille", (30_000, 100_000)),
]


def seed(bank: Bank, today: date) -> Customer:
    """Create the demo customer, or refuse if it already exists."""
    existing = bank.db.execute(
        "SELECT number FROM customer WHERE name = ?", (DEMO_NAME,)
    ).fetchone()
    if existing:
        raise SystemExit(
            f"Le client de démonstration existe déjà : numéro {existing[0]}, code {DEMO_PIN}."
        )
    try:
        customer = bank.open_customer(DEMO_NAME, DEMO_PIN)
    except BankError as err:
        raise SystemExit(f"Impossible de créer le client de démonstration : {err}") from err
    rng = random.Random(42)
    courant, livret = bank.accounts(customer)
    real_today = bank.today
    try:
        start = (today.replace(day=1) - timedelta(days=62)).replace(day=1)
        day = start
        while day <= today:
            bank.today = lambda d=day: d
            if day.day == 1:
                bank.deposit(customer, courant.id, 1_350_000, "Salaire")
            if day.day == 3:
                bank.transfer(customer, courant.id, livret.id, 150_000, "Épargne du mois")
            if rng.random() < 0.45:
                label, category, (low, high) = rng.choice(SPENDING)
                amount = rng.randrange(low, high, 500)
                if amount <= bank.accounts(customer)[0].available:
                    bank.withdraw(customer, courant.id, amount, label, category)
            day += timedelta(days=1)
    finally:
        bank.today = real_today
    for category, monthly in (
        ("Alimentation", 450_000),
        ("Transport", 150_000),
        ("Loisirs", 60_000),
        ("Famille", 200_000),
    ):
        bank.set_budget(customer, category, monthly)
    return customer
