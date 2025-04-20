from typing import Any
from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter

from pydantic import BaseModel, Field

from beeai_framework.tools import JSONToolOutput, Tool, ToolRunOptions


class ThreatIntelligenceToolInput(BaseModel):
    """Input model for the Threat Intelligence Tool."""

    query: str = Field(description="The query to search for threat intelligence.")


class ThreatIntelligenceTool(
    Tool[ThreatIntelligenceToolInput, ToolRunOptions, JSONToolOutput]
):
    name: str = "Threat Intelligence Tool"
    description: str = "A tool to query threat intelligence data."
    input_schema = ThreatIntelligenceToolInput

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "custom_tools", "ti_tool"],
            creator=self,
        )

    async def _run(
        self,
        input: ThreatIntelligenceToolInput,
        options: ToolRunOptions | None,
        context: RunContext,
    ) -> JSONToolOutput:
        query = input.query

        # Simulate a call to a threat intelligence API
        # In a real implementation, you would replace this with actual API calls

        # For demonstration, let's assume we have a mock response
        mock_response = {
            "query": query,
            "malicious": True,
            "confidence": 0.95,
            "threat_type": "malware",
        }

        return JSONToolOutput(
            result=mock_response,
        )
