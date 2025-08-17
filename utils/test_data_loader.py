import json
import os
from typing import Dict, Any, List, Optional
from utils.logger import logger

class TestDataLoader:
    """Utility class for loading and managing test data"""
    
    def __init__(self, data_file_path: str = None):
        """
        Initialize TestDataLoader
        
        Args:
            data_file_path: Path to the test data JSON file
        """
        self.data_file_path = data_file_path or "test_data/test_data.json"
        self._test_data = None
        self._load_test_data()
    
    def _load_test_data(self) -> None:
        """Load test data from JSON file"""
        try:
            if os.path.exists(self.data_file_path):
                with open(self.data_file_path, 'r', encoding='utf-8') as file:
                    self._test_data = json.load(file)
                logger.info(f"✅ Test data loaded successfully from {self.data_file_path}")
            else:
                logger.warning(f"⚠️ Test data file not found: {self.data_file_path}")
                self._test_data = {}
        except Exception as e:
            logger.error(f"❌ Failed to load test data: {str(e)}")
            self._test_data = {}
    
    def get_user_data(self, user_type: str) -> Dict[str, Any]:
        """
        Get user data by type
        
        Args:
            user_type: Type of user (valid_user, invalid_user, admin_user)
            
        Returns:
            Dictionary containing user data
        """
        try:
            user_data = self._test_data.get("users", {}).get(user_type, {})
            if not user_data:
                logger.warning(f"⚠️ User type '{user_type}' not found in test data")
            return user_data
        except Exception as e:
            logger.error(f"❌ Failed to get user data for {user_type}: {str(e)}")
            return {}
    
    def get_url(self, url_key: str) -> str:
        """
        Get URL by key
        
        Args:
            url_key: Key for the URL (github_cli, login, dashboard, etc.)
            
        Returns:
            URL string
        """
        try:
            url = self._test_data.get("urls", {}).get(url_key, "")
            if not url:
                logger.warning(f"⚠️ URL key '{url_key}' not found in test data")
            return url
        except Exception as e:
            logger.error(f"❌ Failed to get URL for {url_key}: {str(e)}")
            return ""
    
    def get_test_data(self, data_key: str) -> Any:
        """
        Get test data by key
        
        Args:
            data_key: Key for the test data
            
        Returns:
            Test data value
        """
        try:
            data = self._test_data.get("test_data", {}).get(data_key, None)
            if data is None:
                logger.warning(f"⚠️ Test data key '{data_key}' not found")
            return data
        except Exception as e:
            logger.error(f"❌ Failed to get test data for {data_key}: {str(e)}")
            return None
    
    def get_assertion_data(self, assertion_type: str, key: str = None) -> Any:
        """
        Get assertion data by type and optional key
        
        Args:
            assertion_type: Type of assertion (expected_titles, expected_texts, timeouts)
            key: Optional specific key within the assertion type
            
        Returns:
            Assertion data
        """
        try:
            assertions = self._test_data.get("assertions", {}).get(assertion_type, {})
            if key:
                data = assertions.get(key, None)
                if data is None:
                    logger.warning(f"⚠️ Assertion key '{key}' not found in {assertion_type}")
                return data
            return assertions
        except Exception as e:
            logger.error(f"❌ Failed to get assertion data for {assertion_type}: {str(e)}")
            return {}
    
    def get_performance_data(self, metric: str = None) -> Any:
        """
        Get performance data by metric
        
        Args:
            metric: Optional specific performance metric
            
        Returns:
            Performance data
        """
        try:
            performance = self._test_data.get("performance", {})
            if metric:
                data = performance.get(metric, None)
                if data is None:
                    logger.warning(f"⚠️ Performance metric '{metric}' not found")
                return data
            return performance
        except Exception as e:
            logger.error(f"❌ Failed to get performance data: {str(e)}")
            return {}
    
    def get_environment_data(self, environment: str) -> Dict[str, Any]:
        """
        Get environment-specific data
        
        Args:
            environment: Environment name (staging, production, development)
            
        Returns:
            Environment configuration data
        """
        try:
            env_data = self._test_data.get("environments", {}).get(environment, {})
            if not env_data:
                logger.warning(f"⚠️ Environment '{environment}' not found in test data")
            return env_data
        except Exception as e:
            logger.error(f"❌ Failed to get environment data for {environment}: {str(e)}")
            return {}
    
    def get_all_users(self) -> Dict[str, Dict[str, Any]]:
        """Get all user data"""
        return self._test_data.get("users", {})
    
    def get_all_urls(self) -> Dict[str, str]:
        """Get all URLs"""
        return self._test_data.get("urls", {})
    
    def get_all_assertions(self) -> Dict[str, Any]:
        """Get all assertion data"""
        return self._test_data.get("assertions", {})
    
    def reload_data(self) -> None:
        """Reload test data from file"""
        logger.info("🔄 Reloading test data from file")
        self._load_test_data()
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of loaded test data"""
        try:
            return {
                "total_users": len(self._test_data.get("users", {})),
                "total_urls": len(self._test_data.get("urls", {})),
                "total_test_data_keys": len(self._test_data.get("test_data", {})),
                "total_assertions": len(self._test_data.get("assertions", {})),
                "total_environments": len(self._test_data.get("environments", {})),
                "data_file_path": self.data_file_path,
                "data_loaded": bool(self._test_data)
            }
        except Exception as e:
            logger.error(f"❌ Failed to get data summary: {str(e)}")
            return {}

# Global test data loader instance
test_data = TestDataLoader()
