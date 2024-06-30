from enum import unique
from fastapi import APIRouter, requests
from fastapi.responses import JSONResponse

import os
import time
from datetime import datetime
import httpx

from ..schema.archive import Doc, Image, archiveMetadata
from ..workers.archive.docs import create_doc, get_docs, delete_docs
from ..workers.archive.images import create_image
import os

router = APIRouter(
    prefix="/api",
    tags=['archive'],
    dependencies=[],
)

LOG_FILE = 'request_log.txt'

WEBPROCESS_BACKEND = os.getenv('WEBPROCESS_BACKEND')
IMAGE_BACKEND = os.getenv('IMAGE_BACKEND')

def log_request(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'{timestamp} - {message}\n'
    with open(LOG_FILE, 'a') as file:
        file.write(log_entry)

class TimeRecorder:
    def __init__(self, process="", is_print=True):
        self.process_ = process
        self.is_print_ = is_print
        self.start_t_ = time.time()
        self.prev_t_ = self.start_t_
        self.record_ = {"sub": [], "total": None}

    def lap(self, subprocess):
        s = time.time()
        d = s - self.prev_t_
        if self.is_print_:
            print(f"[Time] {subprocess} in {self.process_}: {d}")
        self.record_["sub"].append({subprocess: d})
        self.prev_t_ = s

    def stop(self):
        s = time.time()
        d = s - self.start_t_
        if self.is_print_:
            print(f"[Time] {self.process_}: {d}")
        self.record_["total"] = d
        self.prev_t_ = s

    def get_record(self):
        return self.record_

# Create a new doc.
@router.post("/archives/add")
async def add_to_archives(archiveMetadata_: archiveMetadata):
    """
    Adds documents to the archive.
    @param archiveMetadata_: metadata of the document to be added.
    @return: JSONResponse
    """
    content, title, image_, embeddings_ = None, None, None, None
    try:
        type_ = archiveMetadata_.type_
        if type_ == "web":
            try:
                async with httpx.AsyncClient() as client:
                    print(f"Requested content from {archiveMetadata_.url_}")
                    response = await client.get(
                        WEBPROCESS_BACKEND + "/api/receive-url",
                        params={
                        "userId": archiveMetadata_.api_key,
                        "url": archiveMetadata_.url_
                        })
                    print(f"Requested content from {archiveMetadata_.url_}")

                    if response.status_code == 200:
                        json_reponse_ = response.json()
                        content = json_reponse_["content"]
                        title = json_reponse_["title"]
                        unique_id = json_reponse_["unique_id"]
                        log_message = f'Content extracted: {content} (Unique ID: {unique_id}), response status: {response.status_code}'
                        log_request(log_message)
                        print(log_message)
                    else:
                        error_message = f'Failed to extract content from url. Status code: {response.status_code}'
                        print(error_message)
                        return JSONResponse({'error': error_message}), 400
            except Exception as e:
                error_message = f"An error occurred while downloading the file: {str(e)}"
                print(error_message)
                return JSONResponse({'error': error_message}), 500
        elif type_ == "image":
            try:
                async with httpx.AsyncClient() as client:
                    print(f"Requested content from {archiveMetadata_.url_}")
                    response = await client.get(
                        IMAGE_BACKEND + "/api/receive_image",
                        params={
                        "url": archiveMetadata_.url_
                        })
                    print(f"Requested content from {archiveMetadata_.url_}")

                    if response.status_code == 200:
                        json_reponse_ = response.json()
                        image_ = json_reponse_["content"]
                        embeddings_ = json_reponse_["title"]
                        log_message = f'Image extracted: {image}, response status: {response.status_code}'
                        log_request(log_message)
                        print(log_message)
                    else:
                        error_message = f'Failed to extract content from url. Status code: {response.status_code}'
                        print(error_message)
                        return JSONResponse({'error': error_message}), 400
            except Exception as e:
                error_message = f"An error occurred while downloading the file: {str(e)}"
                print(error_message)
                return JSONResponse({'error': error_message}), 500
        elif type_ == "text":
            # TODO: Add support for text processing
            try:
                content = archiveMetadata_.text_
                if content is None:
                    return JSONResponse(content={"message": "text content is missing"}, status_code=400)
                else:
                    title = content[:10] + "..."
            except Exception as e:
                return JSONResponse(content={"message": "error in processing text; " + str(e)}, status_code=400)
        else:
            error_message = f"Unsupported type: {type_}"
            return JSONResponse(content={"message": error_message}, status_code=400)
    except Exception as e:
        return {"message": str(e)}
    try:
        if archiveMetadata_.type_ == "image":
            image = Image(
                api_key=archiveMetadata_.api_key,
                url=archiveMetadata_.url_,
                image=image_,
                embeddings=embeddings_
            )
            res = create_image(image)
            if not res:
                error_message = f"Failed to archive image: {archiveMetadata_.url_}"
                return JSONResponse(content={"message": error_message}, status_code=400)
        else:
            doc = Doc(
                api_key=archiveMetadata_.api_key,
                url=archiveMetadata_.url_,
                title=title,
            )
            res = create_doc(doc, content)
            if not res:
                error_message = f"Failed to archive url: {archiveMetadata_.url_}"
                return JSONResponse(content={"message": error_message}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)

    return JSONResponse(content={"message": f"{archiveMetadata_.url_} archived successfully"}, status_code=200)

# Get archives
@router.get("/archives/get")
async def get_archives(api_key: str):
    """
    Get all the archives of the user.
    @param api_key: API key of the user.
    @return: JSONResponse
    """
    # Get all docs of the user
    docs = get_docs(api_key=api_key, doc_id=None)
    if docs is not None:
        return JSONResponse(content={"message": "Archives found", "archives": docs}, status_code=200)
    else:
        return JSONResponse(content={"message": "Archives not found"}, status_code=200)

# Clear archives
@router.delete("/archives/delete")
async def clear_archives(api_key: str):
    """
    Delete all the archives of the user.
    @param api_key: API key of the user.
    @return: JSONResponse
    """
    # Delete all docs of the user
    if delete_docs(api_key=api_key, doc_id=None):
        return JSONResponse(content={"message": "Archives deleted successfully"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Archives deletion failed"}, status_code=400)
