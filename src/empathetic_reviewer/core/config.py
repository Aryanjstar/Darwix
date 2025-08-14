"""
Configuration management for the Empathetic Code Reviewer.

This module handles all configuration loading, validation, and management
including environment variables, API keys, and processing parameters.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from .models import ProcessingConfig


class ConfigurationError(Exception):
    """Raised when there's an error in configuration."""
    pass


class Config:
    """
    Centralized configuration management for the application.
    
    This class handles loading configuration from environment variables,
    .env files, and provides sensible defaults for all settings.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to .env file (optional)
        """
        self.config_path = config_path or ".env"
        self._load_environment()
        self._setup_logging_config()
        self._setup_ai_config()
        self._setup_processing_config()
        
    def _load_environment(self):
        """Load environment variables from .env file if it exists."""
        env_path = Path(self.config_path)
        if env_path.exists():
            load_dotenv(env_path)
            logging.info(f"Loaded environment configuration from {env_path}")
        else:
            logging.info("No .env file found, using system environment variables")
    
    def _setup_logging_config(self):
        """Setup logging configuration."""
        self.log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        self.log_file = os.getenv('LOG_FILE', 'empathetic_reviewer.log')
        self.enable_console_logging = os.getenv('ENABLE_CONSOLE_LOGGING', 'true').lower() == 'true'
        
    def _setup_ai_config(self):
        """Setup AI/OpenAI configuration."""
        # Azure OpenAI Configuration
        self.azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.azure_openai_api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.azure_openai_deployment = os.getenv('AZURE_OPENAI_CHATGPT_DEPLOYMENT', 'gpt-4')
        self.azure_openai_model = os.getenv('AZURE_OPENAI_CHATGPT_MODEL', 'gpt-4')
        self.azure_openai_api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2023-12-01-preview')
        
        # Fallback OpenAI Configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Validate AI configuration
        self._validate_ai_config()
        
    def _setup_processing_config(self):
        """Setup processing configuration."""
        self.processing = ProcessingConfig(
            max_comments=int(os.getenv('MAX_COMMENTS', '10')),
            max_tokens=int(os.getenv('MAX_TOKENS', '1500')),
            temperature=float(os.getenv('TEMPERATURE', '0.8')),
            top_p=float(os.getenv('TOP_P', '0.95')),
            frequency_penalty=float(os.getenv('FREQUENCY_PENALTY', '0.1')),
            presence_penalty=float(os.getenv('PRESENCE_PENALTY', '0.1')),
            enable_logging=os.getenv('ENABLE_LOGGING', 'true').lower() == 'true',
            log_level=self.log_level
        )
    
    def _validate_ai_config(self):
        """Validate AI configuration."""
        has_azure = all([
            self.azure_openai_endpoint,
            self.azure_openai_api_key,
            self.azure_openai_deployment
        ])
        
        has_openai = bool(self.openai_api_key)
        
        if not (has_azure or has_openai):
            raise ConfigurationError(
                "No valid AI API configuration found. Please set either:\n"
                "- Azure OpenAI: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_CHATGPT_DEPLOYMENT\n"
                "- OpenAI: OPENAI_API_KEY"
            )
        
        self.use_azure = has_azure
        
    @property
    def is_azure_configured(self) -> bool:
        """Check if Azure OpenAI is properly configured."""
        return self.use_azure
    
    @property
    def ai_config(self) -> Dict[str, Any]:
        """Get AI configuration dictionary."""
        if self.use_azure:
            return {
                'api_type': 'azure',
                'api_base': self.azure_openai_endpoint,
                'api_key': self.azure_openai_api_key,
                'api_version': self.azure_openai_api_version,
                'deployment_name': self.azure_openai_deployment,
                'model_name': self.azure_openai_model
            }
        else:
            return {
                'api_type': 'openai',
                'api_key': self.openai_api_key,
                'deployment_name': 'gpt-4',
                'model_name': 'gpt-4'
            }
    
    def get_resource_mappings(self) -> Dict[str, Dict[str, list]]:
        """Get comprehensive resource mappings for different programming languages."""
        return {
            'python': {
                'performance': [
                    'https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions',
                    'https://wiki.python.org/moin/PythonSpeed/PerformanceTips',
                    'https://docs.python.org/3/library/profile.html'
                ],
                'readability': [
                    'https://pep8.org/', 
                    'https://google.github.io/styleguide/pyguide.html',
                    'https://realpython.com/python-code-quality/'
                ],
                'convention': [
                    'https://peps.python.org/pep-0008/', 
                    'https://peps.python.org/pep-0257/',
                    'https://docs.python-guide.org/writing/style/'
                ],
                'logic': [
                    'https://docs.python.org/3/tutorial/controlflow.html',
                    'https://realpython.com/python-conditional-statements/'
                ],
                'security': [
                    'https://owasp.org/www-project-top-ten/',
                    'https://bandit.readthedocs.io/en/latest/'
                ],
                'maintainability': [
                    'https://refactoring.guru/refactoring',
                    'https://martinfowler.com/books/refactoring.html'
                ]
            },
            'javascript': {
                'performance': [
                    'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Loops_and_iteration',
                    'https://web.dev/fast/',
                    'https://developers.google.com/web/fundamentals/performance'
                ],
                'readability': [
                    'https://google.github.io/styleguide/jsguide.html',
                    'https://github.com/airbnb/javascript',
                    'https://standardjs.com/'
                ],
                'convention': [
                    'https://eslint.org/docs/rules/',
                    'https://prettier.io/docs/en/rationale.html'
                ],
                'logic': [
                    'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling',
                    'https://javascript.info/logical-operators'
                ],
                'security': [
                    'https://owasp.org/www-project-top-ten/',
                    'https://snyk.io/learn/javascript-security/'
                ],
                'maintainability': [
                    'https://refactoring.guru/refactoring',
                    'https://github.com/ryanmcdermott/clean-code-javascript'
                ]
            },
            'java': {
                'performance': [
                    'https://docs.oracle.com/javase/tutorial/collections/algorithms/',
                    'https://www.oracle.com/technical-resources/articles/java/performance-tuning.html'
                ],
                'readability': [
                    'https://google.github.io/styleguide/javaguide.html',
                    'https://www.oracle.com/java/technologies/javase/codeconventions-contents.html'
                ],
                'convention': [
                    'https://checkstyle.sourceforge.io/',
                    'https://pmd.github.io/'
                ],
                'maintainability': [
                    'https://refactoring.guru/refactoring',
                    'https://martinfowler.com/books/refactoring.html'
                ]
            },
            'typescript': {
                'performance': [
                    'https://www.typescriptlang.org/docs/handbook/performance.html',
                    'https://github.com/Microsoft/TypeScript/wiki/Performance'
                ],
                'readability': [
                    'https://google.github.io/styleguide/tsguide.html',
                    'https://typescript-eslint.io/rules/'
                ],
                'convention': [
                    'https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html',
                    'https://typescript-eslint.io/rules/'
                ]
            }
        }
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"Config(azure={self.use_azure}, log_level={self.log_level})"
