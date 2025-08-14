"""
Sentiment analysis module for code review comments.

This module analyzes the sentiment and severity of code review comments
to determine how harsh or supportive they are.
"""

import logging
from typing import Dict, List, Tuple
from ..core.models import SeverityLevel


class SentimentAnalyzer:
    """
    Advanced sentiment analyzer for code review comments.
    
    This class analyzes the tone and severity of feedback to help
    generate appropriately empathetic responses.
    """
    
    def __init__(self):
        """Initialize the sentiment analyzer with pattern mappings."""
        self.logger = logging.getLogger(__name__)
        self._setup_patterns()
    
    def _setup_patterns(self):
        """Setup sentiment analysis patterns."""
        self.severity_patterns = {
            'critical': {
                'patterns': ['terrible', 'awful', 'horrible', 'disaster', 'broken', 
                           'completely wrong', 'garbage', 'trash', 'useless', 'stupid'],
                'weight': 4.0
            },
            'high': {
                'patterns': ['bad', 'wrong', 'inefficient', 'poor', 'don\'t', 'never', 
                           'avoid', 'terrible', 'horrible', 'ugly', 'messy'],
                'weight': 3.0
            },
            'medium': {
                'patterns': ['should', 'better', 'improve', 'consider', 'prefer', 
                           'recommend', 'change', 'fix', 'update', 'modify'],
                'weight': 2.0
            },
            'low': {
                'patterns': ['could', 'might', 'perhaps', 'suggestion', 'minor', 
                           'optional', 'nice to have', 'consider', 'maybe'],
                'weight': 1.0
            }
        }
        
        # Positive indicators that reduce severity
        self.positive_indicators = [
            'good', 'nice', 'great', 'excellent', 'well done', 'solid',
            'clean', 'clear', 'readable', 'elegant', 'smart'
        ]
        
        # Context modifiers
        self.intensity_modifiers = {
            'very': 1.5, 'extremely': 2.0, 'really': 1.3, 'quite': 1.2,
            'somewhat': 0.8, 'slightly': 0.6, 'a bit': 0.7, 'kind of': 0.8
        }
        
        # Constructive language indicators
        self.constructive_indicators = [
            'suggest', 'recommend', 'consider', 'perhaps', 'maybe',
            'what if', 'how about', 'you could', 'try', 'think about'
        ]
    
    def analyze_sentiment(self, comment: str) -> Tuple[SeverityLevel, float, Dict]:
        """
        Analyze the sentiment and severity of a comment.
        
        Args:
            comment: The comment to analyze
            
        Returns:
            Tuple of (severity_level, confidence, analysis_details)
        """
        comment_lower = comment.lower()
        analysis_details = {
            'severity_scores': {},
            'positive_indicators': [],
            'constructive_indicators': [],
            'intensity_modifiers': [],
            'overall_tone': 'neutral'
        }
        
        # Calculate severity scores
        severity_scores = self._calculate_severity_scores(comment_lower, analysis_details)
        
        # Apply modifiers
        modified_scores = self._apply_modifiers(comment_lower, severity_scores, analysis_details)
        
        # Determine primary severity
        if not modified_scores:
            return SeverityLevel.LOW, 0.3, analysis_details
        
        primary_severity_str = max(modified_scores, key=modified_scores.get)
        primary_severity = SeverityLevel(primary_severity_str)
        
        # Calculate confidence
        confidence = self._calculate_confidence(modified_scores, analysis_details)
        
        # Determine overall tone
        analysis_details['overall_tone'] = self._determine_tone(analysis_details)
        analysis_details['severity_scores'] = modified_scores
        
        self.logger.debug(f"Sentiment analysis: {primary_severity.value} (confidence: {confidence:.2f})")
        
        return primary_severity, confidence, analysis_details
    
    def _calculate_severity_scores(self, comment_lower: str, analysis_details: Dict) -> Dict[str, float]:
        """Calculate base severity scores."""
        severity_scores = {}
        
        for severity, config in self.severity_patterns.items():
            score = 0.0
            patterns = config['patterns']
            weight = config['weight']
            
            for pattern in patterns:
                if pattern in comment_lower:
                    # Count occurrences but cap to avoid skewing
                    occurrences = min(comment_lower.count(pattern), 3)
                    score += weight * occurrences
            
            if score > 0:
                # Normalize by pattern count and weight
                normalized_score = score / (len(patterns) * weight)
                severity_scores[severity] = normalized_score
        
        return severity_scores
    
    def _apply_modifiers(self, comment_lower: str, severity_scores: Dict, analysis_details: Dict) -> Dict[str, float]:
        """Apply intensity and context modifiers."""
        modified_scores = severity_scores.copy()
        
        # Check for positive indicators
        positive_count = 0
        for indicator in self.positive_indicators:
            if indicator in comment_lower:
                positive_count += 1
                analysis_details['positive_indicators'].append(indicator)
        
        # Check for constructive language
        constructive_count = 0
        for indicator in self.constructive_indicators:
            if indicator in comment_lower:
                constructive_count += 1
                analysis_details['constructive_indicators'].append(indicator)
        
        # Check for intensity modifiers
        intensity_factor = 1.0
        for modifier, factor in self.intensity_modifiers.items():
            if modifier in comment_lower:
                intensity_factor *= factor
                analysis_details['intensity_modifiers'].append((modifier, factor))
        
        # Apply modifiers
        for severity in modified_scores:
            # Reduce severity for positive/constructive language
            if positive_count > 0:
                modified_scores[severity] *= (1.0 - 0.2 * positive_count)
            
            if constructive_count > 0:
                modified_scores[severity] *= (1.0 - 0.15 * constructive_count)
            
            # Apply intensity modifiers
            modified_scores[severity] *= intensity_factor
        
        return modified_scores
    
    def _calculate_confidence(self, severity_scores: Dict, analysis_details: Dict) -> float:
        """Calculate confidence score for the analysis."""
        if not severity_scores:
            return 0.3
        
        max_score = max(severity_scores.values())
        score_spread = max_score - min(severity_scores.values()) if len(severity_scores) > 1 else max_score
        
        # Higher confidence for clear severity signals
        confidence = min(max_score * 2, 1.0)
        
        # Reduce confidence for mixed signals
        if len(severity_scores) > 2:
            confidence *= 0.8
        
        # Boost confidence for clear indicators
        if analysis_details['positive_indicators'] or analysis_details['constructive_indicators']:
            confidence *= 1.1
        
        return min(confidence, 1.0)
    
    def _determine_tone(self, analysis_details: Dict) -> str:
        """Determine the overall tone of the comment."""
        positive_count = len(analysis_details['positive_indicators'])
        constructive_count = len(analysis_details['constructive_indicators'])
        
        if positive_count > 0 and constructive_count > 0:
            return 'constructive'
        elif positive_count > 0:
            return 'positive'
        elif constructive_count > 0:
            return 'neutral-constructive'
        elif any(score > 0.7 for score in analysis_details['severity_scores'].values()):
            return 'harsh'
        else:
            return 'neutral'
    
    def get_empathy_level_needed(self, severity: SeverityLevel, tone: str) -> str:
        """
        Determine the level of empathy needed in the response.
        
        Args:
            severity: The severity level of the comment
            tone: The overall tone of the comment
            
        Returns:
            Empathy level needed ('low', 'medium', 'high', 'maximum')
        """
        if severity == SeverityLevel.CRITICAL or tone == 'harsh':
            return 'maximum'
        elif severity == SeverityLevel.HIGH:
            return 'high'
        elif severity == SeverityLevel.MEDIUM and tone in ['neutral', 'neutral-constructive']:
            return 'medium'
        else:
            return 'low'
    
    def suggest_response_tone(self, severity: SeverityLevel, analysis_details: Dict) -> Dict[str, str]:
        """
        Suggest the appropriate response tone and approach.
        
        Returns:
            Dictionary with tone suggestions
        """
        tone = analysis_details['overall_tone']
        empathy_level = self.get_empathy_level_needed(severity, tone)
        
        suggestions = {
            'empathy_level': empathy_level,
            'approach': '',
            'key_phrases': [],
            'avoid_phrases': []
        }
        
        if empathy_level == 'maximum':
            suggestions['approach'] = 'highly_supportive'
            suggestions['key_phrases'] = [
                'Great effort on this!', 'I really appreciate your work here',
                'This shows good thinking', 'Let me share a gentle suggestion'
            ]
            suggestions['avoid_phrases'] = [
                'This is wrong', 'You should know', 'Obviously', 'Simply'
            ]
        elif empathy_level == 'high':
            suggestions['approach'] = 'supportive'
            suggestions['key_phrases'] = [
                'Nice work!', 'Good foundation here', 'Here\'s an idea',
                'Consider this approach'
            ]
        elif empathy_level == 'medium':
            suggestions['approach'] = 'constructive'
            suggestions['key_phrases'] = [
                'Good code!', 'Here\'s a suggestion', 'You might consider',
                'This could be enhanced'
            ]
        else:
            suggestions['approach'] = 'collaborative'
            suggestions['key_phrases'] = [
                'Nice approach', 'Small enhancement', 'Quick suggestion',
                'Minor improvement'
            ]
        
        return suggestions
