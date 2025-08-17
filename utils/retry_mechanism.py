import time
import functools
from typing import Callable, Any, Optional
from selenium.common.exceptions import (
    TimeoutException, 
    StaleElementReferenceException,
    ElementClickInterceptedException,
    WebDriverException
)
from utils.logger import logger

def retry_on_exception(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple = (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException),
    backoff_factor: float = 2.0
):
    """
    Decorator to retry functions on specific exceptions
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        exceptions: Tuple of exceptions to catch and retry
        backoff_factor: Multiplier for delay on each retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    logger.debug(f"Attempt {attempt + 1}/{max_attempts} for {func.__name__}")
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {current_delay} seconds..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}. "
                            f"Last error: {str(e)}"
                        )
            
            raise last_exception
        return wrapper
    return decorator

class ElementRetry:
    """Utility class for retrying element operations"""
    
    def __init__(self, max_attempts: int = 3, delay: float = 1.0):
        self.max_attempts = max_attempts
        self.delay = delay
    
    def retry_until_success(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Retry an operation until it succeeds or max attempts reached
        
        Args:
            operation: Function to retry
            *args: Arguments for the operation
            **kwargs: Keyword arguments for the operation
            
        Returns:
            Result of the operation
            
        Raises:
            Last exception if all attempts fail
        """
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                logger.debug(f"Retry attempt {attempt + 1}/{self.max_attempts}")
                return operation(*args, **kwargs)
                
            except (TimeoutException, StaleElementReferenceException, WebDriverException) as e:
                last_exception = e
                if attempt < self.max_attempts - 1:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                    time.sleep(self.delay)
                else:
                    logger.error(f"All retry attempts failed. Last error: {str(e)}")
        
        raise last_exception
    
    def retry_with_condition(
        self, 
        operation: Callable, 
        condition: Callable[[Any], bool],
        *args, **kwargs
    ) -> Any:
        """
        Retry an operation until a condition is met
        
        Args:
            operation: Function to retry
            condition: Function that takes the result and returns True if condition is met
            *args: Arguments for the operation
            **kwargs: Keyword arguments for the operation
            
        Returns:
            Result of the operation when condition is met
            
        Raises:
            TimeoutException if condition is never met
        """
        for attempt in range(self.max_attempts):
            try:
                result = operation(*args, **kwargs)
                if condition(result):
                    return result
                    
                logger.debug(f"Condition not met on attempt {attempt + 1}. Retrying...")
                time.sleep(self.delay)
                
            except Exception as e:
                if attempt < self.max_attempts - 1:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                    time.sleep(self.delay)
                else:
                    raise
        
        raise TimeoutException(f"Condition never met after {self.max_attempts} attempts")
