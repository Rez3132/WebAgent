#!/usr/bin/env python3
"""
Production run script for the Adult Video Search Application
"""

import os
import sys
import logging
from app import app
from config import get_config

def setup_logging(config):
    """Configure logging based on environment"""
    log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper())
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set Flask app logger
    app.logger.setLevel(log_level)

def validate_environment():
    """Validate required environment variables and configuration"""
    config = get_config()
    validation_results = config.validate_config()
    
    failed_validations = [key for key, result in validation_results.items() if not result]
    
    if failed_validations:
        print("❌ Configuration validation failed:")
        for item in failed_validations:
            print(f"  - {item}")
        print("\nPlease check your configuration and environment variables.")
        return False
    
    print("✅ Configuration validation passed")
    return True

def main():
    """Main application entry point"""
    print("🚀 Starting Adult Video Search Application...")
    
    # Load configuration
    config = get_config()
    
    # Setup logging
    setup_logging(config)
    
    # Validate configuration
    if not validate_environment():
        sys.exit(1)
    
    # Configure Flask app
    app.config.update({
        'SECRET_KEY': config.flask.SECRET_KEY,
        'DEBUG': config.flask.DEBUG,
        'SESSION_COOKIE_SECURE': config.flask.SESSION_COOKIE_SECURE,
        'SESSION_COOKIE_HTTPONLY': config.flask.SESSION_COOKIE_HTTPONLY,
        'PERMANENT_SESSION_LIFETIME': config.flask.PERMANENT_SESSION_LIFETIME
    })
    
    # Print startup information
    print(f"📡 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🌐 Host: {config.flask.HOST}")
    print(f"🔌 Port: {config.flask.PORT}")
    print(f"🔍 Default APIs: {', '.join(config.search.DEFAULT_APIS)}")
    print(f"🔒 Age verification: {'Enabled' if config.security.AGE_VERIFICATION_REQUIRED else 'Disabled'}")
    print("\n" + "="*50)
    print("📱 Access the application at:")
    print(f"   http://{config.flask.HOST}:{config.flask.PORT}")
    print("="*50 + "\n")
    
    try:
        # Run the application
        app.run(
            host=config.flask.HOST,
            port=config.flask.PORT,
            debug=config.flask.DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()