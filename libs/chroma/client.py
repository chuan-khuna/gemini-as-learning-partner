import pandas as pd

import chromadb
import google.generativeai as genai
import google.ai.generativelanguage as glm
from chromadb import Documents, EmbeddingFunction, Embeddings

from tqdm import tqdm
import os


class GeminiEmbeddingFunc(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model = 'models/embedding-001'
        title = 'Custom Query'

        return genai.embed_content(
            model=model, content=input, task_type="retrieval_document", title=title
        )["embedding"]


class ChromaClient:
    def __init__(self, collection_name: str, persist: bool = False, re_initialise: bool = False):
        self.collection_name = collection_name
        self.persist = persist
        self.re_initialise = re_initialise
        self.client = self.__init_chroma_client()
        self.collection = self.__init_collection()

    def __init_chroma_client(self):
        if self.persist:
            client = chromadb.PersistentClient(f'chromadb/{self.collection_name}')
        else:
            client = chromadb.Client()

        return client

    def __init_collection(self):
        if self.re_initialise:
            print("Re-initialising collection")
            try:
                print("Deleting collection")
                self.client.delete_collection(self.collection_name)
            except:
                print("Error whilst deleting collection")
                pass

        collection = self.client.get_or_create_collection(
            name=self.collection_name, embedding_func=GeminiEmbeddingFunc()
        )

        return collection

    def add_documents(self, doc_df: pd.DataFrame):
        """add documents to the collection

        Args:
            doc_df (pd.DataFrame): document dataframe with columns ['id', 'text']
        """

        for i, row in tqdm(doc_df.iterrows(), desc="Adding documents"):
            doc_id = row['id']
            doc = row['text']
            self.collection.add(documents=[doc], ids=[doc_id])

    def search_related(self, **kwargs) -> list[str]:
        """search related documents via chromadb `collection.query()`"""
        docs = self.collection.query(**kwargs)['documents'][0]
        return docs
