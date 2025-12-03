from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.monitoring.metrics import start_prometheus_server

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import os

# configure tracer provider
resource = Resource(attributes={
    "service.name": os.getenv("OTEL_SERVICE_NAME", "llmops-monitoring")
})
provider = TracerProvider(resource=resource)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("OTEL_EXPORTER_JAEGER_AGENT_HOST", "localhost"),
    agent_port=int(os.getenv("OTEL_EXPORTER_JAEGER_AGENT_PORT", "6831")),
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
trace.set_tracer_provider(provider)

app = FastAPI(title="LLM-Ops Monitoring")

# auto-instrument
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

# APIs
app.include_router(api_router, prefix="/api")

# Prometheus metrics server
start_prometheus_server(port=8001)

@app.get("/")
async def root():
    return {"status": "ok", "service": "llmops-monitoring"}
