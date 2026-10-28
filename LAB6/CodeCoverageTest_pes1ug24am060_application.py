import pytest
from income_tax import taxable_income, tax_due, refund_status


# ---------- taxable_income ----------
def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_negative_income_raises():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_old_regime_investments_capped():
    # investments 200000 are capped at 150000 -> deduction 200000
    assert taxable_income(1000000, "old", 200000) == 800000


def test_unknown_regime_raises():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "foo", 0)


def test_deduction_exceeds_gross_returns_zero():
    assert taxable_income(10000, "new", 0) == 0


# ---------- tax_due ----------
def test_below_exemption():
    assert tax_due(200000, 30) == 0


def test_negative_taxable_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


def test_super_senior_exemption():
    assert tax_due(400000, 85) == 0


def test_senior_five_percent_slab():
    # slab = 400000 - 300000 = 100000 -> 5%
    assert tax_due(400000, 65) == 5000


def test_general_twenty_percent_slab():
    # slab = 550000 -> 12500 + 300000 * 20% = 72500
    assert tax_due(800000, 30) == 72500


# ---------- refund_status ----------
def test_refund_on_time():
    assert refund_status(1000, 500, True) == "refund"


def test_refund_late():
    assert refund_status(1000, 500, False) == "refund delayed"


def test_pay_balance_on_time():
    assert refund_status(500, 1000, True) == "pay balance"


def test_pay_balance_late():
    assert refund_status(500, 1000, False) == "pay balance with penalty"


def test_settled():
    assert refund_status(500, 500, True) == "settled"
