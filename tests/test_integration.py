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

    @pytest.mark.asyncio

    @pytest.mark.asyncio
