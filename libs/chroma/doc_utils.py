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


def get_or_create_db(documents, db_name, re_init=False, persist=False):
    if persist:
        client = chromadb.PersistentClient(f'chromadb/{db_name}')
    else:
        client = chromadb.Client()

    if re_init:
        try:
            client.delete_collection(db_name)
        except:
            pass

        db = client.create_collection(name=db_name, embedding_function=GeminiEmbeddingFunc())
        for i, doc in tqdm(enumerate(documents)):
            db.add(documents=doc, ids=str(i))
    else:
        db = client.get_or_create_collection(name=db_name, embedding_function=GeminiEmbeddingFunc())

    return db


def create_chroma_db(documents, db_name):
    client = chromadb.Client()

    # delete db
    try:
        client.delete_collection(db_name)
    except:
        pass

    db = client.create_collection(name=db_name, embedding_function=GeminiEmbeddingFunc())

    for i, doc in tqdm(enumerate(documents)):
        db.add(documents=doc, ids=str(i))

    return db


def get_relevant_docs(keywords, db, n_results=5):
    filter_dict = {'$or': [{"$contains": kw} for kw in keywords]}
    if len(keywords) == 1:
        filter_dict = {"$contains": keywords[0]}

    docs = db.query(query_texts=keywords, n_results=n_results, where_document=filter_dict)[
        'documents'
    ][0]
    return docs
