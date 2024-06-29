import cohere
import os

from typing import List

from ...schema.search import ResponseSchema, ResultSchema

co = cohere.AsyncClient(os.environ.get("COHERE_API_KEY"))

async def rerank(query_: str, responses: ResponseSchema) -> ResponseSchema:
    if responses is None:
        print("No results to rerank")
        return responses

    original_results_: List[ResultSchema] = responses.results

    documents_ = [result.model_dump() for result in original_results_]

    reranked_response = await co.rerank(
        model="rerank-english-v3.0",
        query= query_,
        documents=documents_,
        rank_fields=["text", "title"],
        return_documents=False
        )

    reranked_results = []
    # Print the reranked response
    for i, result in enumerate(reranked_response.results):
        index_: int = result.index
        original_result: ResultSchema = original_results_[index_]
        original_result.relevance_score = result.relevance_score
        original_result.index = i
        reranked_results.append(original_result)

    responses.results = reranked_results
    return responses
