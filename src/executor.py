from developer import load_config

class Execution:
    def __init__(self, config):
        self.slippage_rate = config.get('slippage_rate', 0.001)
        self.fee_rate = config.get('fee_rate', 0.001)

    def slippage(self, price, amount):
        slipped_price = price * (1 + self.slippage_rate)
        return slipped_price, amount

    def fee(self, amount):
        return amount * self.fee_rate

    def simulate_order(self, price, amount):
        price_slip, amt = self.slippage(price, amount)
        fee_amt = self.fee(amt)
        return price_slip, amt - fee_amt

if __name__ == '__main__':
    config = load_config()
    exec_mod = Execution(config)
    price, amount = exec_mod.simulate_order(100.0, 10.0)
    print(f"Executed order at price {price}, amount after fee {amount}")
