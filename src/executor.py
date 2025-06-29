"""
Executormodule voor orderverwerking en batching.
"""

from typing import List, Any
from math import ceil
from liquidity_helper import get_average_liquidity

class Execution:
    def __init__(self, config):
        self.slippage_rate = config.get('slippage_rate', 0.001)
        self.fee_rate = config.get('fee_rate', 0.001)

    def slippage(self, price, amount):
        slipped_price = price * (1 + self.slippage_rate)
        return slipped_price, amount

    def fee(self, amount):
        return amount * self.fee_rate

def simulate_order(
    price: float,
    amount: float,
    slippage_rate: float,
    fee_rate: float,
    side: str
) -> dict:
    """
    Execute a simulated LIMIT order applying slippage and fee.
    Returns a dict with keys:
      'price_in', 'price_effective', 'amount_in', 'amount_out', 'fee_amount'
    Only limit orders are supported: amount_out = amount * price_effective minus fees.
    """
    # Validate amount: treat non-positive amounts as no-op
    if amount <= 0:
        return {
            'price_in': round(price, 8),
            'price_effective': round(price, 8),
            'amount_in': round(amount, 8),
            'amount_out': 0.0,
            'fee_amount': 0.0
        }

    # Validate slippage_rate and fee_rate
    if slippage_rate < 0:
        raise ValueError(f"Slippage rate must be non-negative, got {slippage_rate}")
    if fee_rate < 0:
        raise ValueError(f"Fee rate must be non-negative, got {fee_rate}")

    # Validate side
    if side not in ('buy', 'sell'):
        raise ValueError(f"Unknown side: {side}")

    # Apply slippage
    if side == 'buy':
        price_effective = price * (1 + slippage_rate)
    else:  # sell
        price_effective = price * (1 - slippage_rate)
    price_effective = round(price_effective, 8)

    # For limit orders, compute gross output by multiplying amount by the effective price
    gross_out = amount * price_effective

    # Fee calculation on gross output
    fee_amount = round(gross_out * fee_rate, 8)

    # Net limit-order amount after fee
    amount_out = round(gross_out - fee_amount, 8)

    return {
        'price_in': round(price, 8),
        'price_effective': price_effective,
        'amount_in': round(amount, 8),
        'amount_out': amount_out,
        'fee_amount': fee_amount
    }


# --- Batching helpers ---
def compute_batches(amount: float, symbol: str, window_hours: int) -> List[float]:
    """
    Splits `amount` into batch sizes based on average liquidity over `window_hours`.
    Returns a list of batch quantities.
    """
    if amount <= 0:
        return []

    avg_liq = get_average_liquidity(symbol, window_hours)
    if avg_liq <= 0:
        return [amount]

    batch_count = ceil(amount / avg_liq)
    base_batch = amount / batch_count
    return [base_batch for _ in range(batch_count)]

def process_order_with_batching(
    price: float,
    amount: float,
    slippage_rate: float,
    fee_rate: float,
    side: str,
    symbol: str,
    window_hours: int
) -> List[dict]:
    """
    Processes an order by splitting into batches and simulating each batch.
    Returns a list of results from `simulate_order` for each batch.
    """
    batch_amounts = compute_batches(amount, symbol, window_hours)
    results = []
    for batch_amount in batch_amounts:
        result = simulate_order(price, batch_amount, slippage_rate, fee_rate, side)
        results.append(result)
    return results


# The following CLI block is excluded from test coverage.
if __name__ == '__main__':  # pragma: no cover
    from developer import load_config
    config = load_config()
    exec_mod = Execution(config)
    result = simulate_order(100.0, 10.0, exec_mod.slippage_rate, exec_mod.fee_rate, 'buy')
    print(f"Executed order at price {result['price_effective']}, amount after fee {result['amount_out']}")
