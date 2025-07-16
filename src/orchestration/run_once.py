# ⚙️ WSClientAdapter wordt nu async gestart om dubbele eventloops te voorkomen.
# ╭───────────────────────────────────────────────────────────╮
# │ File: src/Orchestration/run_once.py                       │
# │ Module: orchestration                                     │
# │ Doel: Aanroepen van de core-logica in replay of live mode │
# │ Auteur: ArchitectGPT                                     │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                           │
# ╰───────────────────────────────────────────────────────────╯
# orchestration/run_once.py

import uuid
import time
import logging
import asyncio
from core.signal_generator import generate_signal
from core.candle_handler import candle_to_event
from batching.batch_builder import BatchBuilder
from executor.execute_batch import Executor
from infra.event_writer import CsvWriter, WebhookWriter, MultiEventWriter
from infra.ws_client_adapter import WSClientAdapter

# Tick to event helper
def tick_to_event(tick, symbol):
    return {
        'symbol': symbol,
        'price': tick['price'],
        'timestamp': tick['timestamp'],
        'event_type': 'tick'
    }

"""
📄 Omruillogica binnen run_once:

Bij een gegenereerd signaal bepaalt de strategie of er van asset A naar asset B wordt omgeruild.
De 'SELL' actie betekent in deze context altijd 'ruil from_asset naar to_asset via USDT', niet verkopen naar cash.

- Hoge ratio: THETA → USDT → TFUEL
- Lage ratio: TFUEL → USDT → THETA

Deze mapping wordt in de payload van het event expliciet meegegeven.
"""

"""
🧠 Functie: run_replay
Voert een replay uit over tickdata en genereert een event met een signaal.

▶ In:
    - ticks (list): lijst van dicts met 'price', 'timestamp', 'symbol'
    - event_writer (EventWriterProtocol): writer voor output

⏺ Out:
    - Geen return; side-effect via event_writer.write()

💡 Gebruikt:
    - core.signal_generator.generate_signal
"""
def run_replay(ticks: list, event_writer):
    first = ticks[0]['price']
    last = ticks[-1]['price']
    signal = generate_signal(first, last)

    # 🔹 Batch input bouwen
    signals = [{
        'timestamp': ticks[-1]['timestamp'],
        'signal': signal,
        'from_asset': 'THETA' if signal == 'SELL' else 'TFUEL',
        'to_asset': 'TFUEL' if signal == 'SELL' else 'THETA',
        'amount': 10000,
        'price': last
    }]

    batches = BatchBuilder.build_batch(signals)

    for batch in batches:
        batch_id = str(uuid.uuid4())
        result = Executor.execute_batch(batch, event_writer)

        event = {
            'batch_id': batch_id,
            'result': result,
            'status': 'completed'
        }
        event_writer.write(event)

"""
🧠 Functie: run_live
Start een live tick-aggregator en genereert events per candle.

▶ In:
    - aggregators (dict): placeholder voor toekomstige candle-aggregatie
    - event_writer (EventWriterProtocol): writer voor output

⏺ Out:
    - Geen return; side-effect via event_writer.write()

💡 Opmerkingen:
    - De WSClient moet hier nog gekoppeld worden aan on_candle.
"""
async def run_live(aggregators, event_writer):
    import pandas as pd
    from strategies.bb_ratio_strategy import bb_ratio_strategy

    # Aggregator per symbol
    dataframes = {
        'THETA-USDT': [],
        'TFUEL-USDT': []
    }

    def on_tick(symbol, tick):
        logging.info(f"[on_tick-quickfix] Tick ontvangen voor {symbol}. Dummy batch direct aanmaken.")

        # Quickfix: ratio berekenen en loggen
        if symbol == 'THETA-USDT':
            price_theta = tick['price']
        elif symbol == 'TFUEL-USDT':
            price_tfuel = tick['price']
        else:
            return  # Onbekend symbool

        try:
            current_ratio = price_theta / price_tfuel
            logging.info(f"[on_tick-quickfix] Huidige ratio: {current_ratio:.2f}")
        except Exception as e:
            logging.warning(f"[on_tick-quickfix] Kan ratio niet berekenen: {e}")
            current_ratio = None

        signals = [{
            'timestamp': pd.Timestamp.utcnow().isoformat(),
            'signal': 'SELL',
            'from_asset': 'THETA',
            'to_asset': 'TFUEL',
            'amount': 10000,
            'price': tick['price']
        }]

        logging.info(f"[on_tick-quickfix] Dummy signaal: {signals}")

        batches = BatchBuilder.build_batch(signals, ratio=current_ratio)

        for batch in batches:
            batch_id = str(uuid.uuid4())
            result = Executor.execute_batch(batch, event_writer)

            event = {
                'batch_id': batch_id,
                'result': result,
                'status': 'completed'
            }
            event_writer.write(event)

    symbols = ['THETA-USDT', 'TFUEL-USDT']
    ws = WSClientAdapter(symbols, on_tick, mode='live')
    await ws.start()

    try:
        # ⚙️ Gebruik asyncio.sleep om de eventloop actief te houden zonder blokkering.
        while True:
            logging.info("Live loop actief... wacht op nieuwe ticks")
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        ws.stop()

"""
🧠 Functie: run_once_main
Orchestration entrypoint. Roept live of replay logica aan.

▶ In:
    - mode (str): 'replay', 'live' of 'historical'
    - ticks (list, optional): tickdata voor replay

⏺ Out:
    - Geen return; voert side-effects uit via event_writer

💡 Gebruikt:
    - core en infra modules via dependency injection
"""
def run_once_main(mode, ticks=None):
    from infra.event_writer import JsonlWriter

    csv_writer = CsvWriter('outbox/events.csv')
    jsonl_writer = JsonlWriter('outbox/events.jsonl')
    webhook_writer = WebhookWriter('http://localhost:5000/webhook') if mode == 'live' else None

    writers = [csv_writer, jsonl_writer]
    if webhook_writer:
        writers.append(webhook_writer)
    writer = MultiEventWriter(writers)

    if mode == 'replay':
        run_replay(ticks, writer)
    elif mode == 'live':
        import asyncio
        asyncio.run(run_live(aggregators={}, event_writer=writer))
    else:
        # historisch: strategy runnen en event_writer.write(event)
        pass

if __name__ == '__main__':
    run_once_main(mode='replay', ticks=[{'price': 100, 'timestamp': '2025-07-13T12:00:00', 'symbol': 'BTC-USDT'}])