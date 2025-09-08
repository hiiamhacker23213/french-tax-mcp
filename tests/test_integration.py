#!/usr/bin/env python3
"""Integration tests for the French Tax MCP Server."""

from unittest.mock import AsyncMock, patch

import pytest

from french_tax_mcp.analyzers.income_analyzer import calculate_income_tax
from french_tax_mcp.constants import TAX_BRACKETS


class TestIntegration:
    """Integration tests for the French Tax MCP Server."""

    @pytest.mark.asyncio
    async def test_income_tax_calculation_integration(self):
        """Test income tax calculation with real data."""
        # Test with a typical salary
        result = await calculate_income_tax(50000, 2.0, 2024)

        assert result["status"] == "success"
        assert "data" in result
        assert result["data"]["net_taxable_income"] == 50000
        assert result["data"]["household_parts"] == 2.0
        assert result["data"]["total_tax"] > 0
        assert result["data"]["average_tax_rate"] >= 0
        assert result["data"]["marginal_tax_rate"] > 0

    def test_tax_brackets_constants(self):
        """Test that tax brackets constants are properly defined."""
        assert 2024 in TAX_BRACKETS
        assert len(TAX_BRACKETS[2024]) == 5

        # Check that brackets are properly structured
        for bracket in TAX_BRACKETS[2024]:
            assert "min" in bracket
            assert "rate" in bracket
            assert bracket["rate"] >= 0
            assert bracket["min"] >= 0

    @pytest.mark.asyncio
    async def test_error_handling_integration(self):
        """Test error handling in calculations."""
        # Test with zero household parts (should handle gracefully)
        result = await calculate_income_tax(50000, 0, 2024)
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_edge_cases_integration(self):
        """Test edge cases in calculations."""
        # Test with zero income
        result = await calculate_income_tax(0, 1.0, 2024)
        assert result["status"] == "success"
        assert result["data"]["total_tax"] == 0

        # Test with very high income
        result = await calculate_income_tax(1000000, 1.0, 2024)
        assert result["status"] == "success"
        assert result["data"]["total_tax"] > 0
        assert result["data"]["average_tax_rate"] > 0
