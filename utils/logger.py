import logging
import os
from datetime import datetime
from typing import Optional
from config.settings import TestSettings

class TestLogger:
    """Centralized logging utility for the automation framework"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TestLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with file and console handlers"""
        self._logger = logging.getLogger('AutomationFramework')
        self._logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self._logger.handlers.clear()
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # File handler
        log_file = f'logs/test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log info message"""
        self._logger.info(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self._logger.debug(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self._logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self._logger.critical(message)
    
    def log_test_start(self, test_name: str):
        """Log test start with timestamp"""
        self.info(f"🚀 Starting test: {test_name}")
    
    def log_test_end(self, test_name: str, status: str):
        """Log test end with status"""
        self.info(f"✅ Test {test_name} completed with status: {status}")
    
    def log_element_action(self, action: str, element_info: str):
        """Log element interactions"""
        self.debug(f"🔍 {action}: {element_info}")
    
    def log_page_navigation(self, url: str):
        """Log page navigation"""
        self.info(f"🌐 Navigating to: {url}")

# Global logger instance
logger = TestLogger()
