import requests
import json
import warnings

PRIVOCIA_API_URL = "https://api.privocia.com"

class PrivociaClient:
    def __init__(self, api_key):
        self.base_url = PRIVOCIA_API_URL
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
        }

    """
    Search Methods:
    """
    def _search(self,
                query: str,
                query_order: int,
                max_results: int = 5,
                archive_id: int = 0,
                namespace_id: str = "",
                index_id: str = "",
                use_cache: bool = True) -> dict:
        """
        Internal search method to send the request to the API.
        """
        query_metadata = {
            "query": query,
            "query_order": query_order,
            "max_results": max_results,
            "api_key": self.api_key,
            "archive_id": archive_id,
            "namespace_id": namespace_id or None,
            "index_id": index_id or None,
            "use_cache": use_cache,
        }
        response = requests.post(self.base_url, data=json.dumps(query_metadata), headers=self.headers, timeout=100)
        return {}  # Return an empty dictionary in case of an unsuccessful status code

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code

    def search_local(self, query, query_order_ = 1, **kwargs):
        """
        Base search method. Set search_depth to 1 (local).
        """
        return self._search(query, query_order=query_order_, **kwargs)

    def search_web(self, query, query_order_ = 0, **kwargs):
        """
        Base search method. Set search_depth to 0 (web).
        """
        return self._search(query, query_order=query_order_, **kwargs)


    """
    Archive Methods:
    """
    def add_to_archives(
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
            "size": size,
            "type": type_,
            "url": url_,
            "vec_modality": vec_modality,
            "vec_dim": vec_dim,
            "index_id": index_id,
            "namespace_id": namespace_id,
            "api_key": self.api_key,
        }
        response = requests.post(self.base_url, data=json.dumps(archive_metadata), headers=self.headers, timeout=100)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            return {}  # Return an empty dictionary in case of an unsuccessful status code

    def add_url_to_archives(
        self,
        url: str,
        **kwargs
        ) -> dict:
        """
        Add URL to archives.
        """
        return self.add_to_archives(type_ = "web", url_=url, **kwargs)

    def add_text_to_archives(
        self,
        text: str,
        **kwargs
        ) -> dict:
        """
        Add text to archives.
        """
        return self.add_to_archives(type_ = "text", text_=text, **kwargs)

    def add_image_to_archives(
        self,
        image_path: str,
        vec_modality: str = "image",
        **kwargs
        ) -> dict:
        """
        Add image to archives.
        """
        return self.add_to_archives(type_ = "image", url_=image_path, vec_modality=vec_modality, **kwargs)

    def get_archives(
        self
        ) -> dict:
        """
        Get archives.
        """
        data = {
            "api_key": self.api_key,
        }
        response = requests.get(self.base_url, data= json.dumps(data), headers=self.headers, timeout=100)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code
            return {}  # Return an empty dictionary in case of an unsuccessful status code

    """
    def get_archive(
        self,
        archive_id: str
        ) -> dict:
        #Get archive.
        data = {
            "api_key": self.api_key,
            "archive_id": archive_id,
        }
        response = requests.get(self.base_url, data= json.dumps(data), headers=self.headers, timeout=100)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            return {}  # Return an empty dictionary in case of an unsuccessful status code
    """


    def _clear_archives(
        self
        ) -> dict:
        """
        Clear archives.
        """
        data = {
            "api_key": self.api_key,
        }
        response = requests.delete(self.base_url, data= json.dumps(data), headers=self.headers, timeout=100)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            return {}  # Return an empty dictionary in case of an unsuccessful status code




class Client(PrivociaClient):
    def __init__(self, *args, **kwargs):
        warnings.warn("Client is deprecated, please use PrivociaClient instead", DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)
