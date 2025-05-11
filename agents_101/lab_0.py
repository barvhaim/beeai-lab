from dotenv import load_dotenv
import asyncio
import sys
import traceback

from beeai_framework.agents.react import ReActAgent
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import TokenMemory
from beeai_framework.tools import AnyTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.emitter import EmitterOptions

from utils.io import ConsoleReader, process_agent_events

load_dotenv()

reader = ConsoleReader()


def _create_agent() -> ReActAgent:
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

    # Configure tools
    tools: list[AnyTool] = [WikipediaTool(), OpenMeteoTool(), DuckDuckGoSearchTool()]

    # Create a ReAct agent with memory (https://github.com/i-am-bee/beeai-framework/blob/main/python/docs/memory.md#overview)
    # and tools (https://github.com/i-am-bee/beeai-framework/blob/main/python/docs/tools.md#built-in-tools)
    agent = ReActAgent(llm=llm, tools=tools, memory=TokenMemory(llm))
    return agent


async def lab_0() -> None:
    """
    Example of using the ReAct agent with a weather tool, Wikipedia tool and DuckDuckGo search tool.
    """

    agent = _create_agent()

    reader.write(
        "🛠️ System: ", "Agent initialized with Wikipedia, DuckDuckGo, and Weather tools."
    )

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
        asyncio.run(lab_0())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())


# Tasks:
# 1. Try to run the lab with either `ollama` or `watsonx.ai` as LLM provider. Inspect the thought process of the agent.
