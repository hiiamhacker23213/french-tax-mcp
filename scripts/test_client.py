#!/usr/bin/env python3
"""Simple test client for the French Tax MCP Server."""

import asyncio
import json
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from fastmcp.client import Client
except ImportError:
    print("fastmcp not installed. Please install with: pip install fastmcp")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO)

async def test_tax_brackets():
    """Test the get_tax_brackets tool."""
    print("\n=== Testing get_tax_brackets ===")
    try:
        client = Client('http://127.0.0.1:8888/mcp', timeout=10)
        async with client:
            result = await client.call_tool("get_tax_brackets", {})
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")

async def test_income_tax_calculation():
    """Test the calculate_income_tax tool."""
    print("\n=== Testing calculate_income_tax ===")
    try:
        client = Client('http://127.0.0.1:8888/mcp', timeout=10)
        async with client:
            result = await client.call_tool("calculate_income_tax", {
                "net_taxable_income": 50000,
                "household_parts": 2.0
            })
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")

async def test_pinel_calculation():
    """Test the calculate_pinel_benefit tool."""
    print("\n=== Testing calculate_pinel_benefit ===")
    try:
        client = Client('http://127.0.0.1:8888/mcp', timeout=10)
        async with client:
            result = await client.call_tool("calculate_pinel_benefit", {
                "property_price": 250000,
                "commitment_period": 9,
                "acquisition_date": "2024-01-01"
            })
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")

async def test_scheme_details():
    """Test the get_scheme_details tool."""
    print("\n=== Testing get_scheme_details ===")
    try:
        client = Client('http://127.0.0.1:8888/mcp', timeout=10)
        async with client:
            result = await client.call_tool("get_scheme_details", {
                "scheme_name": "pinel"
            })
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")

async def test_form_details():
    """Test the get_form_details tool."""
    print("\n=== Testing get_form_details ===")
    try:
        client = Client('http://127.0.0.1:8888/mcp', timeout=10)
        async with client:
            result = await client.call_tool("get_form_details", {
                "form_number": "2042"
            })
            print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")

async def test_all_tools():
    """Test all available tools."""
    print("French Tax MCP Server - Test Client")
    print("=" * 50)
    
    await test_tax_brackets()
    await test_income_tax_calculation()
    await test_pinel_calculation()
    await test_scheme_details()
    await test_form_details()
    
    print("\n" + "=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    print("Make sure the server is running on http://127.0.0.1:8888")
    print("You can start it with: python scripts/run_server.py")
    print()
    
    try:
        asyncio.run(test_all_tools())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)