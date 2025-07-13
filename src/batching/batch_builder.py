

# ╭───────────────────────────────────────────────────────────╮
# │ File: src/batching/batch_builder.py                       │
# │ Module: batching                                          │
# │ Doel: Bouwen van batches van signalen voor de executor    │
# │ Auteur: DeveloperGPT                                     │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: stable                                           │
# ╰───────────────────────────────────────────────────────────╯

import math

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
    def build_batch(signals: list[dict], max_signals_per_batch: int = 3) -> list[dict]:
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
            batch = {
                'signals': signals[start:end]
            }
            batches.append(batch)

        return batches