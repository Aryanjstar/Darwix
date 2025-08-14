"""
Core data models for the Empathetic Code Reviewer.

This module defines the data structures used throughout the application
for representing code review comments and their analysis.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class SeverityLevel(Enum):
    """Enumeration for comment severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CategoryType(Enum):
    """Enumeration for feedback categories."""
    PERFORMANCE = "performance"
    READABILITY = "readability"
    CONVENTION = "convention"
    LOGIC = "logic"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    GENERAL = "general"


class ImpactLevel(Enum):
    """Enumeration for impact levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ReviewComment:
    """
    Represents a single code review comment with comprehensive analysis.
    
    This class encapsulates all the information about a code review comment,
    from the original feedback to the AI-generated empathetic response.
    """
    
    # Original comment data
    original: str
    
    # Analysis results
    severity: SeverityLevel = SeverityLevel.MEDIUM
    category: CategoryType = CategoryType.GENERAL
    impact_level: ImpactLevel = ImpactLevel.MEDIUM
    confidence: float = 0.0  # AI confidence score (0.0-1.0)
    
    # AI-generated responses
    positive_rephrase: str = ""
    explanation: str = ""
    code_suggestion: str = ""
    learning_objective: str = ""
    
    # Additional resources
    resources: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization processing."""
        # Convert string enums to enum objects if needed
        if isinstance(self.severity, str):
            self.severity = SeverityLevel(self.severity)
        if isinstance(self.category, str):
            self.category = CategoryType(self.category)
        if isinstance(self.impact_level, str):
            self.impact_level = ImpactLevel(self.impact_level)


@dataclass
class ReviewSummary:
    """
    Summary statistics and metadata for a code review analysis.
    """
    
    total_comments: int
    language: str
    categories: List[CategoryType]
    severity_distribution: dict
    avg_confidence: float
    high_impact_count: int
    processing_time: float
    timestamp: str
    
    @property
    def primary_focus_areas(self) -> str:
        """Get the primary focus areas as a formatted string."""
        return ', '.join([cat.value for cat in self.categories[:3]])


@dataclass
class ProcessingConfig:
    """
    Configuration settings for the review processing.
    """
    
    max_comments: int = 10
    max_tokens: int = 1500
    temperature: float = 0.8
    top_p: float = 0.95
    frequency_penalty: float = 0.1
    presence_penalty: float = 0.1
    enable_logging: bool = True
    log_level: str = "INFO"
