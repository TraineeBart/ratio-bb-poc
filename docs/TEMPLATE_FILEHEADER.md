

# Bestandtemplate & Documentatiestandaard – Ratio Trades

Deze template dient als standaard voor alle Python-bestanden in het Ratio Trades-project. Gebruik dit format om bestanden herkenbaar, overdraagbaar en goed documenteerbaar te maken — zowel voor jezelf als voor GPT-agenten.

## 🧱 Bestandheader (bovenaan elke .py file)
```python
# ╭───────────────────────────────────────────────────────────╮
# │ File: src/path/to/your_file.py                           │
# │ Module: your_module_name                                 │
# │ Doel: Korte omschrijving van de functie van dit bestand  │
# │ Auteur: [GPT-rol of naam]                                │
# │ Laatste wijziging: YYYY-MM-DD                            │
# │ Status: [draft | stable | legacy | experimental]         │
# ╰───────────────────────────────────────────────────────────╯
```

### 🧾 Docstring-standaard per functie
Gebruik duidelijke uitleg, inclusief input/output:
```python
def functie_naam(...):
    """
    🧠 Functie: functie_naam
    Korte beschrijving van wat de functie doet.

    ▶ In:
        - param_1 (type): uitleg
        - param_2 (type): uitleg
    ⏺ Out:
        - return_type: uitleg

    💡 Gebruikt:
        - eventuele afhankelijke modules of bestanden
    """
```

### 📝 Comment-richtlijnen binnen de code
Gebruik uniforme symbolen om semantiek aan te geven:

| Symbool | Gebruik                                                      |
|---------|--------------------------------------------------------------|
| 🔹      | Functionele toelichting op code                              |
| ⚠      | Waarschuwing of uitzonderlijk gedrag                         |
| TODO    | Nog uit te voeren taken                                      |
| NOTE    | Belangrijke opmerkingen/kanttekeningen                       |

**Voorbeeld**:
```python
# 🔹 Start WebSocket-client
ws = WSClient(self.config)

# ⚠ Callback verwerkt signalen asynchroon
ws.set_signal_callback(self.on_signal)
ws.run_forever()
```

### 🆔 File-identificatie
Zet altijd de relatieve padnaam in de header (bijv. `src/strategies/basic_strategy.py`).  
Optioneel kun je een hash-ID toevoegen voor extra controle:
```python
# ID: strategy_py__a1b2c3d4   # SHA1 of UUID van bestandsnaam + timestamp
```