#!/usr/bin/env python3
"""
Empathetic Code Reviewer - Main Application Entry Point

Production-grade AI-powered tool that transforms harsh code review feedback
into empathetic, educational guidance that promotes team collaboration.
"""

import sys
import json
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from empathetic_reviewer import EmpathethicCodeReviewer


def create_argument_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Transform code review feedback into empathetic guidance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py input.json
  echo '{"code_snippet": "def func(): pass", "review_comments": ["Add docstring"]}' | python main.py -
  python main.py --config custom.env input.json
        """
    )
    
    parser.add_argument(
        'input_file',
        help='JSON input file or "-" for stdin'
    )
    
    parser.add_argument(
        '--config', '-c',
        default='.env',
        help='Configuration file path (default: .env)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser


def read_input(input_file: str) -> dict:
    """Read and parse JSON input."""
    try:
        if input_file == '-':
            print("📥 Reading from stdin...", file=sys.stderr)
            input_text = sys.stdin.read()
        else:
            input_path = Path(input_file)
            if not input_path.exists():
                raise FileNotFoundError(f"Input file '{input_file}' not found")
            
            print(f"📥 Reading from {input_path}...", file=sys.stderr)
            with open(input_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
        
        return json.loads(input_text)
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON input - {e}")
        print("💡 Tip: Ensure your JSON is properly formatted")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def write_output(content: str, output_file: str = None):
    """Write output to file or stdout."""
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Output written to {output_path}", file=sys.stderr)
    else:
        print(content)


def main():
    """Main application entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    try:
        # Display banner
        print("🤖 Empathetic Code Review - AI-Powered Feedback Transformer", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        
        # Read input
        input_data = read_input(args.input_file)
        
        # Initialize reviewer
        print("🚀 Initializing Empathetic Code Reviewer...", file=sys.stderr)
        reviewer = EmpathethicCodeReviewer(config_path=args.config)
        
        # Process review
        print("🔄 Processing code review feedback...", file=sys.stderr)
        markdown_report = reviewer.process_review(input_data)
        
        # Write output
        write_output(markdown_report, args.output)
        
        print("✅ Review processing completed successfully!", file=sys.stderr)
        
    except ValueError as e:
        print(f"❌ Input Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        print("💡 Please check your input format and configuration", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
