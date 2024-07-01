import json
import os

from dotenv import load_dotenv
from fastapi import HTTPException

from ....schema.search import ResponseSchema
from .providers.base import GenProvider
from .providers.openai import OpenAIGenProvider
from .providers.anthropic import AnthropicGenProvider

load_dotenv()



def get_openai_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI API key is not set in the environment variables. Please set the OPENAI_API_KEY environment variable or set GEN_PROVIDER to 'anthropic' or 'local'.",
        )
    return openai_api_key

def get_anthropic_api_key():
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise HTTPException(
            status_code=500,
            detail="Tavily API key is not set in the environment variables. Please set the TAVILY_API_KEY environment variable or set SEARCH_PROVIDER to 'searxng' or 'serper'.",
        )
    return anthropic_api_key


def get_search_provider() -> SearchProvider:
    tavily_api_key = get_tavily_api_key()
    return TavilySearchProvider(tavily_api_key)


def perform_search(api_key: str, query: str) -> ResponseSchema:
    search_provider = get_search_provider()

    try:
        web_response = search_provider.search(api_key, query)

        return web_response
    except Exception:
        raise HTTPException(
            status_code=500, detail="There was an error while searching."
        )
