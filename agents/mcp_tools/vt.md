# VirusTotal MCP Server
_Based on https://mcp.so/server/mcp-virustotal/BurtTheCoder_

## What is VirusTotal MCP Server?
The VirusTotal MCP Server is a Model Context Protocol (MCP) server designed for querying the VirusTotal API, facilitating the analysis of URLs, file hashes, and IP address reports.

## Key features of VirusTotal MCP Server?
- URL Scanning for potential security threats
- Analysis of file hashes
- Retrieval of security reports for IP addresses
- Relationship analysis between URLs, files, and IPs

## Installation
1. Install the server globally via npm:
```bash
npm install -g @burtthecoder/mcp-virustotal
```

2. Add to your Claude Desktop configuration file:
```json
{
  "mcpServers": {
    "virustotal": {
      "command": "mcp-virustotal",
      "env": {
        "VIRUSTOTAL_API_KEY": "your-virustotal-api-key"
      }
    }
  }
}
```


## Setting up the VirusTotal MCP Tool