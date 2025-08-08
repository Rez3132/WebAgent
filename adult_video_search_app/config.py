import os
from typing import Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

@dataclass
class APIConfig:
    """Configuration for different adult video APIs"""
    
    # Eporner API Configuration
    EPORNER_BASE_URL: str = "https://www.eporner.com/api/v2/video/search/"
    EPORNER_MAX_PER_PAGE: int = 50
    EPORNER_RATE_LIMIT: float = 1.0  # seconds between requests
    
    # RedGifs API Configuration
    REDGIFS_BASE_URL: str = "https://api.redgifs.com/v2/search"
    REDGIFS_AUTH_URL: str = "https://api.redgifs.com/v2/auth/temporary"
    REDGIFS_MAX_PER_PAGE: int = 80
    REDGIFS_RATE_LIMIT: float = 1.0
    
    # PornHub API Configuration (if using unofficial APIs)
    PORNHUB_API_KEY: str = os.getenv("PORNHUB_API_KEY", "")
    PORNHUB_BASE_URL: str = "https://www.pornhub.com/webmasters/"
    PORNHUB_RATE_LIMIT: float = 2.0
    
    # General API Settings
    REQUEST_TIMEOUT: int = 10
    MAX_RETRIES: int = 3
    USER_AGENT: str = "AdultVideoSearchApp/1.0"

@dataclass
class FlaskConfig:
    """Flask application configuration"""
    
    SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key-in-production")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("FLASK_PORT", "5000"))
    
    # Session Configuration
    SESSION_COOKIE_SECURE: bool = os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    SESSION_COOKIE_HTTPONLY: bool = True
    PERMANENT_SESSION_LIFETIME: int = 3600  # 1 hour

@dataclass
class SearchConfig:
    """Search and filtering configuration"""
    
    DEFAULT_QUERY: str = "footjob+wife"
    DEFAULT_APIS: list = None
    MAX_RESULTS_PER_API: int = 10
    DEFAULT_SORT: str = "views"  # views, rating, added, title
    ENABLE_NSFW_FILTER: bool = False
    
    def __post_init__(self):
        if self.DEFAULT_APIS is None:
            self.DEFAULT_APIS = ["eporner", "redgifs"]

@dataclass
class SecurityConfig:
    """Security and content filtering configuration"""
    
    AGE_VERIFICATION_REQUIRED: bool = True
    ENABLE_RATE_LIMITING: bool = True
    MAX_REQUESTS_PER_MINUTE: int = 60
    BLOCKED_KEYWORDS: list = None
    ALLOWED_CATEGORIES: list = None
    
    def __post_init__(self):
        if self.BLOCKED_KEYWORDS is None:
            self.BLOCKED_KEYWORDS = []
        if self.ALLOWED_CATEGORIES is None:
            self.ALLOWED_CATEGORIES = []

class Config:
    """Main configuration class that combines all config sections"""
    
    def __init__(self):
        self.api = APIConfig()
        self.flask = FlaskConfig()
        self.search = SearchConfig()
        self.security = SecurityConfig()
        
        # Environment-specific overrides
        self._load_environment_config()
    
    def _load_environment_config(self):
        """Load environment-specific configuration overrides"""
        env = os.getenv("FLASK_ENV", "development").lower()
        
        if env == "production":
            self.flask.DEBUG = False
            self.flask.SESSION_COOKIE_SECURE = True
            self.security.ENABLE_RATE_LIMITING = True
            # Increase rate limits for production
            self.api.EPORNER_RATE_LIMIT = 0.5
            self.api.REDGIFS_RATE_LIMIT = 0.5
        
        elif env == "testing":
            self.flask.DEBUG = True
            self.security.AGE_VERIFICATION_REQUIRED = False
            # Faster requests for testing
            self.api.EPORNER_RATE_LIMIT = 0.1
            self.api.REDGIFS_RATE_LIMIT = 0.1
    
    def get_api_config(self, api_name: str) -> Dict[str, Any]:
        """Get configuration for a specific API"""
        configs = {
            "eporner": {
                "base_url": self.api.EPORNER_BASE_URL,
                "max_per_page": self.api.EPORNER_MAX_PER_PAGE,
                "rate_limit": self.api.EPORNER_RATE_LIMIT,
                "timeout": self.api.REQUEST_TIMEOUT,
                "user_agent": self.api.USER_AGENT
            },
            "redgifs": {
                "base_url": self.api.REDGIFS_BASE_URL,
                "auth_url": self.api.REDGIFS_AUTH_URL,
                "max_per_page": self.api.REDGIFS_MAX_PER_PAGE,
                "rate_limit": self.api.REDGIFS_RATE_LIMIT,
                "timeout": self.api.REQUEST_TIMEOUT,
                "user_agent": self.api.USER_AGENT
            },
            "pornhub": {
                "base_url": self.api.PORNHUB_BASE_URL,
                "api_key": self.api.PORNHUB_API_KEY,
                "rate_limit": self.api.PORNHUB_RATE_LIMIT,
                "timeout": self.api.REQUEST_TIMEOUT,
                "user_agent": self.api.USER_AGENT
            }
        }
        return configs.get(api_name, {})
    
    def validate_config(self) -> Dict[str, bool]:
        """Validate configuration and return status of each component"""
        validation_results = {}
        
        # Validate Flask config
        validation_results["flask_secret_key"] = len(self.flask.SECRET_KEY) >= 16
        validation_results["flask_port"] = 1 <= self.flask.PORT <= 65535
        
        # Validate API config
        validation_results["eporner_url"] = self.api.EPORNER_BASE_URL.startswith("https://")
        validation_results["redgifs_url"] = self.api.REDGIFS_BASE_URL.startswith("https://")
        validation_results["request_timeout"] = self.api.REQUEST_TIMEOUT > 0
        
        # Validate search config
        validation_results["default_apis"] = len(self.search.DEFAULT_APIS) > 0
        validation_results["max_results"] = self.search.MAX_RESULTS_PER_API > 0
        
        return validation_results
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary (excluding sensitive data)"""
        return {
            "api": {
                "eporner_base_url": self.api.EPORNER_BASE_URL,
                "redgifs_base_url": self.api.REDGIFS_BASE_URL,
                "request_timeout": self.api.REQUEST_TIMEOUT,
                "max_retries": self.api.MAX_RETRIES
            },
            "flask": {
                "debug": self.flask.DEBUG,
                "host": self.flask.HOST,
                "port": self.flask.PORT
            },
            "search": {
                "default_query": self.search.DEFAULT_QUERY,
                "default_apis": self.search.DEFAULT_APIS,
                "max_results_per_api": self.search.MAX_RESULTS_PER_API,
                "default_sort": self.search.DEFAULT_SORT
            },
            "security": {
                "age_verification_required": self.security.AGE_VERIFICATION_REQUIRED,
                "rate_limiting_enabled": self.security.ENABLE_RATE_LIMITING,
                "max_requests_per_minute": self.security.MAX_REQUESTS_PER_MINUTE
            }
        }

# Global config instance
config = Config()

# Environment-specific configurations
class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.flask.DEBUG = True
        self.security.AGE_VERIFICATION_REQUIRED = False
        
class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.flask.DEBUG = False
        self.flask.SESSION_COOKIE_SECURE = True
        self.security.ENABLE_RATE_LIMITING = True

class TestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.flask.DEBUG = True
        self.security.AGE_VERIFICATION_REQUIRED = False
        self.api.EPORNER_RATE_LIMIT = 0.1
        self.api.REDGIFS_RATE_LIMIT = 0.1

# Factory function to get config based on environment
def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv("FLASK_ENV", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    return config_class()