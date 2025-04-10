import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM


load_dotenv()


def lab_0():
    """
    Sanity check for the running watsonx.ai LLM.
    """
    parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 100,
        "min_new_tokens": 1,
        "temperature": 0.5,
        "top_k": 50,
        "top_p": 1,
    }

    watsonx_llm = WatsonxLLM(
        model_id="ibm/granite-13b-instruct-v2",
        url=os.getenv("WATSONX_API_ENDPOINT"),
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        apikey=os.getenv("WATSONX_API_KEY"),
        params=parameters,
    )

    response = watsonx_llm.invoke("Who is man's best friend?")
    print(response)


if __name__ == "__main__":
    lab_0()
