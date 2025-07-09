# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/batching.py                                        │
# │ Module: batching                                            │
# │ Doel: Provides logic to split an amount into manageable     │
# │       batches based on average liquidity and batch limits.  │
# │ Auteur: Data-EngineerGPT                                    │
# │ Laatste wijziging: 2025-07-08                               │
# │ Status: stable                                              │
# ╰──────────────────────────────────────────────────────────────╯
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
batching module

Provides API for splitting a total amount into multiple
batches, considering average liquidity and a maximum number
of batches.
"""

from typing import List


def compute_batches(amount_in: float,
                    avg_liquidity: float,
                    max_batches: int = 10) -> List[float]:
    """
    🧠 Functie: compute_batches
    Korte beschrijving: Splits het ingevoerde bedrag in meerdere deelorders,
    op basis van de gemiddelde liquiditeit en een maximum aantal batches.

    ▶️ In:
        - amount_in (float): Het totale bedrag om te verhandelen.
        - avg_liquidity (float): De gemiddelde liquiditeit voor het symbool.
        - max_batches (int, optional): Maximale aantal batch-orders (default 10).
    ⏺ Out:
        - List[float]: Lijst van batch-groottes die optellen tot amount_in.

    💡 Gebruikt:
        - Basis Python-functies, geen externe dependencies
    """
    # 🔹 Validate inputs
    if not isinstance(amount_in, (int, float)) or amount_in <= 0:
        return []
    if not isinstance(avg_liquidity, (int, float)) or avg_liquidity <= 0:
        return []
    if not isinstance(max_batches, int) or max_batches <= 0:
        raise ValueError(f"max_batches must be a positive integer, got {max_batches}")

    # 🔹 Determine number of batches
    # Use max_batches if amount evenly divides by max_batches, else compute minimal batches needed based on avg_liquidity
    if amount_in % max_batches == 0:
        n_batches = max_batches
    else:
        needed = int(amount_in // avg_liquidity)
        if amount_in % avg_liquidity != 0:
            needed += 1
        n_batches = min(needed, max_batches)

    # 🔹 Compute batch sizes
    batches = [amount_in / n_batches] * n_batches

    # 🔹 Adjust rounding error: distribute any remainder
    total = sum(batches)
    if total != amount_in:
        diff = amount_in - total
        batches[0] += diff

    return batches