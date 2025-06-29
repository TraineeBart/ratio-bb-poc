import sys
from pathlib import Path
# Ensure project root is on sys.path so 'src' package is importable
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import csv
import pytest
from pathlib import Path
from src.orchestrator import Orchestrator

@pytest.fixture
def tmp_csv_dir(tmp_path):
    # Use a temporary csv file in a fresh directory
    out_file = tmp_path / "outdir" / "output.csv"
    config = {'backtest_output_csv': str(out_file)}
    # Ensure no pre-existing directory
    if out_file.parent.exists():
        for child in out_file.parent.iterdir():
            if child.is_file():
                child.unlink()
        out_file.parent.rmdir()
    return config, out_file

def test_on_signal_happy_path(tmp_csv_dir):
    config, out_file = tmp_csv_dir
    orch = Orchestrator(config)
    payload = {'symbol': 'AAA', 'timestamp': 123, 'signal': 'BUY', 'price': 1.23, 'amount': 100}
    orch.on_signal(payload)
    # CSV file should now exist
    assert out_file.exists()
    # Read back and check header and row
    with open(out_file, newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows[0] == ['symbol', 'timestamp', 'signal', 'price', 'amount']
    assert rows[1] == ['AAA', '123', 'BUY', '1.23', '100']

def test_on_signal_creates_directory(tmp_csv_dir):
    config, out_file = tmp_csv_dir
    # Remove directory explicitly
    if out_file.parent.exists():
        out_file.parent.rmdir()
    orch = Orchestrator(config)
    payload = {'symbol': 'BBB', 'timestamp': 456, 'signal': 'SELL', 'price': 4.56, 'amount': 200}
    orch.on_signal(payload)
    # Directory should be created
    assert out_file.parent.exists()
    assert out_file.exists()

def test_on_signal_permission_error(tmp_csv_dir, monkeypatch):
    config, out_file = tmp_csv_dir
    orch = Orchestrator(config)
    # Patch open to raise PermissionError when opening our target file
    import builtins
    real_open = builtins.open
    def fake_open(path, mode='r', *args, **kwargs):
        if str(out_file) in str(path):
            raise PermissionError("No permission")
        return real_open(path, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, 'open', fake_open)
    payload = {'symbol': 'CCC', 'timestamp': 789, 'signal': 'HOLD', 'price': 7.89, 'amount': 300}
    with pytest.raises(PermissionError):
        orch.on_signal(payload)