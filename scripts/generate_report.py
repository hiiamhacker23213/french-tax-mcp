#!/usr/bin/env python3

from fastmcp.client import Client
import asyncio
import json

async def main():
    print("Connecting to MCP server at http://127.0.0.1:8888/mcp...")
    client = Client('http://127.0.0.1:8888/mcp', timeout=10)
    
    async with client:
        print("Connected! Getting tax brackets and generating a report...")
        
        # First get tax data
        tax_brackets_result = await client.call_tool("get_tax_brackets", {})
        tax_brackets_json = json.loads(tax_brackets_result[0].text)
        
        # Now generate a report
        report_result = await client.call_tool("generate_tax_report", {
            "tax_data": tax_brackets_json,
            "topic_name": "Tranches d'imposition 2025",
            "format": "markdown"
        })
        
        print("\nGenerated Tax Report:")
        print(report_result[0].text)

if __name__ == "__main__":
    asyncio.run(main())
