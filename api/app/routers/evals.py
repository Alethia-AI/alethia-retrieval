import json
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from ..workers.evals.service import generate_corpus_qa

from ..schema.search import ResponseSchema, ResultSchema, queryMetadata

router = APIRouter(
    prefix="/api",
    tags=['evals'],
    dependencies=[],
)

@router.post('/generate_qa/')
async def generate_dataset(api_key: str, archive_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_qa, api_key)
    return JSONResponse(content={"message": "Generating QA data in the background."})

async def background_task(api_key: str, archive_id: int):
    generate_corpus_qa(api_key)
