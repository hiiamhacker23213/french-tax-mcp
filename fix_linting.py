#!/usr/bin/env python3
"""
Script to fix common linting issues in the French Tax MCP codebase.
"""

import os
import re
from pathlib import Path

def fix_header_comments(file_path):
    """Fix the long header comments in Python files."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the long header comment with a shorter one
    old_header = '''"""
French Tax MCP Server - A Model Context Protocol server for French tax calculations and information retrieval.

This module provides comprehensive French tax calculation capabilities including:
- Income tax calculations with progressive brackets
- Property tax calculations (Pinel, LMNP schemes)
- Business tax calculations (micro-enterprise, auto-entrepreneur)
- Tax form information and legal references
- Integration with official French government websites

Author: Corneliu CROITORU
License: MIT
"""'''
    
    new_header = '''"""French Tax MCP Server - Tax calculations and information retrieval."""'''
    
    # Also handle variations of the header
    patterns = [
        r'"""[\s\S]*?French Tax MCP Server[\s\S]*?"""',
        r'"""[\s\S]*?Model Context Protocol server for French tax[\s\S]*?"""',
    ]
    
    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, new_header, content, count=1)
            break
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_unused_imports(file_path):
    """Remove common unused imports."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Common unused imports to remove
    unused_patterns = [
        r'from typing import.*List.*',
        r'from typing import.*Tuple.*', 
        r'from typing import.*Union.*',
        r'from typing import.*Optional.*',
        r'import os\n',
        r'from datetime import datetime\n',
    ]
    
    new_lines = []
    for line in lines:
        should_remove = False
        for pattern in unused_patterns:
            if re.match(pattern, line.strip()):
                # Check if it's actually used in the file
                content = ''.join(lines)
                if 'List[' not in content and 'List ' not in content and 'from typing import.*List' in pattern:
                    should_remove = True
                elif 'Tuple[' not in content and 'Tuple ' not in content and 'from typing import.*Tuple' in pattern:
                    should_remove = True
                elif 'Union[' not in content and 'Union ' not in content and 'from typing import.*Union' in pattern:
                    should_remove = True
                elif 'Optional[' not in content and 'Optional ' not in content and 'from typing import.*Optional' in pattern:
                    should_remove = True
                elif 'os.' not in content and 'import os' in pattern:
                    should_remove = True
                elif 'datetime(' not in content and 'datetime.' not in content and 'from datetime import datetime' in pattern:
                    should_remove = True
                break
        
        if not should_remove:
            new_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def main():
    """Fix linting issues in all Python files."""
    python_files = []
    
    # Find all Python files
    for root, dirs, files in os.walk('french_tax_mcp'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files to fix")
    
    for file_path in python_files:
        print(f"Fixing {file_path}")
        fix_header_comments(file_path)
        # fix_unused_imports(file_path)  # Commented out for now as it's complex
    
    print("Done!")

if __name__ == '__main__':
    main()