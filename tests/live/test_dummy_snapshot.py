"""
test_dummy_snapshot.py

Deze test demonstreert het gebruik van snapshot testing in het project.
Snapshot testing is handig om complexe outputs eenvoudig te valideren.

De test vergelijkt een vaste waarde met een opgeslagen snapshot om regressies te voorkomen.

Dit bestand dient als voorbeeld en kan later uitgebreid worden met reële live data snapshot tests.
"""
def test_dummy_snapshot(snapshot):
    value = {"key": "value"}
    assert value == snapshot