#!/usr/bin/env python3

from unittest.mock import AsyncMock, patch

import pytest

from french_tax_mcp.analyzers.income_analyzer import calculate_income_tax
from french_tax_mcp.constants import TAX_BRACKETS


class TestIntegration:

    @pytest.mark.asyncio
    async def test_income_tax_calculation_integration(self):
        result = await calculate_income_tax(50000, 2.0, 2024)

        assert result["status"] == "success"
        assert "data" in result
        assert result["data"]["net_taxable_income"] == 50000
        assert result["data"]["household_parts"] == 2.0
        assert result["data"]["total_tax"] > 0
        assert result["data"]["average_tax_rate"] >= 0
        assert result["data"]["marginal_tax_rate"] > 0

    def test_tax_brackets_constants(self):
        assert 2024 in TAX_BRACKETS
        assert len(TAX_BRACKETS[2024]) == 5

        for bracket in TAX_BRACKETS[2024]:
            assert "min" in bracket
            assert "rate" in bracket
            assert bracket["rate"] >= 0
            assert bracket["min"] >= 0

    @pytest.mark.asyncio
    async def test_error_handling_integration(self):
        result = await calculate_income_tax(50000, 0, 2024)
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_edge_cases_integration(self):
        result = await calculate_income_tax(0, 1.0, 2024)
        assert result["status"] == "success"
        assert result["data"]["total_tax"] == 0

        result = await calculate_income_tax(1000000, 1.0, 2024)
        assert result["status"] == "success"
        assert result["data"]["total_tax"] > 0
        assert result["data"]["average_tax_rate"] > 0
