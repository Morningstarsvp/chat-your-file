from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore

from config import EMBEDDING_FUNCTIONS
from database import crud, schemas


def get_temp_vectorstore(file_vs_id: str) -> VectorStore:
    vs_collection: schemas.VSCollection = crud.get_vs_collection_by_id(file_vs_id)
    vectorstore = Chroma(
        collection_name=vs_collection.collection_name,
        persist_directory=vs_collection.persist_directory,
        embedding_function=EMBEDDING_FUNCTIONS[vs_collection.embedding_function]
    )
    return vectorstore
