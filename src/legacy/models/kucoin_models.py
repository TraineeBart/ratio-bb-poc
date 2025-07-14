# File: src/models/kucoin_models.py

from dataclasses import dataclass

@dataclass
class Candle:
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass
class OrderBookEntry:
    price: float
    size: float

@dataclass
class TradeEntry:
    trade_id: str
    price: float
    size: float
    side: str
    time: int