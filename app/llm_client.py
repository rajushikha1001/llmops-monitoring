import time
import uuid
from typing import Any, Dict
from app.monitoring.collector import record_request

class FakeLLM:
    """A tiny fake LLM for demonstration. Replace with real SDK calls."""

    def __init__(self, model_name: str = "gpt-demo"):
        self.model_name = model_name

    def generate(self, prompt: str, user_id: str = "anonymous") -> Dict[str, Any]:
        request_id = str(uuid.uuid4())
        start = time.perf_counter()

        # simulate processing time
        time.sleep(0.05 + (len(prompt) % 10) * 0.01)
        duration = time.perf_counter() - start

        response = {
            "request_id": request_id,
            "model": self.model_name,
            "prompt": prompt,
            "response": f"Echo: {prompt[:120]}",
            "tokens": len(prompt.split()),
            "duration": duration,
            "status": "success",
            "user_id": user_id,
        }

        # record monitoring information
        record_request(response)

        return response
