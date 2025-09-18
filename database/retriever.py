from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from typing import List

def search_transcript_chunks(
    documents: List[Document],
    query: str,
    k: int = 3,
    collection_name: str = "youtube_transcript"
) -> List[Document]:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


    db = Chroma.from_documents(documents, embedding=embeddings)

    query_vector = embeddings.embed_query(query)

    results = db.similarity_search_by_vector(query_vector, k=k)
    return results
