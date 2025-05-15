# VirusTotal MCP Server

A Model Control Protocol (MCP) server that provides access to VirusTotal API data through a standardized interface.

## Overview

This project implements a FastMCP server that wraps the VirusTotal API, allowing you to query information about:
- IP addresses
- Domains
- File hashes
- URLs
- Threat categories
- MITRE ATT&CK tactics and techniques
- VirusTotal comments
- File behavior analysis

## Prerequisites

- Python 3.11 or higher
- VirusTotal API key `VIRUSTOTAL_API_KEY` in `.env` file

## Installation

1. Clone the repository:
   ```
   git clone git@github.com:barvhaim/local-mcp-virustotal.git
   cd local-mcp-virustotal
   ```

2. Install dependencies:
   ```
   uv sync
   ```

## Configuration

Create a `.env` file in the project root with your VirusTotal API key:
```
VIRUSTOTAL_API_KEY=your_api_key_here
```

You can obtain a VirusTotal API key by registering at [VirusTotal](https://www.virustotal.com/).

## Usage

Start the MCP server:
```
uv run server.py
```

The server exposes the following tools:

- `vt_ip_report`: Get information about an IP address
- `vt_domain_report`: Get information about a domain
- `vt_filehash_report`: Get information about a file by its hash
- `vt_url_report`: Get information about a URL
- `vt_threat_categories`: List popular threat categories
- `vt_attack_tactic`: Get information about a MITRE ATT&CK tactic
- `vt_attack_technique`: Get information about a MITRE ATT&CK technique
- `vt_comments`: Get comments with a specific tag
- `vt_behavior`: Get behavior summary for a file hash

## Connecting to the Server

You can connect to this MCP server using any MCP client. For example, using the Python MCP client:

```python
from mcp.client import Client

client = Client("http://localhost:8000")
response = await client.call("vt_ip_report", {"ip": "8.8.8.8"})
print(response)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
