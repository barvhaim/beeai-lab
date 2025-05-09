# VirusTotal MCP Server
_Based on https://mcp.so/server/mcp-virustotal/BurtTheCoder_

## What is VirusTotal MCP Server?
The VirusTotal MCP Server is a Model Context Protocol (MCP) server designed for querying the VirusTotal API, facilitating the analysis of URLs, file hashes, and IP address reports.

## Tools
* **get_url_report** - Get a comprehensive URL analysis report including security scan results and key relationships (communicating files, contacted domains/IPs, downloaded files, redirects, threat actors). Returns both the basic security analysis and automatically fetched relationship data.
* **get_url_relationship** - Query a specific relationship type for a URL with pagination support. Choose from 17 relationship types including analyses, communicating files, contacted domains/IPs, downloaded files, graphs, referrers, redirects, and threat actors. Useful for detailed investigation of specific relationship types.
* **get_file_report** - Get a comprehensive file analysis report using its hash (MD5/SHA-1/SHA-256). Includes detection results, file properties, and key relationships (behaviors, dropped files, network connections, embedded content, threat actors). Returns both the basic analysis and automatically fetched relationship data.
* **get_file_relationship** - Query a specific relationship type for a file with pagination support. Choose from 41 relationship types including behaviors, network connections, dropped files, embedded content, execution chains, and threat actors. Useful for detailed investigation of specific relationship types.
* **get_ip_report** - Get a comprehensive IP address analysis report including geolocation, reputation data, and key relationships (communicating files, historical certificates/WHOIS, resolutions). Returns both the basic analysis and automatically fetched relationship data.
* **get_ip_relationship** - Query a specific relationship type for an IP address with pagination support. Choose from 12 relationship types including communicating files, historical SSL certificates, WHOIS records, resolutions, and threat actors. Useful for detailed investigation of specific relationship types.
* **get_domain_report** - Get a comprehensive domain analysis report including DNS records, WHOIS data, and key relationships (SSL certificates, subdomains, historical data). Optionally specify which relationships to include in the report. Returns both the basic analysis and relationship data.

## Installation
1. Create MCP client in your BeeAI agent:
```python
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@burtthecoder/mcp-virustotal"],
    env={
        "VIRUSTOTAL_API_KEY": os.environ["VIRUSTOTAL_API_KEY"],
    },
)
```

2. Select the relevant tools for your agent:
```python
async def get_tools(session) -> List[MCPTool]:
    tools = await MCPTool.from_client(session)
    filtered_tools = [
        tool for tool in tools if tool.name.lower() in ["get_domain_report", "get_ip_report"]
    ]
    return filtered_tools
```