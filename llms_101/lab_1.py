from llm_provider import get_llm_client
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from termcolor import colored


def lab_1():
    """
    SIEM Detection Rule Generation -
    Demonstrates how to use an LLM (via LangChain) to convert a plain-language threat description into a structured detection rule for SIEMs, along with metadata like tactic/technique, rule type, and severity.
    """
    llm_parameters = {
        "decoding_method": "sample",
        "max_tokens": 200,
        "min_tokens": 1,
        "temperature": 0.05,
        "top_k": 5,
        "top_p": 0.5,
    }

    model_name = "meta-llama/llama-3-3-70b-instruct"  # watsonx.ai
    # model_name = "granite3.3:2b"  # ollama

    llm = get_llm_client(model_name=model_name, model_parameters=llm_parameters)

    prompt = PromptTemplate(
        template="""
You are a security assistant that generates SIEM detection rules (for Splunk, Sentinel, or Elastic) from plain-language threat descriptions. Output only the detection rule and required metadata in JSON. Do not include any explanations or comments.

Threat Description:
{requirement}

Output format:
{{
  "detection_rule": "<the SIEM rule in SPL, KQL, or EQL>",
  "tactic": "<MITRE ATT&CK tactic, e.g., Exfiltration>",
  "technique": "<MITRE ATT&CK technique, e.g., Exfiltration Over Command and Control Channel>",
  "rule_type": "<e.g., Correlation, Threshold, Anomaly>",
  "severity": "<e.g., Low, Medium, High, Critical>"
}}
""",
        input_variables=["requirement"],
    )

    # Example threat description (can be replaced with user input)
    requirement = "A suspicious PowerShell process downloads an executable from an external IP and runs it."

    chain = prompt | llm | JsonOutputParser()
    result = chain.invoke({"requirement": requirement})

    print(colored(result, "green"))

    # Tasks:
    # 1. Run the lab with the default model.


if __name__ == "__main__":
    lab_1()
