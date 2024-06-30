
from ...schema.search import ResponseSchema

from ...dependencies import supabase

def add_to_results(api_key: str, query_results: ResponseSchema) -> bool:
    if query_results is None:
        print("No query results")
        return True
    prev_query_id = get_prev_query_id(api_key)
    for query_result in query_results:
        # Add the results to the database
        try:
            res = supabase.from_("results") \
                .insert({
                    # result_id will be generated automatically
                    "url_id": query_result.url_id,
                    "url": query_result.url,
                    "title": query_result.title,
                    "content_id": query_result.text_id,
                    "content": query_result.text,
                    "query_order": query_result.query_order,
                    "api_key": query_result.api_key,
                    "query_id": prev_query_id + 1
                    }) \
                .execute()

            # Check if results was added
            if len(res.data) <= 0:
                print("Failed to add to results")
                return False

        except Exception as e:
            print(f"Failed to add to results: {str(e)}")
            return False
    return True

def get_prev_query_id(api_key: str) -> int:
    try:
        res = supabase.from_("results") \
            .select("query_id") \
            .eq("api_key", api_key) \
            .order("query_id", desc=True) \
            .execute()
        if res is None or res.data == [] or res.data is None:
            return 0
        query_id = res.data[0]["query_id"]
        print(f"Previous query id: {query_id}")
        return query_id
    except Exception as e:
        print(f"No query processed before.")
        return 0
