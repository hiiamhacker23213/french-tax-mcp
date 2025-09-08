#!/usr/bin/env python3

import pytest

from french_tax_mcp.analyzers.income_analyzer import IncomeTaxAnalyzer


class TestIncomeTaxAnalyzer:

    @pytest.mark.asyncio
    async def test_calculate_income_tax(self):
        analyzer = IncomeTaxAnalyzer()
        result = await analyzer.calculate_income_tax(50000, 2.0, 2024)

        assert result["status"] == "success"
        assert "data" in result
        assert result["data"]["net_taxable_income"] == 50000
        assert result["data"]["household_parts"] == 2.0
        assert result["data"]["total_tax"] > 0
        assert result["data"]["average_tax_rate"] >= 0
        assert result["data"]["marginal_tax_rate"] > 0

    @pytest.mark.asyncio
    async def test_calculate_household_parts(self):
        analyzer = IncomeTaxAnalyzer()
        result = await analyzer.calculate_household_parts("married", 2, 1)

        assert result["status"] == "success"
        assert "data" in result
        assert "marital_status" in result["data"]
        assert result["data"]["marital_status"] == "married"
        assert "num_children" in result["data"]
        assert result["data"]["num_children"] == 2
        assert "disabled_dependents" in result["data"]
        assert result["data"]["disabled_dependents"] == 1
        assert "total_parts" in result["data"]
        assert result["data"]["total_parts"] == 3.5
