import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


def test_credit_band_categories():
    assert credit_band(800) == "excellent"
    assert credit_band(700) == "good"
    assert credit_band(600) == "fair"
    assert credit_band(400) == "poor"


def test_invalid_low_credit_score():
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(200)


def test_unknown_employment():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "unemployed", 800)


def test_age_below_minimum():
    assert is_eligible(20, 50000, "salaried", 800) is False


def test_income_below_minimum():
    assert is_eligible(30, 20000, "salaried", 800) is False


def test_poor_credit_score_not_eligible():
    assert is_eligible(30, 50000, "salaried", 400) is False


def test_eligible_self_employed():
    assert is_eligible(30, 50000, "self_employed", 700) is True


def test_interest_rate_categories():
    assert interest_rate(800, "salaried", False) == 8
    assert interest_rate(700, "salaried", False) == 10
    assert interest_rate(600, "salaried", False) == 13


def test_interest_rate_adjustments():
    assert interest_rate(800, "self_employed", False) == 9
    assert interest_rate(800, "salaried", True) == 6
