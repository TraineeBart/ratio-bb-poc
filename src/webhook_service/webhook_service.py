
"""
📄 Webhook Service – Context binnen Ratio-BB-POC:

Deze service leest de outbox en verstuurt alleen 'trade_signal' events.
Belangrijk: 'SELL' betekent in deze context een omruilactie via USDT:

- Hoge ratio: THETA → USDT → TFUEL
- Lage ratio: TFUEL → USDT → THETA

De payload van het event bevat altijd 'from_asset' en 'to_asset' om verwarring te voorkomen.
"""

# ╭───────────────────────────────────────────────────────────╮
# │ File: src/webhook_service/webhook_service.py              │
# │ Module: webhook_service                                   │
# │ Doel: Leest outbox events en verstuurt trade_signals via  │
# │       HTTP POST naar opgegeven endpoint                   │
# │ Auteur: Quality EngineerGPT                               │
# │ Laatste wijziging: 2025-07-13                             │
# │ Status: draft                                             │
# ╰───────────────────────────────────────────────────────────╯


import argparse
import json
import logging
import os
import requests

logging.basicConfig(level=logging.INFO)

def send_http(event, endpoint):
    """Verstuur event via HTTP POST naar opgegeven endpoint."""
    try:
        logging.info(f"Versturen trade_signal: {event['payload']['from_asset']} → {event['payload']['to_asset']} (actie: {event['payload']['action']})")
        response = requests.post(endpoint, json=event)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Fout bij verzenden van event {event.get('id', '')}: {e}")

def process_outbox(outbox_path, endpoint):
    """Lees outbox bestand en verstuur trade_signal events."""
    if not os.path.exists(outbox_path):
        logging.warning(f"Outbox bestand {outbox_path} bestaat niet.")
        return

    with open(outbox_path, "r") as f:
        for line in f:
            try:
                event = json.loads(line)
                event_type = event.get("event_type")

                if event_type == "trade_signal":
                    send_http(event, endpoint)

                elif event_type == "batch_result":
                    logging.info(f"Versturen batch_result: batch_id={event.get('batch_id', '')}, aantal signalen={len(event.get('signals', []))}")
                    send_http(event, endpoint)
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode fout: {e}")

def main():
    parser = argparse.ArgumentParser(description="Webhook Service voor trade_signals.")
    parser.add_argument("--outbox", type=str, default="outbox/events.jsonl",
                        help="Pad naar outbox bestand.")
    parser.add_argument("--endpoint", type=str, required=True,
                        help="HTTP endpoint voor POST requests.")
    args = parser.parse_args()

    process_outbox(args.outbox, args.endpoint)

if __name__ == "__main__":
    main()