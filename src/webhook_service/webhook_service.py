
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
from webhook_service.telegram_helper import send_telegram_message

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
                    try:
                        signals = event.get('signals', [])
                        first_signal = signals[0] if signals else {}
                        action = first_signal.get('signal', 'UNKNOWN')
                        from_asset = first_signal.get('from_asset', 'UNKNOWN')
                        to_asset = first_signal.get('to_asset', 'UNKNOWN')
                        volume = sum([s.get('amount', 0) for s in signals])
                        ratio = event.get('ratio', 'N/A')
                        timestamp = event.get('timestamp', '')
                        batch_id = event.get('batch_id', '')

                        # Bepaal uitleg op basis van ratio
                        uitleg = ""
                        try:
                            ratio_float = float(ratio)
                        except Exception:
                            ratio_float = None
                        if ratio_float is not None and ratio_float >= 25:
                            uitleg = "Bij een hoge ratio wordt Theta verkocht tegen USDT, waarna USDT wordt gebruikt om TFuel te kopen."
                            stappen = "Theta → USDT → TFuel"
                            actie_str = f"SELL {from_asset}"
                        elif ratio_float is not None and ratio_float <= 22:
                            uitleg = "Bij een lage ratio wordt TFuel verkocht tegen USDT, waarna USDT wordt gebruikt om Theta te kopen."
                            stappen = "TFuel → USDT → Theta"
                            actie_str = f"SELL {from_asset}"
                        else:
                            uitleg = "Ratio binnen middengebied – strategie bepaalt dynamisch de actie."
                            stappen = f"{from_asset} → USDT → {to_asset}"
                            actie_str = f"{action} {from_asset}"

                        message = f"""
📡 *BB-Ratio Trade Signaal*

🔁 Actie: {actie_str}
📊 Ratio: {ratio}
⚖️ Volume: {volume} {to_asset}
🕒 Tijd: {timestamp}
🔗 Batch-ID: {batch_id}

ℹ️ Uitleg:
{uitleg}

Trade stappen:
{stappen}
                        """
                        send_telegram_message(message.strip())
                    except Exception as e:
                        logging.error(f"Fout bij verzenden Telegram melding: {e}")
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