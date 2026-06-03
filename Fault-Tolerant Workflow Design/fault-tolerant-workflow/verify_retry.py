#!/usr/bin/env python3

from workflow_engine import WorkflowStep, RetryConfig
from test_operations import unreliable_api_call

# Test with high failure rate
config = RetryConfig(max_attempts=5, base_delay=0.5)
step = WorkflowStep("test_retry", unreliable_api_call, config)

try:
    result = step.execute(failure_rate=0.7)
    print(f"Success after retries: {result}")
except Exception as e:
    print(f"Failed after all retries: {e}")

print(f"Step status: {step.status}")
