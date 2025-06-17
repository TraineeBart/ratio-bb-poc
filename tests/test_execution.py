import pytest
from executor import Execution

def test_simulate_order_default():
    cfg = {'slippage_rate': 0.001, 'fee_rate': 0.001}
    exec_mod = Execution(cfg)
    price_slip, amt_after_fee = exec_mod.simulate_order(100.0, 10.0)
    assert price_slip > 100.0
    assert amt_after_fee < 10.0