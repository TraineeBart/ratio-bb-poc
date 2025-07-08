

# Executor Flow & Batching Integration

Deze documentatie beschrijft de end-to-end flow van order-uitvoering in `run_once.py`, inclusief de nieuwe batching-logica.

```mermaid
graph TD
    subgraph Config & Setup
        A[load_config()] --> B[Init Executor / Orchestrator]
    end

    subgraph Live or Backtest Branch
        B --> C{Replay Mode?}
        C -->|Yes| D[load ticks via WSReplay]
        C -->|No| E{MODE=live?}
        E -->|Yes| F[init WSClient]
        E -->|No| F[load historical CSV]
    end

    subgraph Order Execution
        F --> G[on_tick() or tick from replay]
        G --> H[apply strategy → signal]
        H --> I[compute price_effective & fee]
        I --> J[get_average_liquidity()]
        J --> K[compute_batches(amount, avg_liquidity, max_batches)]
        K --> L[loop over batches]
        L --> M[simulate_order(batch_amount, price_effective)]
        M --> N[write CSV & dispatch webhook]
    end

    subgraph Shutdown & Cleanup
        N --> O[stop WSClient & health server]
    end
```

1. **load_config()**  
   Laadt alle configuratie-parameters, incl. `symbols`, `webhook_url`, `batching.window_hours`, `batching.max_batches`.

2. **Replay vs Live**  
   - Replay Mode (`--replay`): invoer via `WSReplay`.  
   - Live Mode (`MODE=live`): verbinding via `WSClient`.  
   - Anders historische CSV inlezen.

3. **Order Execution**  
   1. Strategy bepaalt `signal`, `amount` en `price_effective`.  
   2. `get_average_liquidity()`: berekent gemiddelde 5-min liquiditeit over `window_hours`.  
   3. `compute_batches()`: splitst `amount` in ≤ `max_batches` gelijke delen.  
   4. Voor elke batch: `simulate_order()` → CSV-output → webhook.

4. **Shutdown & Cleanup**  
   - Stop alle threads: WSClient, health server.