# ╭───────────────────────────────────────────────────────────╮
# │ File: src/batching/batch_builder.py                       │
# │ Module: batching                                          │
# │ Doel: Bouwen van batches van signalen voor de executor    │
# │ Auteur: DeveloperGPT                                     │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                           │
# ╰───────────────────────────────────────────────────────────╯

import math
import pandas as pd

class BatchBuilder:
    """
    🧠 Klasse: BatchBuilder
    Verwerkt een lijst van signalen tot batches voor de executor.

    ▶ In:
        - signals (list[dict]): Lijst van signal dicts met keys zoals 'symbol', 'signal', 'amount'

    ⏺ Out:
        - list of batches (list[dict]): Lijst van batch dicts, geschikt voor Executor

    💡 Opmerkingen:
        - Dit is een eenvoudige batching: max 3 signalen per batch
        - Kan worden uitgebreid naar geavanceerde slicing of gewichtstoekenning
    """

    @staticmethod
    def build_batch(signals: list[dict], max_signals_per_batch: int = 3, ratio: float = None) -> list[dict]:
        """
        🧠 Functie: build_batch
        Verdeel signalen over batches.

        ▶ In:
            - signals (list[dict]): Lijst van signalen
            - max_signals_per_batch (int): Max aantal signalen per batch

        ⏺ Out:
            - list[dict]: Batches met elk een 'signals' key

        💡 Gebruikt:
            - Pure logica, geen externe afhankelijkheden
        """
        batches = []
        total = len(signals)
        num_batches = math.ceil(total / max_signals_per_batch)

        for i in range(num_batches):
            start = i * max_signals_per_batch
            end = start + max_signals_per_batch
            # Voeg de ratio toe aan de batch voor downstream verwerking (bijv. webhook meldingen)
            batch = {
                'signals': signals[start:end],
                'ratio': ratio if ratio is not None else signals[start]['ratio'] if 'ratio' in signals[start] else "-"
            }
            batches.append(batch)

        return batches

    @staticmethod
    def df_to_signals(df: pd.DataFrame) -> list[dict]:
        """
        Converteer DataFrame naar lijst van signal dicts voor batching.

        ▶ In:
            - df: DataFrame met kolommen ['symbol', 'signal', 'amount' (optioneel)]

        ⏺ Out:
            - list[dict]: Signal dicts per actie (BUY/SELL)

        🧠 Werkt samen met bb_ratio_strategy output.
        """
        assert 'ratio' in df.columns, "De kolom 'ratio' ontbreekt in de dataframe maar is vereist voor batch signals."
        signals = []
        filtered = df[df['signal'] != 'HOLD']

        for _, row in filtered.iterrows():
            signal = {
                'symbol': row['symbol'],
                'signal': row['signal'],
                'amount': row.get('amount', None),  # optioneel veld
                'ratio': row['ratio']  # verplichte toevoeging
            }
            signals.append(signal)

        return signals