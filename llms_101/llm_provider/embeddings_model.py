import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from llm_provider.provider_type import LLMProviderType

load_dotenv()

LLM_PROVIDER = LLMProviderType(os.getenv("LLM_PROVIDER", LLMProviderType.WATSONX.value))


def _get_base_embeddings_settings(
    model_name: str, model_parameters: Optional[Dict] = None
) -> Dict:
    """Get base settings for the embeddings model based on the provider type."""
    if model_parameters is None:
        model_parameters = {}

    if LLM_PROVIDER == LLMProviderType.OLLAMA:
        return {
            "model": model_name,
        }

    elif LLM_PROVIDER == LLMProviderType.WATSONX:
        return {
            "url": os.getenv("WATSONX_URL"),
            "project_id": os.getenv("WATSONX_PROJECT_ID"),
            "apikey": os.getenv("WATSONX_APIKEY"),
            "model_id": model_name,
        }

    raise ValueError(f"Incorrect LLM provider: {LLM_PROVIDER}")


def get_embeddings_model(
    model_name: Optional[str] = None,
    model_parameters: Optional[Dict] = None,
) -> Any:
    """Get an embeddings model based on the provider type.

    Args:
        model_name: The name of the model to use. If None, a default model will be used based on the provider.
        model_parameters: Additional parameters for the model.

    Returns:
        An embeddings model instance.
    """
    if model_name is None:
        if LLM_PROVIDER == LLMProviderType.WATSONX:
            model_name = "ibm/slate-125m-english-rtrvr"
        elif LLM_PROVIDER == LLMProviderType.OLLAMA:
            # based on https://ollama.com/blog/embedding-models
            model_name = "nomic-embed-text"
        else:
            raise ValueError(f"Unsupported provider: {LLM_PROVIDER}")

    if LLM_PROVIDER == LLMProviderType.WATSONX:
        from langchain_ibm import WatsonxEmbeddings

        return WatsonxEmbeddings(
            **_get_base_embeddings_settings(
                model_name=model_name, model_parameters=model_parameters
            )
        )

    elif LLM_PROVIDER == LLMProviderType.OLLAMA:
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            **_get_base_embeddings_settings(
                model_name=model_name, model_parameters=model_parameters
            )
        )

    return None
