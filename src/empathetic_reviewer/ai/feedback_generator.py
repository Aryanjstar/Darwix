"""
AI feedback generation module using Azure OpenAI.
"""

import openai
import logging
from typing import Dict, Any
from ..core.models import ReviewComment
from .prompt_engineer import PromptEngineer


class FeedbackGenerator:
    """AI-powered empathetic feedback generator."""
    
    def __init__(self, ai_config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.prompt_engineer = PromptEngineer()
        self._setup_openai(ai_config)
    
    def _setup_openai(self, ai_config: Dict[str, Any]):
        """Setup OpenAI configuration."""
        if ai_config['api_type'] == 'azure':
            openai.api_type = "azure"
            openai.api_base = ai_config['api_base']
            openai.api_key = ai_config['api_key']
            openai.api_version = ai_config.get('api_version', '2023-12-01-preview')
            self.deployment_name = ai_config['deployment_name']
        else:
            openai.api_type = "open_ai"
            openai.api_key = ai_config['api_key']
            self.deployment_name = ai_config['deployment_name']
        
        self.model_name = ai_config['model_name']
    
    def generate_empathetic_response(self, code_snippet: str, comment: ReviewComment, 
                                   language: str, processing_config: Any) -> ReviewComment:
        """Generate empathetic response using AI."""
        
        prompt = self.prompt_engineer.create_empathy_prompt(code_snippet, comment, language)
        
        try:
            response = openai.ChatCompletion.create(
                engine=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert senior software engineer and mentor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=processing_config.max_tokens,
                temperature=processing_config.temperature,
                top_p=processing_config.top_p,
                frequency_penalty=processing_config.frequency_penalty,
                presence_penalty=processing_config.presence_penalty
            )
            
            content = response.choices[0].message.content.strip()
            sections = self._parse_response(content)
            
            # Clean up positive rephrase - remove extra quotes
            positive_rephrase = sections.get('rephrase', 'Great work! Here\'s a suggestion.')
            if positive_rephrase.startswith('""') and positive_rephrase.endswith('""'):
                positive_rephrase = positive_rephrase[2:-2]
            elif positive_rephrase.startswith('"') and positive_rephrase.endswith('"'):
                positive_rephrase = positive_rephrase[1:-1]
            
            # Clean up explanation - remove extra quotes  
            explanation = sections.get('explanation', 'This will enhance code quality.')
            if explanation.startswith('"') and explanation.endswith('"'):
                explanation = explanation[1:-1]
            
            comment.positive_rephrase = positive_rephrase
            comment.explanation = explanation
            
            # Clean up code suggestion - remove markdown formatting and quotes
            code_suggestion = sections.get('code', '// Improved code here')
            # Remove extra markdown code blocks if present
            if '```' in code_suggestion:
                lines = code_suggestion.split('\n')
                cleaned_lines = []
                for line in lines:
                    if not line.strip().startswith('```') and line.strip():
                        cleaned_lines.append(line)
                code_suggestion = '\n'.join(cleaned_lines).strip()
            
            # Remove quotes if present
            if code_suggestion.startswith('"') and code_suggestion.endswith('"'):
                code_suggestion = code_suggestion[1:-1]
            
            comment.code_suggestion = code_suggestion
            comment.learning_objective = sections.get('learning', 'Focus on best practices.')
            
            return comment
            
        except Exception as e:
            self.logger.error(f"AI generation failed: {e}")
            return self._fallback_response(comment)
    
    def _parse_response(self, content: str) -> Dict[str, str]:
        """Parse AI response into sections."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            if line.startswith('POSITIVE_REPHRASE:'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'rephrase'
                current_content = [line.replace('POSITIVE_REPHRASE:', '').strip()]
            elif line.startswith('EXPLANATION:'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'explanation'
                current_content = [line.replace('EXPLANATION:', '').strip()]
            elif line.startswith('CODE_IMPROVEMENT:'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'code'
                current_content = [line.replace('CODE_IMPROVEMENT:', '').strip()]
            elif line.startswith('LEARNING_OBJECTIVE:'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'learning'
                current_content = [line.replace('LEARNING_OBJECTIVE:', '').strip()]
            elif current_section and line:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _fallback_response(self, comment: ReviewComment) -> ReviewComment:
        """Provide fallback response when AI fails."""
        comment.positive_rephrase = "Great work! Here's an opportunity to enhance this further."
        comment.explanation = "This improvement will enhance code quality and maintainability."
        comment.code_suggestion = "// Enhanced code would go here"
        comment.learning_objective = "Focus on continuous improvement and best practices."
        comment.confidence = 0.3
        return comment
