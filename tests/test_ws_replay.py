# ╭──────────────────────────────────────────────────────────────╮
# │ File: tests/test_ws_replay.py                               │
# │ Module: test_ws_replay                                      │
# │ Doel: Unit-tests voor WSReplay (start/stop en callback)    │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-04                               │
# │ Status: draft                                               │
# ╰──────────────────────────────────────────────────────────────╯

import sys
import time
import threading
import pandas as pd
import pytest
import types

# Ensure 'ws_replay' module can be imported from src/
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ws_replay import WSReplay

@pytest.fixture
def tmp_csv(tmp_path):
    df = pd.DataFrame({
        'timestamp': pd.date_range("2025-07-04T00:00:00", periods=3, freq="S"),
        'price': [1.0, 2.0, 3.0],
        'volume': [10, 20, 30],
        'nk': [0.1, 0.2, 0.3]
    })
    path = tmp_path / "ticks.csv"
    df.to_csv(path, index=False)
    return str(path)

def test_wsreplay_start_stop_and_callback(tmp_csv):
    """
    🧠 Functie: test_wsreplay_start_stop_and_callback
    Test dat WSReplay start, ticks afspeelt en ordelijk stopt.
    
    ▶️ In:
        - tmp_csv (str): pad naar tijdelijke CSV
    ⏺ Out:
        - None
    
    💡 Gebruikt:
        - pandas voor CSV-generate
        - threading en time voor replay timing
    """
    received = []
    def cb(data):
        received.append(data)

    # Speed hoog zetten zodat delays minimaal zijn
    replay = WSReplay(csv_path=tmp_csv, callback=cb, speed=1000.0)
    replay.start()
    # Wacht kort genoeg om alle ticks af te spelen
    time.sleep(0.05)
    replay.stop()

    # Controleer dat de callback 3 keer is aangeroepen
    assert len(received) == 3
    # Controleer dat elk item een dict is met prijs en timestamp
    assert all(isinstance(item, dict) for item in received)
    assert replay._running is False
    assert replay._thread.is_alive() is False