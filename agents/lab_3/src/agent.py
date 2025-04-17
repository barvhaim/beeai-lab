from typing import AsyncGenerator
from beeai_sdk.providers.agent import Server
from beeai_sdk.schemas.text import TextInput, TextOutput
from .configuration import load_env

load_env()
server = Server("lab-3-agent")


# TBD
@server.agent()
async def run_agent(input: TextInput) -> AsyncGenerator[TextOutput, None]:
    output: TextOutput = TextOutput(text="")
    print("Agent input: ", input.text)

    output.text = f"Hello, {input.text}!"
    yield output
