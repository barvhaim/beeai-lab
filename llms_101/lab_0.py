from llm_provider import get_llm_client


def lab_0():
    """
    Sanity check for the running watsonx.ai LLM or Ollama LLM.
    """
    parameters = {
        "decoding_method": "sample",
        "max_tokens": 100,
        "min_tokens": 1,
        "temperature": 0.5,
        "top_k": 50,
        "top_p": 1,
    }

    # (watsonx.ai)
    llm = get_llm_client(
        model_name="ibm/granite-13b-instruct-v2",
        model_parameters=parameters
    )

    # (ollama)
    # llm = get_llm_client(
    #     model_name="llama3.1:8b",
    #     model_parameters=parameters
    # )

    response = llm.invoke("Who is man's best friend?")
    print(response)


if __name__ == "__main__":
    lab_0()
