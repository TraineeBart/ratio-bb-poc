import time
import os
import json
import logging

OUTBOX_PATH = "/opt/ratio-bb-poc/outbox/events.jsonl"
LOG_PATH = "/opt/ratio-bb-poc/logs/ratio_bb.log"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def tail_file(file_path):
    with open(file_path, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            yield line.strip()

def monitor_outbox():
    logging.info("Start monitoring outbox...")
    for line in tail_file(OUTBOX_PATH):
        try:
            event = json.loads(line)
            batch_id = event.get("batch_id", "onbekend")
            event_type = event.get("type", "onbekend")
            ratio = event.get("ratio", "-")
            logging.info(f"[OUTBOX] Batch: {batch_id} | Type: {event_type} | Ratio: {ratio}")
        except Exception as e:
            logging.error(f"Fout bij verwerken outbox regel: {e}")

def monitor_logs():
    if not os.path.exists(LOG_PATH):
        logging.warning(f"Logbestand {LOG_PATH} niet gevonden. Sla log-monitoring over.")
        return

    logging.info("Start monitoring logs...")
    for line in tail_file(LOG_PATH):
        print(f"[LOG] {line}")

if __name__ == "__main__":
    from threading import Thread

    t1 = Thread(target=monitor_outbox)
    t2 = Thread(target=monitor_logs)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
