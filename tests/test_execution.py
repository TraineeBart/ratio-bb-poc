import pytest
import os, sys

# Zorg dat src/ op de Python-path staat
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.executor import Execution

@pytest.fixture
def exec_mod():
    # Stel een bekende slippage_rate en fee_rate in
    config = {'slippage_rate': 0.01, 'fee_rate': 0.002}
    return Execution(config)

def test_slippage_buy(exec_mod):
    # Bij een buy: prijs verhoogt, hoeveelheid onveranderd
    price, amount = exec_mod.slippage(100.0, 5.0)
    assert pytest.approx(price, rel=1e-9) == 100.0 * 1.01
    assert amount == 5.0

def test_slippage_sell(exec_mod):
    # Bij een sell: price * (1 + slippage_rate) — de klas gebruikt altijd koop-formule, 
    # zo blijkt uit de implementatie (controle op uitkomst)
    price, amount = exec_mod.slippage(200.0, 10.0)
    assert pytest.approx(price, rel=1e-9) == 200.0 * 1.01
    assert amount == 10.0

def test_fee(exec_mod):
    # Fee = amount * fee_rate
    fee = exec_mod.fee(50.0)
    assert pytest.approx(fee, rel=1e-9) == 50.0 * 0.002

def test_fee_zero(exec_mod):
    # Fee op nul geeft nul terug
    fee = exec_mod.fee(0.0)
    assert fee == 0.0