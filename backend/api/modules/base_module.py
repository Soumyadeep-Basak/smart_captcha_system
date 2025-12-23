"""
Base Module for Bot Detection

This module provides a common base class for all detection modules,
ensuring consistent interfaces and shared functionality.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging


class BaseDetectionModule(ABC):
    """
    Abstract base class for all bot detection modules.
    
    All detection modules should inherit from this class and implement
    the required abstract methods.
    """
    
    def __init__(self, module_name: str, version: str):
        """
        Initialize the base detection module.
        
        Args:
            module_name: Name of the detection module
            version: Version string of the module
        """
        self.module_name = module_name
        self.version = version
        self.logger = logging.getLogger(f"{__name__}.{module_name}")
        self.logger.info(f"Initializing {module_name} v{version}")
    
    @abstractmethod
    def analyze(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Perform analysis on the provided data.
        
        This method must be implemented by all subclasses.
        
        Returns:
            Dictionary containing analysis results
        """
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the module.
        
        Returns:
            Dictionary containing module metadata
        """
        pass
    
    def create_standardized_result(
        self,
        is_bot: bool,
        confidence: float,
        score: float,
        threat_level: str,
        indicators: List[str],
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized result structure.
        
        Args:
            is_bot: Whether bot behavior was detected
            confidence: Confidence score (0-1)
            score: Risk/threat score (0-1)
            threat_level: Threat level classification
            indicators: List of detected threat indicators
            additional_data: Optional additional module-specific data
            
        Returns:
            Standardized result dictionary
        """
        result = {
            'analysis': {
                'score': score,
                'threat_level': threat_level,
                'indicators': indicators,
                'total_indicators': len(indicators),
                'timestamp': self._get_timestamp()
            },
            'verdict': {
                'is_bot': is_bot,
                'confidence': confidence,
                'recommendation': self._get_recommendation(threat_level),
                'bot_probability': score
            },
            'module_info': {
                'module': self.module_name,
                'version': self.version
            }
        }
        
        if additional_data:
            result.update(additional_data)
        
        return result
    
    def create_error_result(self, error_message: str) -> Dict[str, Any]:
        """
        Create a standardized error result.
        
        Args:
            error_message: Description of the error
            
        Returns:
            Standardized error result dictionary
        """
        self.logger.error(f"Error in {self.module_name}: {error_message}")
        
        return {
            'analysis': {
                'score': 0.5,
                'threat_level': 'medium',
                'indicators': ['analysis_error'],
                'error': error_message,
                'timestamp': self._get_timestamp()
            },
            'verdict': {
                'is_bot': True,  # Default to bot on error for safety
                'confidence': 0.3,
                'recommendation': 'monitor',
                'bot_probability': 0.5
            },
            'module_info': {
                'module': self.module_name,
                'version': self.version,
                'status': 'error'
            }
        }
    
    def _get_timestamp(self) -> str:
        """Get ISO-formatted UTC timestamp."""
        return datetime.utcnow().isoformat() + 'Z'
    
    def _get_recommendation(self, threat_level: str) -> str:
        """
        Get recommendation based on threat level.
        
        Args:
            threat_level: The threat level classification
            
        Returns:
            Action recommendation string
        """
        recommendations = {
            'critical': 'block',
            'high': 'block',
            'medium': 'monitor',
            'low': 'allow',
            'minimal': 'allow'
        }
        return recommendations.get(threat_level.lower(), 'monitor')
    
    def log_analysis_start(self, data_summary: str):
        """Log the start of an analysis."""
        self.logger.info(f"Starting {self.module_name} analysis: {data_summary}")
    
    def log_analysis_complete(self, result_summary: str):
        """Log the completion of an analysis."""
        self.logger.info(f"{self.module_name} analysis complete: {result_summary}")
    
    def validate_input(self, required_fields: List[str], data: Dict[str, Any]) -> bool:
        """
        Validate that required fields are present in input data.
        
        Args:
            required_fields: List of required field names
            data: Input data dictionary
            
        Returns:
            True if all required fields are present, False otherwise
        """
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            self.logger.warning(f"Missing required fields: {missing_fields}")
            return False
        
        return True


class ConfigurableModule(BaseDetectionModule):
    """
    Base class for modules that use configuration.
    
    Extends BaseDetectionModule with configuration management.
    """
    
    def __init__(self, module_name: str, version: str, config: Dict[str, Any]):
        """
        Initialize the configurable module.
        
        Args:
            module_name: Name of the detection module
            version: Version string of the module
            config: Configuration dictionary
        """
        super().__init__(module_name, version)
        self.config = config
        self._validate_config()
    
    def _validate_config(self):
        """
        Validate the module configuration.
        
        Subclasses can override this to add specific validation logic.
        """
        if not self.config:
            self.logger.warning(f"No configuration provided for {self.module_name}")
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Safely get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def update_config(self, key: str, value: Any):
        """
        Update a configuration value.
        
        Args:
            key: Configuration key
            value: New value
        """
        self.config[key] = value
        self.logger.info(f"Updated config: {key} = {value}")
