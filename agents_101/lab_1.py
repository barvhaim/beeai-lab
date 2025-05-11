import os
from typing import List
from dotenv import load_dotenv
import asyncio
import sys
import traceback

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.errors import FrameworkError
from beeai_framework.tools.mcp import MCPTool
from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.emitter import EmitterOptions
from beeai_framework.memory import TokenMemory

from utils.io import ConsoleReader, process_agent_events

load_dotenv()


reader = ConsoleReader()

# Explore MCPs on https://mcp.so/

# Create MCP server parameters
server_params = StdioServerParameters(
    command="uv",
    args=["--directory", "mcp_tools/local-mcp-virustotal", "run", "server.py"],
    env={
        "VIRUSTOTAL_API_KEY": os.environ["VIRUSTOTAL_API_KEY"],
    },
)


async def _get_vt_tools(session: ClientSession) -> List[MCPTool]:
    tools: List[MCPTool] = await MCPTool.from_client(session)
    filtered_tools = [
        tool
        for tool in tools
        if tool.name.lower()
        in [
            "vt_domain_report",
            "vt_ip_report",
        ]  # MCP server offers multiple tools, we only need these two
    ]
    return filtered_tools


async def _create_agent(session: ClientSession) -> ReActAgent:
    """Create and configure the agent with tools and LLM"""
    # Other models to try:
    # "ollama:llama3.1"
    # "ollama:granite3.1-dense:8b"
    # "watsonx:meta-llama/llama-3-3-70b-instruct"
    # with Ollama, ensure the model is pulled before running.
    # with watsonx.ai, ensure relevant ENV is set.
    model_name = "ollama:llama3.1"
    # model_name = "watsonx:meta-llama/llama-3-3-70b-instruct"

    llm = ChatModel.from_name(
        model_name,
        ChatModelParameters(temperature=0),
    )

    vt_tools = await _get_vt_tools(session)

    agent = ReActAgent(
        llm=llm,
        tools=vt_tools,
        memory=TokenMemory(llm),
    )
    return agent


async def lab_1() -> None:
    """
    Example of using the ReAct agent with a weather tool and a Wikipedia search tool.
    """

    async with (
        stdio_client(server_params) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        agent = await _create_agent(session)

        reader.write("🛠️ System: ", "Agent initialized with VirusTotal tools.")

        # Main interaction loop with user input
        for prompt in reader:
            # Run agent with the prompt
            response = await agent.run(
                prompt=prompt,
                execution=AgentExecutionConfig(
                    max_retries_per_step=3, total_max_retries=10, max_iterations=20
                ),
            ).on(
                "*",
                lambda data, event: process_agent_events(reader, data, event),
                EmitterOptions(match_nested=False),
            )

            reader.write("Agent 🤖 : ", response.result.text)


if __name__ == "__main__":
    try:
        asyncio.run(lab_1())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
