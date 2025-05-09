# Tavily MCP Server
_Based on https://docs.tavily.com/documentation/mcp_

## The Tavily MCP server provides:
* Seamless interaction with the tavily-search and tavily-extract tools
* Real-time web search capabilities through the tavily-search tool
* Intelligent data extraction from web pages via the tavily-extract tool
* 
## Installation
1. Create MCP client in your BeeAI agent:
```python
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "tavily-mcp"],
    env={
        "TAVILY_API_KEY": os.environ["TAVILY_API_KEY"],
    },
)
```

2. Select the relevant tools for your agent:
```python
async def get_tools(session) -> List[MCPTool]:
    return await MCPTool.from_client(session)
```