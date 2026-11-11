import time,logging
from pathlib import Path
from src.config.database import SessionLocal
from src.config.queue import queue
from src.services.run_service import compute,mark_failed,QUEUE
logging.basicConfig(level=logging.INFO)
while True:
    Path('/tmp/heartbeat').touch()
    try:
        item=queue.blpop(QUEUE,timeout=4)
        if not item:continue
        run_id=int(item[1])
        with SessionLocal() as db:
            try:compute(db,run_id)
            except Exception as exc:
                db.rollback();mark_failed(db,run_id,exc)
                logging.exception('calibration failed')
    except Exception:logging.exception('worker loop');time.sleep(2)
