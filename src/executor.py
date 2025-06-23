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
    Execute a simulated order applying slippage and fee.
    Returns a dict with keys:
      'price_in', 'price_effective', 'amount_in', 'amount_out', 'fee_amount'
    """
    # Validate side
    if side not in ('buy', 'sell'):
        raise ValueError(f"Unknown side: {side}")

    # Apply slippage
    if side == 'buy':
        price_effective = price * (1 + slippage_rate)
    else:  # sell
        price_effective = price * (1 - slippage_rate)
    price_effective = round(price_effective, 8)

    # Amount out before fee
    gross_out = amount / price_effective

    # Fee calculation
    fee_amount = round(gross_out * fee_rate, 8)

    # Net amount after fee
    amount_out = round(gross_out - fee_amount, 8)

    return {
        'price_in': round(price, 8),
        'price_effective': price_effective,
        'amount_in': round(amount, 8),
        'amount_out': amount_out,
        'fee_amount': fee_amount
    }

# The following CLI block is excluded from test coverage.
if __name__ == '__main__':  # pragma: no cover
    from developer import load_config
    config = load_config()
    exec_mod = Execution(config)
    result = simulate_order(100.0, 10.0, exec_mod.slippage_rate, exec_mod.fee_rate, 'buy')
    print(f"Executed order at price {result['price_effective']}, amount after fee {result['amount_out']}")
