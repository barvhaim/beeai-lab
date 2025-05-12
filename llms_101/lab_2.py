import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from llm_provider import get_llm_client
from termcolor import colored


def _load_context():
    """
    Load the context for the prompt.
    """
    with open("data/example_cti_report.txt", "r") as file:
        context = file.read()
    return context


def lab_2():
    """
    Using LangChain with LLM that uses prompt templates and output parsers.
    This example uses a CTI report and asks the LLM to summarize it in JSON format.
    """
    llm_parameters = {
        "decoding_method": "sample",
        "max_tokens": 1024,
        "min_tokens": 1,
        "temperature": 0.05,
        "top_k": 5,
        "top_p": 0.5,
        "stop_sequences": ["\nREQUEST:", "\n}"],
    }

    llm = get_llm_client(
        model_name="meta-llama/llama-3-3-70b-instruct",
        model_parameters=llm_parameters,
    )

    # Based on https://smith.langchain.com/hub/aaronkaplan/cti-llm
    prompt = PromptTemplate(
        template="""Please summarize the following report according to the following REQUEST.
Use JSON format with the keys "summary", "attacker", "victim", "tools", "TTPs", "CVEs", "why (motivation)", "when_first_discovered", "last_time_observed", "what_are_they_targetting", "mitigation_recommendation", "how_to_detect (IoCs)".
Return only the JSON object, no additional text.

REQUEST:
1. Summarize the main points as bullet points (as a list of strings). The summary is for high level management, not a technical audience. Keep it simple and understandable. Keep it short and concise. Make it less technical. Focus on the implications.
2. DO NOT include any unnecessary information.
3. Try to answer the "w" questions: 
    - 'who is the attacker?', 
    - 'whom are they targeting?', 
    - 'which tools are they using?', 
    - 'which TTPs?', 
    - 'What CVEs are they exploiting?'
    - 'why are they doing it  ? (motivation)?',
    - 'when did this happen?', 
    - 'when was it discovered the first and last time observed?',  
    - 'what are they targeting?', 
    - 'what recommendations are mentioned to mitigate the attack (if known)?', 
    - 'how to detect the attack (IoCs)?'
4. If the text does not answer a 'w' question, DO NOT INVENT anything. Just answer the question as 'not known'

BE SHORT AND CONCISE! Make sure all relevant points are covered.

CONTEXT:
{context}

SUMMARY:
""",
        input_variables=["context"],
    )

    chain = prompt | llm | JsonOutputParser()
    context = _load_context()
    response = chain.invoke({"context": context})
    print(colored(json.dumps(response, indent=2), "green"))

    # Tasks:
    # 1. Run the lab with the default model.
    # 2. Try a smaller model, for example "phi3" or "granite3.3:2b", does it work?


if __name__ == "__main__":
    lab_2()
