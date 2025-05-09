from dotenv import load_dotenv
import asyncio
import sys
import traceback
import argparse

from beeai_framework.agents.react import ReActAgent, ReActAgentRunOutput
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.tools.search.wikipedia import WikipediaTool

load_dotenv()


async def main(prompt: str) -> None:
    """
    Example of using the ReAct agent with a weather tool and a Wikipedia search tool.
    :param prompt: The prompt to provide to the agent.
    """
    # Other models to try:
    # "ollama:llama3.1"
    # "ollama:granite3.1-dense:8b"
    # "watsonx:meta-llama/llama-3-3-70b-instruct"
    # with Ollama, ensure the model is pulled before running.
    # with watsonx.ai, ensure relevant ENV is set.
    llm = ChatModel.from_name(
        "ollama:llama3.1",
        ChatModelParameters(temperature=0),
    )
    agent = ReActAgent(
        llm=llm, tools=[OpenMeteoTool(), WikipediaTool()], memory=UnconstrainedMemory()
    )

    output: ReActAgentRunOutput = await agent.run(prompt).on(
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
