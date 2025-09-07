#!/usr/bin/env python3
"""Script to run the French Tax MCP Server for development and testing."""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from french_tax_mcp.server import main

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run the French Tax MCP Server')
    parser.add_argument(
        '--port', 
        type=int, 
        default=8888, 
        help='Port to run the server on (default: 8888)'
    )
    parser.add_argument(
        '--transport',
        choices=['sse', 'streamable-http'],
        default='streamable-http',
        help='Transport protocol to use (default: streamable-http)'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Log level (default: INFO)'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    print(f"Starting French Tax MCP Server on port {args.port}")
    print(f"Transport: {args.transport}")
    print(f"Log level: {args.log_level}")
    print("Press Ctrl+C to stop the server")
    
    # Override sys.argv to pass arguments to the main function
    sys.argv = [
        'french-tax-mcp',
        '--port', str(args.port),
        f'--{args.transport}' if args.transport == 'sse' else '--streamable-http'
    ]
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)