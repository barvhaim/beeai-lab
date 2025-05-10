from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from llm_provider import get_llm_client
from termcolor import colored


def lab_3():
    """
    Multiple LLMs and chains in a single application.
    """

    llm_parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 128,
        "min_new_tokens": 1,
        "temperature": 0.05,
        "top_k": 5,
        "stop_sequences": ["\nQ."],
    }

    model_name_1 = "ibm/granite-13b-instruct-v2"
    # model_name_1 = "granite3.3:2b"
    model_name_2 = "meta-llama/llama-3-3-70b-instruct"
    # model_name_2 = "phi3"

    llm_1 = get_llm_client(
        model_name=model_name_1,
        model_parameters=llm_parameters,
    )

    llm_2 = get_llm_client(
        model_name=model_name_2,
        model_parameters=llm_parameters,
    )

    prompt_1 = PromptTemplate.from_template("Q. what is the city {person} is from?\nA.")
    prompt_2 = PromptTemplate.from_template(
        "Q. what country is the city {city} in? respond in {language}\nA."
    )

    chain_1 = prompt_1 | llm_1 | StrOutputParser()
    chain_2 = prompt_2 | llm_2 | StrOutputParser()

    city = chain_1.invoke({"person": "Bill Gates"})
    country = chain_2.invoke({"city": city, "language": "Spanish"})

    print(colored(city, "green"))
    print(colored(country, "green", attrs=["bold"]))

    # Tasks:
    # 1. Run the lab with the default model.
    # 2. Change the model parameters to make the model more creative.
    # 3. Use a different model from `watsonx.ai` (https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html?context=wx#provided) or `ollama` (https://ollama.com/search).
    # 4. Add a third chain that uses a third model to answer the question "what is the language of the city {city} in?"


if __name__ == "__main__":
    lab_3()
