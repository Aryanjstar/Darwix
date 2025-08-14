"""
Hackathon-specific markdown formatter that matches the EXACT required format.
"""

from typing import List
from ..core.models import ReviewComment


class HackathonFormatter:
    """Formats output to match hackathon requirements exactly."""
    
    def generate_hackathon_report(self, code_snippet: str, comments: List[ReviewComment], language: str) -> str:
        """Generate report in EXACT hackathon format."""
        
        report = []
        
        # Process each comment in the exact format required
        for comment in comments:
            report.append("---")
            report.append(f'### Analysis of Comment: "{comment.original}"')
            report.append("")
            
            # Positive Rephrasing (EXACT format)
            report.append(f"* **Positive Rephrasing:** \"{comment.positive_rephrase}\"")
            report.append("")
            
            # The 'Why' (EXACT format)  
            report.append(f"* **The 'Why':** {comment.explanation}")
            report.append("")
            
            # Suggested Improvement (EXACT format)
            report.append("* **Suggested Improvement:**")
            report.append(f"```{language}")
            report.append(comment.code_suggestion)
            report.append("```")
            report.append("")
        
        report.append("---")
        
        # Add holistic summary
        report.append("")
        report.append("## Overall Assessment")
        report.append("")
        report.append(f"Great work on this code! The {len(comments)} suggestions above represent valuable learning opportunities that will help you grow as a developer. Remember, every experienced developer has received similar feedback throughout their journey - it's all part of the collaborative process that makes our code stronger and our teams more effective.")
        report.append("")
        report.append("Each suggestion is designed to help you write more maintainable, efficient, and readable code. Take your time implementing these changes, and don't hesitate to ask questions if anything needs clarification. You're on a great path, and these improvements will make your code even better!")
        report.append("")
        report.append("Keep up the excellent work! 🚀")
        
        return "\n".join(report)
