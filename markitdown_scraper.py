"""
Minimal MarkItDown scraper for French tax data
"""
from markitdown import MarkItDown
import re
from typing import Dict, List, Optional

class MarkItDownScraper:
    def __init__(self):
        self.md = MarkItDown()
    
    def get_tax_brackets(self, year: Optional[int] = None) -> Dict:
        """Get tax brackets using MarkItDown"""
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
        """Extract tax brackets from markdown content"""
        brackets = []
        
        # Look for percentage patterns in markdown
        percentage_lines = re.findall(r'.*?(\d+(?:,\d+)?)\s*%.*?(\d+(?:\s?\d+)*)', content)
        
        for match in percentage_lines:
            rate_str, amount_str = match
            try:
                rate = float(rate_str.replace(',', '.'))
                amount = int(amount_str.replace(' ', ''))
                brackets.append({"rate": rate, "threshold": amount})
            except ValueError:
                continue
                
        return brackets

# Usage example
if __name__ == "__main__":
    scraper = MarkItDownScraper()
    result = scraper.get_tax_brackets()
    print(result)
