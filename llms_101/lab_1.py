import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


load_dotenv()


def lab_1():
    """
    Using LangChain with watsonx.ai that uses prompt templates and output parsers.
    """
    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 100,
        "min_new_tokens": 1,
        "temperature": 0.05,
        "top_k": 50,
        "top_p": 1,
    }

    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-13b-instruct-v2",
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params=parameters,
    )

    prompt = PromptTemplate(
        template="""You are a helpful assistant that provides information about countries.
Given a country name, provide the following information in JSON format:
- capital
- population

Input: "France"
Output: {{
    "capital": "Paris",
    "population": 67081000
}}

Input: "{country}"
Output: """,
        input_variables=["country"],
    )

    chain = prompt | watsonx_llm | JsonOutputParser()
    response = chain.invoke({"country": "Israel"})
    print(response)


if __name__ == "__main__":
    lab_1()
