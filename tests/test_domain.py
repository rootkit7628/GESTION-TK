import random
from datetime import date, datetime, timedelta

import pytest

from gestion_tk import security
from gestion_tk.bank import Bank, BankError
from gestion_tk.loan import simulate
from gestion_tk.money import fmt, parse

# --- Money ----------------------------------------------------------------------------------


def test_format_with_narrow_spaces_and_signs():
    assert fmt(1250000) == "1\u00a0250\u00a0000 Ar"
    assert fmt(-500, sign=True) == "−500 Ar"
    assert fmt(500, sign=True) == "+500 Ar"
    assert fmt(0, sign=True) == "0 Ar"


@pytest.mark.parametrize(
    "text, value", [("150 000", 150000), ("1.250.000", 1250000), ("80000 Ar", 80000)]
)
def test_parse_amounts_as_people_type_them(text, value):
    assert parse(text) == value


@pytest.mark.parametrize("text", ["", "abc", "0", "12,5x", "-30"])
def test_parse_rejects_invalid_amounts(text):
    with pytest.raises(ValueError):
        parse(text)


# --- Loan -----------------------------------------------------------------------------------


def test_loan_schedule_repays_exactly_the_amount():
    loan = simulate(10_000_000, 14.5, 24)
    assert len(loan.schedule) == 24
    assert sum(i.principal for i in loan.schedule) == 10_000_000
    assert loan.schedule[-1].remaining == 0
    assert loan.total_cost == 10_000_000 + loan.total_interest


def test_loan_monthly_payment_matches_the_formula():
    # 1 200 000 Ar at 12 % over 12 months: 106 618.55 Ar a month
    assert simulate(1_200_000, 12, 12).monthly_payment == 106_619


def test_zero_rate_loan_has_no_interest():
    loan = simulate(1_200_000, 0, 12)
    assert loan.total_interest == 0
    assert {i.payment for i in loan.schedule} == {100_000}


@pytest.mark.parametrize("args", [(0, 10, 12), (1000, 10, 0), (1000, 10, 400), (1000, -1, 12)])
def test_loan_rejects_impossible_inputs(args):
    with pytest.raises(ValueError):
        simulate(*args)


# --- Security -------------------------------------------------------------------------------


def test_pin_is_salted_and_checked():
    a, b = security.hash_pin("482913"), security.hash_pin("482913")
    assert a != b  # different salts
    assert security.check_pin("482913", a)
    assert not security.check_pin("482914", a)
    assert not security.check_pin("482913", "garbage")


def test_keypad_holds_every_digit_once_in_a_new_order():
    layouts = {tuple(security.keypad_layout(random.Random(seed))) for seed in range(5)}
    assert len(layouts) > 1
    assert all(sorted(layout) == list("0123456789") for layout in layouts)


# --- Bank -----------------------------------------------------------------------------------


class Clock:
    def __init__(self):
        self.now = datetime(2026, 3, 10, 9, 0)

    def today(self):
        return self.now.date()

    def time(self):
        return self.now


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def bank(clock):
    return Bank(today=clock.today, now=clock.time)


@pytest.fixture
def rina(bank):
    return bank.open_customer("Rina Rakoto", "482913")


def courant(bank, c):
    return next(a for a in bank.accounts(c) if a.kind == "courant")


def livret(bank, c):
    return next(a for a in bank.accounts(c) if a.kind == "livret")


def test_new_customer_gets_a_number_and_two_empty_accounts(bank, rina):
    assert len(rina.number) == 8
    assert [(a.kind, a.balance) for a in bank.accounts(rina)] == [("courant", 0), ("livret", 0)]
    other = bank.open_customer("Hery", "730481")
    assert int(other.number) == int(rina.number) + 1


@pytest.mark.parametrize("pin", ["12345", "1234567", "abcdef", "111111", "123456", "654321"])
def test_weak_or_malformed_pins_are_refused(bank, pin):
    with pytest.raises(BankError):
        bank.open_customer("Rina", pin)


def test_login(bank, rina):
    assert bank.login(rina.number, "482913") == rina
    with pytest.raises(BankError, match="2 essais restants"):
        bank.login(rina.number, "000000")
    with pytest.raises(BankError, match="Numéro client ou code incorrect"):
        bank.login("99999999", "482913")


def test_three_wrong_pins_lock_the_account_for_15_minutes(bank, rina, clock):
    for _ in range(2):
        with pytest.raises(BankError):
            bank.login(rina.number, "000000")
    with pytest.raises(BankError, match="bloqué 15 min"):
        bank.login(rina.number, "000000")
    with pytest.raises(BankError, match="bloqué encore"):
        bank.login(rina.number, "482913")  # even the right PIN
    clock.now += timedelta(minutes=16)
    assert bank.login(rina.number, "482913") == rina


def test_success_resets_the_failed_counter(bank, rina):
    with pytest.raises(BankError):
        bank.login(rina.number, "000000")
    bank.login(rina.number, "482913")
    with pytest.raises(BankError, match="2 essais restants"):
        bank.login(rina.number, "000000")


def test_deposit_withdraw_and_history_with_running_balance(bank, rina, clock):
    acc = courant(bank, rina)
    bank.deposit(rina, acc.id, 500_000, "Salaire")
    clock.now += timedelta(days=1)
    bank.withdraw(rina, acc.id, 120_000, "Marché", "Alimentation")
    hist = bank.history(rina, acc.id)
    assert [(m.label, m.amount, m.balance_after) for m in hist] == [
        ("Marché", -120_000, 380_000),
        ("Salaire", 500_000, 500_000),
    ]
    assert courant(bank, rina).balance == 380_000


def test_cannot_spend_more_than_available(bank, rina):
    acc = courant(bank, rina)
    bank.deposit(rina, acc.id, 10_000)
    with pytest.raises(BankError, match="Solde insuffisant"):
        bank.withdraw(rina, acc.id, 10_001)
    assert courant(bank, rina).balance == 10_000


def test_transfer_between_own_accounts_is_atomic(bank, rina):
    c, s = courant(bank, rina), livret(bank, rina)
    bank.deposit(rina, c.id, 300_000)
    bank.transfer(rina, c.id, s.id, 100_000)
    assert (courant(bank, rina).balance, livret(bank, rina).balance) == (200_000, 100_000)
    with pytest.raises(BankError, match="Solde insuffisant"):
        bank.transfer(rina, s.id, c.id, 100_001)
    assert (courant(bank, rina).balance, livret(bank, rina).balance) == (200_000, 100_000)


def test_transfer_to_another_customer_by_number(bank, rina):
    hery = bank.open_customer("Hery Rabe", "730481")
    bank.deposit(rina, courant(bank, rina).id, 50_000)
    bank.transfer(rina, courant(bank, rina).id, hery.number, 20_000)
    assert courant(bank, hery).balance == 20_000
    assert bank.history(hery, courant(bank, hery).id)[0].label == "Virement de Rina Rakoto"
    with pytest.raises(BankError, match="Aucun autre client"):
        bank.transfer(rina, courant(bank, rina).id, rina.number, 1_000)


def test_customers_cannot_touch_each_others_accounts(bank, rina):
    hery = bank.open_customer("Hery Rabe", "730481")
    with pytest.raises(BankError, match="ne t'appartient pas"):
        bank.deposit(hery, courant(bank, rina).id, 1_000)
    with pytest.raises(BankError):
        bank.history(hery, courant(bank, rina).id)


def test_budget_counts_only_this_months_spending_in_the_category(bank, rina, clock):
    acc = courant(bank, rina)
    bank.deposit(rina, acc.id, 1_000_000)
    bank.set_budget(rina, "Alimentation", 300_000)
    bank.withdraw(rina, acc.id, 80_000, "Marché", "Alimentation")
    bank.withdraw(rina, acc.id, 50_000, "Taxi-be", "Transport")
    clock.now = datetime(2026, 4, 2, 9, 0)
    bank.withdraw(rina, acc.id, 30_000, "Épicerie", "Alimentation")

    [line] = bank.budget(rina, date(2026, 3, 1))
    assert (line.category, line.monthly, line.spent, line.left) == (
        "Alimentation",
        300_000,
        80_000,
        220_000,
    )
    [april] = bank.budget(rina)
    assert april.spent == 30_000

    bank.set_budget(rina, "Alimentation", None)
    assert bank.budget(rina) == []


# --- Demo data ------------------------------------------------------------------------------


def test_demo_customer_has_three_months_of_consistent_activity(bank):
    from gestion_tk.demo import DEMO_PIN, seed

    customer = seed(bank, date(2026, 3, 20))
    assert bank.login(customer.number, DEMO_PIN) == customer
    for acc in bank.accounts(customer):
        assert acc.balance >= 0
        history = bank.history(customer, acc.id)
        assert history and history[0].balance_after == acc.balance
    assert {line.category for line in bank.budget(customer)} >= {"Alimentation", "Transport"}
    with pytest.raises(SystemExit, match="existe déjà"):
        seed(bank, date(2026, 3, 20))
