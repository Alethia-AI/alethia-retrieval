from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter

from corpus.llamaindex import llama_text_node_to_parquet
from utils.ascii import load_ascii_art

import pandas as pd
from llama_index.llms.openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()

from qa.llama_index import generate_qa_llama_index
from qa.base import make_single_content_qa

def generate_qa(dir_path: str, output_corpus_path: str, output_qa_path: str):
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


if __name__ == '__main__':
    # Display the ASCII art:
    print("Welcome to the Alethia Evaluation Generator!")
    print("===========================================")
    load_ascii_art()
    print("===========================================")
    generate_qa(
        dir_path='data/raw',
        output_corpus_path=f'data/corpus_qa/corpus.parquet',
        output_qa_path=f'data/corpus_qa/qa.parquet'
