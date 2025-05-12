from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from llm_provider import get_llm_client
from termcolor import colored
import json


def lab_3():
    """
    Few-Shot Prompting with LangChain -
    Demonstrates how to use few-shot prompting to guide an LLM with examples,
    resulting in more consistent and accurate outputs for specific tasks.
    """
    llm_parameters = {
        "decoding_method": "sample",
        "max_tokens": 512,
        "min_tokens": 1,
        "temperature": 0.1,
        "top_k": 5,
        "top_p": 0.5,
        "stop_sequences": ["\nInput:", "\n\n"],
    }

    model_name = "meta-llama/llama-3-3-70b-instruct"  # watsonx.ai
    # model_name = "granite3.3:2b"  # ollama

    llm = get_llm_client(model_name=model_name, model_parameters=llm_parameters)

    # Define examples for few-shot learning
    examples = [
        {
            "input": "A user clicked on a suspicious link in an email and entered their credentials.",
            "output": {
                "incident_type": "Phishing Attack",
                "severity": "High",
                "immediate_actions": [
                    "Reset user's password",
                    "Enable MFA if not already active",
                    "Check for suspicious login activities",
                ],
                "investigation_steps": [
                    "Analyze email headers to identify sender",
                    "Check if other users received similar emails",
                    "Determine what information was compromised",
                ],
                "mitigation": [
                    "Security awareness training",
                    "Deploy email filtering solution",
                    "Implement DMARC, SPF, and DKIM",
                ],
            },
        },
        {
            "input": "Multiple failed login attempts were detected on the admin portal from foreign IP addresses.",
            "output": {
                "incident_type": "Brute Force Attack",
                "severity": "Medium",
                "immediate_actions": [
                    "Temporarily block the suspicious IPs",
                    "Review successful logins during the timeframe",
                    "Verify admin account security",
                ],
                "investigation_steps": [
                    "Analyze login attempt patterns",
                    "Check for other targeted accounts",
                    "Verify if any accounts were compromised",
                ],
                "mitigation": [
                    "Implement account lockout policies",
                    "Add IP-based access controls",
                    "Deploy a Web Application Firewall",
                ],
            },
        },
        {
            "input": "An employee's laptop containing customer data was stolen from their car.",
            "output": {
                "incident_type": "Physical Device Theft",
                "severity": "High",
                "immediate_actions": [
                    "Remote wipe the device if possible",
                    "Change all passwords for accounts accessed from that device",
                    "Notify affected customers as required by regulations",
                ],
                "investigation_steps": [
                    "Interview the employee about circumstances",
                    "Determine what data was on the device",
                    "Check if device encryption was enabled",
                ],
                "mitigation": [
                    "Enforce device encryption",
                    "Implement MDM solution",
                    "Update physical security policies",
                ],
            },
        },
    ]

    # Convert the examples to strings for the prompt template
    formatted_examples = []
    for example in examples:
        formatted_examples.append(
            {"input": example["input"], "output": json.dumps(example["output"])}
        )

    # Create an example template
    example_template = """
Input: {{input}}
Output: {{output}}
"""

    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template=example_template,
        template_format="jinja2",
    )

    # Create the few-shot prompt template
    few_shot_prompt = FewShotPromptTemplate(
        template_format="jinja2",
        examples=formatted_examples,
        example_prompt=example_prompt,
        prefix="""You are a cybersecurity incident response expert. Given a brief description of a security incident, 
provide a structured JSON response with the following fields:
- incident_type: The type of security incident
- severity: The severity level (Low, Medium, High, Critical)
- immediate_actions: List of immediate actions to take
- investigation_steps: List of steps to investigate the incident
- mitigation: List of long-term mitigation strategies

Here are some examples:""",
        suffix="""
Input: {{input}}
Output:""",
        input_variables=["input"],
    )

    # Create the chain
    chain = few_shot_prompt | llm | JsonOutputParser()

    # Example security incident
    incident = "Unusual outbound network traffic was detected from a server to an unknown IP address, transferring several gigabytes of data."

    # Run the chain
    result = chain.invoke({"input": incident})

    print("\nSecurity Incident:")
    print(colored(incident, "yellow"))
    print("\nResponse:")
    print(colored(json.dumps(result, indent=2), "green"))

    # Tasks:
    # 1. Run the lab with the default model.
    # 2. Try a smaller model and compare the results.
    # 3. Experiment with different numbers of examples (add or remove examples).
    # 4. Try different temperature settings to see how it affects consistency.


if __name__ == "__main__":
    lab_3()
