# ╭───────────────────────────────────────────────────────────╮
# │ File: src/Orchestration/run_once.py                       │
# │ Module: orchestration                                     │
# │ Doel: Aanroepen van de core-logica in replay of live mode │
# │ Auteur: ArchitectGPT                                     │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                           │
# ╰───────────────────────────────────────────────────────────╯
# orchestration/run_once.py

from core.signal_generator import generate_signal
from core.candle_handler import candle_to_event
from infra.event_writer import CsvWriter, WebhookWriter, MultiEventWriter

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
    event = {
        'timestamp': ticks[-1]['timestamp'],
        'payload': {
            'from_asset': 'THETA' if signal == 'SELL' else 'TFUEL',
            'to_asset': 'TFUEL' if signal == 'SELL' else 'THETA',
            'action': signal,
            'amount': 10000,  # Placeholder voor test
            'price': last
        }
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
def run_live(aggregators, event_writer):
    def on_candle(symbol, candle):
        event = candle_to_event(candle, symbol)
        event_writer.write(event)
    # WSClient aanmaken en starten (details hier weggelaten voor brevity)
    pass

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
    csv_writer = CsvWriter('tmp/output.csv')
    webhook_writer = WebhookWriter('http://example.com/webhook')
    writer = MultiEventWriter([csv_writer, webhook_writer])

    if mode == 'replay':
        run_replay(ticks, writer)
    elif mode == 'live':
        run_live(aggregators={}, event_writer=writer)
    else:
        # historisch: strategy runnen en event_writer.write(event)
        pass

if __name__ == '__main__':
    run_once_main(mode='replay', ticks=[{'price': 100, 'timestamp': '2025-07-13T12:00:00', 'symbol': 'BTC-USDT'}])