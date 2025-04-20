import os
from operator import itemgetter
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ibm import WatsonxLLM

load_dotenv()


def lab_3():
    model = WatsonxLLM(
        model_id="meta-llama/llama-3-3-70b-instruct",
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={
            "decoding_method": "sample",
            "max_new_tokens": 128,
            "min_new_tokens": 1,
            "temperature": 0.05,
            "top_k": 5,
            "stop_sequences": ["\n"],
        },
    )

    prompt1 = PromptTemplate.from_template("Q. what is the city {person} is from? \nA.")
    prompt2 = PromptTemplate.from_template(
        "Q. what country is the city {city} in? respond in {language} \nA."
    )

    chain1 = prompt1 | model | StrOutputParser()

    response = chain1.invoke({"person": "Elon Musk"})
    print(response)

    chain2 = (
            {"city": chain1, "language": itemgetter("language")}
            | prompt2
            | model
            | StrOutputParser()
    )

    response = chain2.invoke({"person": "Elon Musk", "language": "Hebrew"})
    print(response)


if __name__ == "__main__":
    lab_3()
