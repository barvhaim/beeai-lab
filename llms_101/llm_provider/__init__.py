import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv
from llm_provider.provider_type import LLMProviderType

load_dotenv()

LLM_PROVIDER = LLMProviderType(os.getenv("LLM_PROVIDER", LLMProviderType.WATSONX.value))


def _get_base_llm_settings(model_name: str, model_parameters: Optional[Dict]) -> Dict:
    if model_parameters is None:
        model_parameters = {}

    if LLM_PROVIDER == LLMProviderType.OLLAMA:
        parameters = {
            "num_predict": model_parameters.get("max_tokens", 100),
            "temperature": model_parameters.get("temperature", 0.9),
            "top_p": model_parameters.get("top_p", 1.0),
            "top_k": model_parameters.get("top_k", 50),
        }

        return {
            "model": model_name,
            **parameters,
        }

    elif LLM_PROVIDER == LLMProviderType.WATSONX:
        parameters = {
            "min_new_tokens": model_parameters.get("min_tokens", 1),
            "max_new_tokens": model_parameters.get("max_tokens", 100),
            "decoding_method": model_parameters.get("decoding_method", "greedy"),
            "temperature": model_parameters.get("temperature", 0.9),
            "repetition_penalty": model_parameters.get("repetition_penalty", 1.0),
            "top_k": model_parameters.get("top_k", 50),
            "top_p": model_parameters.get("top_p", 1.0),
            "stop_sequences": model_parameters.get("stop_sequences", []),
        }

        return {
            "url": os.getenv("WATSONX_URL"),
            "project_id": os.getenv("WATSONX_PROJECT_ID"),
            "apikey": os.getenv("WATSONX_APIKEY"),
            "model_id": model_name,
            "params": parameters,
        }

    raise ValueError(f"Incorrect LLM provider: {LLM_PROVIDER}")


def get_llm_client(
    model_name: str = "meta-llama/llama-3-3-70b-instruct",
    model_parameters: Optional[Dict] = None,
) -> Any:
    if LLM_PROVIDER == LLMProviderType.WATSONX:
        from langchain_ibm import WatsonxLLM

        return WatsonxLLM(
            **_get_base_llm_settings(
                model_name=model_name, model_parameters=model_parameters
            )
        )

    elif LLM_PROVIDER == LLMProviderType.OLLAMA:
        from langchain_ollama.llms import OllamaLLM

        return OllamaLLM(
            **_get_base_llm_settings(
                model_name=model_name, model_parameters=model_parameters
            )
        )
    return None
