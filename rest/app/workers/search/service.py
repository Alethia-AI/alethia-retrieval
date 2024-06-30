from fastapi import HTTPException

import os
import redis
import json

from typing import List

from ..embeddings.embeddings import prompt_embedding
from .archive_search import perform_archive_search
from .web_search.web_service import perform_search
from .related_search import perform_related_search

from app.schema.search import ResultSchema, ResponseSchema


METRIC = "inner_product"
# METRIC = "cosine"

redis_url = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(redis_url) if redis_url else None

def respond_to_search(query_order: int, prompt: str, api_key: str) -> ResponseSchema:
    # TODO: Add support for the following:
            # - max_results.
            # - archive_id, namespace_id, index_id.
            # - use_cache.
    try:
        cache_key = f"search:{prompt}"
        if redis_client and (cached_results := redis_client.get(cache_key)):
            cached_json = json.loads(json.loads(cached_results.decode("utf-8")))  # type: ignore
            return ResponseSchema(**cached_json)

        query_response: ResponseSchema = call_services(query_order, prompt, api_key)

        if redis_client:
            redis_client.set(cache_key, json.dumps(query_response.model_dump_json()), ex=7200)

        return query_response
    except Exception:
        raise HTTPException(
                    status_code=500, detail="There was an error while searching."
                )


def call_services(query_order: int, prompt: str, api_key: str) -> ResponseSchema:
    query_response: ResponseSchema = None
    if query_order == 0:
        web_response: ResponseSchema = perform_search(api_key, prompt)
        query_response = web_response
    elif query_order == 1:
        embedding = prompt_embedding(prompt)
        query_response = perform_archive_search(api_key, embedding, metric=METRIC)
    elif query_order > 1:
        query_response: ResponseSchema = perform_related_search(api_key, prompt, metric=METRIC)
    else:
        return None


def jsonify_results(query_results: List[ResultSchema]):
    results_ = []
    for _, result in enumerate(query_results):
        results_.append(
            {
                "index": result.index,
                "title": result.title,
                "URL": result.url,
                "text": result.text,
                "relevance_score": result.relevance_score,
            }
            )
    json_response_ = {}
    json_response_["results"] = results_
    return json_response_
