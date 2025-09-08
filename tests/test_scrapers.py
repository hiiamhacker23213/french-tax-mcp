#!/usr/bin/env python3

import pytest
from bs4 import BeautifulSoup

from french_tax_mcp.scrapers.base_scraper import BaseScraper


class TestBaseScraper:

    def test_parse_html(self):
        scraper = BaseScraper("https://example.com")
        html = "<html><body><p>Test</p></body></html>"
        
        soup = scraper.parse_html(html)
        assert isinstance(soup, BeautifulSoup)
        assert soup.find("p").text == "Test"

    def test_format_result(self):
        scraper = BaseScraper("https://example.com")
        
        result = scraper.format_result("success", {"test": "data"}, "Test message")
        assert result["status"] == "success"
        assert result["data"]["test"] == "data"
        assert result["message"] == "Test message"


class TestImpotsScraper:

    @pytest.mark.asyncio
    async def test_get_tax_brackets(self):
        from french_tax_mcp.scrapers.impots_scraper import get_tax_brackets
        
        result = await get_tax_brackets(2024)
        
        assert result["status"] == "success"
        assert "data" in result
        assert "brackets" in result["data"]
        assert len(result["data"]["brackets"]) > 0
        assert "source" in result
