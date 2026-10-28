import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


@pytest.mark.parametrize("score, expected", [
    (300, "poor"), (549, "poor"),
    (550, "fair"), (649, "fair"),
    (650, "good"), (749, "good"),
    (750, "excellent"), (900, "excellent"),
])
def test_credit_band_boundaries(score, expected):
    assert credit_band(score) == expected


@pytest.mark.parametrize("score", [299, 901])
def test_invalid_scores(score):
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(score)


@pytest.mark.parametrize("age, income, employment, score, expected", [
    (20, 50000, "salaried", 800, False),
    (21, 50000, "salaried", 800, True),
    (60, 50000, "salaried", 800, True),
    (61, 50000, "salaried", 800, False),
    (30, 24999, "salaried", 800, False),
    (30, 25000, "salaried", 800, True),
    (30, 39999, "self_employed", 800, False),
    (30, 40000, "self_employed", 800, True),
    (30, 50000, "salaried", 400, False),
    (30, 50000, "salaried", 600, True),
])
def test_eligibility(age, income, employment, score, expected):
    assert is_eligible(age, income, employment, score) is expected


def test_unknown_employment():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "unemployed", 800)


@pytest.mark.parametrize("score, employment, collateral, expected", [
    (800, "salaried", False, 8),
    (700, "salaried", False, 10),
    (600, "salaried", False, 13),
    (800, "self_employed", False, 9),
    (800, "salaried", True, 6),
    (700, "self_employed", True, 9),
    (600, "self_employed", True, 12),
])
def test_interest_rate(score, employment, collateral, expected):
    assert interest_rate(score, employment, collateral) == expected
