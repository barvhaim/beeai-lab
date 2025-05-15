import os
import base64
import aiohttp
import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()


# Initialize FastMCP with the custom auth hook
mcp = FastMCP(name="VirusTotal MCP Server")

# Base URL for VirusTotal API
BASE_URL = "https://www.virustotal.com/api/v3"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def fetch_vt_data(endpoint: str) -> dict:
    """Fetch data from VirusTotal API asynchronously."""
    api_key = os.getenv("VIRUSTOTAL_API_KEY")
    if not api_key:
        logging.error("VIRUSTOTAL_API_KEY is missing.")
        return {"error": "VIRUSTOTAL_API_KEY is missing."}

    url = f"{BASE_URL}/{endpoint}"
    headers = {"x-apikey": api_key}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    text = await response.text()
                    logging.error(f"API request failed ({response.status}): {text}")
                    return {"error": f"API request failed ({response.status})"}
        except aiohttp.ClientError as e:
            logging.error(f"Network error: {e}")
            return {"error": "Network error while fetching data from VirusTotal."}


def format_response(title: str, data: dict, fields: list) -> str:
    """Format VirusTotal API responses into readable text."""
    if "error" in data:
        return f"Error: {data['error']}"

    attributes = data.get("data", {}).get("attributes", {})
    if not attributes:
        return f"No valid data found for {title}."

    lines = [f"**{title} Report**"]
    for field, label in fields:
        value = attributes.get(field, "N/A")
        lines.append(f"**{label}:** {value}")
    return "\n".join(lines)


# Tool definitions
@mcp.tool("vt_ip_report")
async def vt_ip_report(ip: str) -> str:
    data = await fetch_vt_data(f"ip_addresses/{ip}")
    return format_response(
        "IP Address",
        data,
        [
            ("reputation", "Reputation"),
            ("continent", "Continent"),
            ("country", "Country"),
            ("asn", "ASN"),
            ("as_owner", "AS Owner"),
        ],
    )


@mcp.tool("vt_domain_report")
async def vt_domain_report(domain: str) -> str:
    data = await fetch_vt_data(f"domains/{domain}")
    return format_response(
        "Domain",
        data,
        [
            ("reputation", "Reputation"),
            ("registrar", "Registrar"),
            ("tld", "Top-Level Domain"),
        ],
    )


@mcp.tool("vt_filehash_report")
async def vt_filehash_report(file_hash: str) -> str:
    data = await fetch_vt_data(f"files/{file_hash}")
    return format_response(
        "File",
        data,
        [
            ("type_extension", "File Type"),
            ("reputation", "Reputation"),
        ],
    )


@mcp.tool("vt_url_report")
async def vt_url_report(url: str) -> str:
    encoded = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    data = await fetch_vt_data(f"urls/{encoded}")
    return format_response(
        "URL",
        data,
        [
            ("last_final_url", "Final URL"),
            ("reputation", "Reputation"),
            ("times_submitted", "Times Submitted"),
            ("total_votes", "Total Votes"),
        ],
    )


@mcp.tool("vt_threat_categories")
async def vt_threat_categories() -> str:
    data = await fetch_vt_data("popular_threat_categories")
    categories = data.get("data", [])
    if not isinstance(categories, list) or not categories:
        return "No threat categories found."
    items = "\n".join(f"🔹 {c}" for c in categories)
    return f"**Threat Categories Report**\n{items}"


@mcp.tool("vt_attack_tactic")
async def vt_attack_tactic(tactic_id: str) -> str:
    data = await fetch_vt_data(f"attack_tactics/{tactic_id}")
    return format_response(
        "Attack Tactic",
        data,
        [
            ("name", "Name"),
            ("description", "Description"),
        ],
    )


@mcp.tool("vt_attack_technique")
async def vt_attack_technique(technique_id: str) -> str:
    data = await fetch_vt_data(f"attack_techniques/{technique_id}")
    return format_response(
        "Attack Technique",
        data,
        [
            ("name", "Name"),
            ("description", "Description"),
        ],
    )


@mcp.tool("vt_comments")
async def vt_comments(tag: str) -> str:
    data = await fetch_vt_data(f"comments?filter=tag%3A{tag}&limit=1")
    comments = data.get("data", [])
    if not comments:
        return "No comments found."
    texts = "\n".join(f" {c['attributes'].get('text', 'N/A')}" for c in comments)
    return f" **VirusTotal Comments**\n{texts}"


@mcp.tool("vt_behavior")
async def vt_behavior(file_hash: str) -> str:
    data = await fetch_vt_data(f"files/{file_hash}/behaviour_summary")
    summary = (
        data.get("data", {})
        .get("attributes", {})
        .get("summary", "No behavior data available.")
    )
    return f" **File Behavior Summary**\n{summary}"


# Run the server
def main():
    logging.info("Starting VirusTotal MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
