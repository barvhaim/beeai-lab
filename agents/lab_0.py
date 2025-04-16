from dotenv import load_dotenv
import asyncio
import sys
import traceback

from beeai_framework.agents.react import ReActAgent, ReActAgentRunOutput
from beeai_framework.backend import ChatModel
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.tools.search.wikipedia import WikipediaTool

load_dotenv()


async def main() -> None:
    """
    Example of using the ReAct agent with a weather tool and watsonx.ai as LLM provider.
    :return:
    """
    llm = ChatModel.from_name("watsonx:meta-llama/llama-3-3-70b-instruct")
    agent = ReActAgent(llm=llm, tools=[OpenMeteoTool(), WikipediaTool()],
                       memory=UnconstrainedMemory())

    output: ReActAgentRunOutput = await agent.run("What's the current weather in Tel Aviv? and what the current population in there?").on(
        "update", lambda data, event: print(f"Agent({data.update.key}) 🤖 : ", data.update.parsed_value)
    )

    print("Agent 🤖 : ", output.result.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())