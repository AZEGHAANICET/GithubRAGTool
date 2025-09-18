from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_core.documents import Document
from typing import List


def get_retriever(documents: List[Document]):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma("youtube_transcript", embeddings)
    vectorstore.from_documents(documents=documents)