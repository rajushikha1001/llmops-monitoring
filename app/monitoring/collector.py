import asyncio
from app.monitoring.metrics import LLM_REQUESTS, LLM_LATENCY
from app.db.models import insert_record_sync

# A small in-process queue and worker to decouple recording from request flow
QUEUE = asyncio.Queue()

async def _worker():
    while True:
        record = await QUEUE.get()
        try:
            model = record.get("model", "unknown")
            status = record.get("status", "unknown")
            duration = float(record.get("duration", 0.0))

            # update Prometheus metrics
            LLM_REQUESTS.labels(model=model, status=status).inc()
            LLM_LATENCY.labels(model=model).observe(duration)

            # persist simple record
            insert_record_sync(record)

        except Exception:
            pass
        finally:
            QUEUE.task_done()

# Start background worker when module is imported
_loop = asyncio.get_event_loop()
if not _loop.is_closed():
    _loop.create_task(_worker())

def record_request(payload: dict):
    """Add a request record to the processing queue."""
    try:
        _loop.call_soon_threadsafe(QUEUE.put_nowait, payload)
    except Exception:
        # fallback: process synchronously
        model = payload.get("model", "unknown")
        status = payload.get("status", "unknown")
        duration = float(payload.get("duration", 0.0))

        LLM_REQUESTS.labels(model=model, status=status).inc()
        LLM_LATENCY.labels(model=model).observe(duration)

        insert_record_sync(payload)
