from tavily import TavilyClient


from .....schema.search import ResponseSchema, ResultSchema
from .base import SearchProvider


class TavilySearchProvider(SearchProvider):
    def __init__(self, tavily_api_key: str):
        self.tavily = TavilyClient(tavily_api_key)

    def search(self, api_key: int, query: str) -> ResponseSchema:
        response = self.tavily.search(
            query=query,
            search_depth="basic",
            max_results=3,
            include_images=True,
        )
        #print(response)
        if response is None:
            raise ValueError("No response from Tavily")

        print(f"Searching for: {query}")
        results = [
            ResultSchema(
                url=result['url'],
                title=result['title'],
                text=result['content'],
                query_order=0,
                api_key=api_key,
                index=i,
                relevance_score=result['score'], # FIXME: Probably not in response
                )
                for i, result in enumerate(response["results"])
                ]

        print(f"Found results for: {query}")
        return ResponseSchema(results=results, images=response["images"])
