import os
from typing import List
from dotenv import load_dotenv
import asyncio
import sys
import traceback
import argparse

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from beeai_framework.agents.react import ReActAgent, ReActAgentRunOutput
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.mcp import MCPTool
from beeai_framework.agents import AgentExecutionConfig

load_dotenv()


# Explore MCPs on https://mcp.so/

# Create MCP server parameters
server_params = StdioServerParameters(
    command="uv",
    args=["--directory", "<PATH_TO>/local-mcp-virustotal", "run", "server.py"],
    env={
        "VIRUSTOTAL_API_KEY": os.environ["VIRUSTOTAL_API_KEY"],
    },
)


async def get_vt_tools(session: ClientSession) -> List[MCPTool]:
    tools = await MCPTool.from_client(session)
    filtered_tools = [
        tool
        for tool in tools
        if tool.name.lower() in ["vt_domain_report", "vt_ip_report"]  # MCP server offers multiple tools, we only need these two
    ]
    return filtered_tools


async def create_agent(session: ClientSession) -> ReActAgent:
    """Create and configure the agent with tools and LLM"""
    # Other models to try:
    # "ollama:llama3.1"
    # "ollama:granite3.1-dense:8b"
    # "watsonx:meta-llama/llama-3-3-70b-instruct"
    # with Ollama, ensure the model is pulled before running.
    # with watsonx.ai, ensure relevant ENV is set.

    llm = ChatModel.from_name(
        "watsonx:meta-llama/llama-3-3-70b-instruct",
        ChatModelParameters(temperature=0),
    )

    vt_tools = await get_vt_tools(session)

    agent = ReActAgent(
        llm=llm,
        tools=vt_tools,
        memory=UnconstrainedMemory(),
    )
    return agent


async def main(prompt: str) -> None:
    """
    Example of using the ReAct agent with a weather tool and a Wikipedia search tool.
    :param prompt: The prompt to provide to the agent.
    """

    async with stdio_client(server_params) as (read, write), ClientSession(
        read, write
    ) as session:
        await session.initialize()
        agent = await create_agent(session)
        output: ReActAgentRunOutput = await agent.run(
            prompt=prompt,
            execution=AgentExecutionConfig(
                max_retries_per_step=3, total_max_retries=10, max_iterations=20
            ),
        ).on(
            "update",
            lambda data, event: print(
                f"Agent({data.update.key}) 🤖 : ", data.update.parsed_value
            ),
        )
        print("Agent 🤖 : ", output.result.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the ReAct agent with a custom prompt."
    )
    parser.add_argument("prompt", type=str, help="The prompt to provide to the agent.")
    args = parser.parse_args()

    try:
        asyncio.run(main(args.prompt))
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
