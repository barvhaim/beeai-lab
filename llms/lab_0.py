import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM
# from langchain_ollama.llms import OllamaLLM


load_dotenv()


def lab_0():
    """
    Sanity check for the running watsonx.ai LLM or Ollama LLM.
    """
    wx_parameters = {
        "decoding_method": "sample",
        "max_new_tokens": 100,
        "min_new_tokens": 1,
        "temperature": 0.5,
        "top_k": 50,
        "top_p": 1,
    }

    wx_llm = WatsonxLLM(
        model_id="ibm/granite-13b-instruct-v2",
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params=wx_parameters,
    )

    # Uncomment the following lines to use Ollama LLM instead
    # ollama_parameters = {
    #     "num_predict": 100,  # max_new_tokens
    #     "temperature": 0.5,
    #     "top_p": 1,
    #     "top_k": 50,
    # }
    #
    # ollama_llm = OllamaLLM(
    #     model="llama3.1:8b",  # ollama pull llama3.1:8b
    #     **ollama_parameters,
    # )

    response = wx_llm.invoke("Who is man's best friend?")
    print(response)


if __name__ == "__main__":
    lab_0()
