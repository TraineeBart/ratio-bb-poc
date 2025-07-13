# ╭───────────────────────────────────────────────────────────╮
# │ File: src/infra/ws_client_adapter.py                      │
# │ Module: infra                                             │
# │ Doel: Adapter voor WebSocket-client zodat deze            │
# │       eenvoudig in de orchestrator kan worden geïnjecteerd│
# │ Auteur: ArchitectGPT                                     │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: draft                                            │
# ╰───────────────────────────────────────────────────────────╯

import threading
import time

# Adapter voor live WebSocket tickdata
# Onderliggend kan dit bijvoorbeeld een KuCoinWSClient of MockClient zijn.
# Deze wrapper maakt het mogelijk om eenvoudig van implementatie te wisselen.

class WSClientAdapter:
    """
    🧠 Klasse: WSClientAdapter
    Wrapper om een WebSocket-client te gebruiken met een uniforme callback-structuur.

    ▶ In:
        - symbols (list[str]): lijst van te volgen trading pairs
        - callback (Callable): functie die aangeroepen wordt bij nieuwe ticks

    ⏺ Out:
        - Start en stop van de WebSocket-verbinding

    💡 Opmerkingen:
        - Deze adapter zorgt ervoor dat de orchestrator onafhankelijk blijft van de concrete WS-implementatie.
        - In deze draft-implementatie wordt een mock ticker gestart.
    """
    def __init__(self, symbols, callback):
        self.symbols = symbols
        self.callback = callback
        self._running = False
        self._thread = None

    def _mock_stream(self):
        # 🔹 Simuleer live ticks met een eenvoudige loop
        while self._running:
            for symbol in self.symbols:
                tick = {'symbol': symbol, 'price': 42.0, 'timestamp': time.time()}
                self.callback(symbol, tick)
            time.sleep(1)

    def start(self):
        # 🔹 Start de (mock) streaming thread
        self._running = True
        self._thread = threading.Thread(target=self._mock_stream, daemon=True)
        self._thread.start()

    def stop(self):
        # 🔹 Stop de streaming thread netjes
        self._running = False
        if self._thread:
            self._thread.join()