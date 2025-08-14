"""
Programming language detection module.

This module provides sophisticated language detection capabilities
for code snippets using pattern matching and confidence scoring.
"""

import logging
from typing import Dict, List, Tuple


class LanguageDetector:
    """
    Advanced programming language detector using pattern matching.
    
    This class analyzes code snippets to determine the most likely
    programming language with confidence scoring.
    """
    
    def __init__(self):
        """Initialize the language detector with pattern mappings."""
        self.logger = logging.getLogger(__name__)
        self._setup_patterns()
    
    def _setup_patterns(self):
        """Setup language detection patterns with weights."""
        self.language_patterns = {
            'python': {
                'patterns': [
                    'def ', 'import ', 'from ', 'class ', ':', '__init__', 'self.',
                    'elif', 'True', 'False', 'None', 'lambda', 'print(', 'len('
                ],
                'strong_indicators': ['def ', 'import ', '__init__', 'self.'],
                'file_extensions': ['.py', '.pyw']
            },
            'javascript': {
                'patterns': [
                    'function', 'const ', 'let ', 'var ', '=>', 'console.log',
                    'document.', 'window.', 'typeof', 'undefined', 'null', '===', '!=='
                ],
                'strong_indicators': ['function', 'const ', 'let ', '=>'],
                'file_extensions': ['.js', '.mjs']
            },
            'typescript': {
                'patterns': [
                    'interface', 'type ', ': string', ': number', ': boolean',
                    'implements', 'extends', 'generic', 'namespace', 'export '
                ],
                'strong_indicators': ['interface', ': string', ': number', 'implements'],
                'file_extensions': ['.ts', '.tsx']
            },
            'java': {
                'patterns': [
                    'public class', 'private ', 'protected ', 'public static void',
                    'import java.', 'System.out.', '@Override', 'throws', 'extends'
                ],
                'strong_indicators': ['public class', 'public static void', 'import java.'],
                'file_extensions': ['.java']
            },
            'cpp': {
                'patterns': [
                    '#include', 'int main', 'std::', 'cout', 'cin', 'namespace',
                    'template', 'class', 'struct', 'using namespace'
                ],
                'strong_indicators': ['#include', 'int main', 'std::', 'using namespace'],
                'file_extensions': ['.cpp', '.cc', '.cxx', '.h', '.hpp']
            },
            'csharp': {
                'patterns': [
                    'using System', 'public class', 'private ', 'public ',
                    'Console.WriteLine', 'string', 'int', 'bool', 'namespace'
                ],
                'strong_indicators': ['using System', 'Console.WriteLine', 'namespace'],
                'file_extensions': ['.cs']
            },
            'go': {
                'patterns': [
                    'package ', 'import (', 'func ', 'var ', 'type ', 'struct',
                    'interface', 'go ', 'defer', 'chan'
                ],
                'strong_indicators': ['package ', 'func ', 'go ', 'defer'],
                'file_extensions': ['.go']
            },
            'rust': {
                'patterns': [
                    'fn ', 'let ', 'mut ', 'struct', 'enum', 'impl', 'trait',
                    'use ', 'mod ', 'pub ', 'match'
                ],
                'strong_indicators': ['fn ', 'let mut', 'impl', 'trait'],
                'file_extensions': ['.rs']
            }
        }
    
    def detect_language(self, code_snippet: str, filename: str = None) -> Tuple[str, float]:
        """
        Detect the programming language of a code snippet.
        
        Args:
            code_snippet: The code to analyze
            filename: Optional filename for additional context
            
        Returns:
            Tuple of (language, confidence_score)
        """
        if not code_snippet or not code_snippet.strip():
            return 'unknown', 0.0
        
        # Check filename extension first if provided
        if filename:
            lang_from_file = self._detect_from_filename(filename)
            if lang_from_file:
                self.logger.debug(f"Language detected from filename: {lang_from_file}")
        
        # Analyze code patterns
        language_scores = self._analyze_patterns(code_snippet)
        
        # Combine filename and pattern analysis
        if filename and lang_from_file and lang_from_file in language_scores:
            language_scores[lang_from_file] *= 1.5  # Boost filename match
        
        # Find the best match
        if not language_scores or max(language_scores.values()) == 0:
            return 'unknown', 0.1
        
        best_language = max(language_scores, key=language_scores.get)
        confidence = min(language_scores[best_language], 1.0)
        
        self.logger.debug(f"Language detection: {best_language} (confidence: {confidence:.2f})")
        self.logger.debug(f"All scores: {language_scores}")
        
        return best_language, confidence
    
    def _detect_from_filename(self, filename: str) -> str:
        """Detect language from filename extension."""
        filename_lower = filename.lower()
        
        for language, config in self.language_patterns.items():
            for ext in config['file_extensions']:
                if filename_lower.endswith(ext):
                    return language
        
        return None
    
    def _analyze_patterns(self, code_snippet: str) -> Dict[str, float]:
        """Analyze code patterns to score languages."""
        language_scores = {}
        code_lower = code_snippet.lower()
        
        for language, config in self.language_patterns.items():
            score = 0.0
            patterns = config['patterns']
            strong_indicators = config['strong_indicators']
            
            # Score regular patterns
            for pattern in patterns:
                if pattern.lower() in code_lower:
                    weight = 2.0 if pattern in strong_indicators else 1.0
                    # Count occurrences for more accurate scoring
                    occurrences = code_lower.count(pattern.lower())
                    score += weight * min(occurrences, 3)  # Cap at 3 to avoid skewing
            
            # Normalize by pattern count
            if patterns:
                normalized_score = score / (len(patterns) * 2)  # Normalize to 0-1 range
                language_scores[language] = normalized_score
        
        return language_scores
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        return list(self.language_patterns.keys())
    
    def get_language_info(self, language: str) -> Dict:
        """Get detailed information about a specific language."""
        return self.language_patterns.get(language, {})
    
    def is_supported_language(self, language: str) -> bool:
        """Check if a language is supported."""
        return language in self.language_patterns
