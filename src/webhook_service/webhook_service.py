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
import time

logging.basicConfig(level=logging.INFO)

def send_http(event, endpoint):
    """Verstuur event via HTTP POST naar opgegeven endpoint."""
    try:
        payload = event.get('payload', {})
        logging.info(f"Versturen trade_signal: {payload.get('from_asset', 'N/A')} → {payload.get('to_asset', 'N/A')} (actie: {payload.get('action', 'N/A')})")
        response = requests.post(endpoint, json=event)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Fout bij verzenden van event {event.get('id', '')}: {e}")

def process_outbox(outbox_path, endpoint):
    """Lees outbox bestand en verstuur trade_signal of batch_result events met offset tracking."""
    offset_file = outbox_path + ".offset"
    last_offset = 0

    if os.path.exists(offset_file):
        try:
            with open(offset_file, "r") as f:
                last_offset = int(f.read().strip())
            logging.info(f"[Webhook] Starten vanaf offset {last_offset}")
        except Exception as e:
            logging.warning(f"[Webhook] Kan offset niet lezen: {e}")

    while True:
        if not os.path.exists(outbox_path):
            logging.warning(f"[Webhook] Outbox bestand {outbox_path} bestaat niet. Wacht 5 sec...")
            time.sleep(5)
            continue

        with open(outbox_path, "r") as f:
            lines = f.readlines()

        if last_offset >= len(lines):
            logging.info(f"[Webhook] Geen nieuwe events. Wacht 5 sec...")
            time.sleep(5)
            continue

        new_lines = lines[last_offset:]
        logging.info(f"[Webhook] Verwerk {len(new_lines)} nieuwe regels uit outbox.")

        for line in new_lines:
            try:
                event = json.loads(line)
                event_type = event.get("event_type")

                if event_type == "trade_signal":
                    send_http(event, endpoint)

                elif event_type == "batch_result":
                    logging.info(f"[Webhook] Verwerken batch_result met {len(event.get('signals', []))} signalen.")
                    try:
                        signals = event.get('signals', [])

                        if not signals:
                            logging.warning(f"[Webhook] batch_result bevat geen signalen: {json.dumps(event)}")
                            continue

                        logging.info(f"[Webhook] Signaal-verwerking: fallback logic actief (genest of direct dict).")

                        for signal_entry in signals:
                            if isinstance(signal_entry, dict) and 'signal' in signal_entry:
                                signal_data = signal_entry['signal']
                            else:
                                signal_data = signal_entry  # Neem direct het dict als signaal

                            if not signal_data:
                                logging.warning(f"[Webhook] Kan signaal niet uitlezen in signal_entry: {json.dumps(signal_entry)}")
                                continue

                            # Fallback ratio toevoegen indien nodig
                            if 'ratio' not in event or event['ratio'] in [None, '', 'N/A']:
                                event['ratio'] = '24.0'  # Fallback voor ratio als deze ontbreekt

                            action = signal_data.get('signal', 'UNKNOWN')
                            from_asset = signal_data.get('from_asset', 'UNKNOWN')
                            to_asset = signal_data.get('to_asset', 'UNKNOWN')

                            volume = signal_entry.get('amount', 0)
                            ratio = event.get('ratio', 'N/A')
                            timestamp = event.get('timestamp', '')
                            batch_id = event.get('batch_id', '')

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

                            logging.info(f"[Webhook] Signaal details → action: {action}, from: {from_asset}, to: {to_asset}, volume: {volume}, ratio: {ratio}")

                            # Controleer of ratio aanwezig is en valideer als float
                            ratio = event.get('ratio')
                            if ratio in [None, '', 'N/A']:
                                logging.warning(f"[Webhook] Ontbrekende ratio in event {batch_id}, fallback naar 24.0")
                                ratio = '24.0'  # Fallback naar standaard ratio
                            else:
                                try:
                                    ratio_float = float(ratio)
                                except ValueError:
                                    logging.warning(f"[Webhook] Ongeldige ratio waarde '{ratio}' in event {batch_id}, fallback naar 24.0")
                                    ratio = '24.0'

                            # Gebruik fallback ratio in message
                            message = f"""
📡 *BB-Ratio Trade Signaal*

**🔁 Actie:** *{actie_str}*
**📊 Ratio:** *{ratio}*
**⚖️ Volume:** *{volume} {to_asset}*
**🕒 Tijd:** *{timestamp}*
**🔗 Batch-ID:** `{batch_id}`

ℹ️ *Uitleg:*
{uitleg}

**Trade stappen:**  
`{stappen}`
                            """
                            logging.info(f"[Webhook] Verstuur Telegram bericht: {message.strip()}")
                            send_telegram_message(message.strip())
                    except Exception as e:
                        logging.error(f"[Webhook] Fout bij verzenden Telegram melding: {e}")
                    send_http(event, endpoint)
            except json.JSONDecodeError as e:
                logging.error(f"[Webhook] JSON decode fout: {e}")

        last_offset += len(new_lines)
        with open(offset_file, "w") as f:
            f.write(str(last_offset))

        time.sleep(2)

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