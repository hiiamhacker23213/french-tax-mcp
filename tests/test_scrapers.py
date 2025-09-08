#!/usr/bin/env python3

from unittest.mock import AsyncMock, patch

import pytest
from bs4 import BeautifulSoup

from french_tax_mcp.scrapers.base_scraper import BaseScraper
from french_tax_mcp.scrapers.legal_scraper import LegalScraper
from french_tax_mcp.scrapers.service_public_scraper import ServicePublicScraper


class TestBaseScraper:

    def test_get_page(self):
        scraper = BaseScraper("https://example.com")
        
        mock_response = AsyncMock()
        mock_response.text = "<html><body>Test</body></html>"
        mock_response.status_code = 200
        
        with patch.object(scraper, '_make_request', return_value=mock_response):
            result = scraper.get_page("/test")
            assert result is not None

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


class TestServicePublicScraper:

    @pytest.mark.asyncio
    async def test_get_tax_procedure(self):
        scraper = ServicePublicScraper()
        
        mock_response = AsyncMock()
        mock_response.text = """
        <html>
            <body>
                <h1>Tax Procedure</h1>
                <p>This is a tax procedure description.</p>
            </body>
        </html>
        """
        mock_response.status_code = 200
        
        with patch.object(scraper, '_make_request', return_value=mock_response):
            result = await scraper.get_tax_procedure("income_tax_declaration")
            
            assert result["status"] == "success"
            assert "data" in result

    @pytest.mark.asyncio
    async def test_get_tax_deadlines(self):
        scraper = ServicePublicScraper()
        
        mock_response = AsyncMock()
        mock_response.text = """
        <html>
            <body>
                <h1>Tax Deadlines</h1>
                <p>15 mai 2024</p>
            </body>
        </html>
        """
        mock_response.status_code = 200
        
        with patch.object(scraper, '_make_request', return_value=mock_response):
            result = await scraper.get_tax_deadlines(2024)
            
            assert result["status"] == "success"
            assert "data" in result


class TestLegalScraper:

    @pytest.mark.asyncio
    async def test_get_tax_article(self):
        scraper = LegalScraper()
        
        mock_response = AsyncMock()
        mock_response.text = """
        <html>
            <body>
                <h1>Article 123</h1>
                <p>This is a tax article.</p>
            </body>
        </html>
        """
        mock_response.status_code = 200
        
        with patch.object(scraper, '_make_request', return_value=mock_response):
            result = await scraper.get_tax_article("123")
            
            assert result["status"] == "success"
            assert "data" in result

    @pytest.mark.asyncio
    async def test_search_tax_law(self):
        scraper = LegalScraper()
        
        mock_response = AsyncMock()
        mock_response.text = """
        <html>
            <body>
                <div class="search-result">
                    <h3>Tax Law Result</h3>
                    <p>Search result description</p>
                </div>
            </body>
        </html>
        """
        mock_response.status_code = 200
        
        with patch.object(scraper, '_make_request', return_value=mock_response):
            result = await scraper.search_tax_law("income tax")
            
            assert result["status"] == "success"
            assert "data" in result
