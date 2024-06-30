import asyncio
import json
from typing import Literal, Sequence

import os
import httpx

PRIVOCIA_API_URL = "https://api.privocia.com"

class AsyncPrivociaClient:
    def __init__(self, api_key: str):
        self._base_data = {
            "api_key": api_key,
        }
        self._client_creator = lambda: httpx.AsyncClient(
            headers={
                "Content-Type": "application/json",
            },
            base_url=PRIVOCIA_API_URL,
            timeout=180,
        )

    """
    Search Methods:
    """
    async def _search(self,
                query: str,
                query_order: int,
                max_results=5,
                archive_id=None,
                namespace_id=None,
                index_id=None,
                use_cache=True,
    ) -> dict:
        """
        Internal search method to send the request to the API.
        """
        query_metadata = {
            **self._base_data,
            "query": query,
            "query_order": query_order,
            "max_results": max_results,
            "archive_id": archive_id or None,
            "namespace_id": namespace_id or None,
            "index_id": index_id or None,
            "use_cache": use_cache,
        }
        async with self._client_creator() as client:
            response = await client.post("/search", data=json.dumps(query_metadata))

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code
            return {}  # Return an empty dictionary in case of an unsuccessful status code

    async def search(self, query, query_order_ = 1, **kwargs) -> dict:
        """
        Base search method. Set search_depth to 1 (local) or 0 (web).
        """
        return await self._search(query, query_order=query_order_, **kwargs)

    """
    Archive Methods:
    """
    async def add_to_archives(
        self,
        type_: str, # web, images, text, etc.
        size: int = 0,
        url_: str = "",
        text_: str = "", # text content
        vec_modality: str = "", # text, image, etc.
        vec_dim: int = 0,
        index_id: str = "",
        namespace_id: str = "",
        ) -> dict:
        """
        Internal method for adding to archives that sends the request to the API.
        """
        archive_metadata = {
            **self._base_data,
            "size": size,
            "type": type_,
            "url": url_,
            "vec_modality": vec_modality,
            "vec_dim": vec_dim,
            "index_id": index_id,
            "namespace_id": namespace_id,
        }
        async with self._client_creator() as client:
            response = await client.post("/archives/add", data=json.dumps(archive_metadata))

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            return {}  # Return an empty dictionary in case of an unsuccessful status code

    async def add_url_to_archives(
        self,
        url: str,
        **kwargs
        ) -> dict:
        """
        Add URL to archives.
        """
        return await self.add_to_archives(type_ = "web", url_=url, **kwargs)

    async def add_text_to_archives(
        self,
        text: str,
        **kwargs
        ) -> dict:
        """
        Add text to archives.
        """
        return await self.add_to_archives(type_ = "text", text_=text, **kwargs)

    async def add_image_to_archives(
        self,
        image_path: str,
        vec_modality: str = "image",
        **kwargs
        ) -> dict:
        """
        Add image to archives.
        """
        return await self.add_to_archives(type_ = "image", url_=image_path, vec_modality=vec_modality, **kwargs)

    async def get_archives(
        self
        ) -> dict:
        """
        Get archives.
        """
        data = {
            **self._base_data,
        }
        async with self._client_creator() as client:
            response = await client.post("/archives/get", data=json.dumps(data))

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code
            return {}  # Return an empty dictionary in case of an unsuccessful status code
    """
    async def get_archive(
        self,
        archive_id: str
        ) -> dict:

        #Get archive.

        data = {
            **self._base_data,
            "archive_id": archive_id,
        }
        async with self._client_creator() as client:
            response = await client.post("/archives/get_one", data=json.dumps(data))

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    """

    async def _clear_archives(
        self
        ) -> dict:
        """
        Clear archives.
        """
        data = {
            **self._base_data,
        }

        async with self._client_creator() as client:
            response = await client.post("/archives/clear", data=json.dumps(data))

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code
            return {}  # Return an empty dictionary in case of an unsuccessful status code
