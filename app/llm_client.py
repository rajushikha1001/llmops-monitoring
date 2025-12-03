# app/llm_client.py

import time
import uuid
from opentelemetry import trace

from app.monitoring.collector import record_request
from app.db.models import insert_record_sync

tracer = trace.get_tracer(__name__)


class FakeLLM:
    """
    A simple mock LLM client used for testing observability.
    It simulates processing, generates a response,
    records metrics, and pushes tracing spans.
    """

    def __init__(self, model_name: str = "gpt-demo"):
        self.model_name = model_name

    async def generate(self, prompt: str, user_id: str = "unknown"):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # ---- OpenTelemetry Tracing ----
        with tracer.start_as_current_span("llm_generate") as span:
            span.set_attribute("llm.model", self.model_name)
            span.set_attribute("llm.prompt.length", len(prompt))
            span.set_attribute("llm.user_id", user_id)
            span.set_attribute("llm.request_id", request_id)

            # simulate processing
            time.sleep(0.05)

            response_text = f"Echo: {prompt}"
            token_count = len(prompt.split())

            duration = time.perf_counter() - start_time

            # ---- Prometheus Metrics ----
            record_request(
                model=self.model_name,
                prompt=prompt,
                tokens=token_count,
                duration=duration,
                status="success",
                user_id=user_id,
            )

            # ---- SQLite Logging ----
            insert_record_sync(
                request_id=request_id,
                model=self.model_name,
                prompt=prompt,
                response=response_text,
                tokens=token_count,
                duration=duration,
                status="success",
                user_id=user_id,
            )

            # add tracing attributes
            span.set_attribute("llm.output.tokens", token_count)
            span.set_attribute("llm.latency_ms", duration * 1000)
            span.set_attribute("llm.response", response_text)

        return {
            "request_id": request_id,
            "model": self.model_name,
            "prompt": prompt,
            "response": response_text,
            "tokens": token_count,
            "duration": duration,
            "status": "success",
            "user_id": user_id,
        }
