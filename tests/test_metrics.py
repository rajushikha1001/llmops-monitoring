def test_metrics_importable():
import app.monitoring.metrics as m
assert hasattr(m, 'LLM_REQUESTS')