from llm_provider import get_llm_client
from termcolor import colored


def lab_0():
    """
    Sanity check for the running watsonx.ai LLM or Ollama LLM.
    """
    llm_parameters = {
        "decoding_method": "sample",
        "max_tokens": 100,
        "min_tokens": 1,
        "temperature": 0.05,
        "top_k": 50,
        "top_p": 1,
    }

    model_name = "ibm/granite-13b-instruct-v2"  # watsonx.ai
    # model_name = "granite3.3:2b"  # ollama

    llm = get_llm_client(
        model_name=model_name,
        model_parameters=llm_parameters
    )

    response = llm.invoke("Who is man's best friend?")
    print(colored(response, 'green'))

    # Additional tasks:
    # 1. Change the llm provider to use "granite3.3:2b" from ollama, make sure you've pulled the model before running! (`ollama pull granite3.3:2b`) and set the `.env` file to use ollama.
    # 2. Change the model parameters to make the model more creative.
    # 3. Use a different model from `watsonx.ai` (https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html?context=wx#provided) or `ollama` (https://ollama.com/search).
    # 4. The output of the LLM might be truncated, increase the `max_tokens` parameter to get more output.


if __name__ == "__main__":
    lab_0()
