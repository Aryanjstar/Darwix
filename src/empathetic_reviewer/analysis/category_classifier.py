"""
Category classification module for code review comments.

This module classifies code review comments into categories like
performance, readability, convention, etc.
"""

import logging
from typing import Dict, List, Tuple
from ..core.models import CategoryType, ImpactLevel


class CategoryClassifier:
    """
    Advanced category classifier for code review comments.
    
    This class analyzes comments to determine their primary category
    and potential impact on the codebase.
    """
    
    def __init__(self):
        """Initialize the category classifier with pattern mappings."""
        self.logger = logging.getLogger(__name__)
        self._setup_patterns()
    
    def _setup_patterns(self):
        """Setup category classification patterns."""
        self.category_patterns = {
            'performance': {
                'patterns': [
                    'slow', 'inefficient', 'performance', 'loop', 'complexity', 'optimization',
                    'memory', 'cpu', 'algorithm', 'big-o', 'scalability', 'bottleneck',
                    'time complexity', 'space complexity', 'optimization', 'caching',
                    'lazy loading', 'eager loading', 'n+1', 'query optimization'
                ],
                'weight': 3.0,
                'typical_impact': 'high'
            },
            'readability': {
                'patterns': [
                    'name', 'variable', 'readable', 'clear', 'confusing', 'understand',
                    'descriptive', 'meaningful', 'self-documenting', 'clarity',
                    'comment', 'documentation', 'explain', 'verbose', 'concise',
                    'naming', 'identifier', 'abbreviation'
                ],
                'weight': 2.0,
                'typical_impact': 'medium'
            },
            'convention': {
                'patterns': [
                    'convention', 'style', 'pep', 'format', 'standard', 'guideline',
                    'consistent', 'coding standard', 'best practice', 'linting',
                    'formatting', 'indentation', 'spacing', 'camelcase', 'snake_case',
                    'pascal case', 'kebab-case'
                ],
                'weight': 1.5,
                'typical_impact': 'low'
            },
            'logic': {
                'patterns': [
                    'logic', 'bug', 'error', 'wrong', 'issue', 'condition', 'boolean',
                    'control flow', 'branch', 'edge case', 'null check', 'validation',
                    'exception', 'handling', 'try-catch', 'if-else', 'switch'
                ],
                'weight': 4.0,
                'typical_impact': 'high'
            },
            'security': {
                'patterns': [
                    'security', 'vulnerability', 'injection', 'validation', 'sanitize',
                    'authentication', 'authorization', 'xss', 'csrf', 'sql injection',
                    'input validation', 'output encoding', 'privilege escalation',
                    'data exposure', 'encryption', 'hashing'
                ],
                'weight': 5.0,
                'typical_impact': 'high'
            },
            'maintainability': {
                'patterns': [
                    'maintainable', 'refactor', 'duplicate', 'dry', 'solid', 'coupling',
                    'cohesion', 'separation', 'modular', 'reusable', 'extensible',
                    'flexible', 'testable', 'clean code', 'technical debt',
                    'code smell', 'single responsibility'
                ],
                'weight': 2.5,
                'typical_impact': 'medium'
            }
        }
        
        # Context-specific patterns that help with disambiguation
        self.context_patterns = {
            'performance': ['faster', 'slower', 'optimize', 'benchmark', 'profiling'],
            'readability': ['understand', 'confusing', 'clear', 'obvious', 'readable'],
            'convention': ['style guide', 'linter', 'format', 'consistent', 'standard'],
            'logic': ['bug', 'incorrect', 'fails', 'broken', 'wrong result'],
            'security': ['attack', 'exploit', 'secure', 'safe', 'protect'],
            'maintainability': ['maintain', 'extend', 'modify', 'change', 'evolve']
        }
        
        # Impact indicators
        self.impact_indicators = {
            'high': [
                'critical', 'important', 'major', 'significant', 'breaking',
                'production', 'user-facing', 'data loss', 'security', 'performance'
            ],
            'medium': [
                'moderate', 'noticeable', 'improvement', 'enhancement', 'quality',
                'maintainability', 'readability', 'team', 'developer experience'
            ],
            'low': [
                'minor', 'small', 'cosmetic', 'style', 'formatting', 'convention',
                'nice to have', 'optional', 'preference'
            ]
        }
    
    def classify_comment(self, comment: str, code_snippet: str = None) -> Tuple[CategoryType, float, ImpactLevel]:
        """
        Classify a comment into a category with confidence and impact assessment.
        
        Args:
            comment: The comment to classify
            code_snippet: Optional code context for better classification
            
        Returns:
            Tuple of (category, confidence, impact_level)
        """
        comment_lower = comment.lower()
        
        # Calculate category scores
        category_scores = self._calculate_category_scores(comment_lower)
        
        # Apply context from code snippet if available
        if code_snippet:
            category_scores = self._apply_code_context(category_scores, code_snippet.lower())
        
        # Determine primary category
        if not category_scores:
            return CategoryType.GENERAL, 0.3, ImpactLevel.LOW
        
        primary_category_str = max(category_scores, key=category_scores.get)
        primary_category = CategoryType(primary_category_str)
        
        # Calculate confidence
        confidence = self._calculate_confidence(category_scores, comment_lower)
        
        # Assess impact level
        impact_level = self._assess_impact_level(primary_category, comment_lower)
        
        self.logger.debug(f"Category classification: {primary_category.value} (confidence: {confidence:.2f}, impact: {impact_level.value})")
        
        return primary_category, confidence, impact_level
    
    def _calculate_category_scores(self, comment_lower: str) -> Dict[str, float]:
        """Calculate base category scores."""
        category_scores = {}
        
        for category, config in self.category_patterns.items():
            score = 0.0
            patterns = config['patterns']
            weight = config['weight']
            
            # Score pattern matches
            for pattern in patterns:
                if pattern in comment_lower:
                    # Count occurrences but cap to avoid skewing
                    occurrences = min(comment_lower.count(pattern), 2)
                    score += weight * occurrences
            
            # Apply context patterns for disambiguation
            if category in self.context_patterns:
                for context_pattern in self.context_patterns[category]:
                    if context_pattern in comment_lower:
                        score *= 1.2  # Boost score for context match
            
            if score > 0:
                # Normalize by pattern count and weight
                normalized_score = score / (len(patterns) * weight)
                category_scores[category] = normalized_score
        
        return category_scores
    
    def _apply_code_context(self, category_scores: Dict, code_snippet_lower: str) -> Dict[str, float]:
        """Apply code context to refine category scores."""
        # Code-based hints for categories
        code_hints = {
            'performance': ['for ', 'while ', 'loop', 'iteration', 'list comprehension'],
            'readability': ['variable', 'function', 'method', 'class'],
            'convention': ['import', 'def ', 'class ', 'function'],
            'logic': ['if ', 'else', 'elif', 'try:', 'except:', 'return'],
            'security': ['input', 'request', 'user', 'data', 'password'],
            'maintainability': ['class', 'function', 'method', 'module']
        }
        
        for category, hints in code_hints.items():
            if category in category_scores:
                hint_matches = sum(1 for hint in hints if hint in code_snippet_lower)
                if hint_matches > 0:
                    # Boost category score based on code context
                    boost_factor = 1.0 + (hint_matches * 0.1)
                    category_scores[category] *= boost_factor
        
        return category_scores
    
    def _calculate_confidence(self, category_scores: Dict, comment_lower: str) -> float:
        """Calculate confidence score for the classification."""
        if not category_scores:
            return 0.3
        
        max_score = max(category_scores.values())
        
        # Base confidence from score strength
        confidence = min(max_score * 1.5, 1.0)
        
        # Reduce confidence for ambiguous cases
        if len(category_scores) > 2:
            confidence *= 0.9
        
        # Check for clear category indicators
        clear_indicators = 0
        for category, patterns in self.context_patterns.items():
            if any(pattern in comment_lower for pattern in patterns):
                clear_indicators += 1
        
        if clear_indicators == 1:  # Exactly one clear indicator
            confidence *= 1.1
        elif clear_indicators > 1:  # Multiple indicators reduce confidence
            confidence *= 0.8
        
        return min(confidence, 1.0)
    
    def _assess_impact_level(self, category: CategoryType, comment_lower: str) -> ImpactLevel:
        """Assess the potential impact level of the issue."""
        # Get typical impact for category
        typical_impact = self.category_patterns.get(category.value, {}).get('typical_impact', 'medium')
        
        # Check for explicit impact indicators in comment
        for impact, indicators in self.impact_indicators.items():
            if any(indicator in comment_lower for indicator in indicators):
                return ImpactLevel(impact)
        
        # Special cases based on category
        if category == CategoryType.SECURITY:
            return ImpactLevel.HIGH
        elif category in [CategoryType.LOGIC, CategoryType.PERFORMANCE]:
            return ImpactLevel.HIGH if any(word in comment_lower for word in ['critical', 'major', 'serious']) else ImpactLevel.MEDIUM
        elif category == CategoryType.CONVENTION:
            return ImpactLevel.LOW
        
        # Fall back to typical impact for category
        return ImpactLevel(typical_impact)
    
    def get_category_description(self, category: CategoryType) -> str:
        """Get a human-readable description of a category."""
        descriptions = {
            CategoryType.PERFORMANCE: "Code efficiency and execution speed",
            CategoryType.READABILITY: "Code clarity and understandability",
            CategoryType.CONVENTION: "Coding standards and style guidelines",
            CategoryType.LOGIC: "Code correctness and business logic",
            CategoryType.SECURITY: "Security vulnerabilities and data protection",
            CategoryType.MAINTAINABILITY: "Code structure and long-term maintainability",
            CategoryType.GENERAL: "General code improvement"
        }
        return descriptions.get(category, "Code improvement")
    
    def get_learning_focus(self, category: CategoryType) -> str:
        """Get the learning focus area for a category."""
        learning_focuses = {
            CategoryType.PERFORMANCE: "Algorithm optimization and performance tuning",
            CategoryType.READABILITY: "Clean code principles and documentation",
            CategoryType.CONVENTION: "Industry standards and best practices",
            CategoryType.LOGIC: "Problem-solving and debugging techniques",
            CategoryType.SECURITY: "Secure coding practices and vulnerability prevention",
            CategoryType.MAINTAINABILITY: "Software architecture and design patterns",
            CategoryType.GENERAL: "Overall software development skills"
        }
        return learning_focuses.get(category, "Software development fundamentals")
