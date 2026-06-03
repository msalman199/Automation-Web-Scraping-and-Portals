import time
import logging
from typing import Callable, Any, Optional
from functools import wraps

# Configure logging
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
    """Configuration for retry behavior"""
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0, 
                 max_delay: float = 60.0, exponential_base: float = 2.0):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base


def retry_with_backoff(config: RetryConfig, 
                       exceptions: tuple = (Exception,)):
    """
    Decorator that implements retry logic with exponential backoff.
    
    Args:
        config: RetryConfig object with retry parameters
        exceptions: Tuple of exception types to catch and retry
    
    Returns:
        Decorated function with retry capability
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            while attempt < config.max_attempts:
                try:
                    # TODO: Implement the retry logic
                    # 1. Increment attempt counter
                    # 2. Log the attempt number
                    # 3. Call the function and return result if successful
                    # 4. Calculate delay using exponential backoff formula
                    # 5. Sleep before next retry
                    pass
                except exceptions as e:
                    # TODO: Handle exceptions
                    # 1. Log the error with details
                    # 2. Check if max attempts reached
                    # 3. If max reached, log final failure and re-raise
                    # 4. Otherwise, continue to next iteration
                    pass
        return wrapper
    return decorator


class WorkflowStep:
    """Represents a single step in a workflow"""
    
    def __init__(self, name: str, function: Callable, 
                 retry_config: Optional[RetryConfig] = None):
        self.name = name
        self.function = function
        self.retry_config = retry_config or RetryConfig()
        self.status = "pending"
        self.result = None
        self.error = None
    
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the workflow step with retry logic.
        
        Returns:
            Result of the function execution
        """
        # TODO: Implement step execution
        # 1. Log step start
        # 2. Apply retry decorator to function
        # 3. Execute function with provided arguments
        # 4. Update status to "completed" and store result
        # 5. Handle any final failures and update status to "failed"
        # 6. Return result or raise exception
        pass
