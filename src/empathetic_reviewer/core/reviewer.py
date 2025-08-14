"""
Main empathetic code reviewer class.
"""

import logging
import time
from typing import Dict, Any, List
from datetime import datetime

from .models import ReviewComment, ReviewSummary
from .config import Config
from ..analysis import LanguageDetector, SentimentAnalyzer, CategoryClassifier
from ..ai import FeedbackGenerator
from ..output import MarkdownReporter
from ..output.hackathon_formatter import HackathonFormatter
from ..utils import ResourceManager


class EmpathethicCodeReviewer:
    """
    Production-grade empathetic code review feedback transformer.
    """
    
    def __init__(self, config_path: str = ".env"):
        """Initialize the reviewer with configuration."""
        self.config = Config(config_path)
        self._setup_logging()
        self._initialize_components()
        
        self.logger.info("Empathetic Code Reviewer initialized successfully")
    
    def _setup_logging(self):
        """Setup production-grade logging."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.log_file),
                logging.StreamHandler() if self.config.enable_console_logging else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _initialize_components(self):
        """Initialize all analysis and generation components."""
        self.language_detector = LanguageDetector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.category_classifier = CategoryClassifier()
        self.feedback_generator = FeedbackGenerator(self.config.ai_config)
        self.markdown_reporter = MarkdownReporter()
        self.hackathon_formatter = HackathonFormatter()
        self.resource_manager = ResourceManager(self.config.get_resource_mappings())
    
    def process_review(self, input_data: Dict[str, Any]) -> str:
        """Process code review and generate empathetic feedback."""
        start_time = time.time()
        
        try:
            self._validate_input(input_data)
            
            code_snippet = input_data['code_snippet']
            review_comments = input_data['review_comments']
            
            self.logger.info(f"Processing review with {len(review_comments)} comments")
            
            # Detect language
            language, lang_confidence = self.language_detector.detect_language(code_snippet)
            self.logger.info(f"Detected language: {language} (confidence: {lang_confidence:.2f})")
            
            # Process each comment
            processed_comments = []
            for i, comment_text in enumerate(review_comments, 1):
                self.logger.debug(f"Processing comment {i}/{len(review_comments)}")
                
                comment = self._analyze_comment(comment_text, code_snippet, language)
                processed_comments.append(comment)
            
            # Generate review summary
            review_summary = self._create_review_summary(processed_comments, language, time.time() - start_time)
            
            # Generate hackathon-format report
            report = self.hackathon_formatter.generate_hackathon_report(
                code_snippet, processed_comments, language
            )
            
            self.logger.info(f"Review processing completed in {review_summary.processing_time:.2f} seconds")
            return report
            
        except Exception as e:
            self.logger.error(f"Error processing review: {e}")
            raise
    
    def _analyze_comment(self, comment_text: str, code_snippet: str, language: str) -> ReviewComment:
        """Analyze a single comment comprehensively."""
        
        # Sentiment analysis
        severity, sev_confidence, sentiment_details = self.sentiment_analyzer.analyze_sentiment(comment_text)
        
        # Category classification
        category, cat_confidence, impact_level = self.category_classifier.classify_comment(
            comment_text, code_snippet
        )
        
        # Create comment object
        comment = ReviewComment(
            original=comment_text,
            severity=severity,
            category=category,
            impact_level=impact_level,
            confidence=min(sev_confidence, cat_confidence)
        )
        
        # Generate empathetic feedback
        comment = self.feedback_generator.generate_empathetic_response(
            code_snippet, comment, language, self.config.processing
        )
        
        # Add resources
        comment.resources = self.resource_manager.get_resources(language, category.value)
        
        return comment
    
    def _create_review_summary(self, comments: List[ReviewComment], language: str, processing_time: float) -> ReviewSummary:
        """Create review summary statistics."""
        categories = list(set(comment.category for comment in comments))
        severity_distribution = {}
        for comment in comments:
            sev = comment.severity.value
            severity_distribution[sev] = severity_distribution.get(sev, 0) + 1
        
        avg_confidence = sum(comment.confidence for comment in comments) / len(comments) if comments else 0
        high_impact_count = sum(1 for comment in comments if comment.impact_level.value == 'high')
        
        return ReviewSummary(
            total_comments=len(comments),
            language=language,
            categories=categories,
            severity_distribution=severity_distribution,
            avg_confidence=avg_confidence,
            high_impact_count=high_impact_count,
            processing_time=processing_time,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _validate_input(self, input_data: Dict[str, Any]) -> None:
        """Validate input data."""
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a valid JSON object")
        
        required_keys = ['code_snippet', 'review_comments']
        for key in required_keys:
            if key not in input_data:
                raise ValueError(f"Input must contain '{key}' key")
        
        code_snippet = input_data['code_snippet']
        review_comments = input_data['review_comments']
        
        if not isinstance(code_snippet, str) or not code_snippet.strip():
            raise ValueError("'code_snippet' must be a non-empty string")
        
        if not isinstance(review_comments, list) or not review_comments:
            raise ValueError("'review_comments' must be a non-empty list")
        
        if len(review_comments) > self.config.processing.max_comments:
            raise ValueError(f"Maximum {self.config.processing.max_comments} comments allowed")
        
        for i, comment in enumerate(review_comments):
            if not isinstance(comment, str) or not comment.strip():
                raise ValueError(f"Comment {i+1} must be a non-empty string")
