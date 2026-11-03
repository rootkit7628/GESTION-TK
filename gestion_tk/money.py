"""Amounts are whole Ariary (MGA), stored as integers: the Ariary has no subunit in use."""

import re


def fmt(amount: int, sign: bool = False) -> str:
    """1250000 -> '1 250 000 Ar'; with sign=True, '+1 250 000 Ar' or '−1 250 000 Ar'."""
    digits = f"{abs(amount):,}".replace(
        ",", "\u00a0"
    )  # no-break space: renders in every font, unlike U+202F
    prefix = (
        ("+" if amount > 0 else "−" if amount < 0 else "") if sign else ("−" if amount < 0 else "")
    )
    return f"{prefix}{digits} Ar"


def parse(text: str) -> int:
    """Read an amount typed by a person: '1 250 000', '1250000 Ar', '1.250.000'."""
    cleaned = re.sub("[\\s\u202f\u00a0.,]|ar$", "", text.strip().lower())
    if not cleaned.isdigit():
        raise ValueError("Saisis un montant en Ariary, sans décimales (ex. 150 000).")
    value = int(cleaned)
    if value <= 0:
        raise ValueError("Le montant doit être supérieur à zéro.")
    return value
