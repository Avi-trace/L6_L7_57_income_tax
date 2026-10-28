import pytest
from income_tax import taxable_income, tax_due, refund_status


# ---------- taxable_income ----------
def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_negative_income_raises():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_zero_income_is_valid():
    # boundary: gross == 0 must NOT raise (gross < 0 is False)
    assert taxable_income(0, "new", 0) == 0


def test_old_regime_investments_below_cap():
    # cap condition False branch: 100000 <= 150000 -> deduction 150000
    assert taxable_income(500000, "old", 100000) == 350000


def test_old_regime_investments_at_cap_boundary():
    # exactly 150000 is NOT > 150000, so no capping needed
    assert taxable_income(500000, "old", 150000) == 300000


def test_old_regime_investments_capped():
    assert taxable_income(1000000, "old", 200000) == 800000


def test_unknown_regime_raises():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "foo", 0)


def test_deduction_exceeds_gross_returns_zero():
    assert taxable_income(10000, "new", 0) == 0


def test_deduction_equals_gross_boundary():
    # taxable == 0 exactly: not < 0, falls through to return taxable
    assert taxable_income(75000, "new", 0) == 0


def test_positive_taxable_after_deduction():
    assert taxable_income(75001, "new", 0) == 1


# ---------- tax_due ----------
def test_below_exemption():
    assert tax_due(200000, 30) == 0


def test_negative_taxable_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


def test_zero_taxable_is_valid():
    assert tax_due(0, 30) == 0


def test_super_senior_exemption():
    assert tax_due(400000, 85) == 0


def test_super_senior_age_boundary_80():
    # age 80 qualifies for the 500000 exemption; 79 only for 300000
    assert tax_due(500000, 80) == 0
    assert tax_due(500000, 79) == 10000


def test_senior_age_boundary_60():
    # age 60 -> 300000 exemption; age 59 -> 250000
    assert tax_due(300000, 60) == 0
    assert tax_due(300000, 59) == 2500


def test_senior_five_percent_slab():
    assert tax_due(400000, 65) == 5000


def test_taxable_equals_exemption_boundary():
    assert tax_due(250000, 30) == 0


def test_slab_at_upper_boundary():
    # slab exactly 250000 -> still the 5% band -> 12500
    assert tax_due(500000, 30) == 12500


def test_slab_just_above_boundary():
    # slab 250001 -> 20% band: 12500 + 1*20//100 = 12500
    assert tax_due(500001, 30) == 12500
    # slab 250005 -> 12500 + 5*20//100 = 12501
    assert tax_due(500005, 30) == 12501


def test_general_twenty_percent_slab():
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


def test_settled_ignores_filing_flag():
    assert refund_status(500, 500, False) == "settled"
