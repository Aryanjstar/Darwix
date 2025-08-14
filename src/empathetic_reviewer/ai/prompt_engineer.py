"""
Advanced prompt engineering for empathetic feedback generation.
"""

import logging
from typing import Dict, Any
from ..core.models import ReviewComment, SeverityLevel, CategoryType, ImpactLevel


class PromptEngineer:
    """Sophisticated prompt engineering for AI feedback generation."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_empathy_prompt(self, code_snippet: str, comment: ReviewComment, 
                            language: str, analysis_details: Dict = None) -> str:
        """Create sophisticated empathy-focused prompt."""
        
        severity_context = {
            SeverityLevel.CRITICAL: "This feedback was extremely harsh. Transform it into highly encouraging, confidence-building language.",
            SeverityLevel.HIGH: "This was quite direct feedback. Transform it into very supportive, mentoring language.",
            SeverityLevel.MEDIUM: "This feedback could be more constructive. Make it encouraging and educational.",
            SeverityLevel.LOW: "This feedback is relatively gentle. Enhance it to be even more supportive."
        }
        
        impact_guidance = {
            ImpactLevel.HIGH: "This is significant - explain importance clearly but encouragingly.",
            ImpactLevel.MEDIUM: "This will enhance code quality - focus on learning opportunity.",
            ImpactLevel.LOW: "This is a minor enhancement - acknowledge current approach while suggesting refinements."
        }
        
        prompt = f"""You're a friendly senior developer giving code review feedback. Keep your responses concise and encouraging, similar to this example:

POSITIVE_REPHRASE: "Great start on the logic here! For better performance, especially with large user lists, we can make this more efficient by combining the checks."

EXPLANATION: "Iterating through a list and performing checks can become slow as the list grows. By using more direct methods like list comprehensions, we can often achieve the same result with cleaner and faster code."

CODE_IMPROVEMENT: "def get_active_users(users):\n    return [user for user in users if user.is_active and user.profile_complete]"

Now transform this comment: "{comment.original}"

For this {language} code:
```{language}
{code_snippet}
```

Keep your response concise, encouraging, and practical. Match the tone and length of the example above."""
        
        return prompt
    
    def create_summary_prompt(self, comments, language: str, review_stats: Dict) -> str:
        """Create prompt for holistic summary generation."""
        
        return f"""You are a senior technical mentor writing a personalized, encouraging conclusion for a code review.

REVIEW ANALYSIS:
- Programming Language: {language}
- Total Comments: {review_stats.get('total_comments', 0)}
- Primary Focus Areas: {review_stats.get('primary_focus_areas', 'various')}
- High-Impact Issues: {review_stats.get('high_impact_count', 0)}
- Overall Confidence: {review_stats.get('avg_confidence', 0.5):.2f}

Write a 2-3 paragraph conclusion that makes the developer feel valued, motivated, and excited about implementing improvements. Focus on growth mindset and collaborative learning.
"""
