import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from executor import simulate_order


def test_negative_amount_noop():
    """
    Scenario: negative amount is treated as no-op,
    dus amount_out en fee_amount zijn 0.0.
    """
    result = simulate_order(1.0, -5.0, 0.0, 0.0, 'buy')
    assert isinstance(result, dict)
    assert result['amount_out'] == 0.0
    assert result['fee_amount'] == 0.0


def test_negative_slippage_raises():
    """Negative slippage should trigger a ValueError."""
    with pytest.raises(ValueError):
        simulate_order(100.0, 1.0, -0.01, 0.0, 'buy')

def test_negative_fee_raises():
    """Negative fee should trigger a ValueError."""
    with pytest.raises(ValueError):
        simulate_order(100.0, 1.0, 0.0, -0.001, 'sell')

def test_invalid_side_raises():
    """Invalid side should trigger a ValueError."""
    with pytest.raises(ValueError):
        simulate_order(100.0, 1.0, 0.0, 0.0, 'hold')

@pytest.mark.parametrize("side, slippage, fee", [
    ('buy', 0.0, 0.0),
    ('sell', 0.0, 0.0),
    ('buy', 0.01, 0.005),
    ('sell', 0.02, 0.01),
])
def test_limit_order_calculation(side, slippage, fee):
    """Test limit-order flow: amount_out = amount*price_effective - fee."""
    price = 10.0
    amount = 5.0
    # Compute expected effective price
    if side == 'buy':
        expected_price_eff = price * (1 + slippage)
    else:
        expected_price_eff = price * (1 - slippage)
    # Compute amount_out and fee
    gross = amount * expected_price_eff
    expected_fee = gross * fee
    expected_out = gross - expected_fee

    result = simulate_order(price, amount, slippage, fee, side)
    assert isinstance(result, dict)
    assert result['price_effective'] == pytest.approx(expected_price_eff)
    assert result['fee_amount'] == pytest.approx(expected_fee)
    assert result['amount_out'] == pytest.approx(expected_out)
