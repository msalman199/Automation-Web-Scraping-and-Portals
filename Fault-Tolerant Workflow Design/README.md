# 🔄 Fault-Tolerant Workflow Design 

<div align="center">

# 🛡️ Building Resilient Automation Workflows

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu_20.04+-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)
![Tenacity](https://img.shields.io/badge/Tenacity-Retry_Library-orange?style=for-the-badge)
![Logging](https://img.shields.io/badge/Logging-Monitoring-blue?style=for-the-badge)
![Automation](https://img.shields.io/badge/Automation-Fault_Tolerance-green?style=for-the-badge)

### ⚡ Retry • Recover • Monitor • Automate

</div>

---

# 📖 Overview

Modern automation systems frequently encounter transient failures such as:

* 🌐 Network outages
* 📡 API rate limits
* 💾 File access issues
* 🗄️ Database timeouts
* ⚠️ Temporary service interruptions

A fault-tolerant workflow automatically detects failures, retries operations, logs incidents, and continues execution whenever possible.

In this lab, you will build a resilient workflow orchestration system using Python.

---

# 🎯 Learning Objectives

By completing this lab, you will:

✅ Implement retry logic with exponential backoff

✅ Build resilient automation pipelines

✅ Handle exceptions gracefully

✅ Create detailed logging systems

✅ Monitor workflow execution

✅ Generate workflow execution reports

---

# 📋 Prerequisites

| Requirement        | Description                    |
| ------------------ | ------------------------------ |
| 🐧 Linux           | Basic command-line proficiency |
| 🐍 Python          | Functions, Classes, Exceptions |
| 📂 File Operations | Read/Write files               |
| ⚠️ Error Handling  | Try/Except blocks              |
| 📊 Logging         | Basic understanding            |

---

# 🏗️ Workflow Architecture

```text
                    ┌───────────────────┐
                    │ Workflow Start    │
                    └─────────┬─────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Workflow Orchestrator    │
                 └─────────┬────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
 ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
 │ API Call    │  │ File Task   │  │ DB Task     │
 └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
        │                │                │
        ▼                ▼                ▼
  Retry Logic      Retry Logic      Retry Logic
        │                │                │
        ▼                ▼                ▼
  Success/Fail     Success/Fail     Success/Fail
        │                │                │
        └────────┬───────┴───────┬────────┘
                 ▼               ▼
           Execution Logs   Summary Report
```

---

# 🚀 Environment Setup

## 🔹 Step 1: Start Lab Environment

Provision your Linux machine and connect via SSH.

---

## 🔹 Step 2: Install Required Tools

```bash
# Update package manager
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Create project directory
mkdir -p ~/fault-tolerant-workflow

cd ~/fault-tolerant-workflow

# Create virtual environment
python3 -m venv venv

source venv/bin/activate

# Install dependencies
pip install requests tenacity
```

---

## 🔹 Step 3: Verify Installation

```bash
python3 --version

pip list | grep -E "requests|tenacity"
```

Expected:

```text
Python 3.x.x
requests
tenacity
```

---

# 🧩 Task 1: Build a Retry Mechanism

---

# 📝 Step 1: Create Workflow Engine

Create:

```bash
nano workflow_engine.py
```

---

## 📄 workflow_engine.py

```python
import time
import logging
from typing import Callable, Any, Optional
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('workflow.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class RetryConfig:

    def __init__(
        self,
        max_attempts=3,
        base_delay=1.0,
        max_delay=60.0,
        exponential_base=2.0
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base


def retry_with_backoff(
    config,
    exceptions=(Exception,)
):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            attempt = 0

            while attempt < config.max_attempts:

                try:

                    logger.info(
                        f"Attempt {attempt+1}/"
                        f"{config.max_attempts} "
                        f"for {func.__name__}"
                    )

                    result = func(
                        *args,
                        **kwargs
                    )

                    return result

                except exceptions as e:

                    logger.error(
                        f"Attempt {attempt+1} failed: {e}"
                    )

                    attempt += 1

                    if attempt >= config.max_attempts:

                        logger.error(
                            f"Maximum retries reached "
                            f"for {func.__name__}"
                        )

                        raise

                    delay = min(
                        config.base_delay *
                        (
                            config.exponential_base
                            ** attempt
                        ),
                        config.max_delay
                    )

                    logger.info(
                        f"Retrying in "
                        f"{delay:.2f} seconds..."
                    )

                    time.sleep(delay)

        return wrapper

    return decorator


class WorkflowStep:

    def __init__(
        self,
        name,
        function,
        retry_config=None
    ):

        self.name = name
        self.function = function
        self.retry_config = (
            retry_config
            or RetryConfig()
        )

        self.status = "pending"
        self.result = None
        self.error = None

    def execute(self, *args, **kwargs):

        logger.info(
            f"Starting step: {self.name}"
        )

        try:

            wrapped = retry_with_backoff(
                self.retry_config
            )(self.function)

            self.result = wrapped(
                *args,
                **kwargs
            )

            self.status = "completed"

            logger.info(
                f"Step completed: {self.name}"
            )

            return self.result

        except Exception as e:

            self.status = "failed"

            self.error = str(e)

            logger.error(
                f"Step failed: "
                f"{self.name}: {e}"
            )

            raise
```

---

# 🧪 Step 2: Create Test Operations

Create:

```bash
nano test_operations.py
```

---

## 📄 test_operations.py

```python
import random
import time

class SimulatedFailure(Exception):
    pass


def unreliable_api_call(
    failure_rate=0.5
):

    if random.random() < failure_rate:

        raise SimulatedFailure(
            "API request failed"
        )

    return {
        "status": "success",
        "message": "API response"
    }


def flaky_file_operation(
    filepath
):

    if random.random() < 0.4:

        raise IOError(
            "File operation failed"
        )

    with open(
        filepath,
        "w"
    ) as f:

        f.write(
            "Workflow data"
        )

    return (
        f"File processed: "
        f"{filepath}"
    )


def database_transaction(
    data
):

    time.sleep(
        random.uniform(
            0.1,
            2.0
        )
    )

    if random.random() < 0.3:

        raise TimeoutError(
            "Database timeout"
        )

    return True
```

---

# ⚙️ Task 2: Create Workflow Orchestrator

---

# 📝 Step 1: Create Orchestrator

Create:

```bash
nano workflow_orchestrator.py
```

---

## 📄 workflow_orchestrator.py

```python
import logging

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:

    def __init__(self, name):

        self.name = name

        self.steps = []

        self.execution_log = []

    def add_step(self, step):

        self.steps.append(step)

        logger.info(
            f"Added step "
            f"{step.name}"
        )

    def execute(
        self,
        continue_on_error=False
    ):

        logger.info(
            f"Starting workflow "
            f"{self.name}"
        )

        results = []

        for step in self.steps:

            try:

                result = step.execute()

                results.append(
                    {
                        "step": step.name,
                        "status": step.status
                    }
                )

            except Exception as e:

                results.append(
                    {
                        "step": step.name,
                        "status": "failed",
                        "error": str(e)
                    }
                )

                if not continue_on_error:

                    break

        return self.get_execution_summary()

    def get_execution_summary(self):

        completed = len([
            s for s in self.steps
            if s.status == "completed"
        ])

        failed = len([
            s for s in self.steps
            if s.status == "failed"
        ])

        pending = len([
            s for s in self.steps
            if s.status == "pending"
        ])

        total = len(self.steps)

        success_rate = (
            completed / total * 100
        ) if total else 0

        return {

            "total_steps": total,

            "completed": completed,

            "failed": failed,

            "pending": pending,

            "success_rate":
                round(success_rate, 2)
        }

    def save_execution_log(
        self,
        filepath
    ):

        with open(
            filepath,
            "w"
        ) as f:

            summary = (
                self.get_execution_summary()
            )

            f.write(
                "WORKFLOW SUMMARY\n"
            )

            f.write(
                str(summary)
            )
```

---

# 🚀 Step 2: Create Main Workflow

Create:

```bash
nano main_workflow.py
```

---

## 📄 main_workflow.py

```python
#!/usr/bin/env python3

from workflow_engine import (
    WorkflowStep,
    RetryConfig
)

from workflow_orchestrator import (
    WorkflowOrchestrator
)

from test_operations import (
    unreliable_api_call,
    flaky_file_operation,
    database_transaction
)


def main():

    workflow = WorkflowOrchestrator(
        "Production Workflow"
    )

    aggressive_retry = RetryConfig(
        max_attempts=5,
        base_delay=0.5
    )

    standard_retry = RetryConfig(
        max_attempts=3,
        base_delay=1
    )

    conservative_retry = RetryConfig(
        max_attempts=2,
        base_delay=2
    )

    api_step = WorkflowStep(
        "API Call",
        unreliable_api_call,
        aggressive_retry
    )

    file_step = WorkflowStep(
        "File Operation",
        lambda:
        flaky_file_operation(
            "workflow.txt"
        ),
        standard_retry
    )

    db_step = WorkflowStep(
        "Database Transaction",
        lambda:
        database_transaction(
            {"id": 1}
        ),
        conservative_retry
    )

    workflow.add_step(api_step)

    workflow.add_step(file_step)

    workflow.add_step(db_step)

    summary = workflow.execute(
        continue_on_error=True
    )

    print("\nExecution Summary")

    print(summary)

    workflow.save_execution_log(
        "workflow_execution.log"
    )


if __name__ == "__main__":
    main()
```

---

# ▶️ Run the Workflow

```bash
chmod +x main_workflow.py

python3 main_workflow.py
```

---

# 📄 View Logs

```bash
cat workflow.log
```

Example:

```text
Attempt 1/5 for unreliable_api_call
Attempt failed
Retrying in 1 second
Attempt 2/5
Success
```

---

# 📊 View Execution Summary

```bash
cat workflow_execution.log
```

Example:

```text
WORKFLOW SUMMARY

Total Steps: 3
Completed: 3
Failed: 0
Pending: 0
Success Rate: 100%
```

---

# ✅ Verification

---

## Verify Retry Logic

Create:

```bash
nano verify_retry.py
```

```python
from workflow_engine import (
    WorkflowStep,
    RetryConfig
)

from test_operations import (
    unreliable_api_call
)

config = RetryConfig(
    max_attempts=5,
    base_delay=0.5
)

step = WorkflowStep(
    "Retry Test",
    unreliable_api_call,
    config
)

try:

    result = step.execute(
        failure_rate=0.7
    )

    print(result)

except Exception as e:

    print(e)

print(step.status)
```

Run:

```bash
python3 verify_retry.py
```

---

## Verify Logging

```bash
test -f workflow.log \
&& echo "Log created"
```

Count attempts:

```bash
grep -c "Attempt" workflow.log
```

View errors:

```bash
grep "ERROR" workflow.log
```

---

## Verify Workflow Report

```bash
test -f workflow_execution.log \
&& cat workflow_execution.log
```

---

# 🎯 Expected Outcomes

Upon completion you should have:

✅ Retry Decorator

✅ Exponential Backoff

✅ Exception Handling

✅ Workflow Orchestration

✅ Centralized Logging

✅ Execution Reporting

---

# 🛠️ Troubleshooting

---

## ❌ Retries Too Fast

Increase delay:

```python
RetryConfig(
    base_delay=5
)
```

---

## ❌ Workflow Stops Early

Enable:

```python
continue_on_error=True
```

---

## ❌ No Logs Generated

Verify permissions:

```bash
ls -la workflow.log
```

Check logging configuration.

---

## ❌ Import Errors

Verify project structure:

```text
fault-tolerant-workflow/
│
├── workflow_engine.py
├── workflow_orchestrator.py
├── test_operations.py
├── main_workflow.py
└── verify_retry.py
```

---

# 🌍 Real-World Applications

### ☁️ Cloud Automation

Retry failed cloud API operations.

### 🚀 CI/CD Pipelines

Recover from transient deployment failures.

### 🏦 Financial Systems

Ensure transaction processing reliability.

### 📊 Data Pipelines

Handle intermittent ETL failures.

### 🔐 Security Automation

Retry security scans and compliance checks.

---

# 🚀 Next Steps

* Add asynchronous workflow execution
* Implement workflow dependencies
* Integrate Prometheus metrics
* Export logs to ELK Stack
* Add Slack/Email notifications
* Build workflow dashboards

---

# 🎉 Lab Completed Successfully

You have successfully built a fault-tolerant workflow system featuring:

🛡️ Automatic Retry Logic

⚡ Exponential Backoff

📊 Workflow Orchestration

📝 Comprehensive Logging

🔍 Failure Monitoring

🚀 Production-Ready Resilience Patterns

These are foundational concepts used in enterprise automation, distributed systems, DevOps pipelines, and cloud-native applications.

---

# 🧹 Cleanup

```bash
# Deactivate virtual environment
deactivate

# Optional cleanup
cd ~

rm -rf ~/fault-tolerant-workflow
```

### 🚀 Happy Automating & Building Resilient Systems!
