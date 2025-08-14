"""
Empathetic Code Reviewer - AI-Powered Code Review Feedback Transformer

A production-grade tool that transforms direct code review feedback into 
constructive, empathetic guidance that promotes team collaboration and learning.

Author: Software Engineering Team
Version: 1.0.0
"""

from .core.reviewer import EmpathethicCodeReviewer
from .core.models import ReviewComment

__version__ = "1.0.0"
__all__ = ["EmpathethicCodeReviewer", "ReviewComment"]
