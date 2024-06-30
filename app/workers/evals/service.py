import pandas as pd
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter

import os
from dotenv import load_dotenv
load_dotenv()


from ...dependencies import supabase

from corpus.llamaindex import llama_text_node_to_parquet
from utils.ascii import load_ascii_art

from qa.llama_index import generate_qa_llama_index
from qa.base import make_single_content_qa


def generate_corpus_qa(api_key: str):
    """
    Given an api_key, generate QA data from the documents in the archive.
    """
    # First fetch data from the given archive_id and get paths for corpus and qa data
    dir_path = get_archive_path(api_key)
    if dir_path is None:
        return None
    output_corpus_path, output_qa_path = f"./data/corpus_qa/corpus_{api_key}.parquet", f"./data/corpus_qa/qa_{api_key}.parquet"

    # Make corpus data from raw documents
    documents = SimpleDirectoryReader(dir_path).load_data()
    nodes = TokenTextSplitter().get_nodes_from_documents(documents=documents, chunk_size=512, chunk_overlap=128)
    corpus_df = llama_text_node_to_parquet(nodes, output_corpus_path)

    # Make qa data from corpus data
    corpus_df = pd.read_parquet(output_corpus_path)
    llm = OpenAI(model='gpt-3.5-turbo',
                temperature=1.0,
                api_key=os.environ["OPENAI_API_KEY"]
                )
    qa_df = make_single_content_qa(corpus_df, 50, generate_qa_llama_index, llm=llm, question_num_per_content=1,
                                output_filepath=output_qa_path)

def get_archive_path(api_key: str):
    try:
        res = supabase.from_("docs") \
            .select("doc_id", "url", "title") \
            .eq("api_key", api_key) \
            .execute()

        if len(res.data) == 0:
            print("No documents found.")
            return None

        dir_path = f"./data/raw/archive_{api_key}"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for doc in res.data:
            url = doc["url"]
            title = doc["title"]
            doc_id = doc["doc_id"]
            if not os.path.exists(f"{dir_path}/{title}.txt"):
                with open(f"{dir_path}/{title}.txt", "w") as f:
                    f.write(url)

        return dir_path
    except Exception as e:
        print(f"Error: {e}")
        return None
