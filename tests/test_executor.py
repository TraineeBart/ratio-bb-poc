import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from src.executor import simulate_order


# Scenario tests for simulate_order
@pytest.mark.parametrize("price, amount, slippage_rate, fee_rate, side, expected", [
    # 1. Geen slippage, geen fee
    (1.0, 100, 0.0, 0.0, 'buy', {'price_effective': 1.0, 'amount_out': 100.0, 'fee_amount': 0.0}),
    # 2. Slippage koop
    (1.0, 100, 0.001, 0.0, 'buy', {'price_effective': 1.001, 'amount_out': 100/1.001, 'fee_amount': 0.0}),
    # 3. Slippage verkoop
    (1.0, 100, 0.001, 0.0, 'sell', {'price_effective': 0.999, 'amount_out': 100/0.999, 'fee_amount': 0.0}),
    # 4. Fee alleen
    (2.0, 50, 0.0, 0.002, 'sell', {'price_effective': 2.0, 'amount_out': pytest.approx(24.95), 'fee_amount': pytest.approx(0.05)}),
    # 5. Slippage + fee
    (1.5, 200, 0.0005, 0.001, 'buy', None),  # validate combined
    # 6. Afronding high-precision
    (0.00012345, 100000, 0.0, 0.0, 'buy', {'price_effective': 0.00012345, 'amount_out': round(100000/0.00012345, 8), 'fee_amount': 0.0}),
])
def test_simulate_order_scenarios(price, amount, slippage_rate, fee_rate, side, expected):
    result = simulate_order(price, amount, slippage_rate, fee_rate, side)
    # Common assertions
    assert result['price_in'] == price

    # Slippage and price_effective
    if expected:
        exp = expected
        assert pytest.approx(result['price_effective'], rel=1e-8) == exp['price_effective']
        assert pytest.approx(result['amount_out'], rel=1e-8) == exp['amount_out']
        assert pytest.approx(result['fee_amount'], rel=1e-8) == exp['fee_amount']
    else:
        # Scenario 5: combined slippage + fee
        pe = price * (1 + slippage_rate) if side == 'buy' else price * (1 - slippage_rate)
        gross = amount / pe
        fee = gross * fee_rate
        net = round(gross - fee, 8)
        assert pytest.approx(result['price_effective'], rel=1e-8) == pe
        assert pytest.approx(result['fee_amount'], rel=1e-8) == round(fee, 8)
        assert pytest.approx(result['amount_out'], rel=1e-8) == net


def test_invalid_side_raises():
    with pytest.raises(ValueError):
        simulate_order(1.0, 100, 0.0, 0.0, 'invalid')
