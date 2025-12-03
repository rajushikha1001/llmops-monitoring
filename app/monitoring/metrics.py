from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Metrics definitions
LLM_REQUESTS = Counter(
    "llm_requests_total",
    "Total LLM requests",
    ["model", "status"],
)

LLM_LATENCY = Histogram(
    "llm_request_duration_seconds",
    "LLM request latency seconds",
    ["model"],
)

LLM_IN_PROGRESS = Gauge(
    "llm_requests_in_progress",
    "Number of LLM requests in progress",
    ["model"],
)

def start_prometheus_server(port: int = 8001):
    """Starts a thread with Prometheus exposition endpoint."""
    start_http_server(port)
