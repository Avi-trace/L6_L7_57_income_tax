# Lab 6: Code and Branch Coverage: Income Tax Calculator

**Name:** Avi (GitHub: Avi-trace)
**SRN:** PES1UG24AM060
**Repo:** L6_L7_57_income_tax

## About

`income_tax.py` is a small Python module with three functions:

| Function | Purpose |
|----------|---------|
| `taxable_income(gross, regime, investments)` | Applies the new regime (flat 75,000 deduction) or old regime (50,000 plus investments capped at 150,000) and returns taxable income, floored at 0. Raises `ValueError` for negative income or an unknown regime. |
| `tax_due(taxable, age)` | Computes tax using an age-based exemption (250,000 / 300,000 for 60+ / 500,000 for 80+), a 5% band on the next 250,000 and 20% beyond. Raises `ValueError` for negative input. |
| `refund_status(tax_paid, tax_due_amount, filed_on_time)` | Returns `refund`, `refund delayed`, `pay balance`, `pay balance with penalty` or `settled`. |

## Files

| File | Description |
|------|-------------|
| `income_tax.py` | Module under test (unchanged) |
| `test_income_tax.py` | Original starter tests |
| `CodeCoverageTest_pes1ug24am060_application.py` | 15 tests for line (code) coverage |
| `BranchCoverageTest_pes1ug24am060_application.py` | 27 tests for branch coverage |
| `code_coverage.png` | Terminal output for the code coverage run |
| `branch_coverage.png` | Terminal output for the branch coverage run |

## Results

| Run | Tests | Statements | Branches | Coverage |
|-----|-------|-----------|----------|----------|
| Starter tests (baseline) | 2 | 39 | 28 | 33% line, 38% total with branches |
| `CodeCoverageTest_...` | 15 | 39 | n/a | **100% line** |
| `BranchCoverageTest_...` | 27 | 39 | 28 | **100% line and branch** |

The code coverage file reaches 100% line coverage but still leaves one branch partially covered (`7->9`, the old regime with investments at or below the cap). That is the line-versus-branch gap the lab is about. The branch file closes it.

## What the branch tests add

Beyond one test per code path, the branch file targets boundaries where `>` versus `>=` mistakes hide:

- `gross == 0` is valid and must not raise
- investments exactly at the 150,000 cap
- `taxable == 0` exactly after deduction
- ages 59/60 and 79/80, the exemption thresholds
- `taxable == exempt` and a slab of exactly 250,000
- `refund_status` with equal amounts regardless of the filing flag

## How to run

```
pip install coverage pytest
cd LAB6
```

Code coverage:

```
coverage erase
coverage run -m pytest CodeCoverageTest_pes1ug24am060_application.py
coverage report -m
```

Branch coverage:

```
coverage erase
coverage run --branch -m pytest BranchCoverageTest_pes1ug24am060_application.py
coverage report -m
```

The `-m` flag on `coverage report` lists the exact missing lines and branches.
