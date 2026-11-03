"""Loan simulation with constant monthly payments (French amortisation)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Installment:
    month: int
    payment: int
    interest: int
    principal: int
    remaining: int


@dataclass(frozen=True)
class Loan:
    amount: int
    annual_rate: float  # percent, e.g. 14.5
    months: int
    schedule: list[Installment]

    @property
    def monthly_payment(self) -> int:
        return self.schedule[0].payment

    @property
    def total_interest(self) -> int:
        return sum(i.interest for i in self.schedule)

    @property
    def total_cost(self) -> int:
        return self.amount + self.total_interest


def simulate(amount: int, annual_rate: float, months: int) -> Loan:
    """Constant payments rounded to the Ariary; the last one absorbs the rounding."""
    if amount <= 0:
        raise ValueError("Le montant emprunté doit être supérieur à zéro.")
    if not 1 <= months <= 360:
        raise ValueError("La durée doit être comprise entre 1 et 360 mois.")
    if not 0 <= annual_rate <= 100:
        raise ValueError("Le taux annuel doit être compris entre 0 et 100 %.")

    r = annual_rate / 100 / 12
    payment = round(amount / months) if r == 0 else round(amount * r / (1 - (1 + r) ** -months))

    schedule = []
    remaining = amount
    for month in range(1, months + 1):
        interest = round(remaining * r)
        principal = payment - interest
        if month == months:  # settle exactly what is left
            principal = remaining
        remaining -= principal
        schedule.append(Installment(month, principal + interest, interest, principal, remaining))
    return Loan(amount, annual_rate, months, schedule)
