from dotenv import load_dotenv
import asyncio
import sys
import traceback
import argparse

from beeai_framework.agents.react import ReActAgent, ReActAgentRunOutput
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.agents import AgentExecutionConfig
from custom_tools.ti_tool import ThreatIntelligenceTool

load_dotenv()


def create_agent() -> ReActAgent:
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

    ti_tool = ThreatIntelligenceTool()

    agent = ReActAgent(
        llm=llm,
        tools=[ti_tool],
        memory=UnconstrainedMemory(),
    )
    return agent


async def main(prompt: str) -> None:
    """
    Example of using the ReAct agent with a weather tool and a Wikipedia search tool.
    :param prompt: The prompt to provide to the agent.
    """
    agent = create_agent()
    output: ReActAgentRunOutput = await agent.run(
        prompt=prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=3, total_max_retries=3, max_iterations=20
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
