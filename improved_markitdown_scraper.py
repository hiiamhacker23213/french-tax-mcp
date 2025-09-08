"""
Improved MarkItDown scraper for French tax data
"""
from markitdown import MarkItDown
import re
from typing import Dict, List, Optional

class ImprovedMarkItDownScraper:
    def __init__(self):
        self.md = MarkItDown()
    
    def get_tax_brackets(self, year: Optional[int] = None) -> Dict:
        """Get tax brackets using MarkItDown with improved parsing"""
        try:
            url = "https://www.service-public.fr/particuliers/vosdroits/F1419"
            result = self.md.convert_url(url)
            markdown_content = result.text_content
            
            # Parse markdown for tax brackets
            brackets = self._parse_brackets_from_markdown(markdown_content)
            return {
                "status": "success",
                "data": {"brackets": brackets, "year": year or 2024},
                "source": "service-public.fr"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _parse_brackets_from_markdown(self, content: str) -> List[Dict]:
        """Extract tax brackets from markdown content with better patterns"""
        brackets = []
        
        # Look for table-like structures with tax brackets
        # Pattern: "De X € à Y € | Z%"
        table_pattern = r'(\d+(?:\s\d+)*)\s*€.*?(\d+(?:\s\d+)*)\s*€.*?(\d+(?:,\d+)?)\s*%'
        matches = re.findall(table_pattern, content)
        
        for match in matches:
            min_str, max_str, rate_str = match
            try:
                min_amount = int(min_str.replace(' ', ''))
                max_amount = int(max_str.replace(' ', '')) if max_str != '∞' else None
                rate = float(rate_str.replace(',', '.'))
                
                brackets.append({
                    "min": min_amount,
                    "max": max_amount,
                    "rate": rate
                })
            except ValueError:
                continue
        
        # Fallback: look for simpler patterns
        if not brackets:
            simple_pattern = r'(\d+)\s*%.*?(\d+(?:\s\d+)*)\s*€'
            simple_matches = re.findall(simple_pattern, content)
            
            for match in simple_matches:
                rate_str, amount_str = match
                try:
                    rate = float(rate_str)
                    amount = int(amount_str.replace(' ', ''))
                    brackets.append({"rate": rate, "threshold": amount})
                except ValueError:
                    continue
        
        return brackets[:5]  # Limit to reasonable number

# Usage
if __name__ == "__main__":
    scraper = ImprovedMarkItDownScraper()
    result = scraper.get_tax_brackets()
    print(f"Found {len(result['data']['brackets'])} brackets")
    for bracket in result['data']['brackets']:
        print(bracket)
