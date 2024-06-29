from ...schema.search import ResultSchema, ResponseSchema
from ...workers.archive.docs import get_doc
from ...dependencies import supabase

from typing import List

def perform_archive_search(api_key, embedding, metric):
    # Search the archive
    matches = search_embeddings(api_key, embedding, metric)
    return ResponseSchema(results=archive_results(api_key, matches))

"""
Get matches from the vector database.
"""
def search_embeddings(api_key, embedding, metric, top_k=5, min_similarity_score=0.5):
    metric2function = {
        'cosine': 'cosine_similarity_search',
        'inner_product': 'inner_product_search',
    }
    # NOTE: Create the function in the editor
    # https://supabase.com/dashboard/project/tmrcduvsgkbfasicfsym/sql/873b4195-dbf5-4718-a8d8-a2c80f6c2a23
    # https://supabase.com/dashboard/project/tmrcduvsgkbfasicfsym/sql/4cf9808b-53f3-4848-b1fd-1c3708af64f1
    res = supabase.rpc(metric2function[metric], {
        'api_key': api_key,
        'embedding': embedding,
        'top_k': top_k,
        'min_similarity_score': min_similarity_score,
        }).execute()
    return res.data

"""
Given similar embeddings from the vector database, return the results.
"""
def archive_results(api_key, matches) -> list[ResultSchema]:
    res = []
    for i, m in enumerate(matches):
        doc = get_doc(api_key, m['doc_id'])
        if doc is None:
            print(f"Doc not found for {m['doc_id']}")
            return []
        res.append(ResultSchema(
            index=i,
            relevance_score=m['similarity_score'],
            url=doc['url'],
            title=doc['title'],
            text_id=m['chunk_id'].split('-')[1], # FIXME: Should asign int id for chunk?
            text=m['text'],
            query_order=1,
            api_key=api_key))
    return res
