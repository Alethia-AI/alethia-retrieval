import json
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from ..workers.search.service import respond_to_search, jsonify_results
from ..workers.search.results import add_to_results
from ..workers.search.rerank import rerank

from ..schema.search import ResponseSchema, ResultSchema, queryMetadata

router = APIRouter(
    prefix="/api",
    tags=['search'],
    dependencies=[],
)

@router.post('/search/')
async def search(query_metadata: queryMetadata, background_tasks: BackgroundTasks):
    prompt = query_metadata.query
    if not prompt:
        prompt = Request.args.get('query', '')
    if prompt:
        query_response: ResponseSchema = None
        try:
            query_response = respond_to_search(query_metadata.query_order, prompt, query_metadata.api_key)
            if query_response is None:
                return JSONResponse(content={"message": "Invalid query order."}, status_code=400)
        except Exception:
            return JSONResponse(content={"message": "There was an error while searching."}, status_code=400)

        # Re-rank the results
        query_response = await rerank(prompt, query_response)

        # Add the results to the database
        background_tasks.add_task(background_task, query_metadata.api_key, query_response.results)

        json_response_ = jsonify_results(query_response.results)

        return JSONResponse(content={"message": json_response_}, status_code=200)
    else:
        return 404

async def background_task(api_key: str, query_results: ResponseSchema):
    add_to_results(api_key, query_results)
