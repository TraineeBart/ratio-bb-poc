# ╭───────────────────────────────────────────────────────────╮
# │ File: tests/integration/test_run_once_sanity.py           │
# │ Module: tests.integration                                 │
# │ Doel: Sanity-check integratietest voor run_once pipeline  │
# │ Auteur: QualityEngineerGPT                                │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                            │
# ╰───────────────────────────────────────────────────────────╯

import pytest
from src.Orchestration.run_once import run_replay
from src.infra.event_writer import CsvWriter

def test_run_once_sanity(tmp_path):
    """
    🧠 Functie: test_run_once_sanity
    Test of run_replay correct een event aanmaakt vanuit tickdata en wegschrijft naar CSV.

    ▶ In:
        - tmp_path (Path): tijdelijke directory van pytest fixture
    ⏺ Out:
        - Geen return; asserts controleren CSV-output

    💡 Gebruikt:
        - run_replay uit src.Orchestration.run_once
        - CsvWriter uit src.infra.event_writer
    """
    ticks = [
        {'timestamp': '2025-07-13T12:00:00Z', 'symbol': 'THETA', 'price': 7.80},
        {'timestamp': '2025-07-13T12:05:00Z', 'symbol': 'THETA', 'price': 8.07}
    ]
    writer = CsvWriter(str(tmp_path / "output.csv"))
    run_replay(ticks, writer)

    with open(tmp_path / "output.csv") as f:
        lines = f.readlines()

    assert len(lines) == 2  # Header + 1 event
    assert "TFUEL,THETA" in lines[1]