#!/usr/bin/env python3

from fastmcp.client import Client
import asyncio
import json

async def main():
    print("Connecting to MCP server at http://127.0.0.1:8888/mcp...")
    client = Client('http://127.0.0.1:8888/mcp', timeout=10)
    
    async with client:
        print("Connected! Sending query to get tax brackets...")
        
        # Call the get_tax_brackets tool
        result = await client.call_tool("get_tax_brackets", {})
        
        # Format the response for better readability
        response_text = result[0].text
        response_json = json.loads(response_text)
        formatted_response = json.dumps(response_json, indent=2)
        
        print("\nRaw Response:")
        print(response_text)
        
        print("\nFormatted Response:")
        print(formatted_response)

if __name__ == "__main__":
    asyncio.run(main())
